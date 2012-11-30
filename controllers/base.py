# coding: utf-8

import tornado.web

import time
import config
from database import db

from models import User
import controllers

config = config.rec()

class BaseHandler(tornado.web.RequestHandler):
    def render(self, *args, **kargs):
        kargs.update(dict(user_count=controllers.user.get_user_count()))
        super(BaseHandler,
                self).render(*args, **kargs)

    def on_finish(self):
        db.close()
        db.rollback()

    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if user_json:
            return db.query(User).get(int(tornado.escape.json_decode(user_json)['id']))
        else:
            return None

    def set_current_user(self, name, id):
        if name and id:
            self.set_secure_cookie("user", tornado.escape.json_encode({'name':
                name, 'id': id}))
        else:
            self.clear_cookie("user")

    def get_timesnap(self):
        user_json = self.get_secure_cookie("timesnap")
        if user_json:
            return int(tornado.escape.json_decode(user_json))
        else:
            self.set_timesnap()
            return int(time.time())

    def set_timesnap(self):
        timesnap = int(time.time())
        self.set_secure_cookie("timesnap", tornado.escape.json_encode(timesnap))

    def get_nrtimesnap(self):
        user_json = self.get_secure_cookie("nrtimesnap")
        if user_json:
            return int(tornado.escape.json_decode(user_json))
        else:
            self.set_nrtimesnap()
            return int(time.time())

    def set_nrtimesnap(self):
        nrtimesnap = int(time.time())
        self.set_secure_cookie("nrtimesnap",
                tornado.escape.json_encode(nrtimesnap))

    def check_admin(self):
        if not self.get_current_user()['id'] != 1:
            return None

    def is_ajax(self):
        if self.request.headers.has_key('X-Requested-With') and\
            self.request.headers['X-Requested-With'].lower() ==\
            'xmlhttprequest':
            return True
        else:
            return False


    @property
    def next_url(self):
        next_url = self.get_argument("next", None)
        return next_url or '/'

    def flash_message(self, value, type):
        return None

