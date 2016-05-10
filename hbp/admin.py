from django.contrib import admin
from django.core import urlresolvers
from .models import *

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
	ordering = ('appt_datetime',)
	list_display = ('appt_date', 'appt_time', 'unit_name', 'booked', 'patient')
	search_fields = ('appt_date',)

	def patient(self, obj):
		if (obj.patient):
			link = urlresolvers.reverse("admin:hbp_patient_change", args=[obj.patient.id])
			return u'<a href="%s">%s</a>' % (link, obj.patient.name)
		else:
			return 'None'
	patient.allow_tags = True

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
	list_display = ('name','dob_date','delivery_date','phone_number',
		'scheduled_appointment', 'answers')
	search_fields = ('name','phone_number')

	def scheduled_appointment(self, obj):
		if (obj.appointment):
			link = urlresolvers.reverse("admin:hbp_appointment_change", args=[obj.appointment.id])
			return u'<a href="%s">%s</a>' % (link, obj.appointment.appt_date)
		else:
			return 'None'
	scheduled_appointment.allow_tags = True

	def answers(self, obj):
		if (obj.personalized_care_answers):
			link = urlresolvers.reverse("admin:hbp_personalizedcareanswers_change", args=[obj.personalized_care_answers.id])
			return u'<a href="%s">%s</a>' % (link, obj.personalized_care_answers)
		else:
			return 'None'
	answers.allow_tags = True

@admin.register(PersonalizedCareAnswers)
class PersonalizedCareAnswersAdmin(admin.ModelAdmin):
	list_display = ('__unicode__', 'patient')

	def patient(self, obj):
		if (obj.patient):
			link = urlresolvers.reverse("admin:hbp_patient_change", args=[obj.patient.id])
			return u'<a href="%s">%s</a>' % (link, obj.patient.name)
		else:
			return 'None'
	patient.allow_tags = True
