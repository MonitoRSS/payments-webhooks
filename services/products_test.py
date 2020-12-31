from db.postgres.StripeUser import StripeUser
from db.postgres.BenefitPackage import BenefitPackage
from db.mongo import Subscriber, mongo_db, MONGODB_DATABASE
import datetime
from services.products import apply_to_customer, create_for_customer
from app import postgres_db


def setup_module():
    postgres_db.drop_all()
    postgres_db.create_all()
    mongo_db.drop_database(MONGODB_DATABASE)


def teardown_module():
    postgres_db.drop_all()
    mongo_db.drop_database(MONGODB_DATABASE)


def test_subscriber_is_added_with_benefits():
    """
    A new subscriber should be made with the benefit package
    """
    stripe_customer_id = 'stripe-id'
    product_id = 'product-id'
    end_date = datetime.datetime.now()
    # Set up the stripe user with a discord ID
    stripe_user = StripeUser(discord_id="discord-id",
                             customer_id=stripe_customer_id)
    postgres_db.session.add(stripe_user)
    # Set up the benefit package definition
    benefit_package = BenefitPackage(
        stripe_product_id=product_id, extra_feeds=10, allow_webhook=True, refresh_rate_seconds=1)
    postgres_db.session.add(benefit_package)
    postgres_db.session.commit()
    # Apply it to the subscriber
    create_for_customer(stripe_customer_id, product_id, end_date)
    # Assert that it was correctly added
    subscriber = Subscriber.objects().get(_id=stripe_customer_id)
    assert next(product for product in subscriber.products if product.productId ==
                product_id) is not StopIteration


def test_product_is_added_after_applied():
    """
    A benefit package of a product should be added to a subscriber
    """
    stripe_customer_id = 'stripe-id'
    product_id = 'product-id'
    end_date = datetime.datetime.now()
    # Set up the subscriber and benefit package definition
    Subscriber(_id=stripe_customer_id, discordId="123", lifetimePaid=0, currency="usd", products=[{
        "productId": "p1",
        "quantity": 1,
        "endDate": datetime.datetime.now(),
        "benefits": {
            "extraFeeds": 1,
            "webhookAccess": True,
            "refreshRateSeconds": 1
        }
    }]).save()
    benefit_package = BenefitPackage(
        stripe_product_id=product_id, extra_feeds=10, allow_webhook=True, refresh_rate_seconds=1)
    postgres_db.session.add(benefit_package)
    postgres_db.session.commit()
    # Apply it to the subscriber
    apply_to_customer(stripe_customer_id, product_id, end_date)
    # Assert that it was correctly added
    subscriber = Subscriber.objects().get(_id=stripe_customer_id)
    assert next(product for product in subscriber.products if product.productId ==
                product_id) is not StopIteration


def test_subscriber_is_created_after_applied():
    """
    While applying a product to a customer, if the equivalent subscriber does not exist, create it
    """
    stripe_customer_id = 'stripe-id'
    product_id = 'product-id'
    end_date = datetime.datetime.now()
    # Set up the stripe user
    stripe_user = StripeUser(discord_id="discord-id",
                             customer_id=stripe_customer_id)
    postgres_db.session.add(stripe_user)
    # Set up the benefit package
    benefit_package = BenefitPackage(
        stripe_product_id=product_id, extra_feeds=10, allow_webhook=True, refresh_rate_seconds=1)
    postgres_db.session.add(benefit_package)
    postgres_db.session.commit()
    # Apply it to the subscriber
    apply_to_customer(stripe_customer_id, product_id, end_date)
    # Assert that it was correctly added
    subscriber = Subscriber.objects().get(_id=stripe_customer_id)
    assert next(product for product in subscriber.products if product.productId ==
                product_id) is not StopIteration
