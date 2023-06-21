import base64
import json
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from django.core.mail import send_mail
from rest_framework.response import Response
from digiinsurance.models import User
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from api.serializers.UserSerializer import SetPassword
from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny

__all__ = ['VerifyEmail', 'EmailHandler', 'setInitialPassword']


class VerifyEmail(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()


class EmailHandler(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, username, to_email):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

        if user.is_verified == True:
            return Response("This email is already Verified")

        token = self.generate_verification_token(user=user)

        # TODO Set Production and Dev urls
        """ if settings.IS_PRODUCTION:
            url = 'https://di-admin-qyhq5.ondigitalocean.app/activate-account'
        else:
            url =  'http://localhost:3001/activate-account' """

        url = 'https://di-admin-qyhq5.ondigitalocean.app/activate-account'

        send_mail(
            'Hello, %s!' % (username),  # title
            '''
            Your account has been created successfully!
            Please click on the link below to activate your account:
            %s/%s/''' % (url, token),  # body
            'marketing@qymera.tech',  # from
            ['%s' % (to_email)],  # to (recepient)
            fail_silently=False)
        return Response('Verification Email Sent')

    @staticmethod
    def generate_verification_token(user):
        token = json.dumps({
            'uid': user.pk,
            'email': user.email,
            'token': default_token_generator.make_token(user)
        }).encode('utf-8')
        return base64.urlsafe_b64encode(token)


class setInitialPassword(RetrieveUpdateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = SetPassword

    def get(self, request, token):
        user = self.verify_token(request, token)
        return Response(status.HTTP_200_OK)

    def put(self, request, token):
        user = self.verify_token(request, token)

        queryset = user
        serializer_class = SetPassword(queryset, data=request.data)

        if (serializer_class.is_valid(raise_exception=True)):
            serializer_class.save()
            return Response(status.HTTP_200_OK)
        return Response(status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def verify_token(request, token):

        try:
            strobject = token[1::]
            print(strobject)
            json_data = base64.urlsafe_b64decode(strobject)
            data = json.loads(json_data)

            uid = data.get('uid', None)
            token = data.get('token', None)
        except (UnicodeDecodeError, base64.binascii.Error):
            raise ValidationError("Invalid Token")

        try:
            user = User.objects.get(id=uid)
        except User.DoesNotExist:
            raise Http404

        if user and user.is_verified:
            raise ValidationError("This email is already Verified")
        return user
