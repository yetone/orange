# coding: utf-8

import tornado.web
import tornado.escape

import random
import os
import shutil
import copy
import time
import tempfile
import Image
import logging
import config
from .base import BaseHandler
import helpers
from database import db
import sqlalchemy as sa
from extensions import md
from sqlalchemy.sql.expression import func, select

from models import User, Post, Follower, Favorite, Retweet
config = config.rec()

def get_user_count():
    return len(db.query(User).all())

def get_unread_count(user):
    return len(user.get_unread_notifiers())


class UserProfileGet(BaseHandler):
    @tornado.web.authenticated
    def get(self, username):
        if self.is_ajax():
            currenter = self.current_user
            user = db.query(User).filter(User.name == username).first()
            if user in currenter.get_followeders():
                f = 1
            else:
                f = 0
            self.write(tornado.escape.json_encode({'username': user.name,
                'avatar': user.get_avatar(), 'description': user.description,
                'f': f}))

class UserListPage(BaseHandler):
    def get(self):
        users = db.query(User).all()
        names = [x.name for x in users]
        if self.is_ajax():
            self.write("%s" % tornado.escape.json_encode(names))
            #self.write("%s" % names)
        else:
            self.render("user/list.html", users=users)
        return

class ReferrerPage(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.current_user
        users = db.query(User).order_by(func.rand()).filter(User.id !=
                user.id).limit(9).all()
        self.render("user/referrers.html", users=users)
        return

class HomeHandler(BaseHandler):
    def get(self, username, page=1):
        page = int(page)
        user = db.query(User).filter(User.name==username).first()
        if not user:
            self.redirect('/')
            return
        posts = db.query(Post).order_by(sa.desc(Post.created_at)).filter(Post.user_id==user.id).offset((page - 1) *
                config.paged).limit(config.paged).all()
        if self.is_ajax():
            self.render("site/ajaxpage.html", user=user, posts=posts,
                    formatDate=helpers.formatDate)
            return
        else:
            self.render("user/index.html", user=user, posts=posts,
                    formatDate=helpers.formatDate, page=page)
            return

class PostsHandler(BaseHandler):
    def get(self, user_name, page=1):
        page = int(page)
        user = db.query(User).filter(User.name == user_name).first()
        posts = user.get_posts(page=page)
        if self.is_ajax():
            self.render("site/ajaxpage.html", posts=posts, page=page, user=user)
        else:
            self.render("user/posts.html", posts=posts, page=page, user=user)
        return

class AvatarUploadHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        if self.request.files == {} or 'myavatar' not in self.request.files:
            self.write('<script>alert("请选择图片")</script>')
            return
        image_type_list = ['image/gif', 'image/jpeg', 'image/pjpeg',
                'image/png', 'image/bmp', 'image/x-png']
        send_file = self.request.files['myavatar'][0]
        if send_file['content_type'] not in image_type_list:
            self.write('<script>alert("仅支持 jpg, jpeg, bmp, gif, png\
                    格式的图片！");</script>')
            return
        if len(send_file['body']) > 4 * 1024 * 1024:
            self.write('<script>alert("请上传4M以下的图片");</script>')
            return
        tmp_file = tempfile.NamedTemporaryFile(delete=True)
        tmp_file.write(send_file['body'])
        tmp_file.seek(0)
        try:
            image_one = Image.open(tmp_file.name)
        except IOError, error:
            logging.info(error)
            logging.info('+'*30 + '\n')
            logging.info(self.request.headers)
            tmp_file.close()
            self.write('<script>alert("图片不合法！");</script>')
            return
        if image_one.size[0] < 180 or image_one.size[1] < 180 or \
                image_one.size[0] > 2000 or image_one.size[1] > 2000:
            tmp_file.close()
            self.write('<script>alert("图片长宽在180px~2000px之间！");</script>')
            return
        user = self.current_user
        image_path = "./static/img/avatar/" + user.name + "/"
        '''
        if not os.path.exists(image_path):
            os.mkdir(image_path)
        '''
        shutil.rmtree(image_path, True)
        os.mkdir(image_path)
        timestamp = str(int(time.time()))
        image_format = send_file['filename'].split('.').pop().lower()
        tmp_name = image_path + timestamp + '.' + image_format
        tmp_name2 = image_path + timestamp + 'x24.' + image_format
        tmp_name3 = image_path + timestamp + 'x48.' + image_format
        tmp_name4 = image_path + timestamp + 'x96.' + image_format
        tmp_name5 = image_path + timestamp + 'x128.' + image_format
        image_two = image_one.copy()
        image_three = image_one.copy()
        image_four = image_one.copy()
        image_five = image_one.copy()
        image_one.save(tmp_name)
        image_two.thumbnail((24, 24), Image.ANTIALIAS)
        image_two.save(tmp_name2)
        image_three.thumbnail((48, 48), Image.ANTIALIAS)
        image_three.save(tmp_name3)
        image_four.thumbnail((96, 96), Image.ANTIALIAS)
        image_four.save(tmp_name4)
        image_five.thumbnail((128, 128), Image.ANTIALIAS)
        image_five.save(tmp_name5)
        tmp_file.close()
        user.avatar = tmp_name
        db.commit()
        self.redirect(self.next_url)
        self.write('<script>alert("文件上传成功，路径为：%s")</script>' % image_path[1:])
        return

class AccountSettingHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("user/setting.html")
        return
    def post(self):
        user = self.current_user
        description = self.get_argument("description", '')
        website = self.get_argument("website", '')
        city = self.get_argument("city", '')
        user.description = md(description)
        user.website = website
        user.city = city
        db.add(user)
        db.commit()
        self.redirect("/user/%s" % (user.name))
        return


class FollowHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, whom_name):
        who = self.current_user
        whom = db.query(User).filter(User.name==whom_name).first()
        if whom is None or whom is who:
            raise tornado.web.HTTPError(404)
        follower = db.query(Follower).filter(sa.and_(Follower.who_id==who.id, Follower.whom_id==whom.id)).first()
        if follower is not None:
            raise tornado.web.HTTPError(404)
        db.add(Follower(who_id=who.id, whom_id=whom.id))
        db.commit()
        self.redirect(self.next_url)
        return

class UnfollowHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, whom_name):
        who = self.current_user
        whom = db.query(User).filter(User.name==whom_name).first()
        if not whom:
            raise tornado.web.HTTPError(404)
        follower = db.query(Follower).filter(sa.and_(Follower.who_id==who.id, Follower.whom_id==whom.id)).first()
        db.delete(follower)
        db.commit()
        self.redirect(self.next_url)
        return

class FollowerHandler(BaseHandler):
    def get(self, username, page=1):
        page = int(page)
        user = db.query(User).filter(User.name==username).first()
        users = user.get_followers()
        if self.is_ajax():
            self.render("user/ajaxpage.html",
                    users=users[(page-1)*config.paged:page*config.paged],
                    currenter=user, page=page)
            return
        else:
            self.render("user/follower.html",
                    users=users[(page-1)*config.paged:page*config.paged],
                    currenter=user, page=page)
            return

class FollowederHandler(BaseHandler):
    def get(self, username, page=1):
        page = int(page)
        user = db.query(User).filter(User.name==username).first()
        users = user.get_followeders()
        if self.is_ajax():
            self.render("user/ajaxpage.html",
                    users=users[(page-1)*config.paged:page*config.paged],
                    currenter=user, page=page)
            return
        else:
            self.render("user/followeder.html",
                    users=users[(page-1)*config.paged:page*config.paged],
                    currenter=user, page=page)
            return

class NotifierHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user = self.current_user
        notifiers = user.get_notifiers()
        self.render("user/notifier.html", notifiers = notifiers)
        unread_notifiers = user.get_unread_notifiers()
        if unread_notifiers != []:
            for n in unread_notifiers:
                n.status = 1
        db.commit()
        return

class FavoriteHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, post_id):
        post_id = int(post_id)
        user = self.current_user
        post = db.query(Post).get(post_id)
        if post and post.user_id != user.id:
            favorite = db.query(Favorite).filter(sa.and_(Favorite.user_id ==\
                user.id, Favorite.post_id == post.id)).first()
            if favorite:
                db.delete(favorite)
            else:
                favorite = Favorite(user_id = user.id, post_id = post.id)
                db.add(favorite)
            db.commit()
        else:
            self.redirect(self.next_url)
        return

class RetweetHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, post_id):
        post_id = int(post_id)
        user = self.current_user
        post = db.query(Post).get(post_id)
        if post and post.type != 2 and post.user_id != user.id:
            re_post = db.query(Post).filter(sa.and_(Post.type == 2,
                Post.user_id == user.id, Post.post_id == post_id)).first()
            if re_post:
                db.delete(re_post)
            else:
                re_post = Post(user_id = user.id, content = '', origin_content
                        = '', type = 2, post_id = post.id)
                db.add(re_post)
            db.commit()
        else:
            self.redirect(self.next_url)
        return

class FavoritesShowHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, page=1):
        page = int(page)
        user = self.current_user
        posts = user.get_favorites(page=page)
        if not self.is_ajax():
            self.render("user/favorite.html", posts = posts, page = page,
                    user=user)
            return
        else:
            self.render("site/ajaxpage.html", posts = posts, page = page,
                    user=user)
            return

class UserFavoritesShowHandler(BaseHandler):
    def get(self, user_name, page=1):
        page = int(page)
        user = db.query(User).filter(User.name == user_name).first()
        posts = user.get_favorites(page=page)
        if not self.is_ajax():
            self.render("user/favorite.html", posts = posts, page = page,
                    user=user)
            return
        else:
            self.render("site/ajaxpage.html", posts = posts, page = page,
                    user=user)
            return

class NotifierLongPollingHandler(BaseHandler):
    @tornado.web.asynchronous
    def post(self):
        self.get_data(callback=self.on_finish)

    def get_data(self, callback):
        if self.request.connection.stream.closed():
            return

        num = get_unread_count(self.current_user)
        tornado.ioloop.IOLoop.instance().add_timeout(
                time.time() + 3,
                lambda: callback(num)
        )

    def on_finish(self, data=0):
        self.write("%d" % data)
        self.finish()

class LoginHandler(BaseHandler):
    def get(self):
        if self.current_user is not None:
            self.redirect("/")
        self.render("user/login.html")

    def post(self):
        name = self.get_argument("name", '')
        password = self.get_argument("password", '')
        if name == '' or password == '':
            self.flash_message('Please fill the required fields', 'error')
            self.render('user/login.html')
            return
        if '@' in name:
            user = db.query(User).filter(User.email==name).first()
        else:
            user = db.query(User).filter(User.name==name).first()
        if user and user.check_password(password):
            self.set_current_user(user.name, user.id)
            self.redirect(self.next_url)
            return
        else:
            self.flash_message('Invalid account or password', 'error')
            self.render('user/login.html')

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect(self.next_url)

class RegisterHandler(BaseHandler):
    def get(self):
        if self.get_current_user is None:
            self.redirect(self.next_url)
        else:
            self.render("user/register.html", name='', email='')

    def post(self):
            name = self.get_argument("name", '')
            email = self.get_argument('email', '')
            password = self.get_argument('password', '')
            password_confirmation = self.get_argument('password_confirmation',
                    '')
            if name == '' or email == '' or password == '':
                self.flash_message("Please fill the required fields", 'error')
                self.render('user/register.html', name=name, email=email)
                return

            if password != password_confirmation:
                self.flash_message("Password doesn't match", 'error')
                self.render('user/register.html', name=name, email=email)
                return

            if not helpers.email(email):
                self.flash_message("Please fill the right email", 'error')
                self.render('user/register.html', name=name, email=email)
                return

            if name.find(' ') != -1:
                self.flash_message("Please fill the right username", 'error')
                self.render('user/register.html', name=name, email=email)
                return

            if not helpers.email(email):
                self.flash_message('Not a valid email address', 'error')
                self.render('user/register.html', name=name, email=email)

            user = db.query(User).filter(User.email==email).first()
            if user:
                self.flash_message("This email is already registerd", 'warn')
                self.render('user/register.html', name=name, email=email)
            user = User(name=name,email=email,password=password)
            user.password = user.create_password(password)
            db.add(user)
            db.commit()
            self.set_current_user(user.name, user.id)
            self.redirect('/referrers')
            return

