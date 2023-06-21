from __future__ import unicode_literals

import logging
import os
from datetime import datetime

from django.conf import settings
from django.db import models

from .extras import TimeStampedModel, ArchivedModel
from digiinsurance.models import Choices

logger = logging.getLogger('digiinsurance.models')


def upload_company_logo(instance, filename):
    ext = filename.split('.')[-1]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = "{}-{}.{}".format(
        str(instance.name.lower().replace(' ', '_')), ts, ext)
    return os.path.join(str(instance.id), 'logo', name)


def upload_company_cover(instance, filename):
    ext = filename.split('.')[-1]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = "{}-{}.{}".format(
        str(instance.name.lower().replace(' ', '_')), ts, ext)
    return os.path.join(str(instance.id), 'cover', name)


class Company(TimeStampedModel, ArchivedModel):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=64, null=True, blank=True, choices=Choices.PH_CITIES)
    province = models.CharField(max_length=64, null=True, blank=True, choices=Choices.PH_PROVINCES)
    region = models.CharField(max_length=64, null=True, blank=True, choices=Choices.PH_REGIONS)
    zip_code = models.CharField(max_length=4, null=True, blank=True, choices=Choices.PH_ZIP_CODES)
    gps_long = models.DecimalField(max_digits=23, decimal_places=20, blank=True, null=True)
    gps_lat = models.DecimalField(max_digits=23, decimal_places=20, blank=True, null=True)

    country = models.CharField(max_length=64, null=True, blank=True)
    website = models.CharField(max_length=128, null=True, blank=True)
    country_code = models.CharField(max_length=5, default='+63', null=True, blank=True)
    area_code = models.CharField(max_length=5, null=True, blank=True)
    mobile_number = models.CharField(max_length=16, null=True, blank=True)
    phone_number = models.CharField(max_length=16, null=True, blank=True)
    email = models.CharField(max_length=128, null=True, blank=True)
    logo = models.ImageField(upload_to=upload_company_logo, null=True, blank=True)
    cover = models.ImageField(upload_to=upload_company_cover, null=True, blank=True)
    domain = models.CharField(max_length=32, null=True, blank=True)
    dragonpay_merchant_id = models.CharField(max_length=32, null=True, blank=True)
    primary_color = models.CharField(max_length=10, null=True, blank=True, default="#F90037")

    class Meta:
        app_label = 'digiinsurance'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.id is None:
            logo = self.logo
            cover = self.cover
            self.logo = None
            self.cover = None
            super(Company, self).save(*args, **kwargs)
            self.logo = logo
            self.cover = cover
            if 'force_insert' in kwargs:
                kwargs.pop('force_insert')

        website = self.website
        if 'https://' in website:
            website = website.replace('https://', '')
        if 'http://' in website:
            website = website.replace('http://', '')
        website = website.split('.')
        if 'www' in website[0]:
            self.domain = website[1].lower()
        else:
            self.domain = website[0].lower()
        super(Company, self).save(*args, **kwargs)

    @property
    def full_address(self):
        address = [
            self.address, self.city, self.get_province_display(),
            self.get_region_display(), self.zip_code]
        return ' '.join(filter(None, address))

    @property
    def courses(self):
        return self.courses.all()

    @property
    def classes(self):
        from digiinsurance.models import Class

        return Class.objects.filter(course__in=self.courses)

    @property
    def staff(self):
        from digiinsurance.models import User

        return User.objects.filter(
            id__in=self.classes.values('staff').distinct())

    @property
    def company_link(self):
        return '%s%s' % (self.domain, settings.WEB_DOMAIN)

    @property
    def primary_color_darker(self):
        rgb_hex = [self.primary_color[x:x + 2] for x in [1, 3, 5]]
        new_rgb_int = [int(hex_value, 16) - 16 for hex_value in rgb_hex]
        new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int]
        return '#' + ''.join([hex(i)[2:].zfill(2) for i in new_rgb_int])
