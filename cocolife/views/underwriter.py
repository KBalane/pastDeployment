from rest_framework.views import APIView
from cocolife.models import Underwriting

from rest_framework.generics import RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from cocolife.serializers.UnderwriterSerializer import UnderwriterSerializer,UnderwriterStatusSerializer





#Specific policy
class Underwriter(RetrieveUpdateAPIView):
    permission_classes=(AllowAny,)
    lookup_field='pk'
    queryset=Underwriting.objects.all()
    serializer_class=UnderwriterSerializer

    # #LOG FOR UNDERWRITING
    # def get_queryset(self):
    #     from cocolife import utils        
    #     utils.coco_user_log(self.__class__.__name__,self.request.user)
    #     return super().get_queryset()


#UNDERWRITER STATUS VIEW LAHAT THEN MAY FILTER

# class UnderwriterAll(APIView):
#     def get(self,request):
#         queryset=Underwriting.objects.all()
#         serializer_class=UnderwriterStatusSerializer(queryset, many = True)
#         return Response(serializer_class.data)

class UnderwriterAll(ListCreateAPIView):
    permission_classes=(AllowAny,)
    queryset=Underwriting.objects.all()
    serializer_class=UnderwriterSerializer

class UnderwriterStatus(APIView):
    permission_classes=(AllowAny,)
    def get(self, request, status):

        queryset=Underwriting.objects.all().filter(underwriter_status=status)
        serializer_class=UnderwriterStatusSerializer(queryset, many=True)
        return Response(serializer_class.data)