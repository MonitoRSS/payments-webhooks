from events.Base import StripeEventBase
from structs.StripeLineItem import StripeLineItem


class RenewedSubscription(StripeEventBase):
    def __init__(self, stripe_event):
        self.purchased_item = StripeLineItem(
            stripe_event['data']['object']['lines']['data'][0])

    def apply_benefit_updates(self):
        """
        1. Get discord ID via customer id
        2. If discord ID exists with this product, set new end date
            else create new subscription
        """
        return
