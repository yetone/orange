# coding: utf-8

import time

import config
from helpers import formatDate, post_put_notifier
from .base import BaseHandler
from extensions import md
from database import db
import tornado.escape
import tornado.web

from models import Post, User

import sqlalchemy as sa

config = config.rec()

class PostHandler(BaseHandler):
    def get(self, post_id):
        post_id = int(post_id)
        post = db.query(Post).get(post_id)
        self.render("post/iterm.html", post=post)
        return

class PostAddHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        user = self.get_current_user()
        origin_content = self.get_argument("content", '')
        content = md(origin_content)
        if origin_content != '':
            post = Post(user_id=user.id, content=content, origin_content=origin_content)
            db.add(post)
            db.commit()
            if self.is_ajax():
                self.write(tornado.escape.json_encode({'username': user.name, 'avatar':
                    user.get_avatar(), 'time': formatDate(int(time.time())),
                    'content': content, 'id': post.id}))
            else:
                self.redirect(self.nex_url())
            if post.content.find('@') != -1:
                post_put_notifier(post)
        else:
            self.redirect(self.next_url)
            return


class PostEditHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        user_id = int(self.get_current_user().id)
        origin_content = self.get_argument("content", '')
        content = md(origin_content)
        if origin_content != '':
            db.add(Post(user_id=user_id, content=content, origin_content=origin_content))
            db.commit()
            user = db.query(User).get(user_id)
            if self.is_ajax():
                self.write(tornado.escape.json_encode({'username': user.name, 'avatar':
                    user.get_avatar(), 'time': formatDate(int(time.time())),
                    'content': content}))
            else:
                self.redirect(self.next_url())
        else:
            self.redirect(self.next_url)
            return

class PostDelHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, post_id):
        post_id = int(post_id)
        user = self.get_current_user()
        post = db.query(Post).get(post_id)
        if post:
            if post.user_id == user.id:
                comments = post.get_comments()
                if comments != []:
                    for comment in comments:
                        db.delete(comment)
                db.delete(post)
                db.commit()
        self.redirect(self.next_url)
        return

class TwitterFormModule(tornado.web.UIModule):
    def render(self):
        return self.render_string("modules/twitterform.html")

class ItermsModule(tornado.web.UIModule):
    def render(self, posts):
        return self.render_string("modules/iterms.html", posts=posts)
