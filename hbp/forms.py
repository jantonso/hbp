from django import forms

LIKERT_CHOICES = [
	(-2,'not at all'),
	(-1,'not really'),
	(0,'neutral'),
	(1,'somewhat'),
	(2,'very important')]

NON_LIKERT_CHOICES = [
	('yes','yes'),
	('no','no'),
	('dk','don\'t know')]

class PersonalizedCareForm(forms.Form):
	q1 = forms.ChoiceField(label='Getting birth control', 
		choices=LIKERT_CHOICES, widget=forms.RadioSelect())
	q2 = forms.ChoiceField(label='Breastfeeding support',
		choices=LIKERT_CHOICES, widget=forms.RadioSelect())
	q3 = forms.ChoiceField(label='Checking on my mood after delivery, screening for depression',
		choices=LIKERT_CHOICES, widget=forms.RadioSelect())
	q4 = forms.ChoiceField(label='Talking to a doctor about how to keep my next pregnancy healthy',
		choices=LIKERT_CHOICES, widget=forms.RadioSelect())
	q5 = forms.ChoiceField(label='Getting advice about diet, exercise, weight loss, and sexual activity after delivery',
		choices=LIKERT_CHOICES, widget=forms.RadioSelect())
	q6 = forms.ChoiceField(label='Discussing issues of bowel or bladder health such as hemorrhoids or leaking urine',
		choices=LIKERT_CHOICES, widget=forms.RadioSelect())
	q7 = forms.ChoiceField(label='Did you have gestational diabetes during this pregnancy?',
		choices=NON_LIKERT_CHOICES, widget=forms.RadioSelect())
	q8 = forms.ChoiceField(label='Did you have high blood pressure during this pregnancy?',
		choices=NON_LIKERT_CHOICES, widget=forms.RadioSelect())
	q9 = forms.ChoiceField(label=' Did you have a preterm labor during this pregnancy?',
		choices=NON_LIKERT_CHOICES, widget=forms.RadioSelect())

class DeliveryDateForm(forms.Form):
	delivery_day = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'DD'}),
						max_length=10)
	delivery_month = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'MM'}),
						max_length=10)
	delivery_year = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'YYYY'}),
						max_length=10)

class SignatureForm(forms.Form):
	sig_name = forms.CharField(max_length=150)
	dob_day = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'DD'}),
						max_length=10)
	dob_month = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'MM'}),
						max_length=10)
	dob_year = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'YYYY'}),
						max_length=10)
	sig_image = forms.CharField(widget=forms.HiddenInput())

class PhoneNumberForm(forms.Form):
	phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'xxx-xxx-xxxx'}),
						max_length=50)