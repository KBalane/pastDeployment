from django.db.models import Count
from django.db.models.functions.datetime import ExtractDay, ExtractMonth, ExtractHour

from cocolife.models.DepartmentEmail import DepartmentEmail
from cocolife.models.Inquiry import Inquiry
from cocolife.serializers import InquirySerializer
from digiinsurance.models import User

from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from api.tasks.email import digi_send_inquiry

import json
from datetime import datetime, time, timedelta

__all__ = [
    'InquiryView', 'InquiriesByYear', 'InquiriesByPastDays', 'InquiriesByWeek', 'InquiriesByMonth', 'InquiriesByDay',
    'InquiriesByDateRange', 'InquiryTypePercentage', 'SendMessage', 'CountInquiry']


def get_inquiry_list():
    inquiry_list = [
        "BANCASSURANCE",
        "CLAIMS",
        "DEPED_LOANS",
        "EMPLOYMENT",
        "GROUP_INSURANCE",
        "HEALTHCARE",
        "INDIVIDUAL",
        "INVESTMENTS",
        "MALL_CLIENTS",
        "MIGRANTS",
        "POLICY",
        "MOBILE_APP_CONCERNS",
        "OTHER"
    ]
    return inquiry_list


class InquiryView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        to_email = self.get_department_email(serializer.data['inquiry_type'])
        user = User.objects.get(id=serializer.data['user'])

        data = {
            "subject": serializer.data['subject'],
            "inq_type": serializer.data['inquiry_type'],
            "content": serializer.data['concern'],
            "attachment": serializer.data['attachment'],
            "policy": serializer.data['policy_number'],
            "user": user,
            "to_email": to_email
        }

        digi_send_inquiry(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def get_department_email(key):
        email_list = {
            "BANCASSURANCE": ["bancasurrance@cocolife.com"],
            "CLAIMS": ["customer_service@cocolife.com"],
            "DEPED_LOANS": ["customer_service@cocolife.com"],
            "EMPLOYMENT": ["employee_selection@cocolife.com"],
            "GROUP_INSURANCE": ["groupmarketing@cocolife.com", "karla_delacruz@cocolife.com"],
            "HEALTHCARE": ["healthcare@cocolife.com"],
            "INDIVIDUAL": ["customer_service@cocolife.com"],
            "INVESTMENTS": ["customer_service@cocolife.com"],
            "MALL_CLIENTS": ["customer_service@cocolife.com"],
            "MIGRANTS": ["migrant_workers@cocolife.com"],
            "POLICY": ["customer_service@cocolife.com"],
            "MOBILE_APP_CONCERNS": ["rybelbes@cocolife.com"],
            "OTHER": ["customer_service@cocolife.com"],
            "TEST": ["vanjo.mampusti0324@gmail.com", "vanjo.mampusti0324@gmail.com"]
        }
        return email_list[key]


"""
@route      GET metrics/inquiry/filterByDate/year/
@desc       GET Filtered Data by year/last year
@access     Private
"""


class InquiriesByYear(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InquirySerializer

    def get(self, request):
        this_year = datetime.now().year
        q_year = request.query_params.get('q_year', this_year)
        last_year = q_year

        if q_year == 'last_year':
            last_year = datetime.now().year - 1

        query = Inquiry.objects.filter(created_at__year=last_year).annotate(month=ExtractMonth('created_at')).values('month')

        inquiry_list = get_inquiry_list()

        months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
                  'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

        counter = {}
        label_data = {}
        context = {}
        label_data['year'] = last_year

        for i in range(len(inquiry_list)):
            counter["%s_counter" % inquiry_list[i]] = query.filter(inquiry_type=inquiry_list[i]).count

        for i in range(len(inquiry_list)):
            label_data[inquiry_list[i]] = {}

        for i in range(len(inquiry_list)):
            label_data[inquiry_list[i]] = counter["%s_counter" % inquiry_list[i]]

        context = json.dumps(label_data)
        context = json.loads(context)

        return Response(label_data, status=status.HTTP_200_OK)


class InquiriesByPastDays(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InquirySerializer

    def get(self, request):
        num_of_days = request.query_params.get('q_days', 0)
        date = datetime.now() - timedelta(days=int(num_of_days))

        queryset = Inquiry.objects.filter(created_at__range=[date, datetime.now()]).values().annotate(
            day=ExtractDay('created_at')).values('day')
        inquiry_list = get_inquiry_list()
        date_list = [datetime.today() - timedelta(days=x) for x in range(int(num_of_days))]

        counter = {}
        label_data = {}
        context = {}
        label_data['past_num_days'] = num_of_days

        # Counts the Query
        for i in range(len(inquiry_list)):
            counter["%s_counter" % inquiry_list[i]] = queryset.filter(inquiry_type=inquiry_list[i]).count()

        # Container for the data
        for i in range(len(inquiry_list)):
            label_data[inquiry_list[i]] = {}

        for i in range(len(inquiry_list)):
            label_data[inquiry_list[i]] = counter["%s_counter" % inquiry_list[i]]

        # Testing purposes
        # print(counter)
        # print(label_data)

        context = json.dumps(label_data)
        context = json.loads(context)

        return Response(label_data, status=status.HTTP_200_OK)


class InquiriesByWeek(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InquirySerializer

    def get(self, request):
        today = datetime.now()
        q_week = request.query_params.get('q_week', today)
        current_week_number = today.isocalendar()[1]
        day_names = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']

        if q_week == 'last_week':
            today = today - timedelta(weeks=1)
            current_wee_number = today.isocalendar()[1]

            current_week_days = [
                today + timedelta(days=i) for i in range(-1 - today.weekday(), 6 - today.weekday())
            ]

            query = Inquiry.objects.all().filter(created_at__range=[
                current_week_days[0].date(), current_week_days[-1].date()
            ])
            inquiry_list = get_inquiry_list()

            counter = {}
            label_data = {}
            context = {}
            label_data['week_number'] = current_week_number

            for i in range(len(inquiry_list)):
                counter["%s_counter" % inquiry_list[i]] = query.filter(inquiry_type=inquiry_list[i]).count()

            for i in range(len(inquiry_list)):
                label_data[inquiry_list[i]] = {}

            for i in range(len(inquiry_list)):
                label_data[inquiry_list[i]] = counter["%s_counter" % inquiry_list[i]]

            context = json.dumps(label_data)
            context = json.loads(context)

            return Response(label_data, status=status.HTTP_200_OK)


class InquiriesByMonth(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InquirySerializer

    def get(self, request):
        last_month = request.query_params.get('last_month', False)
        this_month = datetime.now().month

        if last_month:
            this_month = this_month - 1

        queryset = Inquiry.objects.all().values().filter(created_at__month=this_month)
        inquiry_list = get_inquiry_list()

        counter = {}
        label_data = {}
        context = {}
        label_data['month_number'] = this_month

        for i in range(len(inquiry_list)):
            counter['%s_counter' % inquiry_list[i]] = queryset.filter(inquiry_type=inquiry_list[i]).count()

        for i in range(len(inquiry_list)):
            label_data[inquiry_list[i]] = {}

        for i in range(len(inquiry_list)):
            label_data[inquiry_list[i]] = counter['%s_counter' % inquiry_list[i]]

        context = json.dumps(label_data)
        context = json.loads(context)

        return Response(label_data, status=status.HTTP_200_OK)


class InquiriesByDay(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    """
    Query Params will determine if the data to be collected is today or yesterday
    Determines when data is created sorted by hour
    Returns json
    """

    def get(self, request):
        today = datetime.now()
        data_filter = request.query_params.get('date_filter', today)

        if data_filter == "yesterday":
            today = today - timedelta(1)

        today_start = today.replace(hour=0, minute=0, second=0)
        today_end = today.replace(hour=23, minute=59, second=59)

        query = Inquiry.objects.all().values().filter(created_at__range=[today_start, today_end])
        inquiry_list = get_inquiry_list()

        counter = {}
        label_data = {}
        context = {}
        label_data['day'] = today.strftime("%B %d, %Y %H:%M:%S")

        for i in range(len(inquiry_list)):
            counter["%s_counter" % inquiry_list[i]] = query.filter(inquiry_type=inquiry_list[i]).count()

        # print(query)
        # print(today)

        # Container for the data
        for i in range(len(inquiry_list)):
            label_data[inquiry_list[i]] = {}

        for i in range(len(inquiry_list)):
            label_data[inquiry_list[i]] = counter["%s_counter" % inquiry_list[i]]

        # Testing purposes
        # print(counter)
        # print(label_data)

        context = json.dumps(label_data)
        context = json.loads(context)

        return Response(label_data, status=status.HTTP_200_OK)


"""
@route      GET metrics/inquiry/filterByDate/custom/
@desc       GET Filtered Data by Date Range
@access     Private
"""


class InquiriesByDateRange(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    """
    Query Params will determine if the data to be collected is in specified date range
    Determines when data is created sorted by data count
    Returns json
    """

    def get(self, request):
        start = request.query_params.get('start_date', None)
        end = request.query_params.get('end_date', None)
        inquiry_list = get_inquiry_list()

        query = Inquiry.objects.all().values().filter(created_at__range=[start, end])

        counter = {}
        label_data = {}
        context = {}
        label_data['dates'] = start + " to " + end
        for i in range(len(inquiry_list)):
            counter["%s_counter" % inquiry_list[i]] = query.filter(inquiry_type=inquiry_list[i]).count()

        # print(query)
        # print(today)

        # Container for the data
        for i in range(len(inquiry_list)):
            label_data[inquiry_list[i]] = {}

        for i in range(len(inquiry_list)):
            label_data[inquiry_list[i]] = counter["%s_counter" % inquiry_list[i]]

        # Testing purposes
        # print(counter)
        # print(label_data)

        context = json.dumps(label_data)
        context = json.loads(context)

        return Response(label_data, status=status.HTTP_200_OK)


class InquiryTypePercentage(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    """
    Query Params will determine if the data to be collected is in specified date range
    Determines when data is created sorted by data count
    Returns json
    """

    def get(self, request):
        start = request.query_params.get('start_date', None)
        end = request.query_params.get('end_date', None)
        inquiry_list = get_inquiry_list()

        # Get Whole List
        inquiry_list = get_inquiry_list()
        # query product ID
        query = Inquiry.objects.all().values().filter(created_at__range=[start, end])
        total_count = Inquiry.objects.all().filter(created_at__range=[start, end]).count()

        # get value store in counter
        print(total_count)
        counter = {}
        counter2 = {}
        label_data = {}
        label_data2 = {}
        context = {}
        if total_count != 0:
            for i in range(len(inquiry_list)):
                print(inquiry_list[i])
                temp = ((query.filter(inquiry_type=inquiry_list[i]).count()) / total_count) * 100
                data = str(format(temp, ".2f")) + "%"
                counter["%s_counter" % inquiry_list[i]] = data


        else:
            for i in range(len(inquiry_list)):
                counter["%s_counter" % inquiry_list[i]] = query.filter(inquiry_type=inquiry_list[i]).count()

        # Container for the data
        for i in range(len(inquiry_list)):
            label_data[inquiry_list[i]] = {}

        # Assign Data to label
        for i in range(len(inquiry_list)):
            label_data[inquiry_list[i]] = counter["%s_counter" % inquiry_list[i]]

        if total_count != 0:
            for i in range(len(inquiry_list)):
                counter2["%s_counter" % inquiry_list[i]] = query.filter(inquiry_type=inquiry_list[i]).count()


        else:
            for i in range(len(inquiry_list)):
                counter2["%s_counter" % inquiry_list[i]] = query.filter(inquiry_type=inquiry_list[i]).count()

        # Container for the data
        for i in range(len(inquiry_list)):
            label_data2[inquiry_list[i]] = {}

        # Assign Data to label
        for i in range(len(inquiry_list)):
            label_data2[inquiry_list[i]] = counter2["%s_counter" % inquiry_list[i]]
            # output data

        context = {
            "Total User messages sent": total_count,
            "Percentage": label_data,
            "Counter": label_data2,

        }

        return Response(context, status=status.HTTP_200_OK)


class SendMessage(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InquirySerializer

    def get(self, request):
        today = datetime.now()
        start_date = request.data.get('date_start', '2021-01-01')
        end_date = request.data.get('end_date', today)

        query = Inquiry.objects.all().filter(created_at__range=[start_date, end_date])

        if query.exists():
            inquiry_count = query.count()
            user_inquiry_count = query.values('user_id').distinct().count()

            context = {
                "inquiry_count": inquiry_count,
                "user_inquiry_count": user_inquiry_count,
            }

            return Response(context, status=status.HTTP_200_OK)
        return Response("No Record", status=status.HTTP_400_BAD_REQUEST)


class CountInquiry(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InquirySerializer

    def get(self, request):
        today = datetime.now()
        start_date = request.data.get('date_start', '2021-01-01')
        end_date = request.data.get('end_date', today)

        query = Inquiry.objects.all().values('inquiry_type').filter(created_at__range=[start_date, end_date]).count()

        context = {
            "query": query,
        }
        return Response(context, status=status.HTTP_200_OK)
