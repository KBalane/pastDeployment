
from cocolife.serializers import CLHealthQuestionSerializer
from cocolife.models import CLHealthQuestions
from rest_framework.views import APIView


from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response



__all__ = ['HealthQuestionViewSet','CLHealthQuestionBaseOnAge']


class HealthQuestionViewSet(ListCreateAPIView):
    permission_classes=(AllowAny,)
    queryset = CLHealthQuestions.objects.all()
    serializer_class = CLHealthQuestionSerializer


class CLHealthQuestionBaseOnAge(APIView):
    queryset = CLHealthQuestions.objects.all()
    serializer_class = CLHealthQuestionSerializer

    def get(self,request,age):
        # age =  ProductInsuree.objects.filter(id=id).values()

        if(age >= 15):
            data = self.queryset.filter(is_adult = True)
            serializer_class = CLHealthQuestionSerializer(data,many = True )
            
        elif(age <= 14):
            data =  self.queryset.filter(is_adult = False)
            serializer_class = CLHealthQuestionSerializer(data,many = True )
      
        return Response(serializer_class.data)


#Manage specific question
# class ManageHealthQuestion(RetrieveUpdateDestroyAPIView):
#     permission_classes = (IsAuthenticated,)

#     lookup_field = 'pk'
#     queryset = CLHealthQuestions.objects.all()
#     serializer_class = CLHealthQuestionSerializer


#Experimental For Geting age using the product_insuree
# class CLgetAgeFromCocoUser(APIView):
#     def get(self, request, id):
#         productinsure = ProductInsuree.objects.filter(id=id).values(
#             'billed_to__age',
#             'billed_to__first_name',
#         )
#         return Response(productinsure)   
