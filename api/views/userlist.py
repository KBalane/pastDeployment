from rest_framework.generics import ListAPIView, GenericAPIView
from api.views import user
from digiinsurance.models import User, AuditEntry
from api.serializers import UserSerializer, KYCListSerializer, UserListSerializer
from kyc.models import TemplateID, UserID
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


__all__ = ['UserList', 'KYCList', 'UserIsVerified']

class UserList(ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserListSerializer

    
    def get_queryset(self):
        #stores activity in activity log
        from cocolife import utils        
        utils.coco_user_log(self.__class__.__name__,self.request.user)
        return super().get_queryset()

class KYCList(ListAPIView):
    queryset = UserID.objects.all()
    serializer_class = KYCListSerializer

class UserIsVerified(GenericAPIView):
    permission_classes = (AllowAny,)
    def get(self, request, id):
        try:
            user = User.objects.filter(id=id).values('email', 'is_verified')[0]
        except Exception as e:
            return Response("Not Found", status=404)
        return Response(user)
    

