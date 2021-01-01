from db.postgresdb.BenefitPackage import BenefitPackage
from db.mongo import mongo_db, MONGODB_DATABASE
from app import postgres_db, app

# Needed for SQLAlchemy to run within a context
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
app.app_context().push()

stripe_product_id = '123'


def setup_module():
    postgres_db.drop_all()
    postgres_db.create_all()
    mongo_db.drop_database(MONGODB_DATABASE)


def teardown_module():
    postgres_db.drop_all()
    mongo_db.drop_database(MONGODB_DATABASE)


def test_get_package_for_product():
    test_package = BenefitPackage(stripe_product_id=stripe_product_id,
                                  extra_feeds=0, allow_webhook=True, refresh_rate_seconds=10)
    postgres_db.session.add(test_package)
    postgres_db.session.commit()
    found_package = BenefitPackage.get_package_for_product(
        stripe_product_id
    )
    assert found_package is not None
