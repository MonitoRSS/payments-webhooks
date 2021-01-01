from datetime import date

# https://stripe.com/docs/api/invoices/line_item


class StripeLineItem:
    def __init__(self, stripe_event_line_item):
        self.quantity = stripe_event_line_item['quantity']
        self.product_id = stripe_event_line_item['price']['product']
        self.end_timestamp = date.fromtimestamp(
            stripe_event_line_item['period']['end'])
