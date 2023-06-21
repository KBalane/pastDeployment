# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date, datetime
from django.db import models

from digiinsurance.models.extras import TimeStampedModel
from digiinsurance.models.InsureePolicy import InsureePolicy
from .CLHealthQuestions import CLHealthQuestions
from cocolife.models.ProductInsuree import ProductInsuree

__all__ = ['CLHealthQuestionsAnswers']


class CLHealthQuestionsAnswers(TimeStampedModel):
    product_insuree = models.ForeignKey(ProductInsuree, on_delete=models.CASCADE)
    question = models.ForeignKey(CLHealthQuestions, on_delete=models.CASCADE)
    answer = models.CharField(max_length=256, null=True)
    status_types = [
        ('Pass', 'pass'),
        ('Fail', 'fail'),
        ('Not Answered', 'not_answered')
    ]
    answer_status = models.CharField(max_length=256, null=False, default="Not Answered", choices=status_types)

    class Meta:
        app_label = 'cocolife'

    @property
    def get_answer_id(self):
        return self.id

    @property
    def get_ProdInsuree_id(self):
        return self.ProdInsuree

    @property
    def get_question_id(self):
        return self.question_id

    @property
    def get_answer(self):
        return self.answer
