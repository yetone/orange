# coding: utf-8

import tornado.web

class TwitterForm(tornado.web.UIModule):
    def render(self):
        return self.render_string("modules/twitterform.html")

class Iterms(tornado.web.UIModule):
    def render(self, posts):
        return self.render_string("modules/iterms.html", posts=posts)

class Profile(tornado.web.UIModule):
    def render(self, user):
        return self.render_string("modules/profile.html", user=user)

class UserList(tornado.web.UIModule):
    def render(self, users):
        return self.render_string("modules/userlist.html", users=users)
