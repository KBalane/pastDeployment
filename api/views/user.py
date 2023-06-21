import logging
import random
import string

import base64
import json

from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.dispatch import receiver
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Permission
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType

from django.db.models import Q
from django.http import Http404

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import status

from api.serializers.UserSerializer import UserSerializer, UserBankAccountSerializer
from api.serializers.PermissionSerializer import PermissionSerializer
from api.serializers.AccountSerializer import AccountInfoSerializer
from api.serializers.BeneficiarySerializer import (BeneficiaryInfoSerializer, BeneficiarySerializer,
                                                   TempBeneficiarySerializer)
from api.serializers.InsureeSerializer import InsureeSerializer
from api.serializers.HealthQASerializer import HealthQASerializer

from digiinsurance.models.User import User
from digiinsurance.models.Insuree import Insuree
from digiinsurance.models.EmailVerification import EmailVerification
from digiinsurance.models.TempBeneficiaries import TempBeneficiaries
from digiinsurance.models.Beneficiaries import Beneficiaries
from digiinsurance.models.Policy import Policy
from digiinsurance.models.InsureePolicy import InsureePolicy
from digiinsurance.models.HealthQuestions import HealthQuestions
from digiinsurance.models.HealthQuestionsAnswers import HealthQuestionsAnswers
from digiinsurance.models.UserBankAccount import UserBankAccount
from digiinsurance.models.Transaction import Transaction

from django.views.decorators.debug import sensitive_post_parameters
from api.tasks.email import send_verification_email
from api.utils import create_token
from django.http.response import HttpResponseRedirect, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.core.mail import EmailMessage

from rest_framework.authtoken.models import Token

from telco.models import TelcoPersonAddress

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('password'))

logger = logging.getLogger('api.views')

__all__ = ['UserViewSet', 'UploadAccInfo', 'EmailVerificationView',
           'UploadBeneficiaries', 'UploadHealthQA', 'UserBankAccount',
           'TermsAndCondition', 'AdminCreate', 'CreateInsuree', 'ViewHealthQA', 'ViewHealthQAAndHealthQuestion',
           'UploadBeneficiaries2']


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser,)

    def queryset(self):
        if self.request.user.is_admin:
            queryset = User.objects.filter(role=User.ADMIN)
        elif self.request.user.is_company:
            company = self.request.user.company.first()
            queryset = company.users.all()
        else:
            queryset = User.objects.filter(id=self.request.user.id)

        search = self.request.query_params.get('query[generalSearch]')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(username__icontains=search))

        return queryset

    def perform_create(self, serializer, instance):
        password = ''.join(random.choice(
            string.ascii_letters + string.digits) for i in range(8))
        user = serializer.save(step=0, is_verified=True)
        user.set_password(password)

        if self.request.user.is_admin:
            user.role = User.ADMIN
            user.is_superuser = True
            change_message = 'Added user %s as admin' % user.username
        # elif self.request.user.is_school:
        #     user.role = User.STAFF
        #     codenames = self.request.data.getlist('permissions')
        #     permissions = Permission.objects.filter(codename__in=codenames)
        #     user.user_permissions.add(*permissions)
        #     school = self.request.user.schools.first()
        #     school.users.add(user)
        #     change_message = 'Added user %s to school %s' % (
        #         user.username, school.name)

        user.save(update_fields=['role', 'password', 'is_superuser'])
        LogEntry.objects.log_action(
            user_id=self.request.user.id,
            content_type_id=ContentType.objects.get_for_model(user).pk,
            object_id=user.id,
            object_repr=str(user),
            action_flag=ADDITION,
            change_message='Added user %s' % instance.user)

        # send_credentials_email.delay(user.id, password)
        logger.info('Created user %s' % user)

    def perform_update(self, serializer):
        instance = serializer.save()

        LogEntry.objects.log_action(
            user_id=self.request.user.id,
            content_type_id=ContentType.objects.get_for_model(instance).pk,
            object_id=instance.id,
            object_repr=str(instance),
            action_flag=CHANGE,
            change_message='Edited user %s details' % instance.username)

    def perform_destroy(self, instance):
        LogEntry.objects.log_action(
            user_id=self.request.user.id,
            content_type_id=ContentType.objects.get_for_model(instance).pk,
            object_id=instance.id,
            object_repr=str(instance),
            action_flag=DELETION,
            change_message='Deleted user %s' % instance.username)

        instance.delete()

    @action(methods=['get', 'post'], detail=True)
    def permissions(self, request, pk=None):
        staff = self.get_object()
        if request.method == 'GET':
            permissions = Permission.objects.filter(user=staff)
            serializer = PermissionSerializer(permissions, many=True)
        elif request.method == 'POST':
            staff.user_permissions.clear()
            codenames = self.request.data.getlist('permissions')
            permissions = Permission.objects.filter(codename__in=codenames)
            staff.user_permissions.add(*permissions)
            serializer = PermissionSerializer(permissions, many=True)
            LogEntry.objects.log_action(
                user_id=self.request.user.id,
                content_type_id=ContentType.objects.get_for_model(staff).pk,
                object_id=staff.id,
                object_repr=str(staff),
                action_flag=CHANGE,
                change_message='Updated user %s permissions' % staff.username)
        else:
            logger.error('Invalid form request.')
            raise Http404

        return Response(serializer.data)


