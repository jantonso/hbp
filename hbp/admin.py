from django.contrib import admin
from .models import *

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
	ordering = ('appt_datetime',)
	list_display = ('appt_date', 'appt_time', 'unit_name', 'booked', 'patient')
	search_fields = ('appt_date',)

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
	list_display = ('name','dob_date','delivery_date','phone_number','appointment')
	search_fields = ('name','phone_number','appointment')