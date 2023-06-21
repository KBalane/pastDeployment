from rest_framework import serializers

from digiinsurance.models import HealthQuestions


class HealthQuestionSerilizer(serializers.ModelSerializer):
    class Meta:
        model = HealthQuestions
        fields = '__all__'

    def validate(self, attrs):
        if attrs['question_type'] == 'MultipleChoice' and attrs['choices'] is None:
            raise serializers.ValidationError({"error" : "The type MultipleChoice requires options"})
        if attrs['question_type'] != 'MultipleChoice' and bool(attrs['choices']):
            raise serializers.ValidationError({"error" : "Invalid question type"})
        return attrs 
    
    def create(self, validated_data):
        return HealthQuestions.objects.create(**validated_data)
