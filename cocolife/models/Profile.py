from django.db import models

from digiinsurance.models.extras import TimeStampedModel
from digiinsurance.models.User import User
from datetime import date

__all__ = ['Profile']


class Profile(TimeStampedModel):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    email = models.EmailField(max_length=128, unique=False)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    mobile_number = models.CharField(max_length=16, null=False, blank=False, unique=False)

    gender = models.CharField(max_length=1, blank=True, null=True, choices=(('F', 'Femal'), ('M', 'Male')))
    birthday = models.DateField(blank=True, null=True, default='1900-05-05')
    tel_number = models.CharField(max_length=16, blank=True, null=True)
    occupation = models.CharField(max_length=64, blank=True, null=True)

    civil_status = models.CharField(max_length=64, blank=True, null=True)
    nationality = models.CharField(max_length=64, blank=True, null=True)
    place_of_birth = models.CharField(max_length=128, blank=True, null=True)
    sss = models.CharField(max_length=16, blank=True, null=True)
    tin = models.CharField(max_length=16, blank=True, null=True)
    business = models.CharField(max_length=64, blank=True, null=True)

    home_address = models.CharField(max_length=255, blank=True, null=True)
    home_village = models.CharField(max_length=255, blank=True, null=True)
    home_city = models.CharField(max_length=64, blank=True, null=True)
    home_province = models.CharField(max_length=64, blank=True, null=True)
    home_zip_code = models.CharField(max_length=10, blank=True, null=True)

    nature_of_business = models.CharField(max_length=64, blank=True, null=True)
    specified_source = models.CharField(max_length=64, blank=True, null=True)
    source_of_funds = models.CharField(max_length=64, blank=True, null=True)

    office_address = models.CharField(max_length=255, blank=True, null=True)
    office_village = models.CharField(max_length=255, blank=True, null=True)
    office_city = models.CharField(max_length=64, blank=True, null=True)
    office_province = models.CharField(max_length=255, blank=True, null=True)
    office_zip_code = models.CharField(max_length=64, blank=True, null=True)

    isArchived = models.BooleanField(default=False)
    tags = models.TextField(blank=True, null=True)
    default_contact_num = models.CharField(max_length=16, blank=True, null=True, choices=(('email', 'Email'), ('mobile', 'Mobile'), ('landline', 'Landline')))

    def __str__(self) -> str:
        return '%s | %s' % (self.email, self.mobile_number)

    def get_full_name(self):
        names = [self.first_name, self.middle_name, self.last_name]
        return ' '.join(filter(None, names))

    def get_age(self):
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
