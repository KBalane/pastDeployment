def FILE_HANDLER(filename, level=None):
    '''Return a template FileHandler logging handler using
    the given filename.'''
    return {
        'level': level or 'DEBUG',
        'class': 'logging.FileHandler',
        'formatter': 'verbose',
        'filename': "logs/%s.log" % filename
    }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s '
                      '[%(module)s.%(filename)s:%(funcName)s:%(lineno)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S %p'
        },
        'simple': {
            'format': '%(levelname)s %(module)s.%(filename)s:%(funcName)s:%(lineno)s > %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'file-critical': FILE_HANDLER('critical', 'ERROR'),
        'file-main': FILE_HANDLER('main'),
        'file-dashboard': FILE_HANDLER('dashboard'),
        'file-api': FILE_HANDLER('api'),
        'file-blockchain': FILE_HANDLER('blockchain'),
        'file-dragonpay': FILE_HANDLER('dragonpay'),
        'file-tasks': FILE_HANDLER('tasks'),
        'file-kyc': FILE_HANDLER('kyc'),
        'file-magpy': FILE_HANDLER('magpy'),
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file-critical'],
            'level': 'INFO', 'propagate': True,
        },
        'api.views': {
            'handlers': ['console', 'file-api'],
            'level': 'DEBUG', 'propagate': False,
        },
        'api.tasks': {
            'handlers': ['console', 'file-tasks'],
            'level': 'DEBUG', 'propagate': False,
        },
        'dragonpay': {
            'handlers': ['console', 'file-dragonpay'],
            'level': 'DEBUG', 'propagate': False,
        },
        'kyc.views': {
            'handlers': ['console', 'file-kyc'],
            'level': 'DEBUG', 'propagate': False,
        },
        'magpy.request': {
            'handlers': ['console', 'file-magpy'],
            'level': 'DEBUG', 'propagate': False,
        }
    }
}
