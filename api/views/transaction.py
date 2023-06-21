from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from api.tasks.email import send_transaction_info
# from django.core.mail import send_mail
# from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.views.generic import View
from datetime import datetime
from django.utils.dateparse import parse_date
from api.tasks.renderPDF import Render

from api.serializers import InsureePolicySerializer, GetTransactionHistorySerializer
from digiinsurance.models import InsureePolicy, Transaction, Insuree
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.http import HttpResponse


__all__ = ['TransactionViewSet', 'TransactionHistory']

# TODO: Change serializer and model to Transaction


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = InsureePolicy.objects.all()
    serializer_class = InsureePolicySerializer

    def create(self, request):
        # subject = 'My Subject'
        # message_body = 'My Message body'
        # from_email = 'marketing@qymera.tech'
        # to = ['mark.christian.paderes@gmail.com']
        # send_mail(
        #   subject,
        #   message_body,
        #   from_email,
        #   to
        # )
        send_transaction_info.delay(123, 'mark.christian.paderes@gmail.com')

        # context = {
        #     'subject': 'Transaction Success',
        #     'transaction_id': '123'
        # }

        # subject = context['subject']

        # text_content = get_template(
        #     'emails/transaction.txt').render(context)
        # html_content = get_template(
        #     'emails/transaction.html').render(context)

        # msg = EmailMultiAlternatives(
        #     subject, text_content, 'DigiInsurance <marketing@qymera.tech>', ['mark.christian.paderes@gmail.com'])
        # msg.attach_alternative(html_content, "text/html")

        # msg.send()

        return Response({'message': 'Email sent'})

# TODO: Change model to transactions once avaialble


class TransactionHistory(GenericAPIView):
    permission_classes = (AllowAny, )

    queryset = Transaction.objects.all()
    serializer_class = GetTransactionHistorySerializer

    def get(self, request, insuree_id, start_date, end_date, authtoken):
        start_date = parse_date(start_date)
        end_date = parse_date(end_date)

        _key = Token.objects.filter(key=authtoken)

        if _key.exists():
            transactions = Transaction.objects.filter(insuree_id=insuree_id).values(
                'transaction_date', 'insureePolicy__policy__name', 'amount', 'channel', 'insureePolicy__policy__company__name')
            insuree = Insuree.objects.filter(pk=insuree_id).values(
                'first_name', 'middle_name', 'last_name', 'email').first()
            transaction_count = transactions.count()
            current_time = datetime.now()
            params = {
                'current_time': datetime.now(),
                'start_date': start_date,
                'end_date': end_date,
                'transaction': transactions,
                'transaction_count': transaction_count,
                'insuree': insuree,
                'insuree_id': insuree_id,
                'request': request,
            }
            return Render.render('transaction_history.html', params)

        else:
            return HttpResponse('Unauthorized', status=401)
