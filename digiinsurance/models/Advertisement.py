# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging
import os
from datetime import date, datetime
from django.db import models
# from digiinsurance.models import User
from .extras import TimeStampedModel
logger = logging.getLogger('digiinsurance.models')


__all__ = ['Advertisement']


def upload_img(instance, filename):
    name = "{}.{}".format(instance.Title, 'jpg')
    return os.path.join('promos', name)


class Advertisement(TimeStampedModel):
    Type = models.CharField(max_length=30, null=True)
    Link = models.CharField(max_length=255, null=True)
    Title = models.CharField(max_length=255)
    Description = models.TextField()
    Publish_Date = models.DateField(default=date.today)
    Expiration_Date = models.DateField(default=date.today)
    Photo = models.ImageField(upload_to=upload_img, null=True, blank=True)
    Status = models.CharField(max_length=20, null=True)
    liked = models.ManyToManyField(
        'User', default=None, blank=True, related_name='liked')
    Policy = models.ForeignKey(
        'Policy', related_name='+', null=True, blank=True, default=2, on_delete=models.CASCADE)

    class Meta:
        app_label = 'digiinsurance'

    @property
    def num_likes(self):
        return self.liked.all().count()


"""
LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.post)
"""
