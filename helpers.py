# coding: utf-8

from HTMLParser import HTMLParser
import os
import re
from hashlib import md5
import time
import config
from database import db
import sqlalchemy as sa
import models as m
#from models import Post, User, Comment, Notifier

config = config.rec()

def getDay(timestamp):
	FORY = '%d'
	os.environ["TZ"] = config.default_timezone
	time.tzset()
	str = time.strftime(FORY, time.localtime(timestamp))
	return str

def getMonth(timestamp):
	FORY = '%b'
	os.environ["TZ"] = config.default_timezone
	time.tzset()
	str = time.strftime(FORY, time.localtime(timestamp))
	return str

def formatDate(timestamp):
	FORY = '%Y-%m-%d @ %H:%M'
	FORM = '%m-%d @ %H:%M'
	FORH = '%H:%M'
	os.environ["TZ"] = config.default_timezone
	time.tzset()
	rtime = time.strftime(FORM, time.localtime(timestamp))
	htime = time.strftime(FORH, time.localtime(timestamp))
	now = int(time.time())
	t = now - timestamp
	if t < 60:
		str = '刚刚'
	elif t < 60 * 60:
		min = t / 60
		str = '%d 分钟前' % min
	elif t < 60 * 60 * 24:
		h = t / (60 * 60)
		str = '%d 小时前 %s' % (h,htime)
	elif t < 60 * 60 * 24 * 3:
		d = t / (60 * 60 * 24)
		if d == 1:
			str = '昨天 ' + rtime
		else:
			str = '前天 ' + rtime
	else:
		str = time.strftime(FORY, time.localtime(timestamp))
	return str

def formatDate2(timestamp):
    FORY = '%Y-%m-%d @ %H:%M'
    os.environ["TZ"] = config.default_timezone
    time.tzset()
    str = time.strftime(FORY, time.localtime(timestamp))
    return str

def getAvatar(email, size=48):
    return \
            'http://gravatar.com/avatar/%s?d=identicon&s=%d&d=http://feather.im/static/img/gravatar.png' \
% (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)

def showPost(content, pid=1):
    end = content.find("<more>")
    if end != -1:
        readmore = '<a class="readmore" href="/post/%d">>> 阅读更多</a>' % (int(pid))
        return content[0:end] + readmore
    else:
        return content

def formatText(text):
    floor = ur'#(\d+)楼\s'
    for match in re.finditer(floor, text):
        url = match.group(1)
        floor = match.group(0)
        nurl = '<a class="toreply" href="#;">#<span class="tofloor">%s</span>楼 </a>' % (url)
        text = text.replace(floor, nurl)
    return text

def replyContent(text):
    return text[0:26]


def regex(pattern, data, flags=0):
    if isinstance(pattern, basestring):
        pattern = re.compile(pattern, flags)

    return pattern.match(data)


def email(data):
    pattern = r'^.+@[^.].*\.[a-z]{2,10}$'
    return regex(pattern, data, re.IGNORECASE)


def url(data):
    pattern = (
        r'(?i)^((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}'
        r'/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+'
        r'|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))$')
    return regex(pattern, data, re.IGNORECASE)


def username(data):
    pattern = r'^[a-zA-Z0-9]+$'
    return regex(pattern, data)

def put_notifier(comment, post):
    all_users = db.query(m.User).all()
    users = []
    for user in all_users:
        if comment.content.find('@' + user.name) != -1:
            users.append(user)
    if users != []:
        for user in users:
            if user.id != post.user_id and user.id != comment.user_id:
                db.add(m.Notifier(who_id=comment.user_id, whom_id=user.id,
                    post_id=post.id, comment_id=comment.id, type=2))
                db.commit()
        for user in users:
            name = '@' + '(' + user.name + ')'
            for match in re.finditer(name, comment.content):
                ame = match.group(0)
                mame = match.group(1)
                retext = '@<a class="mention" href="/user/%s">%s</a>' % (mame, mame)
                text = comment.content.replace(ame, retext)
        comment.content = text
        db.commit()
    return True

def post_put_notifier(post):
    all_users = db.query(m.User).all()
    users = []
    for user in all_users:
        if post.content.find('@' + user.name) != -1:
            users.append(user)
    if users != []:
        for user in users:
            if user.id != post.user_id:
                db.add(m.Notifier(who_id=post.user_id, whom_id=user.id,
                    post_id=post.id, comment_id=0, type=3))
                db.commit()
        for user in users:
            name = '@' + '(' + user.name + ')'
            for match in re.finditer(name, post.content):
                ame = match.group(0)
                mame = match.group(1)
                retext = '@<a class="mention" href="/user/%s">%s</a>' % (mame, mame)
                text = post.content.replace(ame, retext)
        post.content = text
        db.commit()
    return True

def strip_tags(html):
    html = html.strip()
    html = html.strip("\n")
    result = []
    parse = HTMLParser()
    parse.handle_data = result.append
    parse.feed(html)
    parse.close()
    return "".join(result)
