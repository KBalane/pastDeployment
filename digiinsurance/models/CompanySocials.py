from __future__ import unicode_literals
from django.db import models
from digiinsurance.models.Company import Company


class CompanySocials(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='socials', null=True, blank=True)
    facebook = models.CharField(max_length=64, null=True, blank=True)
    twitter = models.CharField(max_length=64, null=True, blank=True)
    linked_in = models.CharField(max_length=64, null=True, blank=True)
    github = models.CharField(max_length=64, null=True, blank=True)
    pinterest = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        app_label = 'digiinsurance'

    def __str__(self):
        return self.company.name
