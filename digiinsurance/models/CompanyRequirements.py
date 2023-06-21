from __future__ import unicode_literals

from django.db import models

from .Company import Company


class CompanyRequirements(models.Model):
    company = models.ForeignKey(Company, related_name='requirements', on_delete=models.CASCADE, null=True, blank=True)
    company_requirements = models.CharField(max_length=64, null=True, blank=True)
    company_req_def = models.TextField(null=True, blank=True)
