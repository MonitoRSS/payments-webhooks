from db.postgres import postgres_db
import stripe
from flask import Flask
from utils.constants import POSTGRES_URI, STRIPE_SECRET_API_KEY
from routes.api import api
import db.mongo
stripe.api_key = STRIPE_SECRET_API_KEY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URI
app.register_blueprint(api, url_prefix='/api')

postgres_db.init_app(app)
