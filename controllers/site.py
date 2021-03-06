# coding: utf-8

import tornado.web
import tornado.websocket
import tornado.ioloop

import time
import logging
import config
from .base import BaseHandler
from database import db

import sqlalchemy as sa

from models import Post

config = config.rec()

def get_unread_count(hi, user):
    if user:
        nrtimesnap = hi.get_nrtimesnap()
        followeder_ids = user.get_followeder_ids()
        count =\
        db.query(Post).order_by(sa.desc(Post.created_at)).filter(sa.and_(Post.user_id.in_(followeder_ids),
            Post.created_at > nrtimesnap, Post.user_id != user.id)).count()
    else:
        count =\
        db.query(Post).order_by(sa.desc(Post.created_at)).filter(Post.created_at
                > nrtimesnap).count()
    return count

class StartHandler(BaseHandler):
    def get(self):
        self.render("site/start.html")

class HomeHandler(BaseHandler):
    def get(self, page=1):
        page = int(page)
        user = self.current_user
        if not self.is_ajax():
            self.set_timesnap()
            self.set_nrtimesnap()
            timesnap = int(time.time())
        else:
            timesnap = self.get_timesnap()
        if not user:
            posts =\
            db.query(Post).order_by(sa.desc(Post.created_at)).filter(Post.created_at
                    < timesnap).offset((page - 1) *
                config.paged).limit(config.paged).all()
            self.render("site/start.html", posts=posts)
            return
        else:
            posts = user.get_timeline(timesnap, page)
        if self.is_ajax():
            self.render("site/ajaxpage.html", posts=posts, page=page)
            return
        else:
            self.render("site/index.html", posts=posts, page=page)
            return

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        current_user = self.current_user
        posts = []
        if current_user:
            return
        posts = db.query(Post).all()
        num = len(posts)
        text = self.request.headers
        self.write_message(str(text))

    def on_message(self, message):
        logging.info("getting message %s", message)
        self.write_message("You say:" + message)

class LongPollingHandler(BaseHandler):
    @tornado.web.asynchronous
    def post(self):
        self.get_data(callback=self.on_finish)

    def get_data(self, callback):
        if self.request.connection.stream.closed():
            return

        num = get_unread_count(self, self.current_user)
        tornado.ioloop.IOLoop.instance().add_timeout(
                time.time() + 3,
                lambda: callback(num)
        )

    def on_finish(self, data=0):
        self.write("%d" % data)
        self.finish()

class LoadUnreadHandler(BaseHandler):
    def get(self):
        if self.request.headers.has_key('X-Requested-With'):
            nrtimesnap = self.get_nrtimesnap()
            self.set_nrtimesnap()
            user = self.current_user
            if user:
                followeder_ids = user.get_followeder_ids() + [user.id]
                posts =\
                db.query(Post).order_by(sa.desc(Post.created_at)).filter(sa.and_(Post.user_id.in_(followeder_ids),
                    Post.created_at > nrtimesnap)).all()
            else:
                posts =\
                db.query(Post).order_by(sa.desc(Post.created_at)).filter(Post.created_at
                        > nrtimesnap).all()
            self.render("site/ajaxpage.html", posts=posts)
            return
        else:
            self.render("site/ajaxpage.html", posts=db.query(Post).all())
            return
