from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import viewsets
from django.http import HttpResponse, Http404
from rest_framework.views import APIView
from rest_framework.response import Response

from api.serializers import HealthQuestionSerilizer
from digiinsurance.models import HealthQuestions
__all__ = ['HealthQuestionsViewSet', 'UpdateHealthQuestion', 'InsureeQuestions']

class HealthQuestionsViewSet(viewsets.ModelViewSet):
    queryset = HealthQuestions.objects.all()
    serializer_class = HealthQuestionSerilizer

    def get_queryset(self):
        queryset = HealthQuestions.objects.all()
        policy = self.request.query_params.get('policy_id')
        if policy:
            queryset = queryset.filter(policy_id=policy)
        return queryset


class UpdateHealthQuestion(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)

    lookup_field = 'id'
    queryset = HealthQuestions.objects.all()
    serializer_class = HealthQuestionSerilizer

class InsureeQuestions(APIView):

    def get(self, request):
        Questions = HealthQuestions.objects.values(
            'question',
            'question_type'
        )
        try:
            Questions = Questions.filter(policy_id='54')
            return Response(Questions)
        except HealthQuestions.DoesNotExist:
            raise Http404
        
    