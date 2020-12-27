import json
import stripe
from flask import Flask, request, jsonify
from utils.constants import STRIPE_SECRET_API_KEY, STRIPE_WEBHOOK_SECRET

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

    payload = request.data

    try:
        sig_header = request.headers.get('stripe-signature')
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except stripe.error.SignatureVerificationError as e:
        print('⚠️  Webhook signature verification failed.' + str(e))
        return jsonify(success=True)
    except Exception as e:
        print('⚠️  Webhook error while parsing basic request.' + str(e))
        return jsonify(success=True)

    event_type = event['type']

    try:
        event_data = event['data']
        event_data_object = event_data['object']
        # A subscription was created
        if event_type == 'invoice.paid' and \
                event_data_object['billing_reason'] == 'subscription_create':
            print("user made a new subscription")

        # A subscription was swapped to a different product/price
        elif event_type == 'invoice.paid' and \
                event_data_object['billing_reason'] == 'subscription_update':
            print("user changed their subscription plan")

        # A subscription advanced into a new period
        elif event_type == 'invoice.paid' and \
                event_data_object['billing_reason'] == 'subscription_cycle':
            print("user paid for a new month for a subscription")

        # A subscription was cancelled
        elif event_type == 'customer.subscription.updated' and \
                event_data['previous_attributes']['cancel_at'] is None and \
                event_data_object['cancel_at'] is not None:

            print("user cancelled subscription")

        # A subscription was re-subscribed to after it was cancelled
        elif event_type == 'customer.subscription.updated' and\
                event_data['previous_attributes']['cancel_at'] is not None and \
                event_data_object['cancel_at'] is None:
            print("user resubscribed to cancelled subscription")

        # Unexpected event type
        else:
            print('Unhandled event type {}'.format(event_type))
            print(json.dumps(event, indent=4))

    # Unexpected event type
    except KeyError:
        print('Unhandled event type {}'.format(event_type))
        print(json.dumps(event, indent=4))
        pass

    return jsonify(success=True)
