from django.db import models
from digiinsurance.models.extras import TimeStampedModel
from digiinsurance.models.User import User
from datetime import date

__all__ = ['DigiInsuree']


class DigiInsuree(TimeStampedModel):
    user = models.OneToOneField(User, related_name='digiinsuree', null=False, on_delete=models.CASCADE, primary_key=True)

    # Fields from User
    email = models.EmailField(max_length=128, unique=True)
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

    isArchived = models.BooleanField(default=False)
    tags = models.TextField(null=True, blank=True)
    default_contact_info = models.CharField(max_length=16, default="email",
     choices=(('email', 'Email'), ('mobile', 'Mobile'), ('landline', 'Landline')))

    def __str__(self):
        return '%s' % (self.first_name)

    def get_full_name(self):
        names = [self.first_name, self.middle_name, self.last_name]
        return ' '.join(filter(None, names))

    def get_age(self):
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
