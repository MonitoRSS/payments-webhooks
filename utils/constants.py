import sys
import os

FLASK_ENV = os.getenv("FLASK_ENV")
FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
STRIPE_SECRET_API_KEY = os.getenv("STRIPE_SECRET_API_KEY")
POSTGRES_URI = 'sqlite:///test.db' if 'pytest' in sys.modules else os.getenv(
    "POSTGRES_URI")
MONGODB_URI = "mongomock://localhost" if 'pytest' in sys.modules else os.getenv(
    "MONGODB_URI")
MONGODB_DATABASE = 'test' if 'pytest' in sys.modules else os.getenv(
    "MONGODB_DATABASE")
