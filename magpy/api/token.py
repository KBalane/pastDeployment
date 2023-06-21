import logging
from magpy.request import MagpieRequest
from requests.auth import HTTPBasicAuth
import requests
import base64

logger = logging.getLogger('magpy.request')


class Token(MagpieRequest):
    def __init__(self, is_sandbox=False, **kwargs):
        super(Token, self).__init__(is_sandbox, **kwargs)
        self.logger = logger
        self.session.auth = (self.pk, '')

    def create(self, name, number, exp_month, exp_year, cvc, address={}):
        payload = {
            'name': name,
            'number': number,
            'exp_month': exp_month,
            'exp_year': exp_year,
            'cvc': cvc,
        }

        for key in ['city', 'country', 'line1', 'line2', 'state', 'zip']:
            if key not in address:
                if self.is_sandbox:
                    continue

                logger.error('address %s not found', key)
                return
            payload['address_%s' % key] = address[key]

        params = {
          'card': payload
        }

        response = self.session.post(
            self.url + '/tokens',
            json=params)

        return self._process_response(response)

    def retrieve(self, token_id):
        response = self.session.get(self.url + '/tokens/%s' % token_id)
        return self._process_response(response)
