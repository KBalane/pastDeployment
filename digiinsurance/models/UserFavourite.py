from .User import User
from .Policy import Policy


import logging
from datetime import date, datetime
from django.db import models
from .extras import TimeStampedModel

logger = logging.getLogger('digiinsurance.models')

__all__ = ['Favourites']


class Favourites(TimeStampedModel):
    user = models.ForeignKey(User, related_name='favourite_user', on_delete=models.CASCADE)
    policy = models.ForeignKey(Policy, related_name='favorite_policy', on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
