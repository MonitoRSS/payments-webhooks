from db.postgres.StripeUser import StripeUser
from db.mongodb.Subscriber import Subscriber, SubscriberProduct
from db.postgres.BenefitPackage import BenefitPackage
from mongoengine import DoesNotExist


def get_subscriber(customer_id: str):
    # This automatically throws if
    return Subscriber.objects().get(_id=customer_id)


def get_product_benefits(product_id: str):
    benefits = BenefitPackage.get_package_for_product(product_id)
    if benefits is None:
        raise DoesNotExist(f"Benefits for {product_id} do not exist")
    return benefits


def create_product_for_customer(customer_id: str, product_id: str, end_date):
    try:
        discord_id = StripeUser.get_customer_discord_id(customer_id)
        if discord_id is None:
            raise Exception(
                f"Discord ID for customer {customer_id} does not exist")
        benefits = get_product_benefits(product_id)
    except Exception as e:
        print(e)
        raise e
    else:
        product_to_add = SubscriberProduct(
            productId=product_id,
            quantity=1,
            endDate=end_date,
            benefits={
                "extraFeeds": benefits.extra_feeds,
                "webhookAccess": benefits.allow_webhook,
                "refreshRateSeconds": benefits.refresh_rate_seconds
            }
        )
        Subscriber(
            _id=customer_id,
            discordId=discord_id,
            lifetimePaid=0,
            currency="usd",
            products=[product_to_add]
        ).save()
    pass


def add_or_create_product_for_customer(customer_id: str, product_id: str, end_date):
    try:
        subscriber = get_subscriber(customer_id)
        benefits = get_product_benefits(product_id)
    except DoesNotExist:
        create(customer_id, product_id, end_date)
    except Exception as e:
        print(e)
        raise e
    else:
        product_to_add = SubscriberProduct(
            productId=product_id,
            quantity=1,
            endDate=end_date,
            benefits={
                "extraFeeds": benefits.extra_feeds,
                "webhookAccess": benefits.allow_webhook,
                "refreshRateSeconds": benefits.refresh_rate_seconds
            }
        )

        for product in subscriber.products:
            if product.productId == product_id:
                # This product was already applied
                return
        subscriber.products.append(product_to_add)
        subscriber.save()


def delete_product_from_customer(customer_id: str, product_id: str):
    try:
        subscriber = get_subscriber(customer_id)
    except DoesNotExist:
        print(
            f"Skipping product deletion of {product_id} for customer {customer_id} "
            "because it doesn't exist")
        return
    except Exception as e:
        print(e)
        raise e
    else:
        subscriber.products = [
            product for product in subscriber.products if product.productId != product_id
        ]
        subscriber.save()


def swap_products_for_customer(customer_id: str, old_product_id: str, new_product_id, end_date):
    try:
        subscriber = get_subscriber(customer_id)
        benefits = get_product_benefits(new_product_id)
    except DoesNotExist:
        create_product_for_customer(customer_id, new_product_id, end_date)
    except Exception as e:
        print(e)
        raise e
    else:
        product_to_add = SubscriberProduct(
            productId=new_product_id,
            quantity=1,
            endDate=end_date,
            benefits={
                "extraFeeds": benefits.extra_feeds,
                "webhookAccess": benefits.allow_webhook,
                "refreshRateSeconds": benefits.refresh_rate_seconds
            }
        )

        for index in range(len(subscriber.products)):
            product = subscriber.products[index]
            if product.productId == old_product_id:
                subscriber.products[index] = product_to_add
                subscriber.save()
                return
        print(
            f"Failed to swap customer {customer_id} product {old_product_id} for {product_to_add} "
            f"because old product does not exist")
