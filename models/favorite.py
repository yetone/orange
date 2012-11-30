# coding: utf-8

import time
from database import mBase
import sqlalchemy as sa


class Favorite(mBase):
    __tablename__ = 'favorites'
    __table_args__ = {
        'mysql_charset': 'utf8',
    }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    user_id = sa.Column(sa.Integer, index = True)
    post_id = sa.Column(sa.Integer, index = True)
    type = sa.Column(sa.Integer, index = True, default = 1)
    created_at = sa.Column(sa.Integer, default = int(time.time()))

    def __init__(self, user_id=user_id, post_id=post_id):
        self.user_id = user_id
        self.post_id = post_id
