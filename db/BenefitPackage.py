from sqlalchemy import Column, String, Integer, Boolean
from db.engine import Base


class BenefitPackage(Base):
    __tablename__ = 'benefits_packages'
    __table_args__ = {
        'useexisting': True
    }
    stripe_product_id = Column(String, primary_key=True)
    extra_feeds = Column(Integer, default=0, nullable=False)
    allow_webhook = Column(Boolean, default=True, nullable=False)
    refresh_rate_seconds = Column(Integer, nullable=False)

    def __repr__(self):
        return ('<BenefitPackage ('
                f'stripe_product_id={self.stripe_product_id}, '
                f'extra_feeds={self.extra_feeds}, '
                f'allow_webhook={self.allow_webhook}, '
                f'refresh_rate_seconds={self.refresh_rate_seconds})')
