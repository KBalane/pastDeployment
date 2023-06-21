from __future__ import absolute_import

from django.db.models import Q
from django.db.models import QuerySet


class PolicyQuerySet(QuerySet):
    def active(self):
        return self.filter(Q(archived=False) & Q(is_draft=False))

    def inactive(self):
        return self.filter(Q(archived=True) | Q(is_draft=True))

    def draft(self):
        return self.filter(is_draft=True)


class ClassQuerySet(QuerySet):
    def active(self):
        return self.filter(archived=False)
        # return [x for x in self.filter(archived=False) if x.status == 2]

    def ongoing_upcoming(self):
        return [x for x in self.filter(archived=False) if x.status in [1, 2]]

    def single(self):
        return self.filter(is_bundled=False)

    def bundled(self):
        return self.filter(is_bundled=True)


class ModuleQuerySet(QuerySet):
    def active(self):
        return self.filter(archived=False)


class ExamQuestionQuerySet(QuerySet):
    def active(self):
        return self.filter(archived=False)


class ScheduleQuerySet(QuerySet):
    def active(self):
        return self.filter(archived=False)


class EnrollmentQuerySet(QuerySet):
    def ongoing(self):
        return self.filter(progress__lt=100)


PolicyManager = PolicyQuerySet.as_manager()
