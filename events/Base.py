class StripeEventBase:

    def __init__(self, stripe_event):
        self.customer_id = stripe_event['data']['object']['customer']

    def apply_benefit_updates(self):
        raise NotImplementedError("apply_benefit_updates must be implemented")
