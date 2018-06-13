import socket

#根据IP地址判断是否是开发环境
if socket.gethostbyname(socket.gethostname())[:3]=='192':
    DEBUG = TEMPLATE_DEBUG = True
else:
    DEBUG = TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['yshblog.com','*.yshblog.com'] #设置允许访问的主机

#管理员邮箱
ADMINS = (
    ('Haddy Yang','*******@163.com'),
)

#非空链接，却发生404错误，发送通知MANAGERS
SEND_BROKEN_LINK_EMAILS = True
MANAGERS = ADMINS

#Email设置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST= 'smtp.qq.com'#QQ邮箱SMTP服务器(邮箱需要开通SMTP服务)
EMAIL_PORT= 25		   #QQ邮箱SMTP服务端口
EMAIL_HOST_USER = '**********@qq.com'  #我的邮箱帐号
EMAIL_HOST_PASSWORD = '**************' #授权码
EMAIL_SUBJECT_PREFIX = 'website' #为邮件标题的前缀,默认是'[django]'
EMAIL_USE_TLS = True #开启安全链接
DEFAULT_FROM_EMAIL = SERVER_EMAIL = EMAIL_HOST_USER #设置发件人

#logging日志配置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {#日志格式 
                   'standard': {
           'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'} 
       },
    'filters': {#过滤器
                'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        }
        },
    'handlers': {#处理器
                 'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
            },
        'mail_admins': {#发送邮件通知管理员
                        'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],# 仅当 DEBUG = False 时才发送邮件
            'include_html': True,
            },
        'debug': {#记录到日志文件(需要创建对应的目录，否则会出错)
                  'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, "log",'debug.log'),#日志输出文件
            'maxBytes':1024*1024*5,#文件大小 
            'backupCount': 5,#备份份数
            'formatter':'standard',#使用哪种formatters日志格式
            },
        'console':{#输出到控制台
                   'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            },
        },
    'loggers': {#logging管理器
                'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False 
            },
        'django.request': {
            'handlers': ['debug','mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            },
        # 对于不在 ALLOWED_HOSTS 中的请求不发送报错邮件
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
            },
        } 
}