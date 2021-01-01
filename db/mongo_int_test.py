from db.mongo import find_stripe_customer_suscriber, Subscriber
import pytest
import datetime
from mongoengine import DoesNotExist


def setup_module():
    Subscriber.drop_collection()
    # mongo_client.drop_database(MONGODB_DATABASE)


def teardown_module():
    Subscriber.drop_collection()


def test_not_found_stripe_customer_subscriber():
    with pytest.raises(DoesNotExist):
        find_stripe_customer_suscriber('random id')


def test_found_stripe_customer_subscriber():
    stripe_customer_id = 'stripe-id'
    Subscriber(_id=stripe_customer_id, discordId="123", lifetimePaid=0, currency="usd", products=[{
        "productId": "p1",
        "quantity": 1,
        "endDate": datetime.datetime.now(),
        "benefits": {
            "extraFeeds": 1,
            "webhookAccess": True,
            "refreshRateSeconds": 90
        }
    }]).save()
    found = find_stripe_customer_suscriber(stripe_customer_id)
    assert found is not None
