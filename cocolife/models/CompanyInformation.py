import os
from datetime import datetime
from django.db import models
from digiinsurance.models.extras import TimeStampedModel


__all__ = ['CompanyInformation']

#Directory upload
def upload_pdf_COA(instance, filename):
    ext = filename.split('.')[-1]
    name = '{}.{}'.format(instance.id, ext)
    return os.path.join('ConsentOfApproval', name)

def upload_pdf_DPI(instance, filename):
    ext = filename.split('.')[-1]
    name = '{}.{}'.format(instance.id, ext)
    return os.path.join('DataPrivacyInformation', name)

def upload_pdf_FAQ(instance, filename):
    ext = filename.split('.')[-1]
    name = '{}.{}'.format(instance.id, ext)
    return os.path.join('FrequentlyAskedQuestion', name)

class CompanyInformation(TimeStampedModel):
    
    pdf_coa = models.FileField(upload_to=upload_pdf_COA, max_length=None, blank=True, null=True)
    pdf_dpi = models.FileField(upload_to=upload_pdf_DPI, max_length=None, blank=True, null=True)
    pdf_faq = models.FileField(upload_to=upload_pdf_FAQ, max_length=None, blank=True, null=True)

