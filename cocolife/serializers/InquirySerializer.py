from rest_framework import serializers

from cocolife.models.Inquiry import Inquiry

__all__ = ['InquirySerializer']


class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = '__all__'
        read_only_fields = ['user']
