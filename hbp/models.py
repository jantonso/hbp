from django.db import models
from django.utils import timezone

def GetImageFolder(instance, filename):
	return filename

class PersonalizedCareAnswers(models.Model):
	q1 = models.IntegerField(null=True, blank=True,
		verbose_name=u'Getting birth control')
	q2 = models.IntegerField(null=True, blank=True,
		verbose_name=u'Breastfeeding support')
	q3 = models.IntegerField(null=True, blank=True,
		verbose_name=u'Checking on my mood after delivery')
	q4 = models.IntegerField(null=True, blank=True,
		verbose_name=u'Planning my next pregnancy')
	q5 = models.IntegerField(null=True, blank=True,
		verbose_name=u'Sexual activity after birth')
	q6 = models.IntegerField(null=True, blank=True,
		verbose_name=u'Discussing issues of bowel or bladder health such as hemorrhoids or leaking urine')
	q7 = models.IntegerField(null=True, blank=True,
		verbose_name=u'Did you have gestational diabetes during this pregnancy?')
	q8 = models.IntegerField(null=True, blank=True,
		verbose_name=u'Did you have high blood pressure during this pregnancy?')
	q9 = models.IntegerField(null=True, blank=True,
		verbose_name=u'Did you have a preterm delivery during this pregnancy?')

	def __unicode__(self):
		return self.patient.name + ' Answers'

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
	personalized_care_answers = models.OneToOneField(PersonalizedCareAnswers, related_name='patient',
		null=True, blank=True)
	appointment = models.OneToOneField(Appointment, related_name='patient', 
		null=True, blank=True)

	def __unicode__(self):
		return self.name
