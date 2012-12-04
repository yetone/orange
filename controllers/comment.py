# coding: utf-8

import time

import tornado.escape
import tornado.web

import config
from helpers import formatDate, put_notifier
from .base import BaseHandler
from extensions import md
from database import db

from models import Post, Comment, Notifier

import sqlalchemy as sa

config = config.rec()

class CommentAddHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, post_id):
        user = self.current_user
        post_id = int(post_id)
        post = db.query(Post).get(post_id)
        if not post:
            raise tornado.web.HTTPError(404)
        else:
            origin_content = self.get_argument("comment-content", '')
            content = md(origin_content)
            if origin_content == '':
                self.redirect(self.next_url)
                return
            comment = Comment(post_id=post_id, user_id=user.id, content=content,
                origin_content=origin_content)
            db.add(comment)
            db.commit()
            the_comment = db.query(Comment).order_by(sa.desc(Comment.created_at)).filter(Comment.user_id ==
                    user.id).first()
            if self.is_ajax():
                self.write(tornado.escape.json_encode({'username': user.name, 'avatar':
                    user.get_avatar(size=24), 'time': formatDate(int(time.time())),
                    'content': content}))
            if post.user_id != user.id:
                db.add(Notifier(post_id=post_id, who_id=user.id,
                    whom_id=post.user_id,
                    comment_id=the_comment.id))
                db.commit()
            if content.find('@') != -1:
                put_notifier(comment=comment, post=post)
