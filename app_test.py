from db.mongodb.Subscriber import Subscriber
from db.postgresdb.BenefitPackage import BenefitPackage
from db.postgresdb.StripeUser import StripeUser
from app import app as flaskapp, postgres_db
from pytest import fixture, MonkeyPatch
from db.mongo import mongo_db, MONGODB_DATABASE
import json
import os
import datetime
current_path = os.getcwd()

# Needed for SQLAlchemy to run within a context
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
flaskapp.app_context().push()


@fixture
def client():
    flaskapp.config['TESTING'] = True
    return flaskapp.test_client()


@fixture
def monkeypatch():
    return MonkeyPatch()


def setup_module():
    postgres_db.drop_all()
    postgres_db.create_all()
    mongo_db.drop_database(MONGODB_DATABASE)


def teardown_module():
    postgres_db.drop_all()
    mongo_db.drop_database(MONGODB_DATABASE)


def test_health(client):
    res = client.get('/api/health')
    assert res.get_json() == {"ok": 1}


def test_processing_error(client):
    """
    If something went wrong while processing the payload, return a success 0
    In reality, it doesn't matter since it's still returning a 200 status to Stripe, but
    this is just for testing purposes
    """
    res = client.post('/api/webhook', json={
        "type": "ooglaboo"
    })
    assert res.get_json() == {"success": 0}


def test_unhandled_event(client, monkeypatch):
    """
    An unhandled event should always return a success response
    """
    def validate_webhook_payload(request):
        return {
            "type": "ooglaboo"
        }
    monkeypatch.setattr('utils.validate_webhook_payload.validate_webhook_payload',
                        validate_webhook_payload)
    res = client.post('/api/webhook', json={
        "type": "ooglaboo"
    })
    assert res.get_json() == {"success": 1}


def test_subscription_created(client, monkeypatch):
    # Read a dummy event
    with open(f'{current_path}\\test\\testdata\\1_created_subscription\\invoice.paid.json') as file:
        stripe_event = json.load(file)

    # Setup the database
    customer_id = stripe_event['data']['object']['customer']
    product_id = stripe_event['data']['object']['lines']['data'][0]['price']['product']
    stripe_user = StripeUser(discord_id="discord-id1",
                             customer_id=customer_id)
    benefit_package = BenefitPackage(
        stripe_product_id=product_id, extra_feeds=10, allow_webhook=True, refresh_rate_seconds=1)
    postgres_db.session.add(stripe_user)
    postgres_db.session.add(benefit_package)
    postgres_db.session.commit()

    # Set up the API request
    def validate_webhook_payload(request):
        return stripe_event
    monkeypatch.setattr('utils.validate_webhook_payload.validate_webhook_payload',
                        validate_webhook_payload)
    client.post('/api/webhook', json={
        "type": "ooglaboo"
    })

    # Check that the product exists for the subscriber
    subscriber = Subscriber.objects().get(_id=customer_id)
    assert next(product for product in subscriber.products if product.productId ==
                product_id) is not StopIteration


def test_subscription_swapped(client, monkeypatch):
    # Read a dummy event
    with open(f'{current_path}\\test\\testdata\\2a_updated_subscription_higher'
              '\\invoice.paid.json') as file:
        stripe_event = json.load(file)

    # Setup the database
    customer_id = stripe_event['data']['object']['customer']
    product_id = stripe_event['data']['object']['lines']['data'][1]['price']['product']
    stripe_user = StripeUser(discord_id="discord-id1",
                             customer_id=customer_id)
    benefit_package = BenefitPackage(
        stripe_product_id=product_id, extra_feeds=10, allow_webhook=True, refresh_rate_seconds=1)
    postgres_db.session.add(stripe_user)
    postgres_db.session.add(benefit_package)
    postgres_db.session.commit()

    # Set up the API request
    def validate_webhook_payload(request):
        return stripe_event
    monkeypatch.setattr('utils.validate_webhook_payload.validate_webhook_payload',
                        validate_webhook_payload)
    client.post('/api/webhook', json={
        "type": "ooglaboo"
    })

    # Check that the product exists for the subscriber
    subscriber = Subscriber.objects().get(_id=customer_id)
    assert next(product for product in subscriber.products if product.productId ==
                product_id) is not StopIteration


def test_subscription_auto_renews(client, monkeypatch):
    # Read a dummy event
    with open(f'{current_path}\\test\\testdata\\5_renewed_subscription\\invoice.paid.json') as file:
        stripe_event = json.load(file)

    # Setup the database
    customer_id = stripe_event['data']['object']['customer']
    product_id = stripe_event['data']['object']['lines']['data'][0]['price']['product']
    stripe_user = StripeUser(discord_id="discord-id1",
                             customer_id=customer_id)
    benefit_package = BenefitPackage(
        stripe_product_id=product_id, extra_feeds=10, allow_webhook=True, refresh_rate_seconds=1)
    postgres_db.session.add(stripe_user)
    postgres_db.session.add(benefit_package)
    postgres_db.session.commit()

    # Set up the API request
    def validate_webhook_payload(request):
        return stripe_event
    monkeypatch.setattr('utils.validate_webhook_payload.validate_webhook_payload',
                        validate_webhook_payload)
    client.post('/api/webhook', json={
        "type": "ooglaboo"
    })

    # Check that the product exists for the subscriber
    subscriber = Subscriber.objects().get(_id=customer_id)
    assert next(product for product in subscriber.products if product.productId ==
                product_id) is not StopIteration


def test_subscription_deleted(client, monkeypatch):
    # Read a dummy event
    with open(f'{current_path}\\test\\testdata\\6_subscription_deleted'
              '\\customer.subscription.deleted.json') as file:
        stripe_event = json.load(file)

    # Setup the database
    customer_id = stripe_event['data']['object']['customer']
    product_id = stripe_event['data']['object']['items']['data'][0]['price']['product']
    stripe_user = StripeUser(discord_id="discord-id2",
                             customer_id=customer_id)
    postgres_db.session.add(stripe_user)
    postgres_db.session.commit()
    Subscriber(_id=customer_id, discordId="discord-id2", lifetimePaid=0, currency="usd", products=[{
        "productId": product_id,
        "quantity": 1,
        "endDate": datetime.datetime.now(),
        "benefits": {
            "extraFeeds": 1,
            "webhookAccess": True,
            "refreshRateSeconds": 1
        }
    }]).save()
    # Set up the API request

    def validate_webhook_payload(request):
        return stripe_event
    monkeypatch.setattr('utils.validate_webhook_payload.validate_webhook_payload',
                        validate_webhook_payload)
    client.post('/api/webhook', json={
        "type": "ooglaboo"
    })
    subscriber = Subscriber.objects().get(_id=customer_id)
    assert len(subscriber.products) == 0
