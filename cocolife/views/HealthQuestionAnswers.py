
from typing import List
from cocolife.serializers import CLHealthQASerializer
from cocolife.models import CLHealthQuestionsAnswers,CLHealthQuestions
from cocolife.models import ProductInsuree,DigiInsuree

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView


__all__ = ['CLHealthQAViewSet','CLHealthQuestionManage']


class CLHealthQAViewSet(ListCreateAPIView):
    permission_classes=(AllowAny,)
    queryset = CLHealthQuestionsAnswers.objects.all()
    serializer_class = CLHealthQASerializer

    #compare correct ans to user input answer 
    #if correct answr = user input answer 
    #ans status is pass
    #if correct answr != user input answer 
    #ans status is fail
    def create(self, request, *args, **kwargs):
        # super().create(request, *args, **kwargs)
        
        ans = request.data.get('answer') 
        question_id = request.data.get('question')
        question = CLHealthQuestions.objects.get(id = question_id)
        prodInsur =  request.data.get('ProdInsuree')
        productinsuree = ProductInsuree.objects.get(id=prodInsur)

        if question.correct_answer.lower() == ans.lower():
            answer_status = CLHealthQuestionsAnswers.objects.create(
                answer = ans,
                answer_status = "pass",
                ProdInsuree = productinsuree,
                question =  question                   
            )
        else:
            answer_status = CLHealthQuestionsAnswers.objects.create(
                answer = ans,
                answer_status = "fail",
                ProdInsuree = productinsuree,
                question =  question                   
            )
        #count correct answers, must have perfect score, if not.
        #update product_insuree status to pending for underwriting.
        answer_status.save()
        return Response(200)


class CLHealthQuestionManage(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    lookup_field = 'pk'
    queryset = CLHealthQuestionsAnswers.objects.all()
    serializer_class = CLHealthQASerializer

    



   

    
   



  

