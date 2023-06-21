import json
import logging
import requests
import base64
from django.conf import settings

SANDBOX_URL = 'https://api.magpie.im/v1.1'
PRODUCTION_URL = 'https://api.magpie.im/v1.1'


class MagpieRequest(object):
    def __init__(self, is_sandbox=False, **kwargs):
        self.is_sandbox = is_sandbox

        self.pk = settings.MAGPIE_PUBLIC_KEY
        self.sk = settings.MAGPIE_SECRET_KEY

        if not self.pk or not self.sk:
            raise Exception('Public or Secret Key not set in Environment')

        elif 'test' in self.pk:
            self.is_sandbox = True

        self.url = SANDBOX_URL if is_sandbox else PRODUCTION_URL

        self.session = requests.Session()
        # self.session.auth = (self.pk, '')
        bearer_token = str(base64.b64encode((self.sk+':').encode()), 'utf8')
        self.session.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Basic {}'.format(bearer_token),
            'Host': 'api.magpie.im',
        }

        self.logger = logging.getLogger('magpy.request')
        self.logger.debug('Initiating request: %s %s', self.pk, self.sk)

    def _process_response(self, response):
        # if response.status_code in [200, 201]:
        #     return json.loads(response.content)

        # elif response.status_code == 401:
        #     self.logger.error('Authorization error. Check your token')
        #     print('Authorization error. Check your token')

        # elif response.status_code == 402:
        #     self.logger.error('Invalid card! %s', response.content)
        #     print('Invalid card!', response.content)

        # elif response.status_code == 404:
        #     self.logger.error('Authorization error. Token not found')
        #     print('Authorization error. Token not fganiound')

        # else:
        #     self.logger.error('Invalid request! %s', response.content)
        #     print('Invalid request', response.content)
        return (response.status_code, json.loads(response.content))
