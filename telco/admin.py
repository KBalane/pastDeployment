from django.contrib import admin

from telco.models import TelcoPersonAddress, TelcoSimDetails

# Register your models here.
admin.site.register(TelcoPersonAddress)
admin.site.register(TelcoSimDetails)
