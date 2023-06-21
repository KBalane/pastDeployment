from rest_framework import serializers
from digiinsurance.models.InsureePolicyDocs import InsureePolicyDocs

__all__ = ['InsureePolicyDocsSerializer', 'UploadSubmittedDocsSerializer']


class InsureePolicyDocsSerializer(serializers.ModelSerializer):

	class Meta:
		model = InsureePolicyDocs
		fields = '__all__'


class UploadSubmittedDocsSerializer(serializers.ModelSerializer):
	class Meta:
		model = InsureePolicyDocs
		field = ('doc', )
