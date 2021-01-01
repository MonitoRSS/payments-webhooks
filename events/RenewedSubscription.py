from services.subscribers import increment_lifetime_paid
from services.products import swap_products_for_customer
from events.Base import StripeEventBase
from structs.StripeLineItem import StripeLineItem


class RenewedSubscription(StripeEventBase):
    def __init__(self, stripe_event):
        super().__init__(stripe_event)
        self.purchased_item = StripeLineItem(
            stripe_event['data']['object']['lines']['data'][0])
        self.amount_paid = stripe_event['data']['object']['amount_paid']

    def apply_benefit_updates(self):
        """
        1. Get discord ID via customer id
        2. If discord ID exists with this product, set new end date
            else create new subscription
        """
        # Swap the product for itself, but only change the end date
        swap_products_for_customer(
            self.customer_id,
            self.purchased_item.product_id,
            self.purchased_item.product_id,
            self.purchased_item.end_timestamp
        )
        increment_lifetime_paid(self.customer_id, self.amount_paid)
        return
