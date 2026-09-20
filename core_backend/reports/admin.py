from django.contrib import admin
from .models import CitizenProfile, Incident

admin.site.register(CitizenProfile)
admin.site.register(Incident)