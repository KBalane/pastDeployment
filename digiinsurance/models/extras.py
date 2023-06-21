from datetime import datetime

from django.db import models
from django.db.models import Subquery


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ArchivedModel(models.Model):
    archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        abstract = True

    @property
    def is_archived(self):
        return self.archived_at is not None

    def archive(self, *args, **kwargs):
        self.archived = True
        self.archived_at = datetime.now()
        self.save()


class CompletableModel(models.Model):
    completed_at = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        abstract = True

    @property
    def is_completed(self):
        return self.completed_at is not None


class SubqueryCount(Subquery):
    template = "(SELECT count(*) FROM (%(subquery)s) _count)"
    output_field = models.IntegerField()


class SubqueryAverage(Subquery):
    template = "(SELECT COALESCE(AVG(score), 0) FROM (%(subquery)s) _average)"
    output_field = models.FloatField()
