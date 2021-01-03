from mongoengine import (
    EmbeddedDocument,
    Document,
    FloatField,
    ListField,
    IntField,
    BooleanField,
    StringField,
    DateTimeField,
    EmbeddedDocumentField
)


class SubscriberProductBenefits(EmbeddedDocument):
    extraFeeds = IntField(required=True)
    webhookAccess = BooleanField(required=True)
    refreshRateSeconds = IntField(required=True)

    def __repr__(self):
        return (f"<SubscriberProductBenefits (extraFeeds={self.extraFeeds}, "
                f"webhookAccess={self.webhookAccess}, "
                f"refreshRateSeconds={self.refreshRateSeconds}")


class SubscriberProduct(EmbeddedDocument):
    productId = StringField(required=True)
    quantity = IntField(required=True)
    endDate = DateTimeField(required=True)
    benefits = EmbeddedDocumentField(
        SubscriberProductBenefits)

    def __repr__(self):
        return (f"<SubscriberProduct (productId={self.productId}, "
                f"quantity={self.quantity}, "
                f"endDate={self.endDate}, "
                f"benefits={self.benefits})>")


class Subscriber(Document):
    meta = {
        'collection': 'subscribers'
    }
    # _id is the stripe customer id
    _id = StringField(required=True)
    discordId = StringField(required=True)
    lifetimePaid = FloatField(default=0)
    products = ListField(EmbeddedDocumentField(SubscriberProduct))

    def __repr__(self):
        return (f"<Subscriber (_id={self._id}, "
                f"discordId={self.discordId}, "
                f"lifetimePaid={self.lifetimePaid}, "
                f"currency={self.currency}), "
                f"products={self.products}), >")
