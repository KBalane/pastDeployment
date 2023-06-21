from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from .UserSerializer import UserSerializer

from digiinsurance.models.Insuree import Insuree
from digiinsurance.models.User import User


class AccountUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    first_name = serializers.CharField()
    middle_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField()
    gender = serializers.CharField(max_length=1)
    birthday = serializers.DateField()
    email = serializers.EmailField()
    mobile_number = serializers.CharField()
    current_add = serializers.CharField()
    occupation = serializers.CharField()
    civil_status = serializers.CharField()
    place_of_birth = serializers.CharField()
    nationality = serializers.CharField()
    sss = serializers.CharField()
    tin = serializers.CharField()
    business = serializers.CharField()
    province = serializers.JSONField()
    number_owner = serializers.CharField()
    owner_relationship = serializers.CharField()
    minor_name = serializers.CharField()

    purpose = serializers.CharField()
    sim_card_serial = serializers.CharField()
    sim_card_number = serializers.CharField()
    isActive = serializers.CharField()

    class Meta:
        model = Insuree
        fields = (
        'user', 'first_name', 'middle_name', 'last_name', 'gender', 'email', 'mobile_number', 'birthday', 'current_add',
        'occupation',
        'civil_status', 'place_of_birth', 'nationality', 'sss', 'tin', 'business',
        'province', 'number_owner', 'owner_relationship', 'minor_name',
        'purpose', 'sim_card_serial', 'sim_card_number', 'isActive')

    def validate_email(self, email):
        user = User.objects.filter(email=email)
        if user.exists():
            raise serializers.ValidationError(
                _("A user is already registered with this e-mail address."))
        return email

    def update(self, instance, validated_data):
        # get user obj from request.
        if 'user' in validated_data:
            # get data from user object.
            user_data = validated_data.pop('user')
            user = instance.user
            # save username data, from user object.
            user.username = user_data.get('username', user.username)
            # save user
            user.save()

        # https://stackoverflow.com/questions/53779723/django-rest-framework-update-with-kwargs-from-validated-data
        # save validated items from request
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        # save insuree
        instance.save()
        return instance


class AccountInfoSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    middle_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField()
    gender = serializers.CharField(max_length=1)
    email = serializers.EmailField()
    mobile_number = serializers.CharField()
    birthday = serializers.DateField()
    current_add = serializers.CharField()
    occupation = serializers.CharField()
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    class Meta:
        model = Insuree
        fields = ('first_name', 'middle_name', 'last_name', 'gender', 'email', 'mobile_number',
                  'birthday', 'current_add')

    def validate_email(self, email):
        user = User.objects.filter(email=email)
        if user.exists():
            raise serializers.ValidationError(
                _("A user is already registered with this e-mail address."))
        return email

    def validate_username(self, username):
        user = User.objects.filter(username=username)
        if user.exists():
            raise serializers.ValidationError(
                _("A user is already registered with this username."))
        return username

    # def validate_mobile_number(self, mobile_number):
    #     user = User.objects.filter(mobile_number=mobile_number)
    #     if self.instance:
    #         user = user.exclude(id=self.instance.id)
    #     if user.exists():
    #         raise serializers.ValidationError(
    #             _("A user is already registered with this mobile number."))
    #     return mobile_number

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            mobile_number=validated_data.get('mobile_number'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name')
        )
        user.set_password(validated_data.get('password'))
        user.save()
        insuree = Insuree.objects.create(
            user_id=user.id,
            first_name=validated_data.get('first_name'),
            middle_name=validated_data.get('middle_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email'),
            gender=validated_data.get('gender'),
            mobile_number=validated_data.get('mobile_number'),
            birthday=validated_data.get('birthday'),
            current_add=validated_data.get('current_add'),
            occupation=validated_data.get('occupation'),
        )
        insuree.save()
        return insuree
