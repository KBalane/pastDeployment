import base64
import json
from django.contrib.auth.tokens import default_token_generator
from api.tasks.email import digi_send_email_verification
from cocolife.models import AppStat
from rest_framework.views import APIView
from cocolife.models import DigiInsuree as CIModel
from cocolife.models import ProductInsuree
from cocolife.models.Product import Benefit
from cocolife.serializers.ProductInsureeSerializer import ProductInsureeSerializer

from rest_framework.generics import ListAPIView, ListCreateAPIView

from digiinsurance.models import User
from rest_framework.views import APIView
from cocolife.models import DigiInsuree as CIModel
from cocolife.serializers.DigiInsureeSerializer import DigiUserSerializer, DigiInsureeSerializer

from rest_framework.generics import ListCreateAPIView, CreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView

from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect

__all__ = ['CocoInsuree', 'CocoInsureePolicies', 'CocoInsureeStats', 'AppDownloadCount',
           'AuthRegister', 'EmailVerificationHandler', 'VerifyEmail', 'CocoInsureeById']


class AuthRegister(CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = DigiUserSerializer


class EmailVerificationHandler(GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, email):
        user = get_object_or_404(User, email=email)

        if user.is_verified:  # TODO mobile_verified fields to user model
            return Response("This email is already verified", status=200)

        token = self.generate_verification_token(user=user)

        digi_send_email_verification(email, token)

        return Response('Verification Email Sent')

    @staticmethod
    def generate_verification_token(user):
        token = json.dumps({
            'uid': user.pk,
            'email': user.email,
            'token': default_token_generator.make_token(user)
        }).encode('utf-8')
        return base64.urlsafe_b64encode(token)


class VerifyEmail(GenericAPIView):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()

    def get(self, request, token):
        response, status = self.verify_token(request, token)
        if status != 200:
            return Response(response, status=status)
        return redirect('https://digiinsurance-yhrbl.ondigitalocean.app/confirmed-email')

    @staticmethod
    def verify_token(request, token):

        try:
            strobject = token[1::]
            json_data = base64.urlsafe_b64decode(strobject)
            data = json.loads(json_data)
            uid = data.get('uid', None)
            token = data.get('token', None)
        except:
            return ("Invalid Token", 400)

        user = get_object_or_404(User, id=uid)

        if user and user.is_verified:
            return ("This email is already verified", 200)

        # update verification flags
        user.is_verified = True
        user.save()

        return ("Email succesfully Verified", 200)


class CocoInsuree(ListCreateAPIView):
    # TODO - Make Authenticated
    permission_classes = (AllowAny,)
    queryset = CIModel.objects.all()
    serializer_class = DigiInsureeSerializer


class CocoInsureeById(RetrieveUpdateDestroyAPIView):
    permission_classes = (AllowAny,)
    lookup_field = 'user_id'
    queryset = CIModel.objects.all()
    serializer_class = DigiInsureeSerializer


class CocoInsureePolicies(ListAPIView):
    permission_classes = (AllowAny,)
    queryset = ProductInsuree.objects.all()
    serializer_class = ProductInsureeSerializer

    def get(self, request, id):
        query = ProductInsuree.objects.all().filter(
            billed_to=id).values('id', 'product__name', 'payment_term', 'variant_id', 'product__category',
                                 'premium_amount_due', 'premium_due_date', 'status')
        benefit_arr = []
        for query in query:
            benefit_qs = Benefit.objects.filter(
                variant=query['variant_id']).values('name', 'face_amount')
            query["benefits"] = benefit_qs
            benefit_arr.append(query)

        return Response(benefit_arr)


class CocoInsureeStats(APIView):
    def get(self, request):
        by_city = CIModel.objects.all().values(
            'home_city'
        ).annotate(registered_users=Count('home_city')).order_by('home_city')

        # continue for count per month, day, week

        # per_month
        per_month = CIModel.objects.all().values(
            'created_at__month'
        ).annotate(registered_users=Count('created_at__month')).order_by()

        # per_year
        per_year = CIModel.objects.all().values(
            'created_at__year'
        ).annotate(registered_users=Count('created_at__year')).order_by()

        res = {
            "by_city": by_city,
            "per_month": per_month,
            "per_year": per_year,
        }

        return Response(res)


######################################################################
####################### APP DOWNLOADS COUNT  #########################
########### RUN A CERTAIN ENDPOINT ONLY ON FIRST TIME APP OPEN #######
# IF FIRST TIME TO OPEN APP
# RUN ENDPOINT FOR APP DOWNLOADS
# ELSE
# DO NOTHING
######################################################################


class AppDownloadCount(APIView):
    def get(self, request):
        appstat = AppStat.objects.get(id=1)
        count = appstat.get_count()
        return Response(count)

    def post(self, request):
        appstat = AppStat.objects.get(id=1)
        count = appstat.get_count() + 1
        update = AppStat.objects.all().values(
            'download').filter(id=1).update(download=count)
        return Response(count)
