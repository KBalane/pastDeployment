import logging
from magpy.request import MagpieRequest

logger = logging.getLogger('magpy.api.token')


class Customer(MagpieRequest):
    def __init__(self, is_sandbox=False, **kwargs):
        super(Customer, self).__init__(is_sandbox, **kwargs)
        self.logger = logger

    def create(self, email, description):
        response = self.session.post(
            self.url + '/customers',
            json={'email': email, 'description': description})

        return self._process_response(response)

    def retrieve(self, customer_id):
        response = self.session.get(self.url + '/customers/%s' % customer_id)

        return self._process_response(response)

    def update(self, customer_id, source):
        response = self.session.put(
            self.url + '/customers/%s' % customer_id,
            json={'source': source})

        return self._process_response(response)

    def delete(self, customer_id):
        response = self.session.delete(self.url + '/customers/%s' % customer_id)
        return self._process_response(response)

    def delete_fund_source(self, customer_id, card_id):
        response = self.session.delete(
            self.url + '/customers/%s/sources/%s' % (customer_id, card_id))

        return self._process_response(response)
