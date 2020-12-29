from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils.constants import POSTGRES_URI

Base = declarative_base()
engine = create_engine(POSTGRES_URI, echo=True)

Session = sessionmaker(bind=engine)
