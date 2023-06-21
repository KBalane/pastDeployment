from django.db import models
from digiinsurance.models.extras import TimeStampedModel

__all__ = ['DepartmentEmail']


def default_json_value():
    return {'no_values': []}


class DepartmentEmail(TimeStampedModel):
    inquiry_type = models.CharField(max_length=100, null=True, blank=True)
    mailto = models.JSONField(blank=True, default=list, null=True)
    cc = models.JSONField(blank=True, default=list, null=True)
    bcc = models.JSONField(blank=True, default=list, null=True)

    def save(self, *args, **kwargs):
        if self.inquiry_type is None:
            self.inquiry_type = default_json_value
        if self.mailto is None:
            self.mailto = default_json_value
        if self.cc is None:
            self.cc = default_json_value
        if self.bcc is None:
            self.bcc = default_json_value
        else:
            pass
        super(DepartmentEmail, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return '[%s] %s' % (self.id, self.inquiry_type)
