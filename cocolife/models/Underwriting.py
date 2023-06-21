from django.db import models
from cocolife.models.ProductInsuree import ProductInsuree
from digiinsurance.models.extras import TimeStampedModel
from digiinsurance.models.User import User

__all__ = ['Underwriting']


class Underwriting(TimeStampedModel):
    UNDERWRITING_APPROVAL = (
        ('pending', 'PENDING'),
        ('approved', 'APPROVED'),
        ('denied', 'DENIED'),
    )
    insuree_policy = models.OneToOneField(ProductInsuree, related_name='underwriting', null=False,
                                          on_delete=models.CASCADE, primary_key=True)
    underwriter_status = models.CharField(max_length=64, default='PENDING', choices=UNDERWRITING_APPROVAL)
    editor = models.ForeignKey(User, null=False, on_delete=models.CASCADE, default=375)
