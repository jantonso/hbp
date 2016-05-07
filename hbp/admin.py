from django.contrib import admin
from .models import *

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
	ordering = ('appt_datetime',)
	list_display = ('appt_date', 'appt_time', 'booked', 'patient')
	search_fields = ('patient__name','appt_date')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
	list_display = ('name','dob_date','delivery_date','phone_number','signature')
	search_fields = ('name','phone_number')