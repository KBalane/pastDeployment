from django.db import models
from digiinsurance.models.extras import TimeStampedModel

__all__ = ['CLFeature']

client_type = [
    ('MO', 'Mobile'),
    ('CL', 'Client'),
    ('AD', 'Admin')
]


class CLFeature(TimeStampedModel):
    feature_name = models.CharField(max_length=50, null=False, unique=True)
    is_feature_active = models.BooleanField(default=False, null=False)
    client_type = models.CharField(max_length=20, choices=client_type, default='AD')
