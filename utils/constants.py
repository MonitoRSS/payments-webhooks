import sys
import os
from dotenv import load_dotenv

load_dotenv()

FLASK_ENV = os.environ["FLASK_ENV"]
STRIPE_WEBHOOK_SECRET = os.environ["STRIPE_WEBHOOK_SECRET"]
STRIPE_SECRET_API_KEY = os.environ["STRIPE_SECRET_API_KEY"]
POSTGRES_URI = 'sqlite:///test.db' if 'pytest' in sys.modules else os.environ[
    "POSTGRES_URI"]
MONGODB_URI = "mongomock://localhost" if 'pytest' in sys.modules else os.environ[
    "MONGODB_URI"]
MONGODB_DATABASE = 'test' if 'pytest' in sys.modules else os.environ[
    "MONGODB_DATABASE"]
