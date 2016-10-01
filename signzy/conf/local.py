from  base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'signzy',
        'USER': 'signzy',
        'PASSWORD': 'signzy',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# LOG_ROOT = '/Users/ankurjain/Work/signzy'
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'filters': {
#         'request_filter': {
#             '()': 'base.filters.RequestIDFilter'
#         },
#         'error_filter': {
#             '()': 'base.filters.LogLevelFilter',
#             'level': logging.ERROR
#         },
#         'warn_filter': {
#             '()': 'base.filters.LogLevelFilter',
#             'level': logging.WARN
#         },
#         'debug_filter': {
#             '()': 'base.filters.LogLevelFilter',
#             'level': logging.DEBUG
#         },
#         'info_filter': {
#             '()': 'base.filters.LogLevelFilter',
#             'level': logging.INFO
#         }
#     },
#     'formatters': {
#         'verbose': {
#             'format': "[%(request_id)s] [%(asctime)s] %(levelname)s  [%(name)s:%(lineno)s] %(message)s",
#             'datefmt': "%d/%b/%Y %H:%M:%S"
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
#         'logstash_fmtr': {
#             'format': "[%(asctime)s] %(levelname)s  [%(name)s:%(lineno)s] %(message)s",
#             'datefmt': "%d/%b/%Y %H:%M:%S"
#         },
#     },
#     'handlers': {
#
#         'error_handler': {
#             'level': 'ERROR',
#             'filters': ['error_filter', 'request_filter'],
#             'class': 'logging.handlers.TimedRotatingFileHandler',
#             'filename': LOG_ROOT + '/app_error.log',
#             'when': 'midnight',
#             'formatter': 'logstash_fmtr',
#             'interval': 1,
#             'backupCount': 0,
#         },
#         'warn_handler': {
#             'level': 'ERROR',
#             'filters': ['warn_filter', 'request_filter'],
#             'class': 'logging.handlers.TimedRotatingFileHandler',
#             'filename': LOG_ROOT + '/app_warn.log',
#             'when': 'midnight',
#             'formatter': 'logstash_fmtr',
#             'interval': 1,
#             'backupCount': 0,
#         },
#         'info_handler': {
#             'level': 'INFO',
#             'filters': ['info_filter', 'request_filter'],
#             'class': 'logging.handlers.TimedRotatingFileHandler',
#             'filename': LOG_ROOT + '/app_info.log',
#             'when': 'midnight',
#             'formatter': 'logstash_fmtr',
#             'interval': 1,
#             'backupCount': 0,
#         },
#         'debug_handler': {
#             'level': 'DEBUG',
#             'filters': ['debug_filter', 'request_filter'],
#             'class': 'logging.handlers.TimedRotatingFileHandler',
#             'filename': LOG_ROOT + '/app_debug.log',
#             'when': 'midnight',
#             'formatter': 'logstash_fmtr',
#             'interval': 1,
#             'backupCount': 0,
#         },
#         'django': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': LOG_ROOT + '/django.log',
#             'filters': ['request_filter'],
#             'formatter': 'logstash_fmtr'
#         },
#         'default': {
#             'level': 'DEBUG',
#             'class': 'logging.handlers.TimedRotatingFileHandler',
#             'filename': LOG_ROOT + '/default.log',
#             'when': 'midnight',
#             'formatter': 'logstash_fmtr',
#             'interval': 1,
#             'backupCount': 0,
#         }
#     },
#     'loggers': {
#         'django.request': {
#             'handlers': ['django'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'apps': {
#             'handlers': ['error_handler', 'warn_handler', 'info_handler', 'debug_handler', 'console'],
#             'level': 'DEBUG',
#         },
#     },
# }
