from db.BenefitPackage import BenefitPackage
from db.mongo import mongo_client, MONGODB_DATABASE
from db.engine import Base, Session, engine

session = None
stripe_product_id = '123'


def setup_module():
    global session
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    session = Session()
    mongo_client.drop_database(MONGODB_DATABASE)


def teardown_module():
    Base.metadata.drop_all(engine)
    mongo_client.drop_database(MONGODB_DATABASE)
    session.close()


def test_get_package_for_product():
    global session
    test_package = BenefitPackage(stripe_product_id=stripe_product_id,
                                  extra_feeds=0, allow_webhook=True, refresh_rate_seconds=10)
    session.add(test_package)

    session.commit()
    found_package = BenefitPackage.get_package_for_product(
        session,
        stripe_product_id
    )
    assert found_package is not None
    pass
