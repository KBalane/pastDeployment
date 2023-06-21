import logging
import datetime
import numpy as np
from datetime import datetime, timedelta, time, date

from decimal import Decimal
from digiinsurance.models import InsureePolicy, Transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum, Avg, Count
from rest_framework import viewsets, generics, status
from django.db.models.functions import Extract, TruncMonth, TruncDay, TruncHour

logger = logging.getLogger('api.views')

__all__ = [
    'GetAveragePolicy_month', 
    'GetAveragePolicy_year', 
    'GetAveragePolicy_day',
    'GetAveragePolicy_week'
    ]

class GetAveragePolicy_day(APIView):

    def get(self, request):

        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time())
        today_end = datetime.combine(tomorrow, time())
        today = date.today()
        queryset = Transaction.objects.filter(completed_at__lte = today_end, completed_at__gte=today_start)
        ave_policy_today = queryset.aggregate(Avg('amount'))
        policy_ave_today = queryset.annotate(hour = TruncHour('completed_at')).values('hour').annotate(transaction = Count('id')).aggregate(Avg('amount'))

        todays_hours = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24']
        data = []

        #labels = []
        #ave = []
        
        #for transaction in policy_ave_today:
            #labels.append(transaction['hour'])
            #data.append(transaction['claims'])
            #ave.append(transaction['amount'])

        # labels = []
        
        for hour in todays_hours:
            data.append(queryset.filter(completed_at__hour = hour).aggregate(Avg('amount')))

            
        context = {
            'labels':todays_hours,
            'data':data,
            'ave_policy_today':ave_policy_today
        }
        
        return Response(context, status=status.HTTP_200_OK)
class GetAveragePolicy_week(APIView):
    def get(self, request):

        this_date=datetime.today()
        week_num = str(this_date.isocalendar()[1])
        queryset = Transaction.objects.filter(completed_at__week=week_num)
        ave_in_week=queryset.aggregate(Avg('amount'))

        days_in_week = ['1','2','3','4','5','6','7']
        labels=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
        data = []    

        for day in days_in_week:
            data.append(queryset.filter(completed_at__iso_week_day = day).aggregate(Avg('amount')))
            
        context = {
            'labels':labels,
            'data':data,
            'avg_policy_week':ave_in_week
        }
        
        return Response(context, status=status.HTTP_200_OK)

class GetAveragePolicy_month(APIView):
    def get(self, request):
        this_month = datetime.now().month
        this_year = datetime.now().year
        queryset = Transaction.objects.filter(completed_at__month = this_month)
        ave_policy_month = queryset.aggregate(Avg('amount'))
        ndays = (date(this_year, this_month+1, 1) - date(this_year, this_month, 1)).days
        d1 = date(this_year, this_month, 1)
        d2 = date(this_year, this_month, ndays)
        delta = d2 - d1
        new_data = []
        labels = []
        
        date_range_month = [(d1 + timedelta(days=i)).strftime('%d') for i in range(delta.days + 1)]

        for days_in in date_range_month:
            labels.append(days_in)
            new_data.append(queryset.filter(completed_at__day = days_in).aggregate(Avg('amount')))
        
        context = {
            'labels':labels,
            'data':new_data,
            'ave_policy_month':ave_policy_month
        }

        return Response(context, status=status.HTTP_200_OK)


class GetAveragePolicy_year(APIView):

    def get_amount(self, transaction):
        return int(transaction.amount)
        
    def get(self, request):
        this_year = datetime.now().year
        
        queryset = Transaction.objects.filter(completed_at__year = this_year)
        ave_policy_value = queryset.aggregate(Avg('amount'))
        round_ave = ave_policy_value.get('amount__avg')
        
        
        months = ['1','2','3','4','5','6','7','8','9','10','11','12']
        labels = []
        new_data = []
        for month in months:
            new_data.append(queryset.filter(completed_at__month = month).aggregate(Avg('amount')))
            datetime_object = datetime.strptime(month, "%m")
            month_name= datetime_object.strftime("%b")
            labels.append(month_name)
            # labels.append()

            
        context = {
            'labels':labels,
            'data': new_data,
            'ave_policy_year':round(round_ave, 2)
        }
        
        return Response(context, status=status.HTTP_200_OK)
        
