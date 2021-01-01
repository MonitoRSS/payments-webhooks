from app import app, postgres_db
from utils.constants import POSTGRES_URI

print(f"Creating tables on {POSTGRES_URI}")

app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_URI
app.app_context().push()
postgres_db.init_app(app)
postgres_db.create_all()

print("Finished")
