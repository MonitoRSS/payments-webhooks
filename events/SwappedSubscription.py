from services.products import swap_products_for_customer
from events.Base import StripeEventBase
from structs.SubscriptionItem import SubscriptionItem


class SwappedSubscription(StripeEventBase):
    def __init__(self, stripe_event):
        super().__init__(stripe_event)
        self.old_item = SubscriptionItem(
            stripe_event['data']['object']['lines']['data'][0])
        self.new_item = SubscriptionItem(
            stripe_event['data']['object']['lines']['data'][1])

    def apply_benefit_updates(self):
        """
        1. Get benefits package for this purchased product
        2. Get discord ID via customer id
        3. If discord ID already exists with this product, delete old product and insert new product
            else create new mongo document
        """
        swap_products_for_customer(
            self.customer_id,
            self.old_item.product_id,
            self.new_item.product_id,
            self.new_item.end_timestamp
        )
        return
