from django.db import models
from django.utils import timezone

def GetImageFolder(instance, filename):
	return filename

class Appointment(models.Model):
	unit_name = models.CharField(max_length = 50)
	appt_datetime = models.DateTimeField()
	# format = 04/13/2016
	appt_date = models.CharField(max_length = 30)
	# format = 10am, 2pm, etc.
	appt_time = models.CharField(max_length = 30)
	booked= models.BooleanField(default=False)

	def __unicode__(self):
		return self.appt_date + ' ' + self.appt_time

class Patient(models.Model):
	name = models.CharField(max_length = 150)
	dob_date = models.CharField(max_length = 30)
	delivery_date = models.CharField(max_length = 30)
	phone_number = models.CharField(max_length = 30)
	appointment = models.OneToOneField(Appointment, related_name='patient', 
		null=True, blank=True)

	def __unicode__(self):
		return self.name
