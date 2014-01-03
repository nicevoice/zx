# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
# from django.conf import settings

urlpatterns = patterns('www.account.views',
                       url(r'^user_profile$', 'user_profile'),
                       url(r'^user_settings$', 'user_settings'),
                       url(r'^user_settings/change_pwd$', 'change_pwd'),
                       url(r'^user_settings/change_email$', 'change_email'),
                       url(r'^user_settings/bind_mobile$', 'bind_mobile'),
                       url(r'^user_settings/security_question$', 'security_question'),
                       url(r'^user_settings/bind_community$', 'bind_community'),
                       )

urlpatterns += patterns('www.account.views_oauth',
                        url(r'^oauth/qq$', 'oauth_qq'),
                        url(r'^oauth/weibo$', 'oauth_weibo'),
                        )
