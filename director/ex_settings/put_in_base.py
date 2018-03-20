# encoding:utf-8
"""
在settings/base.py 后部，引入该文件
from helpers.director.ex_settings.put_in_base import common_setting

dc = common_setting(globals())
globals().update(dc)

"""
from  __future__ import unicode_literals
import os

def common_setting(BASE_DIR):
    ROOT_URLCONF = 'urls'
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR,'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]
    
    WSGI_APPLICATION = 'wsgi.application'
    
    
    LANGUAGE_CODE = 'zh-hans'
    TIME_ZONE='Asia/Shanghai'
    
    # 优先使用app目录下的templates
    
    STATICFILES_FINDERS=[
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'django.contrib.staticfiles.finders.FileSystemFinder',
    ]
    
    
    import sys
    if 'collectstatic' not in sys.argv:
        STATICFILES_DIRS = (
            os.path.join(BASE_DIR, 'static').replace('\\', '/'),
        )
    else:
        STATIC_ROOT= os.path.join(BASE_DIR, 'static').replace('\\', '/')
    
    MEDIA_ROOT= os.path.join( os.path.dirname(BASE_DIR),'media')
    MEDIA_URL = '/media/'
    return locals()