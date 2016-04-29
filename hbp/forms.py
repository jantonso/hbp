from django import forms
from datetime import datetime

from .models import Appointment

import re

LIKERT_CHOICES = [
	(-2,'not at all'),
	(-1,'not really'),
	(0,'somewhat'),
	(1,'important'),
	(2,'very important')]

NON_LIKERT_CHOICES = [
	(2,'yes'),
	(-2,'no'),
	(0,'don\'t know')]

class ConsentForm(forms.Form):
	participant_name = forms.CharField(max_length=150)
	participant_day = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'DD'}),
						max_length=10)
	participant_month = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'MM'}),
						max_length=10)
	participant_year = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'YYYY'}),
						max_length=10)
	participant_sig = forms.CharField(widget=forms.HiddenInput())
	
	obtaining_name = forms.CharField(max_length=150)
	obtaining_role = forms.CharField(max_length=300)
	obtaining_day = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'DD'}),
						max_length=10)
	obtaining_month = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'MM'}),
						max_length=10)
	obtaining_year = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'YYYY'}),
						max_length=10)
	obtaining_sig = forms.CharField(widget=forms.HiddenInput())

	def clean(self):
		cleaned_data = super(ConsentForm, self).clean()
		participant_day = cleaned_data.get('participant_day')
		participant_month = cleaned_data.get('participant_month')
		participant_year = cleaned_data.get('participant_year')
		obtaining_day = cleaned_data.get('obtaining_day')
		obtaining_month = cleaned_data.get('obtaining_month')
		obtaining_year = cleaned_data.get('obtaining_year')

		# Make sure that the dates entered are real dates
		if participant_day and participant_month and participant_year and obtaining_day and obtaining_month and obtaining_year:

			participant_date = validateDate(participant_day, participant_month, participant_year)
			obtaining_date = validateDate(obtaining_day, obtaining_month, obtaining_year)

			if participant_date and obtaining_date:
				cleaned_data['participant_date'] = participant_date
				cleaned_data['obtaining_date'] = obtaining_date
				return cleaned_data
			else:
				raise forms.ValidationError('The date is in an incorrect format...')

class PersonalizedCareForm(forms.Form):
	q1 = forms.ChoiceField(label='Getting birth control', 
		required=False, choices=LIKERT_CHOICES, widget=forms.RadioSelect())
	q2 = forms.ChoiceField(label='Breastfeeding support',
		required=False, choices=LIKERT_CHOICES, widget=forms.RadioSelect())
	q3 = forms.ChoiceField(label='Checking on my mood after delivery',
		required=False, choices=LIKERT_CHOICES, widget=forms.RadioSelect())
	q4 = forms.ChoiceField(label='Planning my next pregnancy',
		required=False, choices=LIKERT_CHOICES, widget=forms.RadioSelect())
	q5 = forms.ChoiceField(label='Sexual activity after birth',
		required=False, choices=LIKERT_CHOICES, widget=forms.RadioSelect())
	q6 = forms.ChoiceField(label='Discussing issues of bowel or bladder health such as hemorrhoids or leaking urine',
		required=False, choices=LIKERT_CHOICES, widget=forms.RadioSelect())
	q7 = forms.ChoiceField(label='Did you have gestational diabetes during this pregnancy?',
		required=False, choices=NON_LIKERT_CHOICES, widget=forms.RadioSelect())
	q8 = forms.ChoiceField(label='Did you have high blood pressure during this pregnancy?',
		required=False, choices=NON_LIKERT_CHOICES, widget=forms.RadioSelect())
	q9 = forms.ChoiceField(label=' Did you have a preterm delivery during this pregnancy?',
		required=False, choices=NON_LIKERT_CHOICES, widget=forms.RadioSelect())

class DeliveryDateForm(forms.Form):
	delivery_day = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'DD'}),
						max_length=10)
	delivery_month = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'MM'}),
						max_length=10)
	delivery_year = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'YYYY'}),
						max_length=10)

	def clean(self):
		cleaned_data = super(DeliveryDateForm, self).clean()
		delivery_day = cleaned_data.get('delivery_day')
		delivery_month = cleaned_data.get('delivery_month')
		delivery_year = cleaned_data.get('delivery_year')

		# Make sure that the date entered is a real date
		if delivery_day and delivery_month and delivery_year:
			delivery_date = validateDate(delivery_day, delivery_month, delivery_year)
			if delivery_date:
				cleaned_data['delivery_date'] = delivery_date
				return cleaned_data
			else:
				raise forms.ValidationError('The date is in an incorrect format...')

class CalendarForm(forms.Form):
	appt_id = forms.IntegerField(widget=forms.HiddenInput())

	def clean(self):
		cleaned_data = super(CalendarForm, self).clean()
		appt_id = cleaned_data.get('appt_id')

		# Make sure the appt id corresponds to an actual appt that is unbooked
		if appt_id:
			try:
				selected_appt = Appointment.objects.get(pk=appt_id)
				if (selected_appt.booked):
					raise forms.ValidationError('That appt is already booked.')
				else:
					cleaned_data['appt_date'] = selected_appt.appt_date
					cleaned_data['appt_time'] = selected_appt.appt_time
					return cleaned_data
			except Appointment.DoesNotExist:
				raise forms.ValidationError('That appt id is invalid.')

class SignatureForm(forms.Form):
	sig_name = forms.CharField(max_length=150)
	dob_day = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'DD'}),
						max_length=10)
	dob_month = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'MM'}),
						max_length=10)
	dob_year = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'YYYY'}),
						max_length=10)
	sig_image = forms.CharField(widget=forms.HiddenInput())

	def clean(self):
		cleaned_data = super(SignatureForm, self).clean()
		dob_day = cleaned_data.get('dob_day')
		dob_month = cleaned_data.get('dob_month')
		dob_year = cleaned_data.get('dob_year')

		# Make sure that the date entered is a real date
		if dob_day and dob_month and dob_year:
			dob_date = validateDate(dob_day, dob_month, dob_year)
			if dob_date:
				cleaned_data['dob_date'] = dob_date
				return cleaned_data
			else:
				raise forms.ValidationError('The date is in an incorrect format...')

class PhoneNumberForm(forms.Form):
	phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'xxx-xxx-xxxx'}),
						max_length=50)

	def clean(self):
		cleaned_data = super(PhoneNumberForm, self).clean()
		phone_number = cleaned_data.get('phone_number')

		# Make sure that the date entered is a real date
		if phone_number:
			# Strip all non digit characters and make sure there are 10 digits
			stripped_phone_number = re.sub('\D','',phone_number)
			if (len(stripped_phone_number) == 10):
				cleaned_data['phone_number'] = stripped_phone_number
				return cleaned_data
			else:
				raise forms.ValidationError('The phone number is invalid...')

# Helper Functions

# Make sure that the date entered is a real date and convert it to 
# a uniform formatted string
def validateDate(day, month, year):
	date = month + '/' + day + '/' + year
	# Try each possible format
	for fmt in ('%b/%d/%y', '%B/%d/%y', '%m/%d/%y',
				'%b/%d/%Y', '%B/%d/%Y', '%m/%d/%Y'):
		try:
			date = datetime.strptime(date, fmt)
			# Convert the date back to a uniformly formatted string
			return date.strftime('%m/%d/%Y')
		except ValueError:
			pass
	return None









