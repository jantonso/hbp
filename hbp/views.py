from django.http import HttpResponse

from django.shortcuts import render, redirect

from .forms import *

# Indicates that the user has finished all the videos
finished_videos_index = 10

# Session values
# 	=> required_videos = list of required videos for the user to watch
#	=> required_topics = list of required_topics that the user wants to learn about
#	=> appointment = {delivery_date, name, date_of_birth, 
#					  signature, appointment_info, phone_number}

def index(request):
	return render(request, 'index.html', {})

# User signs consent page for the initial study
def consent(request):
	if request.method == 'GET':
		form = ConsentForm()
		return render(request, 'consent.html', {'form': form})
	elif request.method == 'POST':
		# Process the ConsentForm
		form = ConsentForm(request.POST)
		if form.is_valid():
			handleConsentForm(request, form)
			return redirect('/pc/')
		else:
			# form is invalid, need to display errors to the user
			print form.errors
			return redirect('/')

# User answers questions about postpartum needs
def personalizedCare(request):
	if request.method == 'GET':
		form = PersonalizedCareForm()
		return render(request, 'personalizedCare.html', {'form': form})
	elif request.method == 'POST':
		# Process the PersonalizedCareForm
		form = PersonalizedCareForm(request.POST)
		if form.is_valid():
			handlePersonalizedCareForm(request, form)
			return redirect('/iv/')
		else:
			# form is invalid, need to display errors to the user
			print form.errors
			return redirect('/')

# User watches informational videos 
def informationalVideos(request, video_index=0):
	try:	
		video_index = int(video_index)

		# Check to see if they have finished all their required videos
		next_video = 0
		finished_videos = True
		required_videos = request.session.get('required_videos')
		required_topics = request.session.get('required_topics')
		# They jumped directly to this page
		if (required_videos == None or required_topics == None):
			print ("There were no required videos?")
			return redirect('/')	
		# They still have required videos to watch		
		elif (len(required_videos) != 0):
			next_video = required_videos[0]
			finished_videos = False
			# Remove the next video from the list of required videos
			request.session['required_videos'] = required_videos[1:]

		return render(request, 'importantInformation.html', {'video_index': video_index, 
						'finished_videos': finished_videos, 'next_video': next_video, 
						'required_topics': required_topics})
	except ValueError as e:
		print e
		return redirect('/')

# Displays intro message for commit and schedule page
def commitAndScheduleIntro(request):
	# Keep track of the appointment info in the user's session
	request.session['appointment'] = {}
	return render(request, 'commitAndScheduleIntro.html', {})

# User enters in delivery date 
def commitAndScheduleDeliveryDate(request):
	# Check to make sure they didn't just jump directly to this page
	appt_info = request.session.get('appointment', None)
	if (appt_info == None):
		print ("There was no appointment in the session")
		return redirect('/')

	if request.method == 'GET':
		form = DeliveryDateForm()
		return render(request, 'commitAndScheduleDeliveryDate.html', {'form': form})
	elif request.method == 'POST':
		# Process the DeliveryDateForm data
		form = DeliveryDateForm(request.POST)
		if form.is_valid():
			handleDeliveryDateForm(request, form, appt_info)
			return redirect('/cs/calendar/')
		else:
			# form is invalid, need to display errors to the user
			print form.errors
			return redirect('/')

# User selects an appt from calendar 
def commitAndScheduleCalendar(request):
	# Check to make sure they didn't just jump directly to this page
	appt_info = request.session.get('appointment', None)
	if (appt_info == None):
		print ("There was no appointment in the session")
		return redirect('/')

	return render(request, 'commitAndScheduleCalendar.html', {})

# User signs and confirms appt 
def commitAndScheduleSignature(request):
	# Check to make sure they didn't just jump directly to this page
	appt_info = request.session.get('appointment', None)
	if (appt_info == None):
		print ("There was no appointment in the session")
		return redirect('/')

	if request.method == 'GET':
		form = SignatureForm()
		return render(request, 'commitAndScheduleSignature.html', {'form': form})
	elif request.method == 'POST':
		# Process the SignatureForm data
		form = SignatureForm(request.POST)
		if form.is_valid():
			handleSignatureForm(request, form, appt_info)
			return redirect('/incentive/')
		else:
			# form is invalid, need to display errors to the user
			print form.errors
			return redirect('/')

# Displays incentive message and user provides phone number
def incentive(request):
	# Check to make sure they didn't just jump directly to this page
	appt_info = request.session.get('appointment', None)
	if (appt_info == None):
		print ("There was no appointment in the session")
		return redirect('/')

	if request.method == 'GET':
		form = PhoneNumberForm()
		return render(request, 'incentive.html', {'form': form})
	elif request.method == 'POST':
		# Process the PhoneNumberForm data
		form = PhoneNumberForm(request.POST)
		if form.is_valid():
			handlePhoneNumberForm(request, form, appt_info)
			storeAppointment(appt_info)
			return redirect('/final/')
		else:
			# form is invalid, need to display errors to the user
			print form.errors
			return redirect('/')		

