# coding: utf-8

import time
from database import mBase, db
import sqlalchemy as sa
from helpers import formatDate

import models as m

class Notifier(mBase):
    __tablename__ = 'notifiers'
    __table_args__ = {
        'mysql_charset': 'utf8',
    }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    who_id = sa.Column(sa.Integer, index = True)
    whom_id = sa.Column(sa.Integer, index = True)
    post_id = sa.Column(sa.Integer, default = 0)
    comment_id = sa.Column(sa.Integer)
    type = sa.Column(sa.Integer, index = True, default = 1)
    status = sa.Column(sa.Integer, index = True, default = 0)
    created_at = sa.Column(sa.Integer)

    def __init__(self, who_id=who_id, whom_id=whom_id, post_id=0,
            comment_id=comment_id, type=1, status=0, created_at=None):
        self.who_id = who_id
        self.whom_id = whom_id
        self.post_id = post_id
        self.comment_id = comment_id
        self.type = type
        self.status = status
        if created_at is None:
            self.created_at = int(time.time())
        else:
            self.created_at = created_at

    def get_who(self):
        return db.query(m.User).filter(m.User.id == self.who_id).first()

    def get_whom(self):
        return db.query(m.User).filter(m.User.id == self.whom_id).first()

    def get_post(self):
        return db.query(m.Post).filter(m.Post.id == self.post_id).first()

    def get_comment(self):
        return db.query(m.Comment).filter(m.Comment.id == self.comment_id).first()

    def format_date(self):
        return formatDate(self.created_at)

    def get_content(self):
        if self.type == 3:
            return db.query(m.Post).filter(m.Post.id ==
                    self.post_id).first().content
        else:
            return db.query(m.Comment).filter(m.Comment.id ==
                    self.comment_id).first().content
