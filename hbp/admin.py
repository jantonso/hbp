from django.contrib import admin
from .models import *

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
	ordering = ('appt_datetime',)
	list_display = ('appt_date', 'appt_time', 'booked', 'patient')
	search_fields = ('patient','appt_date')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
	list_display = ('name','dob_date','delivery_date','phone_number','signature')
	search_fields = ('name',)

@admin.register(ConsentInfo)
class ConsentInfoAdmin(admin.ModelAdmin):
	ordering = ('timestamp',)
	list_display = ('participant_name', 'participant_date', 'participant_sig', 'obtaining_name', 'obtaining_sig')
	search_fields = ('participant_name', 'participant_date')