#coding: utf-8

import time
import sqlalchemy as sa
from database import mBase, db
from helpers import formatDate

from .user import User

class Comment(mBase):
    __tablename__ = 'comments'
    __table_args__ = {
        'mysql_charset': 'utf8',
    }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    post_id = sa.Column(sa.Integer, index = True)
    user_id = sa.Column(sa.Integer, nullable = False)
    content = sa.Column(sa.Text)
    origin_content = sa.Column(sa.Text)
    created_at = sa.Column(sa.Integer)
    updated_at = sa.Column(sa.Integer)

    def __init__(self, post_id=post_id, user_id=user_id, content=content,
            origin_content=None, created_at=None, updated_at=None):
        if content is None:
            return None
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
        self.updated_at = updated_at
        if origin_content is None:
            self.origin_content = content
        else:
            self.origin_content = origin_content
        if created_at is None:
            self.created_at = int(time.time())
        else:
            self.created_at = created_at

    def get_author(self):
        return db.query(User).get(self.user_id)

    def format_date(self):
        return formatDate(self.created_at)
