from events.Base import StripeEventBase
from structs.StripeLineItem import StripeLineItem
from services.products import add_or_create_product_for_customer


class NewSubscription(StripeEventBase):
    def __init__(self, stripe_event):
        super().__init__(stripe_event)
        self.purchased_item = StripeLineItem(
            stripe_event['data']['object']['lines']['data'][0])

    def apply_benefit_updates(self):
        """
        1. Get benefits package for this purchased product
        2. Get discord ID via customer id
        3. If discord ID already exists with this product, overwrite product,
            else create a new document
        """
        add_or_create_product_for_customer(
            self.customer_id,
            self.purchased_item.product_id,
            self.purchased_item.end_timestamp
        )
        return
