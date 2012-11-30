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
                '''
                self.render('site/ajaxpage.html', posts = [post])
                '''
            else:
                self.redirect(self.next_url())
            if post.content.find('@') != -1:
                post_put_notifier(post)
        else:
            self.redirect(self.next_url)
        return


class PostEditHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, post_id):
        post_id = int(post_id)
        origin_content = self.get_argument("content", '')
        if origin_content != '':
            content = md(origin_content)
            user = self.current_user
            post = db.query(Post).get(post_id)
            post.origin_content = origin_content
            post.content = content
            db.commit()
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
    def get(self, post_id):
        post_id = int(post_id)
        user = self.get_current_user()
        post = db.query(Post).get(post_id)
        if post and post.user_id == user.id:
            comments = post.get_comments()
            retweets = post.get_retweets()
            if comments != []:
                for comment in comments:
                    db.delete(comment)
            if retweets != []:
                for retweet in retweets:
                    db.delete(retweet)
            db.delete(post)
            db.commit()
        else:
            self.redirect(self.next_url)
        return

