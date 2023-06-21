import os
import time
import errno
import io
import logging
import json

from rest_framework.generics import  ListAPIView, RetrieveAPIView
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from api import serializers
from django.db.models import Q

from api.serializers import InsureePolicyDocsSerializer, UploadSubmittedDocsSerializer, ClaimsSerializer, ClaimsDocsSerializer

from digiinsurance import settings
from digiinsurance.storage_backend import get_s3_client
from digiinsurance.models import InsureePolicyDocs, Claims

from django.core.files import File
from django.http import HttpResponse, Http404, JsonResponse

logger = logging.getLogger('digiinsurance.views')

__all__ = ['GetSubmittedDocs', 'DownloadSubmittedDocs', 'UploadSubmittedDocs','GetSubmittedClaims']

class GetSubmittedDocs(generics.ListAPIView):
	permissions_classes=(IsAuthenticated, )
	serializer_class = InsureePolicyDocsSerializer

	def get_queryset(self):
		Insuree_docs_id=self.kwargs['insuree_id']
		return InsureePolicyDocs.objects.filter(insuree_docs=Insuree_docs_id)

class GetSubmittedClaims(generics.ListAPIView):
	"""
	This is where you get the document uploaded for claims.

	Sample reuqest: https:/digiinsurance.qymera.tech/api/v1/insuree/submitted_claims/149/99/

	"""
	queryset = Claims.objects.all
	serializer_class = ClaimsDocsSerializer
	def get_queryset(self):
		insuree_id=self.kwargs['insuree_id']
		insuree_policy_id=self.kwargs['insuree_policy_id']
		
		return Claims.objects.filter(Q(UserPolicy_id__insuree = insuree_id) & Q(UserPolicy_id = insuree_policy_id)).order_by('-modified_at')

	# def get(self, request, insuree_id,insuree_policy_id):
	# 	queryset = Claims.objects.all().filter(Q(UserPolicy_id__insuree = insuree_id) & Q(UserPolicy_id = insuree_policy_id)).order_by('-modified_at')
	# 	serializer = ClaimsDocsSerializer(queryset, many=True)

	# 	return Response(serializer.data)

class UploadSubmittedDocs(APIView):
	serializer_class = InsureePolicyDocsSerializer
	queryset = InsureePolicyDocs.objects.all()

	def get_upload_to_space(self, context, request):
		if settings.IS_PRODUCTION:
			serializeddata = context

			insuree = str(serializeddata.get('insuree_docs'))
			insuree_docs_id = serializeddata.get('id')
			# insuree_pdf = request.data.get('doc')
			# print(insuree_pdf)
			pdffile=InsureePolicyDocs.objects.get(id=insuree_docs_id)
			file= open(pdffile.doc.path, 'rb')

			file_key = 'submitted_docs/user_%s/%s' %  (insuree, insuree_docs_id)
			client = get_s3_client()
			client.put_object(Bucket= settings.AWS_STORAGE_BUCKET_NAME ,Key= file_key, Body= file ,ACL='private', ContentType="application/pdf")
			# client.upload_file(file, settings.AWS_STORAGE_BUCKET_NAME, file_key)

			sucess_message = "successfully uploaded"

			return sucess_message
		else:
			error_message = "Error in uploading"

			return error_message

		
	def post(self, request):
			serializer = InsureePolicyDocsSerializer(data = request.data)
			if serializer.is_valid():
				serializer.save()
				if settings.IS_PRODUCTION:
					context =serializer.data
					return Response(self.get_upload_to_space(context, request))
				else:
					return Response(serializer.data, status=status.HTTP_200_OK)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
			
class DownloadSubmittedDocs(RetrieveAPIView):
	queryset = InsureePolicyDocs.objects.all()
	serializer_class = InsureePolicyDocsSerializer

	def get_object(self, id):
		try:
			return InsureePolicyDocs.objects.get(id=id)
		except InsureePolicyDocs.DoesNotExist:
			raise Http404

	def get(self, request, id, insuree_id):
		if settings.IS_PRODUCTION:
			# user_id = request.data.get('insuree_docs')
			file_key = 'submitted_docs/user_%s/%s' %  (insuree_id , id)
			client = get_s3_client()
			url = client.generate_presigned_url(
				ClientMethod = 'get_object', 
				Params = {
					'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 
					'Key': file_key
					}, 
				ExpiresIn=300)

			return Response(url, status=status.HTTP_200_OK)

		else:
			pdffile=InsureePolicyDocs.objects.get(id=id)
			file=open(pdffile.doc.path, 'rb')
			pdfFile=File(file)
			response=HttpResponse(pdfFile.read(), content_type="application/pdf")
			response['Content-Disposition']='attachment; filename=' + pdffile.filename
			return response