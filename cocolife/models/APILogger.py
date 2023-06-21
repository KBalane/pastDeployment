from django.db import models
from digiinsurance.models.extras import TimeStampedModel


__all__ = ['APILogger']


class APILogger(TimeStampedModel):
    api_call = models.CharField(max_length=255, null=True, blank=True)
    response = models.JSONField(null=True)
    status = models.BooleanField()

    def __str__(self) -> str:
        return 'Datetime: %s ||| [ API: %s ] ||| ( status: %s )' % (self.created_at, self.api_call, self.status)
