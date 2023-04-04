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
            'class': 'logging.FileHandler',
            'filename': 'activity_logs.log',
            'mode': 'w',
        },
        'debug_logs': {
            'level': 'DEBUG',
            'formatter': 'heavy',
            'class': 'logging.FileHandler',
            'filename': 'debug_logs.log',
            'mode': 'w',
        },
        'error_logs': {
            'level': 'ERROR',
            'formatter': 'heavy',
            'class': 'logging.FileHandler',
            'filename': 'error_logs.log',
            'mode': 'w',
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
