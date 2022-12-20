from sqlalchemy import create_engine
from urllib.parse import quote_plus
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"

uri = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# Engine is responsible for establishing connection 

engine = create_engine(uri)


# To talk to a SQL DB we have to make use of a session
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()