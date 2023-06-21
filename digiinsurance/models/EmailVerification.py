from __future__ import unicode_literals

from datetime import date, datetime, timedelta
from .User import User
from django.db import models

from .extras import TimeStampedModel

__all__ = ['EmailVerification']


class EmailVerification(TimeStampedModel):
    VERIFICATION = 'v'
    FORGOT_PASSWORD = 'p'

    TYPES = (
        (VERIFICATION, 'User Verification'),
        (FORGOT_PASSWORD, 'Forgot Password'))

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_verification', null=True,
                                blank=True)
    email = models.EmailField()
    token = models.TextField()
    is_archived = models.BooleanField(default=False)
    type = models.CharField(max_length=1, choices=TYPES)

    class Meta:
        app_label = 'digiinsurance'

    def __str__(self):
        return '%s - %s' % (self.email, self.get_type_display())

    @property
    def is_expired(self):
        # Always expired, but useful as One Time only Link
        return self.created_at + timedelta(hours=24) < datetime.now()
