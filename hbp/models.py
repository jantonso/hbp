from django.db import models

class Patient(models.Model):
	name = models.CharField(max_length = 150)
	dob_date = models.DateTimeField()
	delivery_date = models.DateTimeField()
	phone_number = models.CharField(max_length = 30)
	signature_image = models.TextField()

class Appointment(models.Model):
	patient = models.ForeignKey(to=Patient, related_name="patient", 
		null=True, blank=True)
	unit_name = models.CharField(max_length = 50)
	appt_time = models.DateTimeField()
	booked= models.BooleanField(default=False)

class ConsentInfo(models.Model):
	participant_name = models.CharField(max_length = 150)
	participant_date = models.DateTimeField()
	participant_signature = models.TextField()
	obtaining_name = models.CharField(max_length = 150)
	obtaining_role = models.CharField(max_length = 300)
	obtaining_date = models.DateTimeField()
	obtaining_signature = models.TextField()