from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from digiinsurance.models.User import User
from digiinsurance.models.UserBankAccount import UserBankAccount


class UserListSerializer(serializers.ModelSerializer):
    is_verified = serializers.BooleanField()
    is_archived = serializers.BooleanField(source='user.is_archived', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'photo', 'country_code',
                  'mobile_number', 'kyc_done', 'info_submitted', 'is_verified', 'is_archived')


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    is_verified = serializers.BooleanField(source='user.is_verified', read_only=True)
    is_archived = serializers.BooleanField(source='user.is_archived', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'photo', 'country_code', 'mobile_number', 'kyc_done',
                  'info_submitted', 'is_verified', 'is_archived')

    def validate_username(self, username):
        user = User.objects.filter(username=username)
        if self.instance:
            user = user.exclude(id=self.instance.id)
        if user.exists():
            raise serializers.ValidationError(
                _("A user is already registered with this username."))
        if ' ' in username:
            raise serializers.ValidationError(
                _("Username can't have spaces."))
        return username

    def validate_email(self, email):
        user = User.objects.filter(email=email)
        if self.instance:
            user = user.exclude(id=self.instance.id)
        if user.exists():
            raise serializers.ValidationError(
                _("A user is already registered with this e-mail address."))
        return email

    # def validate_mobile_number(self, mobile_number):
    #     user = User.objects.filter(mobile_number=mobile_number)
    #     if self.instance:
    #         user = user.exclude(id=self.instance.id)
    #     if user.exists():
    #         raise serializers.ValidationError(
    #             _("A user is already registered with this mobile number."))
    #     return mobile_number


class UserBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBankAccount
        # fields = ('id', 'first_name', 'middle_name', 'last_name')
        fields = '__all__'


class GetSubmittedID(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'photo')


class SetPassword(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def update(self, instance, validated_data):
        instance.is_verified = True
        instance.set_password(validated_data['password'])
        instance.save()

        return instance
