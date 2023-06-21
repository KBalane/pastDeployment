from django.db import models
from cocolife.models.ProductInsuree import ProductInsuree


__all__ = ['Beneficiary']


class Beneficiary(models.Model):

    SEX = (
        ('Male', 'MALE'),
        ('Female', 'FEMALE'),
    )
    PRIORITY_TYPE = (
        ('Primary', 'PRIMARY'),
        ('Contingent', 'CONTINGENT'),
    )
    BENEFIT_TYPE = (
        ('Revocable', 'REVOCABLE'),
        ('Irrevocable', 'IRREVOCABLE'),
    )

    product_insuree = models.ForeignKey(
        ProductInsuree, on_delete=models.CASCADE, null=False, blank=False)
    full_name = models.CharField(blank=False, max_length=255, null=False)
    address = models.CharField(blank=False, max_length=255, null=False)
    contact_no = models.CharField(blank=False, max_length=20, null=False)
    birth_place = models.CharField(blank=False, max_length=255, null=False)
    birth_date = models.DateField(blank=False, null=False)
    citizenship = models.CharField(blank=False, max_length=50, null=False)
    sex = models.CharField(choices=SEX, max_length=10, null=False)
    relationship = models.CharField(blank=False, max_length=50, null=False)
    percentage_share = models.DecimalField(
        blank=False, decimal_places=2, default=0, max_digits=10)
    priority_type = models.CharField(
        choices=PRIORITY_TYPE, max_length=20, null=False)
    benefit_type = models.CharField(
        choices=BENEFIT_TYPE, max_length=20, null=False)
