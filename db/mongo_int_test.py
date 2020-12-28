from db.mongo import find_stripe_customer_suscriber, mongo_client, MONGODB_DATABASE, mongo_db
import pytest


def setup_module():
    mongo_client.drop_database(MONGODB_DATABASE)


def teardown_module():
    mongo_client.drop_database(MONGODB_DATABASE)


def test_not_found_stripe_customer_subscriber():
    found = find_stripe_customer_suscriber('random id')
    assert found is None


@pytest.mark.integration
def test_found_stripe_customer_subscriber():
    stripe_customer_id = 'stripe-id'
    mongo_db.subscribers.insert_one({
        "_id": stripe_customer_id
    })
    found = find_stripe_customer_suscriber(stripe_customer_id)
    assert found is not None
