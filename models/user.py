# coding: utf-8

import hashlib
from random import choice
import time
import sqlalchemy as sa
from database import db, mBase
import config
import models as m
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

    def get_timeline(self, timesnap, page):
        '''
        followeder_ids = self.get_followeder_ids()
        followeder_ids.append(self.id)
        retweet_relationships =\
            db.query(m.Retweet).filter(m.Retweet.user_id.in_(followeder_ids)).all()
        retweet_post_ids = []
        if retweet_relationships != []:
            for r in retweet_relationships:
                if r.post_id not in retweet_post_ids:
                    retweet_post_ids.append(r.post_id)
        retweets =\
            db.query(m.Post).filter(m.Post.id.in_(retweet_post_ids)).all()
        '''
        '''
        followeders = self.get_followeders()
        origin_posts = []
        #posts = retweets
        followeders.append(self)
        if followeders != []:
            for f in followeders:
                origin_posts += f.get_posts_and_retweets()
        posts = {}.fromkeys(origin_posts).keys()
        posts.sort(lambda p1, p2: -cmp(p1.get_created_in(self),
            p2.get_created_in(self)))
        posts = posts[((page - 1) * config.paged) : (page * config.paged)]
        '''
        followeder_ids = self.get_followeder_ids()
        followeder_ids.append(self.id)
        posts =\
        db.query(m.Post).order_by(sa.desc(m.Post.created_at)).filter(sa.and_(m.Post.user_id.in_(followeder_ids),
            m.Post.created_at < timesnap)).offset((page - 1) *
            config.paged).limit(config.paged).all()
        return posts

    def get_followers(self):
        whoes =\
            db.query(m.Follower).order_by(sa.desc(m.Follower.created_at)).filter(m.Follower.whom_id == self.id).all()
        followers = []
        for who in whoes:
            followers += [db.query(User).filter(User.id == who.who_id).first()]
        return followers

    def get_followeders(self):
        whoms =\
            db.query(m.Follower).order_by(sa.desc(m.Follower.created_at)).filter(m.Follower.who_id == self.id).all()
        followeders = []
        for whom in whoms:
            followeders += [db.query(User).filter(User.id == whom.whom_id).first()]
        return followeders

    def get_notifiers(self):
        notifiers =\
        db.query(m.Notifier).order_by(sa.desc(m.Notifier.created_at)).filter(m.Notifier.whom_id
                == self.id).all()
        return notifiers

    def get_unread_notifiers(self):
        notifiers =\
        db.query(m.Notifier).order_by(sa.desc(m.Notifier.created_at)).filter(sa.and_(m.Notifier.whom_id
                == self.id, m.Notifier.status == 0)).all()
        return notifiers

    def get_follower_ids(self):
        whoes =\
            db.query(m.Follower).order_by(sa.desc(m.Follower.created_at)).filter(m.Follower.whom_id == self.id).all()
        follower_ids = []
        for who in whoes:
            follower_ids.append(who.who_id)
        return follower_ids

    def get_followeder_ids(self):
        whoms =\
            db.query(m.Follower).order_by(sa.desc(m.Follower.created_at)).filter(m.Follower.who_id == self.id).all()
        followeder_ids = []
        for whom in whoms:
            followeder_ids.append(whom.whom_id)
        return followeder_ids

    def get_posts_and_retweets(self, page=1):
        retweet_relationships = db.query(m.Retweet).filter(m.Retweet.user_id ==\
                self.id).all()
        retweet_post_ids = []
        if retweet_relationships != []:
            for r in retweet_relationships:
                retweet_post_ids.append(r.post_id)
        retweets =\
        db.query(m.Post).filter(m.Post.id.in_(retweet_post_ids)).all()
        posts = db.query(m.Post).filter(m.Post.user_id ==\
                self.id).all() + retweets
        #return posts[((page - 1) * config.paged): (page * config.paged)]
        return posts

    def get_posts(self, page=1):
        posts =\
        db.query(m.Post).order_by(sa.desc(m.Post.created_at)).filter(m.Post.user_id ==\
                self.id).offset((page - 1) * config.paged).limit(config.paged).all()
        return posts

    def get_posts_amount(self):
        posts = db.query(m.Post).filter(m.Post.user_id == self.id).all()
        return len(posts) if posts else 0

    def get_followers_amount(self):
        followers = self.get_followers()
        return len(followers)

    def get_followeders_amount(self):
        followeders = self.get_followeders()
        return len(followeders)

    def get_favorites(self, page=1):
        favorites =\
        db.query(m.Favorite).order_by(sa.desc(m.Favorite.created_at)).filter(m.Favorite.user_id ==\
                self.id).offset((page - 1) *
                        config.paged).limit(config.paged).all()
        posts = []
        for favorite in favorites:
            posts += [db.query(m.Post).filter(m.Post.id ==\
                favorite.post_id).first()]
        return posts

    @property
    def favorites(self, page=1):
        favorites =\
        db.query(m.Favorite).order_by(sa.desc(m.Favorite.created_at)).filter(m.Favorite.user_id ==\
                self.id).all()
        posts = []
        for favorite in favorites:
            posts += [db.query(m.Post).filter(m.Post.id ==\
                favorite.post_id).first()]
        return posts

    def faved_it(self, post):
        favorite =\
        db.query(m.Favorite).filter(sa.and_(m.Favorite.user_id ==
            self.id, m.Favorite.post_id == post.id)).first()
        return favorite

    def retweeted_it(self, post):
        retweet = db.query(m.Post).filter(sa.and_(m.Post.type == 2,
            m.Post.user_id == self.id, m.Post.post_id == post.id)).first()
        return retweet

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
