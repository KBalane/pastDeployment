from __future__ import unicode_literals
from django.db import models
import os

from digiinsurance.models.InsureePolicy import InsureePolicy

__all__ = ['InsureePolicyDocs']


def upload_insuree_docs(instance, filename):
    ext = filename.split('.')[-1]
    name = '{}.{}'.format(instance.id, ext)
    return os.path.join('users', name)


class InsureePolicyDocs(models.Model):
    insuree_docs = models.ForeignKey(InsureePolicy, related_name='insuree_docs', on_delete=models.CASCADE)
    doc = models.FileField(upload_to=upload_insuree_docs, max_length=None)
    filename = models.CharField(max_length=100, blank=True, default='')
    date_uploaded = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'digiinsurance'

# def __str__(self):
# 	return '[%s] %s-%s-%s' % (self.id, self.insuree_docs, self.doc,self)
