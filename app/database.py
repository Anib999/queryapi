from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse
from .config import settings

password = urllib.parse.quote_plus(settings.database_password)
DATABASE_URL = f'mssql+pyodbc://{settings.database_username}:{password}@{settings.database_hostname}/{settings.database_name}?driver=ODBC+Driver+17+for+SQL+Server'
# DATABASE_URL = 'mssql+pyodbc://<username>:<password>@<ipaddress/hostname>/<databasename>'

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
