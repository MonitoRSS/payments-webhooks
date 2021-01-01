from db.postgresdb.StripeUser import StripeUser
from db.postgresdb.BenefitPackage import BenefitPackage
from db.mongo import Subscriber, mongo_db, MONGODB_DATABASE
import datetime
from services.products import (
    create_product_for_customer,
    add_or_create_product_for_customer,
    delete_product_from_customer,
    swap_products_for_customer
)
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
    stripe_user = StripeUser(discord_id="discord-id1",
                             customer_id=stripe_customer_id)
    postgres_db.session.add(stripe_user)
    # Set up the benefit package definition
    benefit_package = BenefitPackage(
        stripe_product_id=product_id, extra_feeds=10, allow_webhook=True, refresh_rate_seconds=1)
    postgres_db.session.add(benefit_package)
    postgres_db.session.commit()
    # Apply it to the subscriber
    create_product_for_customer(stripe_customer_id, product_id, end_date)
    # Assert that it was correctly added
    subscriber = Subscriber.objects().get(_id=stripe_customer_id)
    assert next(product for product in subscriber.products if product.productId ==
                product_id) is not StopIteration


def test_product_is_added_after_applied():
    """
    A benefit package of a product should be added to a subscriber
    """
    stripe_customer_id = 'id1'
    product_id = 'product-id1'
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
    add_or_create_product_for_customer(
        stripe_customer_id, product_id, end_date)
    # Assert that it was correctly added
    subscriber = Subscriber.objects().get(_id=stripe_customer_id)
    assert next(product for product in subscriber.products if product.productId ==
                product_id) is not StopIteration


def test_subscriber_is_created_after_applied():
    """
    While applying a product to a customer, if the equivalent subscriber does not exist,
    create the subscriber with the product
    """
    stripe_customer_id = 'id2'
    product_id = 'product-id2'
    end_date = datetime.datetime.now()
    # Set up the stripe user
    stripe_user = StripeUser(discord_id="discord-id2",
                             customer_id=stripe_customer_id)
    postgres_db.session.add(stripe_user)
    # Set up the benefit package
    benefit_package = BenefitPackage(
        stripe_product_id=product_id, extra_feeds=10, allow_webhook=True, refresh_rate_seconds=1)
    postgres_db.session.add(benefit_package)
    postgres_db.session.commit()
    # Apply it to the subscriber
    add_or_create_product_for_customer(
        stripe_customer_id, product_id, end_date)
    # Assert that it was correctly added
    subscriber = Subscriber.objects().get(_id=stripe_customer_id)
    assert next(product for product in subscriber.products if product.productId ==
                product_id) is not StopIteration


def test_product_is_deleted():
    """
    Test that deleting a product from a subscriber works correctly
    """
    stripe_customer_id = 'id4'
    product_id = 'product-id4'
    # Set up the subscriber and benefit package definition
    Subscriber(_id=stripe_customer_id, discordId="1234", lifetimePaid=0, currency="usd", products=[{
        "productId": product_id,
        "quantity": 1,
        "endDate": datetime.datetime.now(),
        "benefits": {
            "extraFeeds": 1,
            "webhookAccess": True,
            "refreshRateSeconds": 1
        }
    }]).save()
    # Apply it to the subscriber
    delete_product_from_customer(stripe_customer_id, product_id)
    # Assert that it was swap_products_for_customer added
    subscriber = Subscriber.objects().get(_id=stripe_customer_id)
    assert len(subscriber.products) == 0


def test_product_is_swapped():
    """
    Test that swapping an old product for a new product on a subscriber works correctly
    """
    stripe_customer_id = 'id4'
    old_product_id = 'product-id4'
    new_product_id = 'product-id5'
    end_date = datetime.datetime.now()
    # Set up the subscriber with the old product
    Subscriber(_id=stripe_customer_id, discordId="1234", lifetimePaid=0, currency="usd", products=[{
        "productId": old_product_id,
        "quantity": 1,
        "endDate": datetime.datetime.now(),
        "benefits": {
            "extraFeeds": 1,
            "webhookAccess": True,
            "refreshRateSeconds": 1
        }
    }]).save()
    # Set up the new product that will replace the existing one
    benefit_package = BenefitPackage(
        stripe_product_id=new_product_id,
        extra_feeds=10,
        allow_webhook=True,
        refresh_rate_seconds=1
    )
    postgres_db.session.add(benefit_package)
    postgres_db.session.commit()
    # Apply the swap
    swap_products_for_customer(stripe_customer_id, old_product_id,
                               new_product_id, end_date)
    # Assert that it was correctly swapped
    subscriber = Subscriber.objects().get(_id=stripe_customer_id)
    assert subscriber.products[0].productId == new_product_id
