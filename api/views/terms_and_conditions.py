from digiinsurance.models import TermsAndCondition
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView, GenericAPIView
from django.template.loader import render_to_string
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404, HttpResponse, JsonResponse
from django.core.files import File
import PyPDF2

from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from api.serializers import UpdateTermsAndCondition, TermsAndConditionsSerializer
__all__=['Terms','TermsUpdate','GetTermsAndCondition', 'GetAllTermsAndCondition']

class GetTermsAndCondition(APIView):
    #claims_per_policy = Policy.objects.values('adminupload')
    permission_classes = (AllowAny, )

    def get(self, request, pk):
        # ATTENTION ATTENTION ATTENTION ATTENTION
        # ATTENTION ATTENTION ATTENTION ATTENTION
        # To make this work, kindly do a pip install.
        # pip install pdfminer
        # it should work after running the line above

        pdffile = TermsAndCondition.objects.get(id=pk)
        output_string = StringIO()
        with open(pdffile.pdfUpload.path, 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)

        context = {
            "pdf_text": output_string.getvalue()
        }
        return Response(context)

class GetAllTermsAndCondition(APIView):
    permission_classes = (AllowAny, )
    def get(self, request):
        terms_and_conditions = TermsAndCondition.objects.all().values(
            'id',
            'company',
            'pdfUpload'
        )

        context = {
            'terms_and_conditions' : terms_and_conditions
        }

        return Response(context)

        

class Terms(ListCreateAPIView):
    permission_classes = (AllowAny, )
    queryset = TermsAndCondition.objects.all()
    serializer_class = UpdateTermsAndCondition

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class TermsUpdate(RetrieveUpdateAPIView):
    permission_classes = (AllowAny, )
    lookup_field = 'pk'
    queryset = TermsAndCondition.objects.all()
    serializer_class = UpdateTermsAndCondition