class UploadAccInfo(CreateAPIView):
    permission_classes = (AllowAny,)

    queryset = User.objects.all()
    serializer_class = AccountInfoSerializer

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super(UploadAccInfo, self).dispatch(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer)
        user_token = create_token(user=user)
        json = serializer.data
        json['insuree_id'] = user.id
        json['token'] = user_token.key

        TelcoPersonAddress.objects.create(
            user=user,
            province=request.data['province'],
            passport_number=request.data['passport_number'],
        )

        headers = self.get_success_headers(serializer.data)
        return Response(json,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        insuree = serializer.save()
        insuree.user.role = 'IN'
        insuree.user.save(update_fields=['role'])

        # try:
        #     insuree = Insuree.objects.get(email=insuree.user.email)
        #     insuree.user = insuree
        #     insuree.save()
        # except Insuree.DoesNotExist:
        #     Insuree.objects.create(user=user, email=insuree.user.email)
        # except MultipleObjectsReturned:
        #     insuree = Insuree.objects.filter(email=insuree.user.email).first()
        #     # insuree.user = user
        #     insuree.save()

        # if not self.request.data.get('is_mobile'):
        #     login(self.request, user)

        LogEntry.objects.log_action(
            user_id=insuree.user.id,
            content_type_id=ContentType.objects.get_for_model(insuree.user).pk,
            object_id=insuree.user.id,
            object_repr=str(insuree.user),
            action_flag=4,
            change_message='Successful login')

        token = self.generate_verification_token(insuree.user)
        verif, created = EmailVerification.objects.get_or_create(
            user=insuree.user,
            type=EmailVerification.VERIFICATION,
            token=token,
            email=insuree.user.email)

        # signup_url = settings.WEB_APP_URL
        # referer = self.request.META.get('HTTP_REFERER')
        # if referer and referer != signup_url:
        #     parsed_uri = urlparse(referer)
        #     redirect = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        # else:
        # redirect = None

        if created:
            send_verification_email(insuree.user.id, token)

        elif verif.is_expired:
            verif.delete()
            return False

        return insuree.user

    @staticmethod
    def generate_verification_token(user):
        token = json.dumps({
            'uid': user.pk,
            'email': user.email,
            'token': default_token_generator.make_token(user)
        }).encode('utf-8')
        return base64.urlsafe_b64encode(token)


class EmailVerificationView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, token):
        user = self.verify_token(request, token)
        if not user.is_verified:
            user.is_verified = True
            user.save(update_fields=['is_verified'])
            if hasattr(user, 'email_verification'):
                user.email_verification.is_archived = True
                user.email_verification.save(update_fields=['is_archived'])

            user_token = create_token(user=user)
            login(request, user)
            message = "Email successfully verified"
            return Response("Email successfully verified")
        # return redirect('https://digiinsurance-yhrbl.ondigitalocean.app/login')
        return Response("Email successfully verified")
        # send_welcome_email.delay(user.id, request.GET.get('redirect'))
        # messages.success(
        #     request, 'Email successfully verified.')

        # if user.company:
        #     return redirect('dashboard:get_started')
        # if user.is_insuree:
        #     if 'redirect' in request.GET:
        #         url = request.GET['redirect']
        #         if user.info_submitted and user.step == 0 and user.user_id:
        #             # return redirect(
        #             #     '%saccounts/?verified=1' % url)
        #             return JsonResponse("goto accounts verified", safe=False)
        #         # return redirect(
        #         #     '%sinsuree/profile/?verified=1' % url)
        #         return JsonResponse("goto insuree profile verified", safe=False)
        #     # return redirect('dashboard:insuree_get_started')
        #     return JsonResponse("goto insuree get started", safe=False)

    @staticmethod
    def verify_token(request, token):

        # strobject = token[1 : : ]
        # json_data = base64.urlsafe_b64decode(strobject)
        # data = json.loads(json_data)

        # uid = data.get('uid', None)
        # token = data.get('token', None)
        # email = data.get('email', None)

        data = Token.objects.get(key=token)

        uid = data.user.id
        token = data.key
        email = data.user.email

        try:
            user = User.objects.get(id=uid)
        except User.DoesNotExist:
            error_message = "User does not exist."
            return Response(error_message, status=status.HTTP_400_BAD_REQUEST)

        if user and user.is_verified:
            messages.error(request, 'This email is already verified. Please continue login.')

        elif not default_token_generator.check_token(user, token):
            msg = "%s %s" % (
                ("This verification link has already expired or associated user does not exist."),
                ("Please generate a new link by clicking the resend button")
            )
            messages.warning(request, msg)

        return user


