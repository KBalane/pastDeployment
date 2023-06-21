import os
from django.db import models
from digiinsurance.models.extras import TimeStampedModel
from digiinsurance.models.User import User


def cert_of_registration(instance, filename):
    ext = filename.split('.')[-1]
    name = '{}.{}'.format(instance.id, ext)
    return os.path.join('cert_of_registration', name)


def resolution(instance, filename):
    ext = filename.split('.')[-1]
    name = '{}.{}'.format(instance.id, ext)
    return os.path.join('resolution', name)


def power_attorney(instance, filename):
    ext = filename.split('.')[-1]
    name = '{}.{}'.format(instance.id, ext)
    return os.path.join('power_attorney', name)


class TelcoPersonAddress(TimeStampedModel):
    user = models.ForeignKey(
        User, related_name='person', on_delete=models.CASCADE)
    province = models.JSONField(blank=True, null=True)
    passport_number = models.CharField(blank=True, max_length=30, null=True)


class TelcoSimDetails(TimeStampedModel):
    user = models.ForeignKey(
        User, related_name='personsim', on_delete=models.CASCADE)
    name = models.CharField(blank=True, max_length=30, null=True)
    number_owner = models.CharField(blank=True, max_length=16, null=True)
    owner_relationship = models.CharField(blank=True, max_length=30, null=True)
    minor_name = models.CharField(blank=True, max_length=50, null=True)
    purpose = models.CharField(blank=True, max_length=50, null=True)
    sim_card_serial = models.CharField(blank=True, max_length=50, null=True)
    sim_card_number = models.CharField(blank=True, max_length=50, null=True)
    isActive = models.CharField(blank=True, max_length=30, null=True)
    # OTP
    # isOTPVerified


class TelcoCompany(TimeStampedModel):
    company_name = models.CharField(blank=True, max_length=50, null=True)
    cert_of_registration = models.FileField(
        upload_to=cert_of_registration, blank=True, null=True)
    resolution = models.FileField(upload_to=resolution, blank=True, null=True)
    power_attorney = models.FileField(
        upload_to=power_attorney, blank=True, null=True)
    company_address = models.CharField(blank=True, max_length=100, null=True)


class JumioToken(TimeStampedModel):
    token = models.CharField(blank=True, max_length=100, null=True)
    data = models.JSONField(blank=True, null=True)
