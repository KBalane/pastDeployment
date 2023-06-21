from django.db import models
from digiinsurance.models.extras import TimeStampedModel


__all__ = ['AppStat']

class AppStat(TimeStampedModel):
    download = models.IntegerField(blank = True, null = True)


    def get_count(self):
        download = self.download
        return download