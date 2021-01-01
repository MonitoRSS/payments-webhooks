from events.DeletedSubscription import DeletedSubscription
from events.NewSubscription import NewSubscription
from events.SwappedSubscription import SwappedSubscription
from events.RenewedSubscription import RenewedSubscription
from flask import Blueprint, request, jsonify
import json
from utils import validate_webhook_payload
api = Blueprint('api', __name__)


@api.route('/health')
def health():
    return {
        "ok": 1
    }


@api.route("/webhook", methods=['POST'])
def webhook_received():
    event = None

    try:
        event = validate_webhook_payload.validate_webhook_payload(
            request)
    except Exception as e:
        print('Failed to validate webhook payload' + str(e))
        return jsonify(success=0)

    event_type = event['type']

    try:
        event_data = event['data']
        event_data_object = event_data['object']

        # A subscription was created, apply benefits
        if event_type == 'invoice.paid' and \
                event_data_object['billing_reason'] == 'subscription_create':
            print("user made a new subscription")
            mapped_event = NewSubscription(event)
            mapped_event.apply_benefit_updates()

        # A subscription was swapped to a different product/price, swap benefits
        elif event_type == 'invoice.paid' and \
                event_data_object['billing_reason'] == 'subscription_update':
            print("user changed their subscription plan")
            mapped_event = SwappedSubscription(event)
            mapped_event.apply_benefit_updates()

        # A subscription advanced into a new period, update end date of benefits
        elif event_type == 'invoice.paid' and \
                event_data_object['billing_reason'] == 'subscription_cycle':
            print("user paid for a new month for a subscription")
            mapped_event = RenewedSubscription(event)
            mapped_event.apply_benefit_updates()

        elif event_type == 'customer.subscription.deleted':
            print("subscription deleted")
            mapped_event = DeletedSubscription(event)
            mapped_event.apply_benefit_updates()

        # Unexpected event type
        else:
            print('Unhandled event type {}'.format(event_type))
            print(json.dumps(event, indent=4))

    # Unexpected event type
    except KeyError:
        print('Unhandled event type {}'.format(event_type))
        # print(json.dumps(event, indent=4))

    return jsonify(success=1)
