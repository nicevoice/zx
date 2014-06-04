# -*- coding: utf-8 -*-

"""
@attention: 定义全局上下文变量
@author: lizheng
@date: 2011-11-28
"""

from django.conf import settings


def config(request):
    """
    @attention: Adds settings-related context variables to the context.
    """
    return {
        'DEBUG': settings.DEBUG,
        'LOCAL_FLAG': settings.LOCAL_FLAG,
        'MEDIA_VERSION': '005',
        'SERVER_DOMAIN': settings.SERVER_DOMAIN,
        'MAIN_DOMAIN': settings.MAIN_DOMAIN,
    }
