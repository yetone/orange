# coding: utf-8


_DBUSER = "username" # 数据库用户名
_DBPASS = "password" # 数据库密码
_DBHOST = "localhost" # 数据库地址
_DBNAME = "orange" # 数据库名称

class rec: pass

rec.database = 'mysql://%s:%s@%s/%s' % (_DBUSER, _DBPASS, _DBHOST,
        _DBNAME)
rec.cookie_secret = 'cookie_secret'
rec.password_secret = 'password_secret'
rec.title = u"Orange"
rec.description = u"Orange"
rec.url = 'http://www.lisplife.com/'
rec.paged = 12
rec.archive_paged = 20
rec.default_timezone = "Asia/Shanghai"
rec.gravatar_extra = ''
rec.gravatar_base_url = "http://www.gravatar.com/avatar/"
