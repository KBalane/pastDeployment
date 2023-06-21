from django.db import models
from digiinsurance.models.extras import TimeStampedModel


__all__ = ['APIKey']


class APIKey(TimeStampedModel):
    key = models.CharField(max_length=255, null=False, unique=True)
    value = models.TextField()

    def __str__(self) -> str:
        return self.key
