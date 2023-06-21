import base64
import json

from django.contrib.auth.tokens import default_token_generator
from api.serializers.InsureeSerializer import InsureeSerializer
from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.contrib.auth import (
    login as django_login,
    logout as django_logout
)
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters

from rest_framework import status, exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.views.decorators.csrf import csrf_exempt
from braces.views import CsrfExemptMixin
from cocolife.models import ProductInsuree

from api.serializers.auth import (LoginSerializer, TokenSerializer, ChangePasswordSerializer, ForgotPasswordSerializer,
                                  ResetPasswordSerializer)
from api.serializers.UserSerializer import UserSerializer

from api.tasks.email import send_forgot_password_email, send_verification_email
from api.utils import create_token, get_google_token_info, fbgraph_token_info_vk
from digiinsurance.models.Insuree import Insuree
from digiinsurance.models.EmailVerification import EmailVerification
from digiinsurance.models.InsureePolicy import InsureePolicy
from digiinsurance.models.User import User

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)

__all__ = [
    'TestLoginView', 'LoginView', 'LogoutView', 'ChangePassword', 'ForgotPassword',
    'ResetPassword', 'CustomObtainAuthToken', 'GoogleSignUp', 'FBSignup']


def getPolicyCountPerUser(insuree_id):
    queryset = InsureePolicy.objects.all().values_list('id')

    count = queryset.filter(insuree=insuree_id).count()
    return count


