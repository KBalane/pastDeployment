from django.db import models
from digiinsurance.models.extras import TimeStampedModel
from cocolife.models.ProductInsuree import ProductInsuree
from cocolife.models.DigiInsuree import DigiInsuree


class PolicyOwner(TimeStampedModel):
    insured_by = models.ForeignKey(DigiInsuree, null=False , on_delete=models.CASCADE)
    product_insuree = models.OneToOneField(ProductInsuree, null=False, on_delete=models.CASCADE)

    email = models.EmailField(max_length=128)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    middle_name = models.CharField(max_length=32, blank=True, null=True)    
    last_name = models.CharField(max_length=32, blank=True, null=False)  
    mobile_number = models.CharField(max_length=16, null=False, blank=False)

    gender = models.CharField(max_length=1, blank=True, null=True, choices=(('F', 'Female'), ('M', 'Male')))
    birthday = models.DateField(blank=True, null=True)
    tel_number = models.CharField(max_length=16, blank=True, null=True)
    occupation = models.CharField(max_length=64, blank=True, null= True)

    civil_status = models.CharField(max_length=64, blank=True, null=True)
    nationality = models.CharField(max_length=64, blank=True, null=True)
    place_of_birth = models.CharField(max_length=128, blank=True, null=True)
    sss = models.CharField(max_length=16, blank=True, null=True)
    tin = models.CharField(max_length=16, blank=True, null=True)
    business = models.CharField(max_length=64, blank=True, null=True)

    home_address = models.CharField(max_length=254, blank=True, null= True)
    home_village = models.CharField(max_length=254, blank=True, null=True)
    home_city = models.CharField(max_length=64, blank=True, null=True)
    home_province = models.CharField(max_length=64, blank=True, null=True)
    home_zip_code = models.CharField(max_length=10, blank=True, null=True)
    
    nature_of_business = models.CharField(max_length=64, blank=True, null=True)
    specified_source = models.CharField(max_length=64, blank=True, null=True)
    source_of_funds = models.CharField(max_length=64, blank=True, null=True)

    office_address = models.CharField(max_length=254, blank=True, null= True)
    office_province = models.CharField(max_length=64, blank=True, null=True)
    office_zip_code = models.CharField(max_length=10, blank=True, null=True)
    office_village = models.CharField(max_length=64, blank=True, null=True)
    office_city = models.CharField(max_length=64, blank=True, null=True)
