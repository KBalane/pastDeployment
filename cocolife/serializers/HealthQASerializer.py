from rest_framework import serializers
from cocolife.models import CLHealthQuestionsAnswers

__all__ = ['CLHealthQASerializer','UpdateHealthQAAnswerStatus']


class CLHealthQASerializer(serializers.ModelSerializer):
    class Meta:
        model = CLHealthQuestionsAnswers
        fields = ('__all__')

class UpdateHealthQAAnswerStatus(serializers.ModelSerializer):
    class Meta:
        model = CLHealthQuestionsAnswers
        fields = ('answer_status',)

     