from django.db import models
from django.utils import timezone

def GetImageFolder(instance, filename):
	return filename

class Patient(models.Model):
	name = models.CharField(max_length = 150)
	dob_date = models.CharField(max_length = 30)
	delivery_date = models.CharField(max_length = 30)
	phone_number = models.CharField(max_length = 30)
	signature_image = models.ImageField(blank=True, upload_to=GetImageFolder)

	def __unicode__(self):
		return self.name

	# For admin page to let superusers download signature images
	def signature(self):
		if self.signature_image:
			print self.signature_image
			return "<a href='%s'>view</a>" % ('/signatures/' + self.signature_image.url,)
		else:
			return "No signature..."
	signature.allow_tags = True

class Appointment(models.Model):
	patient = models.ForeignKey(to=Patient, related_name="patient", 
		null=True, blank=True)
	unit_name = models.CharField(max_length = 50)
	appt_datetime = models.DateTimeField()
	# format = 04/13/2016
	appt_date = models.CharField(max_length = 30)
	# format = 10am, 2pm, etc.
	appt_time = models.CharField(max_length = 30)
	booked= models.BooleanField(default=False)

	def __unicode__(self):
		return self.appt_date + ' ' + self.appt_time

