from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from datetime import timedelta, datetime

from cocolife.serializers import AuditLogSerializer
from cocolife.models import AuditLog


__all__ = ['AuditLogAPI', 'AuditLogListAPI']


class AuditLogAPI(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer

    def get(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(login_user=self.request.user)


class AuditLogListAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer

    def post(self, request, *args, **kwargs):
        data = self.request.data
        res = self.get_response(data)
        return Response(res, status=status.HTTP_200_OK)

    def get_response(self, data):
        date_from = datetime.combine(datetime.strptime(data['date_from'], '%Y-%m-%d'), datetime.min.time())
        if 'action' in data and 'user' in data and 'date_from' in data and 'date_to' in data:
            date_to = datetime.combine(datetime.strptime(data['date_to'], '%Y-%m-%d'), datetime.max.time())
            res = self.list_audit_logs(
                action=data['action'], user_id=data['user'], created_at__range=(date_from, date_to)
            )
        elif 'action' in data and 'user' in data and 'date_from' in data:
            res = self.list_audit_logs(action=data['action'], user_id=data['user'], created_at__gte=date_from)
        elif 'date_from' in data and 'days' in data:
            date_to = date_from + timedelta(days=data['days'] + 1)
            res = self.list_audit_logs(created_at__range=(date_from, date_to))
        elif 'date_from' in data:
            res = self.list_audit_logs(created_at__range=(date_from, datetime.now()))
        else:
            res = self.list_audit_logs()
        return res

    def list_audit_logs(self, **kwargs):
        audit_logs = self.get_audit_query(**kwargs)
        log_list = []
        for audit_log in audit_logs:
            log_list.append(AuditLogSerializer(audit_log).data)
        return {"result": log_list}

    @staticmethod
    def get_audit_query(**kwargs):
        if kwargs:
            return AuditLog.objects.filter(**kwargs).order_by('-created_at')
        return AuditLog.objects.all().order_by('-created_at')
