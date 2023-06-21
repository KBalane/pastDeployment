from django.http.response import Http404
from digiinsurance.models import Claims, Transaction, User
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response

from django.core.files import File

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

from django.db.models.functions import Concat
from django.db.models import CharField, Value as V

from rest_framework.permissions import AllowAny

__all__ = ['GeneratePDF_Claims', 'GeneratePDF_Transaction', 'TransactionHistory', 'DownloadPDF_Claims',
           'TransactionHistory_Base']


class GeneratePDF_Transaction(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, id_search, *args, **kwargs):
        try:
            transaction = Transaction.objects.all().filter(insuree_id=id_search)
            name = Transaction.objects.all().values_list('insuree').annotate(name=Concat(
                'insuree__first_name',
                V(' '), 'insuree__last_name', V(''),
                output_field=CharField()
            )).filter(insuree_id=id_search).first()
            data = {
                'transactions': transaction,
                'name': name[1],
                'id': name[0]
            }
            template = get_template('transaction_invoice.html')
            data_p = template.render(data)
            response = BytesIO()
            pdf_page = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)
            if not pdf_page.err:
                # return HttpResponse(response.getvalue(), content_type='application/pdf')
                response = HttpResponse(response.getvalue(), content_type='application/pdf')
                filename = "transaction_invoice_%s.pdf" % id_search
                content = "inline; filename=%s" % filename
                download = request.GET.get("download")
                # if download: #to enable viewing functionality, uncomment this line and indent the next line.
                content = "attachment; filename=%s" % filename
                response['Content-Disposition'] = content
                return response
            else:
                return HttpResponse("Error Generating PDF")
        except TypeError as e:
            raise Http404


class GeneratePDF_Claims(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, id_search, *args, **kwargs):
        try:
            claim = Claims.objects.all().filter(UserPolicy_id__insuree=id_search)
            name = Claims.objects.all().values_list(
                'UserPolicy_id__insuree').annotate(policy_holder=Concat(
                'UserPolicy_id__insuree__first_name',
                V(' '), 'UserPolicy_id__insuree__last_name', V(''),
                output_field=CharField()
            )).filter(UserPolicy_id__insuree=id_search).first()

            data = {
                'claims': claim,
                'name': name[1],
                'id': name[0]
            }
            template = get_template('claims_invoice.html')
            data_p = template.render(data)
            response = BytesIO()
            pdf_page = pisa.pisaDocument(BytesIO(data_p.encode("UTF-8")), response)
            if not pdf_page.err:
                response = HttpResponse(response.getvalue(), content_type='application/pdf')
                filename = "claim_invoice_%s.pdf" % id_search
                content = "inline; filename=%s" % filename
                download = request.GET.get("download")
                # if download: #to enable viewing functionality, uncomment this line and indent the next line.
                content = "attachment; filename=%s" % filename
                response['Content-Disposition'] = content
                return response
            else:
                return HttpResponse("Error Generating PDF")
        except TypeError as te:
            raise Http404


class TransactionHistory(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, insuree, start_date, end_date):
        criteria_id = Q(insuree=insuree)
        criteria_start = Q(created_at=start_date)
        criteria_end = Q(modified_at=end_date)
        transactions_per = Transaction.objects.all().values(
            'insuree_id',
            'txn_id',
            'transaction_date',
            'amount',
            'processor_type'
        ).filter(criteria_id & criteria_start & criteria_end).order_by('-transaction_date')
        return Response(transactions_per)


class TransactionHistory_Base(APIView):
    """
    Lists all Transaction History based on insuree id.
    From newest to oldest.
    """

    def get(self, request, insuree):
        transactions_per = Transaction.objects.all().values(
            'insuree_id',
            'txn_id',
            'transaction_date',
            'amount',
            'processor_type'
        ).filter(insuree=insuree).order_by('-transaction_date')
        return Response(transactions_per)


class DownloadPDF_Claims(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, claim_id):
        # downloads pdf from claims table (db)
        pdffile = Claims.objects.get(id=claim_id)
        file = open(pdffile.claim_docs.path, 'rb')
        pdfFile = File(file)
        response = HttpResponse(pdfFile.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'attachment; filename=' + str(pdffile.claim_docs) + ".pdf"
        return response
