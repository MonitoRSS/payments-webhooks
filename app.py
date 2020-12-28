import json
import stripe
from flask import Flask, request, jsonify
from utils.constants import STRIPE_SECRET_API_KEY
from utils.validate_webhook_payload import validate_webhook_payload
from events import (
    NewSubscription,
    RenewedSubscription,
    SwappedSubscription,
    CancelledSubscription,
    RestartedCancelledSubscription
)
stripe.api_key = STRIPE_SECRET_API_KEY

app = Flask(__name__)


@app.route('/health')
def health():
    return {
        "ok": 1
    }


@app.route('/webhook', methods=['POST'])
def webhook_received():
    event = None

    try:
        event = validate_webhook_payload(request)
    except Exception as e:
        print('Failed to validate webhook payload' + str(e))
        return jsonify(success=False)

    event_type = event['type']

    try:
        event_data = event['data']
        event_data_object = event_data['object']
        # A subscription was created, apply benefits
        if event_type == 'invoice.paid' and \
                event_data_object['billing_reason'] == 'subscription_create':
            print("user made a new subscription")
            NewSubscription(event)

        # A subscription was swapped to a different product/price, swap benefits
        elif event_type == 'invoice.paid' and \
                event_data_object['billing_reason'] == 'subscription_update':
            print("user changed their subscription plan")
            SwappedSubscription(event)

        # A subscription advanced into a new period, update end date of benefits
        elif event_type == 'invoice.paid' and \
                event_data_object['billing_reason'] == 'subscription_cycle':
            print("user paid for a new month for a subscription")
            RenewedSubscription(event)

        # A subscription renewal failed, cancel benefits
        elif event_type == 'invoice.payment_failed':
            print("user's payment failed for subscription")

        # A subscription was cancelled, cancel benefits
        elif event_type == 'customer.subscription.updated' and \
                event_data['previous_attributes']['cancel_at'] is None and \
                event_data_object['cancel_at'] is not None:
            print("user cancelled subscription")
            CancelledSubscription(event)

        # A subscription was re-subscribed to after it was cancelled, apply benefits
        elif event_type == 'customer.subscription.updated' and\
                event_data['previous_attributes']['cancel_at'] is not None and \
                event_data_object['cancel_at'] is None:
            print("user resubscribed to cancelled subscription")
            RestartedCancelledSubscription(event)

        # Unexpected event type
        else:
            print('Unhandled event type {}'.format(event_type))
            print(json.dumps(event, indent=4))

    # Unexpected event type
    except KeyError:
        print('Unhandled event type {}'.format(event_type))
        # print(json.dumps(event, indent=4))
        pass

    return jsonify(success=True)
