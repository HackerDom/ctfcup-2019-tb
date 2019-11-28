import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.filters import add_filters


ADMIN_LOGIN = "admin"
HASH_SALT = os.environ["HASH_SALT"]

app = Flask(__name__)

postgres_host = os.environ["POSTGRES_HOST"]
postgres_port = os.environ["POSTGRES_PORT"]
postgres_db = os.environ["POSTGRES_DB"]
postgres_user = os.environ["POSTGRES_USER"]
postgres_password = os.environ["POSTGRES_PASSWORD"]

SQLALCHEMY_DATABASE_URI = f'postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}'
app.config.update(
    dict(
        SECRET_KEY=os.environ['FLASK_SECRET_KEY'],
        SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI
    )
)

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base = declarative_base()
Session = sessionmaker(bind=engine)
db = SQLAlchemy(app)
add_filters(app)

from views import *
from models import *

Base.metadata.create_all(bind=engine)
