import logging
from logging.handlers import TimedRotatingFileHandler
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s]: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'heavy': {
            'format': '%(asctime)s [%(levelname)s] %(module)s/%(funcName)s/%(lineno)d: %(message)s'
        },
        'light': {
            'format': '%(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'WARNING',
            'formatter': 'light',
            'class': 'logging.StreamHandler',
        },
        'activity_logs': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'activity_logs.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 5,
        },
        'debug_logs': {
            'level': 'DEBUG',
            'formatter': 'heavy',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'debug_logs.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 5,
        },
        'error_logs': {
            'level': 'ERROR',
            'formatter': 'heavy',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'error_logs.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 5,
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['activity_logs', 'console'],
            'level': 'INFO',
            'propagate': False
        },
        'my.packg': {
            'handlers': ['activity_logs', ],
            'level': 'INFO',
            'propagate': False
        },
        'opcua.server.address_space': {
            'handlers': ['error_logs', ],
            'level': 'INFO',
            'propagate': False
        },
        '__main__': {  # if __name__ == '__main__'
            'handlers': ['activity_logs', 'debug_logs', 'console', 'error_logs'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
