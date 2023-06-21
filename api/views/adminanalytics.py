import logging
from datetime import datetime, timedelta, time, date

from decimal import Decimal
from digiinsurance.models import InsureePolicy, Transaction, User, Insuree
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Avg, Count
from django.db.models.functions import Extract, TruncMonth, TruncDay, TruncYear
from rest_framework import viewsets, generics, status

logger = logging.getLogger('api.views')

__all__ = [
    'GetPaidPolicyPercentage',
    'GetClientCount_year',
    'GetClientCount_month',
    'GetClientCount_week',
    'GetClientCount_day'
    ]

class GetPaidPolicyPercentage(APIView):
    def get(self, request):
        this_month =datetime.now().month
        paid_for_the_month = Transaction.objects.filter(completed_at__month=this_month).count()
        insuree_policy = InsureePolicy.objects.all().count()

        ave_paid_user = (paid_for_the_month / insuree_policy) * 100

        context = {
            'paid_for_this_month':paid_for_the_month,
            'total_insuree_policy':insuree_policy,
            'ave_of_paid_user':round(ave_paid_user, 0)
        }

        return Response(context, status=status.HTTP_200_OK)

class GetClientCount_year(APIView):
    def get(self, request):
        today = datetime.now()
        insuree_year = Insuree.objects.filter(created_at__year=today.year)
        insuree_total = insuree_year.count()

        clients_count =[]
        labels = ['1','2','3','4','5','6','7','8','9','10','11','12']
        string_month = []

        for label in labels:
            clients_count.append(insuree_year.filter(created_at__month = label).aggregate(Count('user_id')))
            datetime_object = datetime.strptime(label, "%m")
            month_name= datetime_object.strftime("%b")
            string_month.append(month_name)

        context = {
            'labels':string_month,
            'clients_count':clients_count,
            'insuree_total':insuree_total
        }
        return Response(context, status=status.HTTP_200_OK)

class GetClientCount_month(APIView):
    def get(self, request):
        this_month = datetime.now().month
        this_year = datetime.now().year
        insuree_month = Insuree.objects.filter(created_at__month = this_month)
        insuree_total = insuree_month.count()

        ndays = (date(this_year, this_month+1, 1) - date(this_year, this_month, 1)).days
        d1 = date(this_year, this_month, 1)
        d2 = date(this_year, this_month, ndays)
        delta = d2 - d1
        date_range_month = [(d1 + timedelta(days=i)).strftime('%d') for i in range(delta.days + 1)]

        insuree_count_month = []
        labels = []

        for days_in in date_range_month:
            labels.append(days_in)
            insuree_count_month.append(insuree_month.filter(created_at__day = days_in).aggregate(Count('user_id')))

        context = {
            'labels':labels,
            'insuree_count_month':insuree_count_month,
            'insuree_month_total':insuree_total
        }

        return Response(context, status=status.HTTP_200_OK)


class GetClientCount_week(APIView):
    def get(self, request):
        this_date=datetime.today()
        week_num = str(this_date.isocalendar()[1])
        queryset = Insuree.objects.filter(created_at__week=week_num)
        insuree_week_total = queryset.count()

        days_in_week = ['1','2','3','4','5','6','7']
        labels=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        data = []    

        for day in days_in_week:
            data.append(queryset.filter(created_at__iso_week_day = day).aggregate(Count('user_id')))
            
        context = {
            'labels':labels,
            'data':data,
            'insuree_week_total':insuree_week_total
        }
        
        return Response(context, status=status.HTTP_200_OK)

class GetClientCount_day(APIView):
   def get(self, request):

        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time())
        today_end = datetime.combine(tomorrow, time())
        today = date.today()
        queryset = Insuree.objects.filter(created_at__lte = today_end, created_at__gte=today_start)
        insuree_day_total = queryset.count()

        todays_hours = [
            '1','2','3','4','5',
            '6','7','8','9','10',
            '11','12','13','14','15',
            '16','17','18','19','20',
            '21','22','23','24'
            ]
        data = []
        
        for hour in todays_hours:
            data.append(queryset.filter(created_at__hour = hour).aggregate(Count('user_id')))
            
        context = {
            'labels':todays_hours,
            'data':data,
            'insuree_day_total':insuree_day_total
        }

        return Response(context, status=status.HTTP_200_OK)