import os

from django.db import models

from digiinsurance.models.extras import TimeStampedModel
from digiinsurance.models import User

from datetime import datetime

__all__ = ['Inquiry']


def upload_img_attachment(instance, filename):
    ext = filename.split('.')[-1]
    name = '{}_{}_{}.{}'.format(instance.inquiry_type, instance.user.last_name, datetime.now(), ext)
    return os.path.join('inquiries', name)


INQUIRY_TYPES = [
    ('BANCASSURANCE', 'Bancassurance'),
    ('CLAIMS', 'Claims'),
    ('DEPED_LOANS', 'DepEd Loans'),
    ('EMPLOYMENT', 'Employment'),
    ('GROUP_INSURANCE', 'Group Insurance'),
    ('HEALTHCARE', 'Healthcare'),
    ('INDIVIDUAL', 'Individual'),
    ('INVESTMENTS', 'Investments'),
    ('MALL_CLIENTS', 'Mall Clients'),
    ('MIGRANTS', 'Migrants'),
    ('POLICY', 'Policy'),
    ('MOBILE_APP_CONCERNS', 'Mobile App Concerns'),
    ('OTHER', 'Other')
]


class Inquiry(TimeStampedModel):
    user = models.ForeignKey(User, related_name='user_inquiries', on_delete=models.CASCADE)
    policy_number = models.CharField(max_length=100, null=True, blank=True)
    inquiry_type = models.CharField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    concern = models.TextField()
    attachment = models.ImageField(upload_to=upload_img_attachment, null=True, blank=True)

    def __str__(self) -> str:
        return self.subject
