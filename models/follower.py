# coding: utf-8

import hashlib
import time
import sqlalchemy as sa
from database import mBase
import config

config = config.rec()

class Follower(mBase):
    __tablename__ = 'followers'
    __table_args__ = {
        'mysql_charset': 'utf8',
    }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    who_id = sa.Column(sa.Integer)
    whom_id = sa.Column(sa.Integer)
    created_at = sa.Column(sa.Integer, default=int(time.time()))

    def __init__(self, who_id=who_id, whom_id=whom_id):
        self.who_id = who_id
        self.whom_id = whom_id
