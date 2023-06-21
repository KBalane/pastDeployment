from django.db import models

from digiinsurance.models.extras import TimeStampedModel


__all__ = ['AuditLog']


class AuditLog(TimeStampedModel):
    action = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.CharField(max_length=255, null=True, blank=True)
    details_id = models.CharField(max_length=255, null=True, blank=True)
    ip_address = models.CharField(max_length=255, null=True, blank=True)
    login_user = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.action} {self.user_id}'
