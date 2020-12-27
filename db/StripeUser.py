from sqlalchemy import Column, String
from db.engine import Base


class StripeUser(Base):
    __tablename__ = 'stripe_users'
    __table_args__ = {
        'useexisting': True
    }
    discord_id = Column(String, primary_key=True)
    customer_id = Column(String, nullable=False)

    def __repr__(self):
        return f'<User (discord_id={self.discord_id}, customer_id={self.customer_id})'