class UploadBeneficiaries(CreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Beneficiaries.objects.all()
    serializer_class = BeneficiaryInfoSerializer


class UploadBeneficiaries2(CreateAPIView):
    """
    To Make A Request, use PUT.
    To Approve a Pending Request, use POST. pass the id.
    
    To Delete a Pending Request, use the link below and pass the id:
    admin/pending_beneficiary/add/{id}/
    then click delete 

    Sample PUT REQUEST:
    {
    "user_policy_id": 386,
    "first_name": "Pia",
    "middle_name": "Wurtsbach",
    "last_name": "Almazan",
    "birthday": "1998-04-05",
    "birthplace": "PH",
    "country": "PH",
    "nationality": "Fil",
    "beneficiary_address": "124 khbckahiu",
    "relationship": "Wife",
    "percentage_of_share": 69,
    "beneficiary_status": "Pending",
    "request_type": "Add",
    "reason": "Adding new wife to master"
    }
    """
    permission_classes = (IsAuthenticated,)
    queryset = Beneficiaries.objects.all()
    serializer_class = BeneficiaryInfoSerializer

    # get all pending bene for add
    def get(self, request, *args, **kwargs):
        queryset = TempBeneficiaries.objects.all().filter(Q(beneficiary_status='PENDING') & Q(request='Add')).order_by(
            '-created_at')
        serializer_class = TempBeneficiarySerializer(queryset, many=True)

        queryset2 = Beneficiaries.objects.all().order_by('-id')
        serializer_class2 = BeneficiarySerializer(queryset2, many=True)

        context = {
            "pending_beneficiaries": serializer_class.data,
            "approved_beneficiaries": serializer_class2.data,
        }
        return Response(context)

    # make pending request
    def put(self, request, *args, **kwargs):

        # 136 account number
        user_policy_inst = InsureePolicy.objects.get(id=request.data.get('user_policy_id'))
        # user_policy_inst = InsureePolicy.objects.filter(insuree_id=request.data.get('user_policy_id')).order_by('-id')
        # [0]

        tempData = TempBeneficiaries.objects.create(
            beneficiary=request.data.get('user_policy_id'),
            birthplace=request.data.get('birthplace'),
            country=request.data.get('country'),
            birthday=request.data.get('birthday'),
            nationality=request.data.get('nationality'),
            beneficiary_address=request.data.get('beneficiary_address'),
            reason=request.data.get('reason'),
            request='Add',

            user_policy=user_policy_inst,
            first_name=request.data.get('first_name'),
            middle_name=request.data.get('middle_name'),
            last_name=request.data.get('last_name'),
            relationship=request.data.get('relationship'),
            beneficiary_status='PENDING',
            percentage_of_share=request.data.get('percentage_of_share'),
        )
        tempData.save()

        queryset = TempBeneficiaries.objects.all().filter(beneficiary=request.data.get('user_policy_id'))
        serializer_class = TempBeneficiarySerializer(queryset, many=True)
        return Response(serializer_class.data)

    # approve pending add request
    def post(self, request, *args, **kwargs):
        # move data from temp to main
        id = request.data.get('id')
        try:
            birthplace = TempBeneficiaries.objects.values_list('birthplace').filter(beneficiary=id)
            country = TempBeneficiaries.objects.values_list('country').filter(beneficiary=id)
            birthday = TempBeneficiaries.objects.values_list('birthday').filter(beneficiary=id)
            nationality = TempBeneficiaries.objects.values_list('nationality').filter(beneficiary=id)
            beneficiary_address = TempBeneficiaries.objects.values_list('beneficiary_address').filter(beneficiary=id)

            user_policy = TempBeneficiaries.objects.values_list('user_policy_id').filter(beneficiary=id)
            first_name = TempBeneficiaries.objects.values_list('first_name').filter(beneficiary=id)
            middle_name = TempBeneficiaries.objects.values_list('middle_name').filter(beneficiary=id)
            last_name = TempBeneficiaries.objects.values_list('last_name').filter(beneficiary=id)
            relationship = TempBeneficiaries.objects.values_list('relationship').filter(beneficiary=id)
            percentage_of_share = TempBeneficiaries.objects.values_list('percentage_of_share').filter(beneficiary=id)
            user_policy_inst = InsureePolicy.objects.get(id=user_policy[0][0])
        except Exception as e:
            return Response(e)

        beneficiary = Beneficiaries.objects.create(
            user_policy=user_policy_inst,
            first_name=first_name[0][0],
            middle_name=middle_name[0][0],
            last_name=last_name[0][0],
            relationship=relationship[0][0],
            birthday=birthday[0][0],
            birthplace=birthplace[0][0],
            nationality=nationality[0][0],
            country=country[0][0],
            beneficiary_address=beneficiary_address[0][0],
            beneficiary_status='APPROVED',
            request_type='Add',
            percentage_of_share=percentage_of_share[0][0],
        )
        beneficiary.save()

        ifexists = TempBeneficiaries.objects.filter(beneficiary=id)
        ifexists.delete()

        return Response("Beneficiary Approved")

    # deny pending request
    def delete(self, request, id, *args, **kwargs):
        users = Beneficiaries.objects.all().values('id'
                                                   ).filter(id=id).update(
            beneficiary_status='DENIED',
            request_type='Add',
        )

        ifexists = TempBeneficiaries.objects.filter(beneficiary=id)
        ifexists.delete()

        return Response("Beneficiary Denied")


class UploadHealthQA(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = HealthQuestionsAnswers.objects.all()
    serializer_class = HealthQASerializer

    def post(self, request, *args, **kwargs):
        serializer = HealthQASerializer(data=request.data)
        # healthQuestionSerializer = HealthQASerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

        user_answer = request.data.get('answer')
        entry_id = request.data.get('id')
        question_id = request.data.get('question_id')
        correct_answer = HealthQuestions.objects.all().values_list('correct_answer', flat=True).filter(id=question_id)
        last_entry = HealthQuestionsAnswers.objects.all().values_list('id', flat=True).last()

        if user_answer == correct_answer[0]:
            HealthQuestionsAnswers.objects.filter(id=last_entry).update(answer_status='Pass')
        elif user_answer != correct_answer[0]:
            HealthQuestionsAnswers.objects.filter(id=last_entry).update(answer_status='Fail')

        queryset = HealthQuestionsAnswers.objects.all().filter(id=last_entry)
        serializer = HealthQASerializer(queryset, many=True)
        return Response(serializer.data)

        # print(correct_answer)


class ViewHealthQA(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, insureePolicy):
        queryset = HealthQuestionsAnswers.objects.all().values(
            'id',
            'insureePolicy',
            'insureePolicy__insuree__first_name',
            'insureePolicy__insuree__last_name',
            'question',
            'question__question_type',
            'question__question',
            'answer',
            'answer_status'
        ).filter(insureePolicy=insureePolicy)

        # serializer = HealthQASerializer(queryset,many=True)
        return Response(queryset)


class ViewHealthQAAndHealthQuestion(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, insureePolicy):
        user = InsureePolicy.objects.all().values(
            'id',
            'insuree__first_name',
            'insuree__last_name'
        ).filter(id=insureePolicy)

        if len(user) <= 0:
            raise Http404

        queryset = HealthQuestionsAnswers.objects.all().values(
            'id',
            'insureePolicy',
            'question',
            'question__question_type',
            'question__question',
            'question__correct_answer',
            'answer',
            'answer_status'
        ).filter(insureePolicy=insureePolicy)

        no_of_passed = self.count(queryset, 'Pass')
        no_of_failed = self.count(queryset, 'Fail')
        no_of_na = self.count(queryset, 'Not Answered')

        data = {
            "user": user[0],
            "num_of_questions": len(queryset),
            "num_of_pass": no_of_passed,
            "num_of_fail": no_of_failed,
            "num_of_not_answered": no_of_na,
            "questions": queryset,
        }
        return Response(data)

    def count(self, data, status):
        return len([(i) for i in data if i['answer_status'] == status])


class UserBankAccount(CreateAPIView):
    queryset = UserBankAccount.objects.all()
    serializer_class = UserBankAccountSerializer


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    # to cover more complex cases:
    # http://stackoverflow.com/questions/4581789/how-do-i-get-user-ip-address-in-django
    ip = request.META.get('REMOTE_ADDR')

    logger.debug('login user: {user} via ip: {ip}'.format(
        user=user,
        ip=ip
    ))


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')

    logger.debug('logout user: {user} via ip: {ip}'.format(
        user=user,
        ip=ip
    ))


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    logger.warning('login failed for: {credentials}'.format(
        credentials=credentials,
    ))


# HTML Template to JSON Object Converter
class TermsAndCondition(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        content = render_to_string("terms_and_condition.html")
        content1 = {"terms_template": content}
        return JsonResponse(content1, safe=False)


class AdminCreate(APIView):
    def get(self, request):
        users = User.objects.all().order_by('-id')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        userData = request.data  # JSONParser().parse(request)
        serializer = UserSerializer(data=userData)
        if serializer.is_valid():
            serializer.save()
            context = {
                "new_admin": serializer.data,
                "id": serializer.data['id'],
                "username": request.data["username"],
                "role": request.data["role"],
                "email": request.data["email"],
                "first_name": request.data["first_name"],
                "middle_name": request.data["middle_name"],
                "last_name": request.data["last_name"],
                "mobile_number": request.data["mobile_number"],
            }
            query = User.objects.all().values(
                'username'
            ).filter(
                username=request.data["username"]
            ).update(is_staff=True, is_superuser=True)
            '''
            #this is where you send the activation email
            new_admin = serializer.data
            user = User.objects.get(email=new_admin['email'])
            token = RefreshToken.for_user(userData).access_token
            #send_verification_email(new_admin['id'],token)
            send_verification_email.delay(new_admin['id'], token)
            current_site = get_current_site(request).domain
            relativeLink = reverse('admin-verify')
            absurl = 'http://'+ current_site + relativeLink + "?token="+ str(token)
            email_body = 'Hi ' + user.username+ 'Use link below to verifhy \n' + absurl
            data = {'email_body':email_body,'to_email':user.email,'email_subject':'Verify your email '}
            send_email(data)
            '''
            return Response(context, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@staticmethod
def send_email(data):
    email = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body']
    ),
    email.send()


class CreateInsuree(CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Insuree.objects.all()
    serializer_class = InsureeSerializer


'''
{
    "username":"salamanca",
    "role":"AD",
    "email":"salamanca@gmail.com",
    "first_name":"Hector",
    "middle_name":"Saul",
    "last_name":"Man",
    "mobile_number":"09174523654"
}
'''
