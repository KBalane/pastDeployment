from __future__ import unicode_literals

import logging

from django.db import models

from .extras import TimeStampedModel

from .HealthQuestions import HealthQuestions
from .InsureePolicy import InsureePolicy
logger = logging.getLogger('digiinsurance.models')
import jsonfield

__all__ = ['HealthQuestionsAnswers']


class HealthQuestionsAnswers(TimeStampedModel):
    insuree_policy = models.ForeignKey(InsureePolicy, on_delete=models.CASCADE)
    question = models.ForeignKey(HealthQuestions, on_delete=models.CASCADE)
    answer = models.CharField(max_length=256, null=True)
    status_types = [
        ('Pass', 'pass'),
        ('Fail', 'fail'),
        ('Not Answered', 'not_answered')
    ]
    answer_status = models.CharField(max_length=256, null=False, default="Not Answered", choices=status_types)

    class Meta:
        app_label = 'digiinsurance'

    @property
    def get_answer_id(self):
        return self.id

    @property
    def get_insureePolicy_id(self):
        return self.insuree_policy_id

    @property
    def get_question_id(self):
        return self.question_id

    @property
    def get_answer(self):
        return self.answer
