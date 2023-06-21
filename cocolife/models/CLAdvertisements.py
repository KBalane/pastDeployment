from __future__ import unicode_literals
import os
from django.db import models
from datetime import date

from cocolife.models.DigiInsuree import DigiInsuree
from cocolife.models.Product import Product


__all__ = ['CLAdvertisements', 'upload_image']


def upload_image(instance, filename):
    name = "{}.{}".format(instance.title, 'jpg')
    return os.path.join('promo', name)


class CLAdvertisements(models.Model):

    CATEGORY = (
        ('article', 'Article'),
        ('promo', 'Promo'),
    )

    category = models.CharField(choices=CATEGORY, max_length=30, null=True)
    link = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    publish_date = models.DateField(default=date.today)
    expiration_date = models.DateField(default=date.today)
    photo = models.ImageField(null=True, blank=True, upload_to=upload_image)
    status = models.CharField(max_length=20, null=True)
    liked = models.ManyToManyField(DigiInsuree, blank=True, default=None, related_name='liked')
    view_count = models.IntegerField(blank=True, default=0, null=True)
    product = models.ForeignKey(Product, blank=True, default=2, null=True, on_delete=models.CASCADE, related_name='+')

    class Meta:
        app_label = 'cocolife'

    @property
    def num_likes(self):
        return self.liked.all().count()
