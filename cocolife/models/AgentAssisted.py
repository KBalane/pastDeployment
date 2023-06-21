from django.db import models
from cocolife.models.Product import Product
from digiinsurance.models.extras import TimeStampedModel
from .DigiInsuree import DigiInsuree

__all__ = ['AgentAssisted']


class AgentAssisted(TimeStampedModel):
    user = models.ForeignKey(DigiInsuree, related_name='agentassists', on_delete=models.CASCADE)
    datetime = models.DateTimeField(null=True, blank=True)
    product = models.ForeignKey(Product, related_name='agentassists', on_delete=models.CASCADE)