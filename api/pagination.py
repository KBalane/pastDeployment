import math
from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        page_size = self.get_page_size(self.request)
        total = self.page.paginator.count
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('meta', OrderedDict([
                ('page', self.request.query_params.get(
                    self.page_query_param, 1)),
                ('pages', math.ceil(total / page_size)),
                ('perpage', page_size),
                ('total', total),
                ('sort', 'asc'),
                ('field', 'id'),
            ])),
            ('data', data)
        ]))