class CustomObtainAuthToken(ObtainAuthToken, CsrfExemptMixin):
    permission_classes = (AllowAny,)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        response = super(
            CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        response = {
            'token': token.key,
            'id': user.id,
            # 'name': user.full_name,
            'insuree_id': None
        }
        if hasattr(user, 'insuree'):
            response['insuree_id'] = user.id

        return Response(response)


class LoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    @csrf_exempt
    def process_login(self):
        LogEntry.objects.log_action(
            user_id=self.user.id,
            content_type_id=ContentType.objects.get_for_model(self.user).pk,
            object_id=self.user.id,
            object_repr=str(self.user),
            action_flag=4,
            change_message='Successful login')

    @csrf_exempt
    def login(self):
        self.user = self.serializer.validated_data['user']
        self.token = create_token(self.user)
        self.process_login()

    def get_response(self):
        serializer_class = TokenSerializer

        serializer = serializer_class(instance=self.token,
                                      context={'request': self.request})
        json = serializer.data
        if self.user:
            json['id'] = self.user.id
            json['email'] = self.user.email
            if hasattr(self.user, 'insuree'):
                json['full_name'] = self.user.insuree.full_name
                json['insuree_id'] = self.user.insuree.pk
                json['policy_count'] = getPolicyCountPerUser(self.user.insuree.pk)
                '''
                try:
                    json['photo'] = self.user.photo
                except FileNotFoundError:
                    json['photo'] = 'File not found'
                '''
            elif hasattr(self.user, 'cocoinsurees'):
                json['full_name'] = self.user.cocoinsurees.get_full_name()
                json['insuree_id'] = self.user.cocoinsurees.pk
                json['policy_count'] = ProductInsuree.objects.filter(billed_to=self.user.id).count()
                json['is_kyc_done'] = self.user.kyc_done
        # json['redirect_url'] = reverse(
        # 'dashboard:dashboard', request=self.request)

        return Response(json, status=status.HTTP_200_OK)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        self.request = request

        # Check Mobile App Version
        # if 'version' in request.data:
        #     if settings.MOBILE_APP_MAINTENANCE:
        #         json = {'error_message': 'App currently under maintenance.  '}
        #         return Response(json, status=status.HTTP_200_OK)

        #     if not request.data['version'] in settings.MOBILE_SUPPORTED_VERSIONS:
        #         json = {'error_message': 'App version unsupported. Please update.'}
        #         return Response(json, status=status.HTTP_200_OK)

        self.serializer = self.get_serializer(
            data=self.request.data, context={'request': request})
        self.serializer.is_valid(raise_exception=True)
        # self.user = self.serializer.validated_data['user']
        # login_url = '%slogin/' % settings.WEB_APP_URL
        # if (self.user.is_student and
        #         self.request.META['HTTP_REFERER'] == login_url):
        #     json = {'error': 'For students, please login through the school portal.'}
        #     return Response(json, status=status.HTTP_403_FORBIDDEN)

        self.login()
        return self.get_response()


class TestLoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(TestLoginView, self).dispatch(*args, **kwargs)

    @csrf_exempt
    def process_login(self):
        if (self.user.role == 'IN' and self.request.get_host() == settings.WEB_APP_URL.lstrip("https://")):
            django_login(self.request, self.user)
            LogEntry.objects.log_action(
                user_id=self.user.id,
                content_type_id=ContentType.objects.get_for_model(self.user).pk,
                object_id=self.user.id,
                object_repr=str(self.user),
                action_flag=4,
                change_message='Successful login')
        elif (self.user.role == 'AD' and self.request.get_host() == settings.WEB_APP_URL_ADMIN.lstrip("https://")):
            django_login(self.request, self.user)
            LogEntry.objects.log_action(
                user_id=self.user.id,
                content_type_id=ContentType.objects.get_for_model(self.user).pk,
                object_id=self.user.id,
                object_repr=str(self.user),
                action_flag=4,
                change_message='Successful login')
        # elif(self.user.role == 'AD' and self.request.get_host() == settings.WEB_APP_URL_LOCALHOST):
        #     django_login(self.request, self.user)
        #     LogEntry.objects.log_action(
        #         user_id=self.user.id,
        #         content_type_id=ContentType.objects.get_for_model(self.user).pk,
        #         object_id=self.user.id,
        #         object_repr=str(self.user),
        #         action_flag=4,
        #         change_message='Successful login')
        # elif(self.user.role == 'IN' and self.request.get_host() == settings.WEB_APP_URL_LOCALHOST):
        #     django_login(self.request, self.user)
        #     LogEntry.objects.log_action(
        #         user_id=self.user.id,
        #         content_type_id=ContentType.objects.get_for_model(self.user).pk,
        #         object_id=self.user.id,
        #         object_repr=str(self.user),
        #         action_flag=4,
        #         change_message='Successful login')
        else:
            msg = _(
                "Account not valid for this host. Login using the other host. Host of request = `" + self.request.get_host() + "` || Role = `" + self.user.role + "` || settings.WEB_APP_URL = `" + settings.WEB_APP_URL.lstrip(
                    "https://") + "` || settings.WEB_APP_URL_ADMIN = `" + settings.WEB_APP_URL_ADMIN.lstrip(
                    "https://") + "`")
            # msg = _("Account not valid for this host. Login using the other host.")
            raise exceptions.ValidationError(msg)

    @csrf_exempt
    def login(self):
        self.user = self.serializer.validated_data['user']
        self.token = create_token(self.user)
        self.process_login()

    def get_response(self):
        serializer_class = TokenSerializer

        serializer = serializer_class(instance=self.token,
                                      context={'request': self.request})
        json = serializer.data
        if self.user:
            json['id'] = self.user.id
            json['email'] = self.user.email
            if hasattr(self.user, 'insuree'):
                json['full_name'] = self.user.insuree.full_name
                json['insuree_id'] = self.user.insuree.pk
                json['policy_count'] = getPolicyCountPerUser(self.user.insuree.pk)
                '''
                try:
                    json['photo'] = self.user.photo
                except FileNotFoundError:
                    json['photo'] = 'File not found'
                '''
        # json['redirect_url'] = reverse(
        # 'dashboard:dashboard', request=self.request)

        return Response(json, status=status.HTTP_200_OK)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        self.request = request

        # Check Mobile App Version
        # if 'version' in request.data:
        #     if settings.MOBILE_APP_MAINTENANCE:
        #         json = {'error_message': 'App currently under maintenance.  '}
        #         return Response(json, status=status.HTTP_200_OK)

        #     if not request.data['version'] in settings.MOBILE_SUPPORTED_VERSIONS:
        #         json = {'error_message': 'App version unsupported. Please update.'}
        #         return Response(json, status=status.HTTP_200_OK)

        self.serializer = self.get_serializer(
            data=self.request.data, context={'request': request})
        self.serializer.is_valid(raise_exception=True)
        # self.user = self.serializer.validated_data['user']
        # login_url = '%slogin/' % settings.WEB_APP_URL
        # if (self.user.is_student and
        #         self.request.META['HTTP_REFERER'] == login_url):
        #     json = {'error': 'For students, please login through the school portal.'}
        #     return Response(json, status=status.HTTP_403_FORBIDDEN)

        self.login()
        return self.get_response()


class LogoutView(APIView):

    def get(self, request, *args, **kwargs):
        return self.logout(request)

    def post(self, request, *args, **kwargs):
        return self.logout(request)

    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(request.user).pk,
            object_id=request.user.id,
            object_repr=str(request.user),
            action_flag=5,
            change_message='Successful logout')

        django_logout(request)

        return Response({"detail": _("Successfully logged out.")},
                        status=status.HTTP_200_OK)


