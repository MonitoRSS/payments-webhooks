import pytest
from services.subscribers import increment_lifetime_paid
from db.mongo import Subscriber, mongo_db, MONGODB_DATABASE
from app import postgres_db, app

# Needed for SQLAlchemy to run within a context
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
app.app_context().push()


@pytest.fixture(autouse=True)
def run_around_tests():
    postgres_db.drop_all()
    postgres_db.create_all()
    mongo_db.drop_database(MONGODB_DATABASE)


def test_increment_lifetime_paid():
    customer_id = '1234'
    Subscriber(_id=customer_id, discordId="1234", lifetimePaid=5,
               products=[]).save()
    increment_lifetime_paid(customer_id, 100)
    subscriber = Subscriber.objects().get(_id=customer_id)
    assert subscriber.lifetimePaid == 105
