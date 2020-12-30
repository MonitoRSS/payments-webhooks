from typing import Union
from app import postgres_db


class StripeUser(postgres_db.Model):
    __tablename__ = 'stripe_users'
    __table_args__ = {
        'useexisting': True
    }
    discord_id = postgres_db.Column(postgres_db.String, primary_key=True)
    customer_id = postgres_db.Column(postgres_db.String, nullable=False)

    def __repr__(self):
        return f'<User (discord_id={self.discord_id}, customer_id={self.customer_id})'

    @staticmethod
    def get_customer_discord_id(customer_id: str) -> Union[str, None]:
        stripe_user = postgres_db.session.query(StripeUser).filter_by(
            customer_id=customer_id).first()
        if stripe_user is None:
            return None
        else:
            return stripe_user.discord_id
