from digiinsurance.models import Policy
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
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
from api.serializers import UpdateTermsAndConditionPerPolicy
__all__=['TermsAndConditionPerPolicy','UpdateTermsAndConditionPerPolicy']

class TermsAndConditionPerPolicy(APIView):
    #claims_per_policy = Policy.objects.values('adminupload')
    permission_classes = (AllowAny, )

    def get(self, request, id_search):
        # ATTENTION ATTENTION ATTENTION ATTENTION
        # ATTENTION ATTENTION ATTENTION ATTENTION
        # To make this work, kindly do a pip install.
        # pip install pdfminer
        # it should work after running the line above

        pdffile = Policy.objects.get(id=id_search)
        output_string = StringIO()
        with open(pdffile.adminupload.path, 'rb') as in_file:
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

class UpdateTermsAndConditionPerPolicy(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    
    lookup_field = 'pk'
    queryset = Policy.objects.all()
    serializer_class = UpdateTermsAndConditionPerPolicy
