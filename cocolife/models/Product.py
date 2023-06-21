import os
from datetime import datetime, date
from django.db import models
from digiinsurance.models.extras import TimeStampedModel
from cocolife.models.DigiInsuree import DigiInsuree

__all__ = ['Product', 'Package', 'Variant', 'Benefit', 'Premium']


def img_upload_dir(instance, filename):
    ext = filename.split('.')[-1]
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = "{}.{}.{}".format(
        str(instance.name.lower().replace(' ', '_')), ts, ext)
    return os.path.join('products', name)


def upload_product_pdf(instance, filename):
    ext = filename.split('.')[-1]
    name = '{}.{}'.format(instance.id, ext)
    return os.path.join('products', name)


def default_json_value():
    return {"key": []}


class Product(TimeStampedModel):
    POLICY_CHOICES = (
        ('life', 'Life'),
        ('health', 'Health'),
        ('home', 'Home'),
        ('car', 'Car'),
        ('vul', 'VUL'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('draft', 'Draft'),
    )

    PREMIUM_INTERVALS = (
        ('one_time', 'One Time'),
        ('annual', 'Annual'),
        ('semi_annual', 'Semi Annual'),
        ('quarterly', 'Quarterly'),
        ('monthly', 'Monthly')
    )

    name = models.CharField(max_length=255, blank=True, null=True)
    image_path = models.CharField(max_length=32, blank=True, null=True)
    image = models.ImageField(upload_to=img_upload_dir, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.JSONField(max_length=64, blank=True, null=True, choices=POLICY_CHOICES)
    status = models.CharField(max_length=64, blank=True, null=True, choices=STATUS_CHOICES)
    is_recommended = models.BooleanField(default=False, null=False)
    passing_score = models.IntegerField(null=True, blank=True)

    coverage_amount_min = models.IntegerField(null=True, blank=True)
    coverage_amount_max = models.IntegerField(null=True, blank=True)

    pdfname = models.CharField(max_length=255, default='pdf', blank=True, null=True)
    pdf = models.FileField(upload_to=upload_product_pdf, max_length=None, blank=True, null=True)

    liked = models.ManyToManyField(DigiInsuree, blank=True, default=None, related_name='liked_prod')

    def __str__(self):
        return '%s' % (self.name)

    @property
    def coverage_amount_range(self):
        return {"min": self.coverage_amount_min, "max": self.coverage_amount_max}


class Package(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='packages')
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '%s' % self.name


class Variant(TimeStampedModel):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True, blank=True, related_name='variants')


class Benefit(TimeStampedModel):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, null=True, blank=True, related_name='benefits')
    name = models.CharField(max_length=255, blank=True, null=True)
    face_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return '%s' % self.name


class Premium(TimeStampedModel):
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, null=True, blank=True,
        related_name='premiums')
    coverage_term = models.IntegerField()
    age_min = models.IntegerField(blank=False, null=False)
    age_max = models.IntegerField(blank=False, null=False)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        # return '[%s] %s' % (self.id, self.full_name)
        return '[%s] Term: %s, %s' % (self.id, self.coverage_term, self.value)
