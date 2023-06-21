from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import GenericAPIView, RetrieveAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import viewsets, generics, status


from django.core.files import File
from api import serializers
from api.serializers import EditPolicyPackagesSerializer, GetAllPolicySerializer, GetPolicyBenefitsSerializer, PolicySerializer , DownloadPDFPolicySerializer, UploadPolicySerializer, CertificateTemplateSerializer, CreateProductSerializer, ViewPolicySerializer, UpdateFileFieldSerializer
from digiinsurance.models import Policy
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from digiinsurance import settings
from digiinsurance.storage_backend import get_s3_client
import json

import os
import os.path
from os import path
from django.conf import settings
from django.http import HttpResponse, Http404
__all__ = [
    'GetAllPoliciesView', 
    'GetPolicyBenefitsView', 
    'PolicyViewSet', 
    'GetSpecificPolicyView',
    'DownloadPdfPolicy', 
    'EditSpecificPolicy',
    'UploadPolicy',
    'CertificateTemplate',
    'CreateProduct',
    'EditPackagePerPolicy',
    'DraftAProduct',
    'ActivateAProduct',
    'PolicyEdit','PolicyFileEdit',
    ]



class GetAllPoliciesView(ListModelMixin, GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = Policy.objects.all()
    serializer_class = GetAllPolicySerializer
    paginate_by = 10
    # def perform_create(self, serializer):
        # author = get_object_or_404(Author, id=self.request.data.get('author_id'))
        # return serializer.save()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, *kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        bool = self.request.query_params.get('is_recommended')
        if bool:
            qs = qs.filter(is_recommended=bool)
        return qs
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwasrgs)
    

class GetSpecificPolicyView(RetrieveAPIView):
    queryset = Policy.objects.all()
    serializer_class = GetAllPolicySerializer



class GetPolicyBenefitsView(RetrieveUpdateAPIView):
    queryset = Policy.objects.all()
    serializer_class = GetPolicyBenefitsSerializer

class PolicyViewSet(viewsets.ModelViewSet):
    queryset = Policy.objects.all().order_by('name')
    serializer_class = PolicySerializer

