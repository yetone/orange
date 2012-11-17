# coding: utf-8

import hashlib
from random import choice
import time
import sqlalchemy as sa
from database import db, mBase
import config
from .follower import Follower
import models
from helpers import formatDate2

config = config.rec()

class User(mBase):
    __tablename__ = 'users'
    __table_args__ = {
        'mysql_charset': 'utf8',
    }

    id = sa.Column(sa.Integer, primary_key = True, autoincrement = True)
    name = sa.Column(sa.String(100), unique = True, index = True)
    email = sa.Column(sa.String(200), unique = True, nullable = False, index =
            True)
    password = sa.Column(sa.String(100), nullable = False)
    avatar = sa.Column(sa.String(400))
    website = sa.Column(sa.String(400))

    role = sa.Column(sa.Integer, default = 1)
    reputation = sa.Column(sa.Integer, default = 0, index = True)
    created_at = sa.Column(sa.Integer, default=int(time.time()))

    city = sa.Column(sa.String(200))
    edit_username_count = sa.Column(sa.Integer, default=2)
    description = sa.Column(sa.Text)

    def __init__(self, name=name, email=email, password=password, avatar=None,
            website=None, city=None, description=None):
        self.name = name
        self.email = email
        self.password = password
        self.avatar = avatar
        self.website = website
        self.city = city
        self.description = description

    def get_avatar(self, size=48):
        if self.avatar:
            avatar = self.avatar
            ext = avatar.split('.').pop()
            length = len(ext) + 1
            avatar = avatar[1:-length]
            return "%sx%s.%s" % (avatar, size, ext)
        md5email = hashlib.md5(self.email).hexdigest()
        query = "%s?s=%s%s" % (md5email, size, config.gravatar_extra)
        return config.gravatar_base_url + query

    def get_followers(self):
        whoes = db.query(Follower).order_by(sa.desc(Follower.created_at)).filter(Follower.whom_id == self.id).all()
        followers = []
        for who in whoes:
            followers += [db.query(User).filter(User.id == who.who_id).first()]
        return followers

    def get_followeders(self):
        whoms = db.query(Follower).order_by(sa.desc(Follower.created_at)).filter(Follower.who_id == self.id).all()
        followeders = []
        for whom in whoms:
            followeders += [db.query(User).filter(User.id == whom.whom_id).first()]
        return followeders

    def get_notifiers(self):
        notifiers =\
        db.query(models.Notifier).order_by(sa.desc(models.Notifier.created_at)).filter(models.Notifier.whom_id
                == self.id).all()
        return notifiers

    def get_unread_notifiers(self):
        notifiers =\
        db.query(models.Notifier).order_by(sa.desc(models.Notifier.created_at)).filter(sa.and_(models.Notifier.whom_id
                == self.id, models.Notifier.status == 0)).all()
        return notifiers

    def get_follower_ids(self):
        whoes = db.query(Follower).order_by(sa.desc(Follower.created_at)).filter(Follower.whom_id == self.id).all()
        follower_ids = []
        for who in whoes:
            follower_ids.append(who.who_id)
        return follower_ids

    def get_followeder_ids(self):
        whoms = db.query(Follower).order_by(sa.desc(Follower.created_at)).filter(Follower.who_id == self.id).all()
        followeder_ids = []
        for whom in whoms:
            followeder_ids.append(whom.whom_id)
        followeder_ids.append(self.id)
        return followeder_ids

    def get_posts_amount(self):
        posts = db.query(models.Post).filter(models.Post.user_id == self.id).all()
        return len(posts) if posts else 0

    def get_followers_amount(self):
        followers = self.get_followers()
        return len(followers)

    def get_followeders_amount(self):
        followeders = self.get_followeders()
        return len(followeders)

    def format_date(self):
        return formatDate2(self.created_at)
    @staticmethod
    def create_password(raw):
        salt = User.create_token(8)
        hsh = hashlib.sha1(salt + raw + config.password_secret).hexdigest()
        return "%s$%s" % (salt, hsh)

    @staticmethod
    def create_token(length=16):
        chars = ('0123456789'
                 'abcdefghijklmnopqrstuvwxyz'
                 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        salt = ''.join([choice(chars) for i in range(length)])
        return salt

    def check_password(self, raw):
        if '$' not in self.password:
            return False
        salt, hsh = self.password.split('$')
        verify = hashlib.sha1(salt + raw + config.password_secret).hexdigest()
        return verify == hsh
