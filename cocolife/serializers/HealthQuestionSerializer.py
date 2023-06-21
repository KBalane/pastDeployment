from rest_framework import serializers

from cocolife.models import CLHealthQuestions

__all__ = ['CLHealthQuestionSerializer']


class CLHealthQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CLHealthQuestions
        fields = '__all__'
