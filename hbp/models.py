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

class ConsentInfo(models.Model):
	timestamp = models.DateTimeField(default=timezone.now)
	participant_name = models.CharField(max_length = 150)
	participant_date = models.CharField(max_length = 30)
	participant_signature = models.ImageField(blank=True, upload_to=GetImageFolder)
	obtaining_name = models.CharField(max_length = 150)
	obtaining_role = models.CharField(max_length = 300)
	obtaining_date = models.CharField(max_length = 30)
	obtaining_signature = models.ImageField(blank=True, upload_to=GetImageFolder)

	def __unicode__(self):
		return self.obtaining_date + ' : ' + self.participant_name

	# For admin page to let superusers download signature images
	def participant_sig(self):
		if self.participant_signature:
			return "<a href='%s'>view</a>" % ('/signatures/' + self.participant_signature.url,)
		else:
			return "No signature..."

	# For admin page to let superusers download signature images
	def obtaining_sig(self):
		if self.obtaining_signature:
			return "<a href='%s'>view</a>" % ('/signatures/' + self.obtaining_signature.url,)
		else:
			return "No signature..."

	participant_sig.allow_tags = True
	obtaining_sig.allow_tags = True
