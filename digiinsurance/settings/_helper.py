import os
from django.core.exceptions import ImproperlyConfigured


# Example Usage:
# API_TOKEN = get_env_settings('API_TOKEN', 'dev_api_token_as_default')
# ENABLE_EMAIL_SENDING = get_env_settings('ENABLE_EMAIL', False)
# ...
# ENABLE_EMAIL_SENDING is loaded as boolean
# if ENABLE_EMAIL_SENDING:
#    send_email()


def getenv(key, default=None):
    '''Load key from the environmental variables. If key is not found from
    the envs, default will be returned.
    Additionally, this utilizes the datatype of default, if a boolean is
    given, the value from envs would also be translated to boolean.
    This method is used as a helper for django settings.'''

    value = os.environ.get(key, default)

    if isinstance(default, bool):
        # if the default value is a boolean, this function will return
        # True or False. None is not allowed and will raise an exception

        if isinstance(value, bool):
            return value

        elif value.lower() in ['true', '1']:
            return True

        elif value.lower() in ['false', '0']:
            return False

        else:
            raise ImproperlyConfigured(
                'Error loading envs. %s cannot be translated to boolean' % key)

    elif value is not None:
        # cast type of value to type of default (if it is not None)
        if default is not None:
            return type(default)(value)

        return value

    raise ImproperlyConfigured(
        'Error loading settings. Env variable %s not found' % key)