class PolicyEdit(RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = Policy.objects.all()
    serializer_class = ViewPolicySerializer

class PolicyFileEdit(RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = Policy.objects.all()
    serializer_class = UpdateFileFieldSerializer

    def put(self, request, pk, *args, **kwargs):
        files = Policy.objects.values_list(
            'benefits_basic','benefits_lite','benefits_standard','benefits_pro').filter(id = pk)
        query = Policy.objects.get(id = pk)
        serializer = UpdateFileFieldSerializer(query, data = request.data)
        b_basic = request.data.get('benefits_basic')
        b_lite = request.data.get('benefits_lite')
        b_standard = request.data.get('benefits_standard')
        b_pro = request.data.get('benefits_pro')
        data = {}
        if serializer.is_valid():
            #basic
            if b_basic is None:
                serializer.validated_data['benefits_basic'] = files[0][0]
            else:
                serializer.validated_data['benefits_basic'] = b_basic
            #lite
            if b_lite is None:
                serializer.validated_data['benefits_lite'] = files[0][1]
            else:
                serializer.validated_data['benefits_lite'] = b_lite
            #standard
            if b_standard is None:
                serializer.validated_data['benefits_standard'] = files[0][2]
            else:
                serializer.validated_data['benefits_standard'] = b_standard
            #pro
            if b_pro is None:
                serializer.validated_data['benefits_pro'] = files[0][3]
            else:
                serializer.validated_data['benefits_pro'] = b_pro
            
                
            serializer.save()
            data["sucesss"] = "Update Successful"
            return Response(data = data)
        

class EditSpecificPolicy(APIView):
    '''
    lookup_field = 'id'
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    
    def update(self, request, *args, **kwargs):

        return super().update(request, *args, **kwargs)
    '''

    
    def get(self, request, id):
        queryset = Policy.objects.all().filter(id=id)
        serializer_class = PolicySerializer(queryset, many=True)
        
        return Response(serializer_class.data)

    def put(self, request, id):
        queryset = Policy.objects.get(id=id)
        serializers = GetAllPolicySerializer(queryset, data=request.data)
        if serializers.is_valid():
            serializers.save()

        packages = request.data.get('packages')
        payment_interval = request.data.get('payment_interval')
        payment_option = request.data.get('payment_option')

        #parse conversion
        #front-end has this problem where they are converting json
        #to string. The string gets passed in the jsonfield.
        #Because of the that the value of the jsonfield
        #is now a string instead of json.
        try:
            payment_option_parsed = json.loads(payment_option)
        except:
            #if proper json data has been passed,
            #converting wouldn't happen
            payment_option_parsed = payment_option

        try:
            packages_parsed = json.loads(packages)
        except:
            packages_parsed = packages

        try: 
            payment_interval_parsed = json.loads(payment_interval)
        except:
            payment_interval_parsed = payment_interval
        
        policy_id = serializers.data['id']
        Policy.objects.filter(id=policy_id).update(
                packages = packages_parsed,
                payment_interval = payment_interval_parsed,
                payment_option = payment_option_parsed
                )

        query = Policy.objects.all().filter(id=policy_id)
        serializer = CreateProductSerializer(query, many=True)
        
        return Response(serializer.data)
    


    
"""
def parse(packages,payment_interval,payment_option):
def put(self,request,id):
    company = request.data.get('company')
    name = request.data.get('name')
    description = request.data.get('description')
    packages = request.data.get('packages')
    payment_interval = request.data.get('payment_interval')
    category = request.data.get('category')
    payment_option = request.data.get('payment_option')
    question = request.data.get('question')
    

    payment_option_parsed = json.loads(payment_option)
    packages_parsed = json.loads(packages)
    payment_interval_parsed = json.loads(payment_interval)

    policy_id = id
    Policy.objects.filter(id=policy_id).update(
            company = company,
            name = name,
            description = description,
            packages = packages_parsed,
            payment_interval = payment_interval_parsed,
            category = category,
            payment_option = payment_option_parsed,
            question = question
            )

    query = Policy.objects.all().filter(id=policy_id)
    serializer = CreateProductSerializer(query, many=True)

    
    return serializer.data  
"""

class EditPackagePerPolicy(RetrieveUpdateAPIView):
    lookup_field = 'id'
    queryset = Policy.objects.all()
    serializer_class = EditPolicyPackagesSerializer

class DownloadPdfPolicy(RetrieveAPIView):
    permission_classes = (AllowAny, )
    queryset = Policy.objects.all()
    serializer_class = DownloadPDFPolicySerializer
    # print(repr(serializer_class))

    def get_object(self, id):

        try:
            return Policy.objects.get(id=id)
        except Policy.DoesNotExist:
            raise Http404

    def get(self, request, id):
        if settings.IS_PRODUCTION:
            file_key = 'policy_docs/policy_%s' % (id)
            client = get_s3_client()
            url = client.generate_presigned_url(
                ClientMethod = 'get_object',
                Params = {
                    'Bucket':settings.AWS_STORAGE_BUCKET_NAME,
                    'Key': file_key
                },
                ExpiresIn=300
            )
            return Response(url, status = status.HTTP_200_OK)
        else:
            pdffile = Policy.objects.get(id=id)
            file = open(pdffile.adminupload.path, 'rb')
            pdfFile = File(file)
            response = HttpResponse(pdfFile.read(),content_type="application/pdf")
            response['Content-Disposition']='attachment; filename='+pdffile.pdfname+".pdf"
            return response

    #  donwloading with filename parameter

    # def get(self,request, filename):
    #     path_to_file = settings.MEDIA_ROOT + '/media/' +filename
    #     file=open(path_to_file, 'rb')
    #     pdfFile=File(file)
    #     response=HttpResponse(pdfFile.read(),content_type="application/pdf")
    #     response['Content-Disposition']='attachment; filename=' + filename
    #     return response

class UploadPolicy(APIView):
    queryset = Policy.objects.all()

    def get_upload_policy_spaces(self, context, request):
        serializeddata = context

        Policy_id = serializeddata.get('id')
        Policy_pdf = Policy.objects.get(id = Policy_id)
        file = open(Policy_pdf.adminupload.path, 'rb')

        file_key = 'policy_docs/policy_%s' % (Policy_id)
        client = get_s3_client()
        client.put_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_key, Body=file, ACL='private', ContentType='application/pdf')

        success_message = "Successfully uploaded"
        
        return success_message
        

    def post(self, request):
        serializer = UploadPolicySerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            if settings.IS_PRODUCTION:
                context = serializer.data
                return Response(self.get_upload_policy_spaces(context, request))
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CertificateTemplate(RetrieveUpdateAPIView):
    lookup_field = 'id'
    queryset = Policy.objects.all()
    serializer_class =  CertificateTemplateSerializer


    def PUT(self, request, id):
        try:
            Pol_obj = Policy.objects.get(id=id)
        except Policy.DoesNotExist:
            raise Http404

        serializer = CertificateTemplateSerializer(Pol_obj, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class CreateProduct(APIView):
    def post(self,request):
        serializer = CreateProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()

        packages = request.data.get('packages')
        payment_interval = request.data.get('payment_interval')
        payment_option = request.data.get('payment_option')

        #parse conversion
        #front-end has this problem where they are converting json
        #to string. The string gets passed in the jsonfield.
        #Because of the that the value of the jsonfield
        #is now a string instead of json.
        try:
            payment_option_parsed = json.loads(payment_option)
        except:
            #if proper json data has been passed,
            #converting wouldn't happen
            payment_option_parsed = payment_option

        try:
            packages_parsed = json.loads(packages)
        except:
            packages_parsed = packages

        try: 
            payment_interval_parsed = json.loads(payment_interval)
        except:
            payment_interval_parsed = payment_interval

        policy_id = serializer.data['id']
        Policy.objects.filter(id=policy_id).update(
                payment_option = payment_option_parsed,
                packages = packages_parsed,
                payment_interval = payment_interval_parsed,
                )

        query = Policy.objects.all().filter(id=policy_id)
        serializer = CreateProductSerializer(query, many=True)

        
        return Response(serializer.data)
        #queryset = Policy.objects.all()
        #serializer_class = CreateProductSerializer

class DraftAProduct(APIView):
    def post(self, request, id):
        product = Policy.objects.all().filter(id=id).update(
            status = 'draft'
        )
        name = Policy.objects.all().values_list('name').filter(id=id)
        id = Policy.objects.all().values_list('id').filter(id=id)

        return Response("Successfully Drafted Product: "  + str(id[0][0]) + ": " + str(name[0][0]))

class ActivateAProduct(APIView):
    def post(self, request, id):
        product = Policy.objects.all().filter(id=id).update(
            status = 'active'
        )
        name = Policy.objects.all().values_list('name').filter(id=id)
        id = Policy.objects.all().values_list('id').filter(id=id)

        return Response("Successfully Activated Product: "  + str(id[0][0]) + ": " + str(name[0][0]))
