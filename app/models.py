from .database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.expression import text


class Company(Base):
    __tablename__ = 'CompanyTbl'

    CId = Column(Integer, primary_key=True, nullable=False)
    CompanyName = Column(String(200), nullable=False)
    DatabaseName = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True),
                        nullable=False, server_default=text('getdate()'))
    # server_default='TRUE'

class User(Base):
    __tablename__ = 'UserTbl'
    UId = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True),
                        nullable=False, server_default=text('getdate()'))
