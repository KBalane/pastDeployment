from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from digiinsurance.models.HealthQuestions import HealthQuestions
from digiinsurance.models.HealthQuestionsAnswers import HealthQuestionsAnswers
from digiinsurance.models.InsureePolicy import InsureePolicy


class HealthQASerializer(serializers.Serializer):
    insureePolicy_id = serializers.IntegerField()
    question_id = serializers.IntegerField()
    answer = serializers.CharField()

    class Meta:
        model = HealthQuestionsAnswers
        fields = ('insureePolicy_id', 'question_id', 'answer')

    def validate_insuree_policy_id(self, insureePolicy_id):
        insureePolicy = InsureePolicy.objects.filter(
            pk=insureePolicy_id)
        if not insureePolicy.exists():
            raise serializers.ValidationError(
                _("insureePolicy_id does not exist!"))
        return insureePolicy_id

    def validate_question_id(self, question_id):
        healthQuestions = HealthQuestions.objects.filter(pk=question_id)
        if not healthQuestions.exists():
            raise serializers.ValidationError(_("question_id does not exist!"))
        return question_id

    # Can add validation for multiple choice type question but stick to manual for now

    def create(self, validated_data):
        return HealthQuestionsAnswers.objects.create(**validated_data)


class UpdateHealthQAAnswerStatus(serializers.ModelSerializer):
    class Meta:
        model = HealthQuestionsAnswers
        fields = ('answer_status',)
