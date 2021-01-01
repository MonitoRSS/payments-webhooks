from services.products import add_or_create_product_for_customer
from events.Base import StripeEventBase
from structs.SubscriptionItem import SubscriptionItem


class RestartedCancelledSubscription(StripeEventBase):
    def __init__(self, stripe_event):
        super().__init__(stripe_event)
        self.purchased_item = SubscriptionItem(
            stripe_event['data']['object']['lines']['data'][0])

    def apply_benefit_updates(self):
        """
        1. Get benefits package for this purchased product
        2. Get discord ID via customer id
        3. If discord ID already exists with this product, overwrite contents,
            else create a new document
        """
        add_or_create_product_for_customer(
            self.customer_id,
            self.purchased_item.product_id,
            self.purchased_item.end_timestamp
        )
        return
