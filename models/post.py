# coding: utf-8

import time
import sqlalchemy as sa
from database import mBase, db
from .user import User
from .comment import Comment
from helpers import formatDate, strip_tags

class Post(mBase):
    __tablename__ = 'posts'
    __table_args__ = {
        'mysql_charset': 'utf8',
    }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    user_id = sa.Column(sa.Integer)
    content = sa.Column(sa.Text)
    origin_content = sa.Column(sa.Text)
    created_at = sa.Column(sa.Integer)
    updated_at = sa.Column(sa.Integer)

    def __init__(self, user_id=user_id, content=content, origin_content=None, created_at=None,
            updated_at=None):
        if content is None or user_id is None:
            return None
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

    def get_comments(self):
        return db.query(Comment).order_by(sa.desc(Comment.created_at)).filter(Comment.post_id
            == self.id).all()

    def format_date(self):
        return formatDate(self.created_at)

    def format_content(self):
        return strip_tags(self.content)[0:40] + '...'

    def __repr__(self):
        return '<Post %s>' % (self.content)
