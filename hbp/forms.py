from django import forms

class DeliveryDateForm(forms.Form):
	delivery_day = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'DD'}),
						max_length=10)
	delivery_month = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'MM'}),
						max_length=10)
	delivery_year = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'YYYY'}),
						max_length=10)

class SignatureForm(forms.Form):
	sig_name = forms.CharField(max_length=50)
	dob_day = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'DD'}),
						max_length=10)
	dob_month = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'MM'}),
						max_length=10)
	dob_year = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'YYYY'}),
						max_length=10)
	sig_image = forms.CharField(widget=forms.HiddenInput())