# Displays final message to the user
def final(request):
	required_topics = request.session.get('required_topics')
	# They jumped directly to this page
	if (required_topics == None):
		print ("There were no required topics?")
		return redirect('/')	
	return render(request, 'final.html', {'required_topics': required_topics})

# ----------------------------- Helper Functions ---------------------------------- #

def	handleConsentForm(request, form):
	participant_name = form.cleaned_data['participant_name']
	participant_day = form.cleaned_data['participant_day']
	participant_month = form.cleaned_data['participant_month']
	participant_year = form.cleaned_data['participant_year']
	participant_sig = form.cleaned_data['participant_sig']
	participant_date = participant_month + '/' + participant_day + '/' + participant_year
	print participant_name, participant_date, len(participant_sig)
	
	obtaining_name = form.cleaned_data['obtaining_name']
	obtaining_role = form.cleaned_data['obtaining_role']
	obtaining_day = form.cleaned_data['obtaining_day']
	obtaining_month = form.cleaned_data['obtaining_month']
	obtaining_year = form.cleaned_data['obtaining_year']
	obtaining_sig = form.cleaned_data['obtaining_sig']
	obtaining_date = obtaining_month + '/' + obtaining_day + '/' + obtaining_year
	print obtaining_name, obtaining_date, len(obtaining_sig), obtaining_role

	return

# ALGORITHM TO DETERMINE THE REQUIRED TOPICS/VIDEOS 
# Choose up to the 5 maximum values for the topics, if there are less than 2, choose 2 default ones
# Likert = -2, -1, 0, 1, 2 ====> not at all, not really, somewhat, important, very important
# Non-Likert = -2, 0, 2 ====> no, don't know, yes
def handlePersonalizedCareForm(request, form):
	list_of_questions = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9']
	list_of_topics = ['birth control', 'breastfeeding support', 'checking on my mood', 'talking to a doctor',
				  'diet, exercise, weight loss, sexual activity', 'bowel and bladder health', 
				  'gestational diabetes', 'high blood pressure', 'preterm labor']
	answers = {}
	for i in xrange(0,len(list_of_questions)):
		question_name = list_of_questions[i]
		question_answer = form.cleaned_data[question_name]	

		answer_value = int(question_answer)
		# Don't add values that were marked 'not important' or 'no'
		if (answer_value >= 0):
			answers[i+1] = answer_value

	# Choose the top five rated topics
	required_videos = sorted(answers, key=answers.get, reverse=True)[:5]
	required_topics = [list_of_topics[index-1] for index in required_videos]	

	# Add the final index to indicate that all the videos were finished
	required_videos += [finished_videos_index]

	# Add a list of the required videos and their respective topics to the session
	request.session['required_videos'] = required_videos
	request.session['required_topics'] = required_topics

	return

def handleDeliveryDateForm(request, form, appt_info):
	delivery_day = form.cleaned_data['delivery_day']
	delivery_month = form.cleaned_data['delivery_month']
	delivery_year = form.cleaned_data['delivery_year']

	# Keep track of the user's appointment info in the session
	delivery_date = delivery_month + '/' + delivery_day + '/' + delivery_year
	appt_info.update({'delivery_date': delivery_date})
	request.session['appointment'] = appt_info
	return

def handleSignatureForm(request, form, appt_info):
	sig_name = form.cleaned_data['sig_name']
	dob_day = form.cleaned_data['dob_day']
	dob_month = form.cleaned_data['dob_month']
	dob_year = form.cleaned_data['dob_year']
	sig_image = form.cleaned_data['sig_image']

	# Add user's appointment info to the session
	dob_date = dob_month + '/' + dob_day + '/' + dob_year
	appt_info.update({'sig_name': sig_name, 
		'dob_date': dob_date, 'sig_image': sig_image})
	request.session['appointment'] = appt_info
	return

def handlePhoneNumberForm(request, form, appt_info):
	phone_number = form.cleaned_data['phone_number']

	# Add user's phone number to the appt in session
	appt_info.update({'phone_number': phone_number})
	request.session['appointment'] = appt_info
	return

def storeAppointment(appt_info):
	sig_name = appt_info.get('sig_name', None)
	dob_date = appt_info.get('dob_date', None)
	delivery_date = appt_info.get('delivery_date', None)
	sig_image = appt_info.get('sig_image', None)
	phone_number = appt_info.get('phone_number', None)
	print sig_name
	print dob_date
	print delivery_date
	print len(sig_image)
	print phone_number
	return