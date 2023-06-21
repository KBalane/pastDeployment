from cocolife.models.DigiInsuree import DigiInsuree
from digiinsurance.models import User
from rest_framework import serializers
from datetime import datetime


__all__ = ['DigiInsureeSerializer', 'DigiUserSerializer']


class DigiInsureeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigiInsuree
        fields = '__all__'


class DigiUserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    last_name = serializers.CharField()
    first_name = serializers.CharField()
    middle_name = serializers.CharField(required=False, allow_blank=True)
    mobile_number = serializers.CharField()
    email = serializers.EmailField()
    default_contact_info = serializers.CharField()
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('user_id', 'last_name', 'first_name', 'middle_name',
                  'mobile_number', 'email', 'default_contact_info', 'password')

    def validate_email(self, email):
        user = User.objects.filter(email=email)
        if user.exists():
            raise serializers.ValidationError(
                "A user is already registered with this e-mail address.")
        return email

    # def validate_mobile_number(self, mobile_number):
    #     user = User.objects.filter(mobile_number=mobile_number)
    #     if self.instance:
    #         user = user.exclude(id=self.instance.id)
    #     if user.exists():
    #         raise serializers.ValidationError(
    #             "A user is already registered with this mobile number.")
    #     return mobile_number

    def validate_default_contact_info(self, default_contact_info):
        if default_contact_info not in ['email', 'mobile', 'landline']:
            raise serializers.ValidationError(
                "Invalid value for default contact information")
        return default_contact_info

    def create(self, validated_data):
        user = User.objects.create(
            username=('%s%s%s'.lower()) % (validated_data.get('first_name'), validated_data.get('last_name'),validated_data.get('mobile_number')[-5:]),
            email=validated_data.get('email'),
            mobile_number=validated_data.get('mobile_number'),
            role='IN',
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name')
        )
        user.set_password(validated_data.get('password'))
        user.save()

        coco_insuree = DigiInsuree.objects.create(
            user=user,
            first_name=user.first_name,
            middle_name=validated_data.get('middle_name'),
            last_name=user.last_name,
            email=user.email,
            mobile_number=user.mobile_number,
            default_contact_info=validated_data.get('default_contact_info')
        )

        return coco_insuree
