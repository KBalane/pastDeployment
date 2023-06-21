from __future__ import unicode_literals

import logging
from django.db import models


from .extras import TimeStampedModel

logger = logging.getLogger('digiinsurance.models')


class Product(TimeStampedModel):
    key = models.CharField(max_length=16)
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        app_label = 'digiinsurance'

    def __str__(self):
        return '%s: %s' % (self.key, self.name)
