import stripe
from utils.constants import STRIPE_WEBHOOK_SECRET


def validate_webhook_payload(request):
    payload = request.data

    try:
        sig_header = request.headers.get('stripe-signature')
        return stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except stripe.error.SignatureVerificationError as e:
        raise Exception('Webhook signature verification failed. ' + str(e))
    except Exception as e:
        raise Exception('Parse request data error ' + str(e))
