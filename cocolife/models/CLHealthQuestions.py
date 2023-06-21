# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.db import models

from digiinsurance.models.extras import TimeStampedModel
from cocolife.models.Product import Product

import jsonfield



__all__ = ['CLHealthQuestions']


class CLHealthQuestions(TimeStampedModel):
    
    choices = models.JSONField(blank=True, null=True)
    correct_answer = models.CharField(null=True, blank=True, max_length=256)
    question_types = (
        ('MultilineText', 'multiline_text'),
        ('Number', 'number'),
        ('MultipleChoice', 'multiple_choice'),
        ('Yes/No','yes/no')
    )

    prod = models.ForeignKey(Product,null=True, blank=True ,on_delete=models.CASCADE)
    question = models.CharField(max_length=256, null=True)
    question_type = models.CharField(
        max_length=20, default='MultilineText', choices=question_types)
    is_adult = models.BooleanField(default=True)


    class Meta:
        app_label = 'cocolife'

    @ property
    def get_question_id(self):
        return self.id

    @ property
    def get_product_id(self):
        return self.product

    @ property
    def get_question(self):
        return self.question

    @ property
    def get_question_type(self):
        return self.question_type
 