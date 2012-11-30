# coding: utf-8

import time
import sqlalchemy as sa
from database import mBase, db
from helpers import formatDate, strip_tags
import models as m

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
    type = sa.Column(sa.Integer, default=1)
    post_id = sa.Column(sa.Integer, default=0)

    def __init__(self, user_id=user_id, content=content, origin_content=None, created_at=None,
            updated_at=None, type=1, post_id=0):
        if content is None or user_id is None:
            return None
        self.user_id = user_id
        self.content = content
        self.updated_at = updated_at
        self.type = type
        self.post_id = post_id
        if origin_content is None:
            self.origin_content = content
        else:
            self.origin_content = origin_content
        if created_at is None:
            self.created_at = int(time.time())
        else:
            self.created_at = created_at

    def get_author(self):
        return db.query(m.User).get(self.user_id)

    def get_comments(self):
        return db.query(m.Comment).order_by(sa.desc(m.Comment.created_at)).filter(m.Comment.post_id
            == self.id).all()

    def get_origin_post(self):
        return db.query(Post).get(self.post_id)

    def get_retweets(self):
        return db.query(Post).filter(Post.post_id == self.id).all()

    def get_retweeters(self):
        retweets = self.get_retweets()
        retweeter_ids = []
        retweeters = []
        if retweets != []:
            for r in retweets:
                retweeter_ids += [r.user_id]
        if retweeter_ids != []:
            for r_id in retweeter_ids:
                retweeters += [db.query(m.User).get(r_id)]
        return retweeters

    def format_date(self):
        return formatDate(self.created_at)

    def format_retweet_date(self, user):
        followeder_ids = user.get_followeder_ids()
        retweet_relationships =\
            db.query(m.Retweet).order_by(sa.desc(m.Retweet.created_at)).filter(sa.and_(m.Retweet.post_id ==\
                    self.id, m.Retweet.user_id.in_(followeder_ids))).all()
        if retweet_relationships != []:
            return formatDate(retweet_relationships[0].created_at)
        else:
            return formatDate(self.created_at)

    def format_content(self):
        return strip_tags(self.content)[0:40] + '...'

    def __repr__(self):
        return '<Post %s>' % (self.content)
