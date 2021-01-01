from db.mongodb.Subscriber import Subscriber


def increment_lifetime_paid(subscriber_id: str, amount: int):
    Subscriber.objects(_id=subscriber_id).update_one(inc__lifetimePaid=amount)
