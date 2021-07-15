
import os
import sys
def SET(scope,path=None,extra_cfg={}):
    BASE_DIR= scope['BASE_DIR']
    if not path:
        LOG_PATH= os.path.join( os.path.dirname(BASE_DIR),'log')
    else:
        LOG_PATH=path
    if os.environ.get('TEST'):
        def is_console(ls):
            return ls+['console']
    else:
        def is_console(ls):
            return ls   
    
    LOGGING = {
      'version': 1, # 标示配置模板版本，int 类型，目前只接收 `1`这个值。
      'disable_existing_loggers': False, 
      'formatters': {
          'standard': {
               #'format': '%(levelname)s %(asctime)s %(message)s',
              'format': '%(levelname)s %(asctime)s %(process)d-%(thread)d %(message)s'
          },
      },
      'filters': {
          # 这里是定义过滤器，需要注意的是，由于 'filters' 是 logging.config.dictConfig 方法要求在配置字典中必须给订的 key ,所以即使不使用过滤器也需要明确给出一个空的结构。
      },
      'handlers': {
           'mail_admins': {
              'level': 'ERROR',
              'class': 'django.utils.log.AdminEmailHandler',
              'formatter':'standard',
          },
  
          'console': {
              'level':'DEBUG',
              'class': 'logging.StreamHandler',
              'stream': sys.stdout
              }, 
           # pip instll concurrent-log-handler   异步日志框架
          'error_warning':{
              'level': 'WARNING',
              'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
              'maxBytes': 1024*1024*5,
              'backupCount':3,
              'formatter':'standard',
              'filename': os.path.join(LOG_PATH,'errors.log'),    
              'encoding': 'utf8',
              
              },
          'general_log':{
              'level': 'DEBUG',
              #'class': 'logging.handlers.RotatingFileHandler',
              'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
              'maxBytes': 1024*1024*5,
              'backupCount':3,
              'formatter':'standard',
              'filename': os.path.join(LOG_PATH,'general_log.log'),     
              'encoding': 'utf8',
            }, 
          'backend_operation':{
              'level': 'DEBUG',
              #'class': 'logging.handlers.RotatingFileHandler',
              'class': 'concurrent_log_handler.ConcurrentRotatingFileHandler',
              'maxBytes': 1024*1024*5,
              'backupCount':3,
              'formatter':'standard',
              'filename': os.path.join(LOG_PATH,'backend_operation.log'),     
              'encoding': 'utf8',
            },            
      },
      'loggers': {
          '': {
              'handlers': ['mail_admins', 'error_warning'], # 'elk_warning',
              'level': 'WARNING',
              'propagate': False,
          },
          'django': {
              'handlers': [] , # 'console', 'djangoout_warning', 'mail_admins', 'elk_warning'],
              'level': 'INFO',
              'propagate': True,
              },          
  
          'general_log': {
              'handlers': is_console( [ 'general_log', ]) ,# 'console','elk_info' ],  #'djangoout_warning',
              'level': 'DEBUG',
              'propagate': False,            
              },
          'ModelFields.save_form': {
              'handlers': ['backend_operation',] , # 'console', 'elk_debug'],
              'level': 'DEBUG',
              'propagate': False,              
              },
          'operation': {
              'handlers': ['backend_operation'] , # ,'console','elk_debug'],
              'level': 'DEBUG',
              'propagate': False,              
              },          
      }
    }
    if 'handlers' in extra_cfg:
        LOGGING['handlers'] .update(extra_cfg.get('handlers'))
    if 'loggers' in extra_cfg:
        LOGGING['loggers'].update(extra_cfg.get('loggers'))
        
    scope.update({
        'LOGGING':LOGGING,
    })