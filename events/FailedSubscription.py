from services.products import delete_product_from_customer
from events.Base import StripeEventBase
from structs.StripeLineItem import StripeLineItem


class FailedSubscription(StripeEventBase):
    def __init__(self, stripe_event):
        super().__init__(stripe_event)
        # StripeEventBase.__init__(self, stripe_event)
        self.cancelled_item = StripeLineItem(
            stripe_event['data']['object']['lines']['data'][0])

    def apply_benefit_updates(self):
        """
        1. Get discord ID via customer id
        2. Delete benefit package from MongoDB doc with product id
        """
        delete_product_from_customer(
            self.customer_id, self.cancelled_item.product_id)
        return
