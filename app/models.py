from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.expression import text


'''Company and Folders'''


class Company(Base):
    __tablename__ = 'CompanyTbl'

    CId = Column(Integer, primary_key=True, nullable=False)
    CompanyName = Column(String(200), nullable=False)
    DatabaseName = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True),
                        nullable=False, server_default=text('getdate()'))
    # server_default='TRUE'


class Folder(Base):
    __tablename__ = 'FolderTbl'

    FId = Column(Integer, primary_key=True, nullable=False)
    FolderName = Column(String(100), nullable=False)
    created_date = Column(DateTime(timezone=True),
                          nullable=False, server_default=text('getdate()'))


'''Query and Details'''


class Query(Base):
    __tablename__ = 'QueryTbl'

    QId = Column(Integer, primary_key=True, nullable=False)
    QueryName = Column(String(300), nullable=False)
    QueryDescription = Column(String, nullable=True)
    QueryIsUsed = Column(Boolean, default=True)
    company_id = Column(Integer, ForeignKey('CompanyTbl.CId', ondelete='CASCADE'), nullable=False)
    folder_id = Column(Integer, ForeignKey('FolderTbl.FId', ondelete='CASCADE'), nullable=False)
    created_date = Column(DateTime(timezone=True),
                          nullable=False, server_default=text('getdate()'))


class QueryDetails(Base):
    __tablename__ = 'QueryDetailsTbl'

    QdId = Column(Integer, primary_key=True, nullable=False)
    QueryDetail = Column(String, nullable=True)
    query_id = Column(Integer, ForeignKey(
        'QueryTbl.QId', ondelete='CASCADE'), nullable=False)
    created_date = Column(DateTime(timezone=True),
                          nullable=False, server_default=text('getdate()'))


'''User Details'''


class User(Base):
    __tablename__ = 'UserTbl'

    UId = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True),
                        nullable=False, server_default=text('getdate()'))


class UserDetails(Base):
    __tablename__ = 'UserDetailsTbl'

    UdId = Column(Integer, primary_key=True, nullable=False)
    FullName = Column(String(300), nullable=False)
    Address = Column(String(200), nullable=True)
    MobileNo = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True),
                        nullable=False, server_default=text('getdate()'))


'''Comments / Remarks and Votes / Likes'''


class Comments(Base):
    __tablename__ = 'CommentsTbl'

    CoId = Column(Integer, primary_key=True, nullable=False)
    CommentDetail = Column(String, nullable=False)
    query_id = Column(Integer, ForeignKey('QueryTbl.QId', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('UserTbl.UId', ondelete='CASCADE'), nullable=False)
    created_date = Column(DateTime(timezone=True),
                          nullable=False, server_default=text('getdate()'))


class Votes(Base):
    __tablename__ = 'VotesTbl'

    VId = Column(Integer, primary_key=True, nullable=False)
    created_date = Column(DateTime(timezone=True),
                          nullable=False, server_default=text('getdate()'))
