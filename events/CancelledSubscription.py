from events.Base import StripeEventBase
from structs.SubscriptionItem import SubscriptionItem


class CancelledSubscription(StripeEventBase):
    def __init__(self, stripe_event):
        self.cancelled_item = SubscriptionItem(
            stripe_event['data']['object']['lines']['data'][0])

    def apply_benefit_updates(self):
        """
        1. Get discord ID via customer id
        2. Delete benefit package from MongoDB doc with product id
        """
        return
