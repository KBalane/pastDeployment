from rest_framework import serializers

from cocolife.models.AuditLog import *


__all__ = ['AuditLogSerializer']


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ['action', 'user_id', 'details_id', 'ip_address']
