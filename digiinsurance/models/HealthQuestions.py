from __future__ import unicode_literals

import logging

from django.db import models

from .InsureePolicy import Policy
from .extras import TimeStampedModel

logger = logging.getLogger('digiinsurance.models')

__all__ = ['HealthQuestions']


class HealthQuestions(TimeStampedModel):
    choices = models.JSONField(blank=True, null=True)
    correct_answer = models.CharField(null=True, blank=True, max_length=256)
    question_types = (
        ('MultilineText', 'multiline_text'),
        ('Number', 'number'),
        ('MultipleChoice', 'multiple_choice'),
        ('Yes/No', 'yes/no')
    )

    policy_id = models.ForeignKey(Policy, on_delete=models.CASCADE)
    question = models.CharField(max_length=256, null=True)
    question_type = models.CharField(max_length=20, default='MultilineText', choices=question_types)

    class Meta:
        app_label = 'digiinsurance'

    @property
    def get_question_id(self):
        return self.id

    @property
    def get_policy_id(self):
        return self.policy_id

    @property
    def get_question(self):
        return self.question

    @property
    def get_question_type(self):
        return self.question_type
