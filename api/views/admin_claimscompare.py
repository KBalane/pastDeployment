import logging
import numpy as np
from datetime import datetime, timedelta, time, date

from django.db.models.expressions import F
from django.db.models.functions.datetime import ExtractDay, ExtractMonth
from digiinsurance.models import Claims, Claims

from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.db.models import Count
from django.db.models import Count, DateTimeField
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay, TruncHour, ExtractHour

logger = logging.getLogger('api.views')
__all__ = [
    'GetClaimsCompare_year',
    'GetClaimsCompare_month',
    'GetClaimsCompare_week',
    'GetClaimsCompare_day'
]

class GetClaimsCompare_year(APIView):
    def get_claims_type(self, claim_per_month):
        return claim_per_month.claim_status
    
    def get_count(self, labels, claims_this_month, claim_status):
        res = {}
        for i, date in enumerate(labels):
            res[i] = next((item['count'] for item in claims_this_month if item['month'] == i+1 and item['claim_status'] == claim_status), 0)
        return res.values()

    def get(self, request):
        today = datetime.now()
        claims_data = Claims.objects.filter(modified_at__year =today.year)
        months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

        claims_per_month = claims_data.annotate(month = ExtractMonth('modified_at')).values('month').annotate(claim_status=F('claim_status')).annotate(count=Count('id'))

        types = list(set(map(self.get_claims_type, claims_data)))
        labels = [] 
        claims = {}

        for item in months:
            labels.append(item)

        for claim_status in types:
            claims[claim_status] = self.get_count(labels, claims_per_month, claim_status)

        context = {
            'labels': labels,
            'claims': claims,
        }
        
        return Response(context)

class GetClaimsCompare_month(APIView):
    def get_claims_type(self, claims_data):
        return claims_data.claim_status

    def days_cur_month(self, month):
        m = month
        y = datetime.now().year
        ndays = (date(y, m+1, 1) - date(y, m, 1)).days
        d1 = date(y, m, 1)
        d2 = date(y, m, ndays)
        delta = d2 - d1

        return [(d1 + timedelta(days=i)).strftime('%d') for i in range(delta.days + 1)]
    
    def get_count(self, labels, claims_this_month, claim_status):
        res = {}
        for i, date in enumerate(labels):
            res[i] = next((item['count'] for item in claims_this_month if item['day'] == int(date) and item['claim_status'] == claim_status), 0)
        return res.values()

    def get(self, request):
        today = datetime.now()
        claims_data = Claims.objects.filter(modified_at__month = today.month, modified_at__year = today.year)

        dates = self.days_cur_month(today.month)

        claims_this_month = claims_data.annotate(day = ExtractDay('modified_at')).values('day').annotate(claim_status=F('claim_status')).annotate(count=Count('id'))
        
        types = list(set(map(self.get_claims_type, claims_data)))

        labels = []
        claims = {} 

        for i, date in enumerate(dates):
            labels.append(date)

        for claim_status in types:
            claims[claim_status] = self.get_count(labels, claims_this_month, claim_status)
        
        context = {
            'labels': labels,
            'claims': claims,
        }

        return Response(context)


class GetClaimsCompare_week(APIView):
    def get_claims_type(self, claims_per_day):
        return claims_per_day.claim_status

    def get_count(self, labels, claims_today, claim_status):
        res = {}
        for i, key in enumerate(labels):
            res[i] = next((item['count'] for item in claims_today if item['day'] == int(key) and item['claim_status'] == claim_status), 0)
        return res.values()
    
    def get(self, request):
        today = datetime.now()
        current_week_days = [today + timedelta(days=i) for i in range(0 - today.weekday(), 7 - today.weekday())]
        day_names = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
        
        claims_data = Claims.objects.filter(modified_at__gte=current_week_days[0], modified_at__lte=current_week_days[-1])

        claims_this_week = claims_data.annotate(day = ExtractDay('modified_at')).values('day').annotate(claim_status=F('claim_status')).annotate(count=Count('id'))

        types = list(set(map(self.get_claims_type, claims_data)))

        labels = []
        labels_dict = {}
        claims = {}

        for index, day in enumerate(current_week_days):
            labels.append(day_names[index])
            labels_dict[current_week_days[index].strftime("%d")] = day_names[index]

        for claim_status in types:
            claims[claim_status] = self.get_count(labels_dict, claims_this_week, claim_status)

        context = {
            'labels': labels,
            'claims': claims,
        }

        return Response(context)
class GetClaimsCompare_day(APIView):
    def get_claims_type(self, claims_per_hour):
        return claims_per_hour.claim_status

    def get_count(self, claims_today, claim_status):
        res = {}
        for i in range(0,24):
            res[i] = next((item['count'] for item in claims_today if item['hour'] == i and item['claim_status'] == claim_status), 0)
        return res.values()

    def get(self, request):
        today = datetime.now()
        claims_data = Claims.objects.filter(Q(modified_at__month = today.month) & Q(modified_at__day = today.day))

        claims_today = claims_data.annotate(hour = ExtractHour('modified_at')).values('hour').annotate(claim_status=F('claim_status')).annotate(count=Count('id'))
        
        claims= {}
        labels = []
        types = list(set(map(self.get_claims_type, claims_data)))
        
        for i in range(0,24):
            labels.append(i)

        for claim_status in types:
            claims[claim_status] = self.get_count(claims_today, claim_status)

        context = {
            'labels': labels,
            'claims': claims
        }

        return Response(context)


