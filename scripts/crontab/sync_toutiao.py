# -*- coding: utf-8 -*-


import sys
import os

# 引入父目录来引入其他模块
SITE_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([os.path.abspath(os.path.join(SITE_ROOT, '../')),
                 os.path.abspath(os.path.join(SITE_ROOT, '../../')),
                 ])
os.environ['DJANGO_SETTINGS_MODULE'] = 'www.settings'

import datetime
import re
import time
import requests
from pyquery import PyQuery as pq
from www.toutiao.models import WeixinMp, Article, BanKey

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:29.0) Gecko/20100101 Firefox/29.0"}


def check_ban_key(title, ban_keys):
    for bk in ban_keys:
        if bk.key in title:
            return False
    return True


def sync_toutiao():
    def _replace_html_tag(text):
        tag_s = re.compile('<.+?>')
        tag_e = re.compile('</\w+?>')
        text = tag_s.sub('', text)
        text = tag_e.sub(' ', text)
        return text

    start_time = time.time()
    all_count = 0
    mp_count = 0
    ban_keys = list(BanKey.objects.all())

    # 文章字数少于300的过滤，每天更新一次
    for mp in WeixinMp.objects.filter(state=True):
        url = u"http://weixin.sogou.com/gzhjs?openid=%s" % mp.open_id
        resp = requests.get(url, headers=headers, timeout=30)
        text = resp.text
        lst_article = eval(re.compile('gzh\((.+)\)').findall(text)[0])["items"]

        for article in lst_article:
            article = article.replace("\\", "")
            url = re.compile('<url>(.+)</url>').findall(article)[0][9:-3]
            timestamp = re.compile('<lastModified>(.+)</lastModified>').findall(article)[0]
            img = re.compile('<imglink>(.+)</imglink>').findall(article)[0][9:-3]
            create_time = datetime.datetime.fromtimestamp(float(timestamp))

            article_detail = pq(requests.get(url, headers=headers, timeout=30).text)
            title = article_detail("#activity-name").html().split("<em")[0].strip()
            content = article_detail("#js_content").html()
            format_content = _replace_html_tag(content).strip()
            if len(format_content) < 300:
                continue

            if mp.is_silence == False and check_ban_key(title, ban_keys) == False:
                continue

            # print url
            # print img
            # print title.encode("utf8")
            # print content.encode("utf8")
            # print create_time

            if not (Article.objects.filter(from_url=url) or Article.objects.filter(title=title)):
                Article.objects.create(title=title, content=content, weixin_mp=mp, from_url=url, img=img,
                                       create_time=create_time, is_silence=mp.is_silence, article_type=mp.article_type)
            else:
                break
            all_count += 1
        mp_count += 1

    end_time = time.time()
    print (u"耗时：%s秒" % int(end_time - start_time)).encode("utf8")
    print (u"共更新%s个公众号" % mp_count).encode("utf8")
    print (u"共新增了%s条" % all_count).encode("utf8")


if __name__ == '__main__':
    sync_toutiao()
