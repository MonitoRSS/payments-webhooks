from db.postgresdb.StripeUser import StripeUser
from db.postgres import postgres_db


class BenefitPackage(postgres_db.Model):
    __tablename__ = 'benefits_packages'
    __table_args__ = {
        'useexisting': True
    }
    stripe_product_id = postgres_db.Column(
        postgres_db.String,
        primary_key=True)
    extra_feeds = postgres_db.Column(
        postgres_db.Integer,
        default=0,
        nullable=False)
    allow_webhook = postgres_db.Column(
        postgres_db.Boolean,
        default=True,
        nullable=False)
    refresh_rate_seconds = postgres_db.Column(
        postgres_db.Integer,
        nullable=False)

    def __repr__(self):
        return ('<BenefitPackage ('
                f'stripe_product_id={self.stripe_product_id}, '
                f'extra_feeds={self.extra_feeds}, '
                f'allow_webhook={self.allow_webhook}, '
                f'refresh_rate_seconds={self.refresh_rate_seconds})')

    @staticmethod
    def get_package_for_product(product_id: str):
        return BenefitPackage.query.filter_by(stripe_product_id=product_id).first()

    def apply_to_customer(self, customer_id: str):
        # Get their Discord ID
        discord_id = StripeUser.get_customer_discord_id(customer_id)
        if discord_id is None:
            print(
                f"Unknown discord id to apply benefit package"
                f"{self.stripe_product_id} to customer {customer_id}"
            )
            return
        # Create the document to be saved

    def remove_from_customer(self, customer_id: str):
        # Get their Discord ID
        discord_id = StripeUser.get_customer_discord_id(customer_id)
        if discord_id is None:
            print(
                f"Unknown discord id to remove benefit package"
                f"{self.stripe_product_id} from customer {customer_id}"
            )
            return
        pass
