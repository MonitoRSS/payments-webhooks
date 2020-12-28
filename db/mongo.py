from utils.constants import MONGODB_URI, MONGODB_DATABASE
from pymongo import MongoClient

mongo_client = MongoClient(MONGODB_URI)
mongo_db = mongo_client[MONGODB_DATABASE]


def find_stripe_customer_suscriber(customer_id: str):
    return mongo_db.subscribers.find_one({
        "_id": customer_id
    })
