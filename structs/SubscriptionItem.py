# https://stripe.com/docs/api/subscription_items/object
class SubscriptionItem:
    def __init__(self, stripe_subscription_item):
        self.quantity = stripe_subscription_item['quantity']
        self.product_id = stripe_subscription_item['price']['product']
        self.end_timestamp = stripe_subscription_item['period']['end']
