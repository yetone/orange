# coding: utf-8

import config

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

config = config.rec()
engine = sa.create_engine(config.database + '?charset=utf8', pool_recycle=7200)

Session = sessionmaker()
Session.configure(autocommit = False, autoflush = False, bind = engine)
db = Session()

mBase = declarative_base()

def create_db():
    mBase.metadata.create_all(engine)
    print("数据库部署完成！")
    return

def drop_db():
    mBase.metadata.drop_all(engine)
    print("数据库删除完成！")
    return
