from sqlalchemy import Table,Column,ForeignKey,create_engine,MetaData
from sqlalchemy.sql.sqltypes import Integer,String

engine = create_engine("sqlite:///bookmarker.db",connect_args={'check_same_thread': False})
meta = MetaData()
conn = engine.connect()

users = Table(
    'users',meta,
    Column('userid',String(100),primary_key=True),
    Column('username',String(255),nullable=True),
    Column('email',String(255),nullable=True),
    Column('password',String(255),nullable=True),
    Column('apikey',String(255),nullable=True),
    Column('userVerificationToken',String(255),nullable=True),
    Column('isVerified',Integer,nullable=True),
    Column('userForgetVkey',String(255),nullable=True)
)

userSettings = Table(
    'userSettings',meta,
    Column('userid',String(255),ForeignKey('users.userid'),primary_key=True),
    Column('isAPIAccess',String(255),nullable=True),
    Column('isExtensionAccess',String(255),nullable=True)
)

bookmarks = Table(
    'bookmarks',meta,
    Column('userid',String(100),ForeignKey('users.userid'),primary_key=True),
    Column('category',String(255),nullable=True),
    Column('url',String(10000),nullable=True),
    Column('label',String(100),nullable=True),
    Column('icon',String(10000),nullable=True)
)

def createRequiredTable():
    try:
        meta.create_all(engine)
        return {
            "status":True
        }
    except:
        return {
            "status":False
        }


