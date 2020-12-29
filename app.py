import stripe
from flask import Flask
from utils.constants import STRIPE_SECRET_API_KEY
from routes.api import api
stripe.api_key = STRIPE_SECRET_API_KEY

app = Flask(__name__)

app.register_blueprint(api, url_prefix='/api')
