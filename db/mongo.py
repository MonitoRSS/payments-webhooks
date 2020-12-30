from db.mongodb.Subscriber import Subscriber
from utils.constants import MONGODB_URI, MONGODB_DATABASE
from mongoengine import (
    connect,
)
# from pymongo import MongoClient

mongo_db = connect(MONGODB_DATABASE, host=MONGODB_URI)


def find_stripe_customer_suscriber(customer_id: str):
    return Subscriber.objects().get(_id=customer_id)
