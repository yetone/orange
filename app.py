# coding: utf-8
import os.path
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options

import config
from controllers import site, post, user, comment
from database import create_db

config = config.rec()
define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", site.HomeHandler),
            (r"/websocket[/]*", site.WebSocketHandler),
            (r"/longpolling[/]*", site.LongPollingHandler),
            (r"/page/(\d+)[/]*", site.HomeHandler),
            (r"/loadunread", site.LoadUnreadHandler),

            (r"/post/(\d+)[/]*", post.PostHandler),
            (r"/post/add[/]*", post.PostAddHandler),
            (r"/post/edit/(\d+)[/]*", post.PostEditHandler),
            (r"/post/del/(\d+)[/]*", post.PostDelHandler),

            (r"/post/(\d+)/comment/add[/]*", comment.CommentAddHandler),

            (r"/login[/]*", user.LoginHandler),
            (r"/logout[/]*", user.LogoutHandler),
            (r"/register[/]*", user.RegisterHandler),
            (r"/notifier[/]*", user.NotifierHandler),
            (r"/notifierpolling[/]*", user.NotifierLongPollingHandler),

            (r"/referrers[/]*", user.ReferrerPage),
            (r"/users[/]*", user.UserListPage),
            (r"/user/([A-Za-z0-9%]+)[/]*", user.HomeHandler),
            (r"/user/profile/([A-Za-z0-9%]+)[/]*", user.UserProfileGet),
            (r"/user/([A-Za-z0-9%]+)/page/(\d+)[/]*", user.HomeHandler),
            (r"/user/([A-Za-z0-9%]+)/follow[/]*", user.FollowHandler),
            (r"/user/([A-Za-z0-9%]+)/unfollow[/]*", user.UnfollowHandler),
            (r"/user/([A-Za-z0-9%]+)/followers[/]*", user.FollowerHandler),
            (r"/user/([A-Za-z0-9%]+)/following[/]*", user.FollowederHandler),
            (r"/user/([A-Za-z0-9%]+)/followers/page/(\d+)[/]*", user.FollowerHandler),
            (r"/user/([A-Za-z0-9%]+)/following/page/(\d+)[/]*", user.FollowederHandler),
            (r"/account/setting[/]*", user.AccountSettingHandler),
            (r"/upload/avatar[/]*", user.AvatarUploadHandler),
        ]
        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__), "views"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            ui_modules = {"TwitterForm": post.TwitterFormModule,
                "Iterms": post.ItermsModule,
                "Profile": user.ProfileModule,
                "UserList": user.UserListModule},
            xsrf_cookies = True,
            cookie_secret = config.cookie_secret,
            autoescape = None,
            title = config.title,
            login_url = "/",
            paged = config.paged,
            debug = True
        )
        tornado.web.Application.__init__(self, handlers, **settings)

def main():
    create_db()
    print("App started. Listenning on %d" % int(os.environ.get('PORT', 8888)))
    tornado.options.parse_command_line()
    tornado.httpserver.HTTPServer(Application(),
            xheaders=True).listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
