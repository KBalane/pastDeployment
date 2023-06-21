
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response




__all__ = ['S1Demo']


class S1Demo(APIView):
    permission_classes = (AllowAny,)
    def get(self,request):
        
        bigDict = [
            {
            "title": "Welcome to COCOLIFE!",
            "desc": "We are happy to have you here with us."
            },

            {
            "title": "Security matters to us",
            "desc": "We value your information and take great pride in keeping it that way."
            },

            {
            "title": "We value your happiness",
            "desc": "Dream as if you'll live forever, live as if you'll die today."
            },
        
        ]
        
        return Response(bigDict)

        