class ChangePassword(GenericAPIView):
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = self.request.user
            if not user.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data.get('new_password1'))
            user.save()

            self.token = create_token(user)
            django_login(self.request, user)

            return Response({'success': True}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPassword(APIView):
    """
    Initiate a password restore procedure.
    """

    # Example request data
    # {
    #   "email" : "somename@somedomain.com"
    # }

    serializer_class = ForgotPasswordSerializer
    permission_classes = ()

    def post(self, request):
        # mode = request.data.get('mode', 'sms')

        # if mode == 'sms':
        #     pass
        # elif mode == 'email':

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid() and hasattr(serializer, 'user'):

            verifs = EmailVerification.objects.filter(
                email=serializer.user.email)
            verifs.delete()
            verif, created = EmailVerification.objects.get_or_create(
                type=EmailVerification.FORGOT_PASSWORD,
                token=serializer.validated_data['uid_and_token_b64'],
                user_id=serializer.user.id,
                email=serializer.user.email)
            if created:
                return self.send_email(serializer)

        return Response(
            {'error': 'User does not exist'}, status=status.HTTP_200_OK)

    @staticmethod
    def send_email(serializer):
        # send_forgot_password_email.delay(
        #     serializer.user.id,
        #     serializer.validated_data['uid_and_token_b64'])
        send_forgot_password_email(
            serializer.user.id,
            serializer.validated_data['uid_and_token_b64'])
        return Response({'success': True})


class ResetPassword(GenericAPIView):
    """
    Validate token and change a user password.
    """

    # Example request data
    # {
    #   "password" : "asdasd",
    #   "password_confirm" : "asdasd",
    #   "uid_and_token_b64" : "eyJ1aWQiOiAxLCAidG9rZW4iOiAiNDN1LWY5ZDIyMmM4YTNkZDhmYjI2OThlIn0="
    # }

    serializer_class = ResetPasswordSerializer
    permission_classes = ()

    def post(self, request):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.user
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response({'success': True})

        return Response(
            {'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GoogleSignUp(APIView):
    permission_classes = [AllowAny]

    # Do we still need to log
    @csrf_exempt
    def process_login(self):
        LogEntry.objects.log_action(
            user_id=self.user.id,
            content_type_id=ContentType.objects.get_for_model(self.user).pk,
            object_id=self.user.id,
            object_repr=str(self.user),
            action_flag=4,
            change_message='Successful login')

    def send_email_verification(self):
        # for newly created account, an email verification link will be sent via to insuree's email
        email_token = self.generate_verification_token(self.user)

        # create an entry for email verification
        verif, created = EmailVerification.objects.get_or_create(
            user=self.user,
            type=EmailVerification.VERIFICATION,
            token=email_token,
            email=self.user.email)

        # send an email if a record has been created
        if created:
            send_verification_email(self.user.id, email_token)

        # redirect user to login page, if already has been verified
        elif verif.is_expired:
            verif.delete()
            return False

    def login(self):
        # create auth token to be stored in local storage
        self.token = create_token(self.user)

        json = {}
        json['key'] = str(self.token)
        json['id'] = self.user.id
        json['email'] = self.user.email
        # add insuree fields if it applies
        if hasattr(self.user, 'insuree'):
            json['full_name'] = self.user.insuree.full_name
            json['insuree_id'] = self.user.insuree.pk
            json['policy_count'] = getPolicyCountPerUser(self.user.insuree.pk)
        return Response(json, status=status.HTTP_200_OK, )

    def post(self, request):
        try:
            token = request.data.get('id_token')
            google_res = get_google_token_info(token)

            if google_res:
                try:
                    email = google_res['email']
                    # add user to self, to be usable around the class.
                    self.user = User.objects.get(email=email)

                    return self.login()
                except User.DoesNotExist as e:
                    # create a user instance out of google response data
                    google_auth_user = {
                        # generate username
                        "username": '%s%s%s' % (
                        google_res.get('given_name').lower(), google_res.get('family_name').lower(),
                        google_res.get('sub')[-5:].lower()),
                        "email": google_res.get('email'),
                        "last_name": google_res.get('family_name'),
                        "first_name": google_res.get('given_name'),
                        "role": "IN"
                    }

                    user = UserSerializer(data=google_auth_user)
                    if user.is_valid():
                        # save user instance if valid TODO - Make this global self.user if better.
                        self.user = user.save()

                        # instantiate insuree from google data
                        google_insuree = {
                            "user_id": user.data['id'],
                            "last_name": google_res.get('family_name'),
                            "first_name": google_res.get('given_name'),
                            "email": user.data['email']
                        }

                        insuree = InsureeSerializer(data=google_insuree)
                        if insuree.is_valid():
                            # save insuree if valid
                            insuree.save()

                            # send email verification
                            self.send_email_verification()

                            # proceed to login
                            return self.login()
                        return Response(insuree.errors, status=status.HTTP_400_BAD_REQUEST)
                    return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                'success': False,
                'message': 'Google OAuth Error'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response("Something went wrong. Try again later.", status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def generate_verification_token(user):
        token = json.dumps({
            'uid': user.id,
            'email': user.email,
            'token': default_token_generator.make_token(user)
        }).encode('utf-8')
        return base64.urlsafe_b64encode(token)


class FBSignup(APIView):
    permission_classes = [AllowAny]

    def login(self):
        # create auth token to be stored in local storage
        self.token = create_token(self.user)
        json = {}
        json['key'] = str(self.token)
        json['id'] = self.user.id
        json['email'] = self.user.email
        # add insuree fields if it applies
        if hasattr(self.user, 'insuree'):
            json['full_name'] = self.user.insuree.full_name
            json['insuree_id'] = self.user.insuree.pk
            json['policy_count'] = getPolicyCountPerUser(self.user.insuree.pk)
        return Response(json, status=status.HTTP_200_OK, )

    def send_email_verification(self):
        # for newly created account, an email verification link will be sent via to insuree's email
        email_token = self.generate_verification_token(self.user)

        # create an entry for email verification
        verif, created = EmailVerification.objects.get_or_create(
            user=self.user,
            type=EmailVerification.VERIFICATION,
            token=email_token,
            email=self.user.email)

        # send an email if a record has been created
        if created:
            send_verification_email(self.user.id, email_token)

        # redirect user to login page, if already has been verified
        elif verif.is_expired:
            verif.delete()
            return False

    def post(self, request):
        try:
            token = request.data.get('accessToken')
            fb_res = fbgraph_token_info_vk(token)
            print(fb_res)

            if fb_res:
                try:
                    email = fb_res['email']
                    self.user = User.objects.get(email=email)

                    return self.login()

                except User.DoesNotExist as e:
                    fb_auth_user = {
                        "username": '%s%s%s' % (fb_res.get('first_name').lower(), fb_res.get('last_name').lower(),
                                                fb_res.get('id')[-5:].lower()),
                        "email": fb_res.get('email'),
                        "last_name": fb_res.get('last_name'),
                        "first_name": fb_res.get('first_name'),
                        "role": "IN"
                    }

                    serializer = UserSerializer(data=fb_auth_user)
                    if serializer.is_valid():
                        # save user
                        self.user = serializer.save()

                        fb_insuree = {
                            "user_id": serializer.data['id'],
                            "last_name": fb_res.get('last_name'),
                            "first_name": fb_res.get('first_name'),
                            "email": serializer.data['email']
                        }

                        insuree = InsureeSerializer(data=fb_insuree)
                        if insuree.is_valid():
                            insuree.save()

                            # send email verif for account
                            self.send_email_verification()

                            return self.login()
                        return Response(insuree.errors, status=status.HTTP_400_BAD_REQUEST)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({
                'success': False,
                'message': 'Facebook OAuth Error'
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def generate_verification_token(user):
        token = json.dumps({
            'uid': user.id,
            'email': user.email,
            'token': default_token_generator.make_token(user)
        }).encode('utf-8')
        return base64.urlsafe_b64encode(token)
