# coding: utf-8

import re
import misaka

def md(text):
    text = img_convert(text)
    return misaka.html(text, extensions=misaka.EXT_FENCED_CODE |
            misaka.EXT_AUTOLINK, render_flags=misaka.HTML_SKIP_HTML)

def img_convert(text):
    img_url = ur'http:\/\/[^\s\"]*\.(jpg|png|bmp|gif)'
    for match in re.finditer(img_url, text):
        url = match.group(0)
        img_tag = '![](%s)' % url
        text = text.replace(url, img_tag)
    return text
