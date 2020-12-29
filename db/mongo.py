from mongoengine.document import EmbeddedDocument
from mongoengine.fields import EmbeddedDocumentField
from utils.constants import MONGODB_URI, MONGODB_DATABASE
from mongoengine import (
    connect,
    StringField,
    FloatField,
    IntField,
    DateTimeField,
    Document,
    BooleanField,
    ListField
)
# from pymongo import MongoClient

mongo_db = connect(MONGODB_DATABASE, host=MONGODB_URI)


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
    _id = StringField(required=True)
    discordId = StringField(required=True)
    lifetimePaid = FloatField(default=0)
    currency = StringField(required=True)
    products = ListField(EmbeddedDocumentField(SubscriberProduct))

    def __repr__(self):
        return (f"<Subscriber (_id={self._id}, "
                f"discordId={self.discordId}, "
                f"lifetimePaid={self.lifetimePaid}, "
                f"currency={self.currency}), "
                f"products={self.products}), >")


def find_stripe_customer_suscriber(customer_id: str):
    return Subscriber.objects().get(_id=customer_id)
