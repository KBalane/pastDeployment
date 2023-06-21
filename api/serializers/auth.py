import base64
import json

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import ugettext_lazy as _
from digiinsurance.models.User import User

from rest_framework import serializers, exceptions
from rest_framework.authtoken.models import Token

__all__ = [
    'LoginSerializer', 'TokenSerializer', 'ChangePasswordSerializer',
    'ForgotPasswordSerializer', 'ResetPasswordSerializer']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def _validate_username(self, username, password):
        user = None

        if username and password:
            fetched_username = User.objects.filter(username=username)
            fetched_email = User.objects.filter(email=username)
            fetched_mobile_number = User.objects.filter(mobile_number=username)
            
            if fetched_username.exists():
                user = authenticate(username=fetched_username[0], password=password)
            elif fetched_email.exists():
                user = authenticate(username=fetched_email[0], password=password)
            elif fetched_mobile_number.exists():
                user = authenticate(username=fetched_mobile_number[0], password=password)

        else:
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = None

        if username:
            user = self._validate_username(username, password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')   
            elif not user.is_verified: # TODO - mobile_verified
                msg = _('Please verify your email')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate_new_password1(self, value):
        validate_password(value)
        return value

    def validate(self, attrs):
        if attrs['new_password1'] != attrs['new_password2']:
            raise serializers.ValidationError(
                _('The two password fields did not match.'))

        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    # def validate_email(self, email):
    #     user_model = get_user_model()

    #     try:
    #         self.user = user_model.objects.get(email=email)
    #     except user_model.DoesNotExist:
    #         raise serializers.ValidationError(
    #             _("We do not have user with given e-mail address in our system."))

    #     return email

    def validate(self, data):
        user_model = get_user_model()

        try:
            self.user = user_model.objects.get(email=data['email'])
            # Serialize uid and token to json then encode to base64
            uid_and_token = json.dumps({
                'uid': self.user.pk,
                'token': default_token_generator.make_token(self.user)
            }).encode('utf-8')
            return {
                'uid_and_token_b64': base64.urlsafe_b64encode(uid_and_token)
            }
        except user_model.DoesNotExist:
            return data


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    # uid_and_token receive json dict encoded with base64
    uid_and_token_b64 = serializers.CharField(required=True)

    def validate_password_confirm(self, value):
        validate_password(value)
        return value

    def validate(self, data):

        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError(_("Password mismatch."))

        return {'password': data['password']}

    def validate_uid_and_token_b64(self, uid_and_token_b64):

        try:
            # Deserialize data from json
            # Make sure any left % in url are unquoted
            json_data = base64.urlsafe_b64decode(uid_and_token_b64)
            data = json.loads(json_data)
        except Exception:
            raise serializers.ValidationError(_("Broken data."))

        uid = data.get('uid', None)
        token = data.get('token', None)

        try:
            assert uid and token and isinstance(uid, int)
        except AssertionError:
            raise serializers.ValidationError(_("Broken data."))

        user_model = get_user_model()

        try:
            self.user = user_model.objects.get(pk=uid)
        except user_model.DoesNotExist:
            raise serializers.ValidationError(_("User not found."))

        # validate token
        if not default_token_generator.check_token(self.user, token):
            msg = "%s %s" % (
                _("This password recovery link has expired or associated user does not exist."),
                _("Use password recovery form to get new e-mail with new link."))
            raise serializers.ValidationError(msg)