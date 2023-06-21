
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.mail import send_mail

__all__ = ['MockPayment']

from datetime import date




class MockPayment(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):

        
        name = request.data.get('name')
        price = request.data.get('price')
        product_name = request.data.get('product_name')
        product_code = request.data.get('product_code')
        description = request.data.get('description')
        today = date.today()
        email = request.data.get('email')
        method = request.data.get('method')

        send_mail(
        'Hi, %s!' % (name), #title
        '''
You have successfully purchased a product!
This email provides you a copy of your payment details:


Name: %s
Product Name: %s
Product Code: %s

Description: %s

Payment Confirmed Date: %s
Price: %s
Paid using: %s

''' % (name, product_name, product_code, description, today, price, method), #body
        'questronix@qymera.tech', #from
        ['%s' % (email)], #to (recepient)
        fail_silently=False)

        return Response("Working")
