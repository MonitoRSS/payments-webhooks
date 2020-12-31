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


def create_for_customer(customer_id: str, product_id: str, end_date):
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


def apply_to_customer(customer_id: str, product_id: str, end_date):
    try:
        subscriber = get_subscriber(customer_id)
        benefits = get_product_benefits(product_id)
    except DoesNotExist:
        create_for_customer(customer_id, product_id, end_date)
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
