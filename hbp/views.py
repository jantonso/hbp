from django.http import HttpResponse
from django.http import Http404

from django.shortcuts import render, redirect

from django.core import serializers
from django.core.files.base import ContentFile

from django.conf import settings

from datetime import datetime, timedelta

from .forms import *
from .models import *

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, Image
from reportlab.lib import colors

import uuid
import os
import csv

# Indicates that the user has finished all the videos since there are 9 total videos
finished_videos_index = 10

# Session values
# 	=> required_videos = list of required videos for the user to watch
#	=> required_topics = list of required_topics that the user wants to learn about
#	=> appointment = {delivery_date, sig_name, dob_date, 
#					  signature, phone_number, appt_id, appt_date, appt_time}
#   => consent_info = {participant_name, participant_date, participant_sig,
#					   obtaining_name, obtaining_role, obtaining_date, 
#					   obtaining_sig}
#   => answer_info = user's answer responses

# ---------------------------------------------------------------------------------------- #
# ---------------------------------- Index Page ------------------------------------------ #
# ---------------------------------------------------------------------------------------- #
def index(request):
	return render(request, 'index.html', {})

# ---------------------------------------------------------------------------------------- #
# --------------------------------- Consent Page ----------------------------------------- #
# ---------------------------------------------------------------------------------------- #
# Participant of the experiment and person running the experiment read consent page
# and both sign providing consent
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
			error_msg = 'Please enter all the required information.'
			return render(request, 'consent.html', 
				{'form': form, 'error_msg': error_msg})

# ---------------------------------------------------------------------------------------- #
# ---------------------------- Personalized Care Page ------------------------------------ #
# ---------------------------------------------------------------------------------------- #
# User answers questions about postpartum needs that we use to determine what 
# topics they are most interested in and what videos we should make them watch 
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
			return render(request, 'personalizedCare.html', {'form': form})

# ---------------------------------------------------------------------------------------- #
# ---------------------------- Informational Videos Page --------------------------------- #
# ---------------------------------------------------------------------------------------- #
# User watches informational videos on the required topics that they marked as important
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
		return redirect('/')

# ---------------------------------------------------------------------------------------- #
# ---------------------------- Commit & Schedule Intro Page ------------------------------ #
# ---------------------------------------------------------------------------------------- #
# Displays intro message for commit and schedule page and prompts user to commit
def commitAndScheduleIntro(request):
	# Keep track of the appointment info in the user's session
	request.session['appointment'] = {}
	return render(request, 'commitAndScheduleIntro.html', {})

# ---------------------------------------------------------------------------------------- #
# ------------------------ Commit & Schedule Delivery Date Page -------------------------- #
# ---------------------------------------------------------------------------------------- #
# User enters in their delivery date 
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
			error_msg = 'Please enter a valid date.'
			return render(request, 'commitAndScheduleDeliveryDate.html', 
				{'form': form, 'error_msg': error_msg })

# ---------------------------------------------------------------------------------------- #
# -------------------------- Commit & Schedule Calendar Page ----------------------------- #
# ---------------------------------------------------------------------------------------- #
# User selects an appointment from a calendar of available appointments
def commitAndScheduleCalendar(request):
	# Check to make sure they didn't just jump directly to this page
	appt_info = request.session.get('appointment', None)
	delivery_date = appt_info.get('delivery_date', None)
	if (appt_info == None or delivery_date == None):
		print ("There was no appointment in the session")
		return redirect('/')

	if request.method == 'GET':
		form = CalendarForm()

		# Pull the appointments from the db that are 6/10 weeks from delivery date
		delivery_datetime = datetime.strptime(delivery_date, '%m/%d/%Y')
		min_date = delivery_datetime + timedelta(days=21)
		max_date = delivery_datetime + timedelta(days=56)

		all_appts = Appointment.objects.filter(appt_datetime__gte=min_date,
			appt_datetime__lte=max_date).order_by('appt_datetime')
		
		appointments = serializers.serialize('json', all_appts)
		return render(request, 'commitAndScheduleCalendar.html', 
			{'appointments': appointments, 'form': form})
	elif request.method == 'POST':
		# Process the CalendarForm data
		form = CalendarForm(request.POST)
		if form.is_valid():
			handleCalendarForm(request, form, appt_info)
			return redirect('/cs/signature/')
		else:
			# Just refresh the calendar on an error
			return redirect('/cs/calendar/')

# ---------------------------------------------------------------------------------------- #
# -------------------------- Commit & Schedule Signature Page ---------------------------- #
# ---------------------------------------------------------------------------------------- #
# User enters name, date of birth, and signs to confirm the appointment
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
			error_msg = 'Please enter all the required information.'
			return render(request, 'commitAndScheduleSignature.html', 
				{'form': form, 'error_msg': error_msg})

# ---------------------------------------------------------------------------------------- #
# -------------------------------- Incentive Page ---------------------------------------- #
# ---------------------------------------------------------------------------------------- #
# Displays incentive message to the user and user provides their phone number
def incentive(request):
	# Check to make sure they didn't just jump directly to this page
	# and actually scheduled an appointment / answered all the questions
	appt_info = request.session.get('appointment', None)
	appt_date = appt_info.get('appt_date', None)
	appt_time = appt_info.get('appt_time', None)
	answer_info = request.session.get('answer_info', None)
	if (appt_info == None or appt_date == None or appt_time == None or 
		answer_info == None):
		print ("There was no appointment scheduled in the session or no answers")
		return redirect('/')

	if request.method == 'GET':
		form = PhoneNumberForm()
		return render(request, 'incentive.html', 
			{'form': form, 'appt_date': appt_date, 'appt_time': appt_time})
	elif request.method == 'POST':
		# Process the PhoneNumberForm data
		form = PhoneNumberForm(request.POST)
		if form.is_valid():
			handlePhoneNumberForm(request, form, appt_info)
			storeInformation(appt_info, answer_info)
			return redirect('/final/')
		else:
			error_msg = 'Please enter a valid phone number.'
			return render(request, 'incentive.html', 
				{'form': form, 'appt_date': appt_date, 'appt_time': appt_time, 'error_msg': error_msg})		

# ---------------------------------------------------------------------------------------- #
# ------------------------------------- Final Page --------------------------------------- #
# ---------------------------------------------------------------------------------------- #
# Displays final information to user about their scheduled appointment
def final(request):
	required_topics = request.session.get('required_topics', None)
	appt_info = request.session.get('appointment', None)
	appt_date = appt_info.get('appt_date', None)
	appt_time = appt_info.get('appt_time', None)
	# They jumped directly to this page or did not schedule an appointment
	if (appt_info == None or appt_date == None or appt_time == None or required_topics == None):
		print ("There were no required topics / no appointment")
		return redirect('/')	
	return render(request, 'final.html', 
		{'required_topics': required_topics, 'appt_date': appt_date, 'appt_time': appt_time})

# ---------------------------------------------------------------------------------------- #
# ---------------------------------- Printing Appt --------------------------------------- #
# ---------------------------------------------------------------------------------------- #
# Allows the user to print their appointment info on the final page
def printAppt(request):
	appt_info = request.session.get('appointment', None)
	answer_info = request.session.get('answer_info', None)

	if (appt_info == None or answer_info == None):
		raise Http404

	# Build the response PDF
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'inline; filename="appointment_info.pdf"'
	
	p = canvas.Canvas(response, pagesize=letter)
	width, height = letter

	# Add the appointment info to the pdf
	a = printAppointment(p, width, height, appt_info, answer_info)
	if not a:
		raise Http404

	consent_info = request.session.get('consent_info', None)
	# If the user filled out the consent form, add this info to the pdf
	if (consent_info != None):
		c = printConsentInfo(p, width, height, consent_info)
		if not c:
			raise Http404

	p.save()

	return response

# ---------------------------------------------------------------------------------------- #
# -------------------------------- Importing Appts --------------------------------------- #
# ---------------------------------------------------------------------------------------- #
# Allows an admin user to import a csv file of appointments
def importAppts(request):
	# Make sure that the user is an admin user and that it is is a POST request
	if not request.user.is_superuser or not request.method == 'POST':
		raise Http404

	form = ImportApptsForm(request.POST, request.FILES)
	if form.is_valid():
		reader = csv.DictReader(form.cleaned_data['appt_file'])
		formats = ['%m/%d/%Y %I%p', '%m/%d/%y %I%p']
		for row in reader:
			appt_date = row['appt_date']
			appt_time = row['appt_time']
			unit_name = row['unit_name']
			able_to_add = False
			for f in formats:
				try:
					appt_datetime = datetime.strptime(
						appt_date + " " + appt_time , f)
					new_appointment = Appointment(unit_name=unit_name,
						appt_datetime=appt_datetime, 
						appt_date=appt_datetime.strftime("%m/%d/%Y"),
						appt_time=appt_time)
					new_appointment.save()
					able_to_add = True
				except ValueError as e:
					continue
			if not able_to_add:
				print "This row wasn't parsed correctly..."
	# Redirect to the admin page that sent the request here
	return redirect(request.META['HTTP_REFERER'])

# ---------------------------------------------------------------------------------------- #
# ---------------------------------- Helper Functions ------------------------------------ #
# ---------------------------------------------------------------------------------------- #

# Stores the consent form information in the DB in the correct format
def	handleConsentForm(request, form):
	participant_name = form.cleaned_data['participant_name']
	participant_date = form.cleaned_data['participant_date']
	participant_sig = form.cleaned_data['participant_sig']

	obtaining_name = form.cleaned_data['obtaining_name']
	obtaining_role = form.cleaned_data['obtaining_role']
	obtaining_date = form.cleaned_data['obtaining_date']
	obtaining_sig = form.cleaned_data['obtaining_sig']

	request.session['consent_info'] = {'participant_name': participant_name,
		'participant_date': participant_date, 'participant_sig': participant_sig,
		'obtaining_name': obtaining_name, 'obtaining_role': obtaining_role,
		'obtaining_date': obtaining_date, 'obtaining_sig': obtaining_sig}

	return

# ALGORITHM TO DETERMINE THE REQUIRED TOPICS/VIDEOS 
# Choose up to the 5 maximum values for the topics, if there are less than 2, choose 2 default ones
# Likert = -2, -1, 0, 1, 2 ====> not at all, not really, somewhat, important, very important
# Non-Likert = -2, 0, 2 ====> no, don't know, yes
def handlePersonalizedCareForm(request, form):
	list_of_questions = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9']
	list_of_topics = ['birth control', 'breastfeeding support', 'checking on my mood', 'planning my next pregnancy',
				  'sexual activity after birth', 'bowel and bladder health', 
				  'gestational diabetes', 'high blood pressure', 'preterm delivery']
	default_videos = [1, 3]
	answers = {}
	for i in xrange(0,len(list_of_questions)):
		question_name = list_of_questions[i]
		question_answer = form.cleaned_data[question_name]	

		try:
			answer_value = int(question_answer)
			# Don't add values that were marked 'not important' or 'no'
			if (answer_value >= 0):
				answers[i+1] = answer_value
		# If they forgot to answer one, skip that question
		except ValueError:
			continue

	# Choose the top five rated topics and videos
	required_videos = sorted(answers, key=answers.get, reverse=True)[:3]

	# If there are less than 2 required videos, choose the default ones
	# make sure not to choose duplicate videos if there was 1 required video chosen
	# by the user
	if (len(required_videos) == 0):
		required_videos = default_videos
	elif (len(required_videos) == 1):
		if (required_videos[0] in default_videos):
			default_videos.remove(required_videos[0])
		required_videos += [default_videos[0]]

	print required_videos

	required_topics = [list_of_topics[index-1] for index in required_videos]	

	# Add the final index to indicate that all the videos were finished
	required_videos += [finished_videos_index]

	# Add a list of the required videos and their respective topics to the session
	request.session['required_videos'] = required_videos
	request.session['required_topics'] = required_topics
	request.session['answer_info'] = answers

	return

# Adds the user's delivery date to the appointment info in the user's session
def handleDeliveryDateForm(request, form, appt_info):
	delivery_date = form.cleaned_data['delivery_date']
	appt_info.update({'delivery_date': delivery_date})
	request.session['appointment'] = appt_info
	return

# Adds the user's chosen appointment to the appointment info in the user's session
def handleCalendarForm(request, form, appt_info):
	appt_id = form.cleaned_data['appt_id']
	appt_date = form.cleaned_data['appt_date']
	appt_time = form.cleaned_data['appt_time']

	appt_info.update({'appt_id': appt_id, 'appt_date': appt_date, 'appt_time': appt_time})
	request.session['appointment'] = appt_info
	return

# Adds the user's name, dob, and signature to the appointment info in the user's session
def handleSignatureForm(request, form, appt_info):
	sig_name = form.cleaned_data['sig_name']
	dob_date = form.cleaned_data['dob_date']
	sig_image = form.cleaned_data['sig_image']

	appt_info.update({'sig_name': sig_name, 
		'dob_date': dob_date, 'sig_image': sig_image})
	request.session['appointment'] = appt_info
	return

# Adds the user's phone number to the appointment info in the user's session
def handlePhoneNumberForm(request, form, appt_info):
	phone_number = form.cleaned_data['phone_number']

	# Add user's phone number to the appt in session
	appt_info.update({'phone_number': phone_number})
	request.session['appointment'] = appt_info
	return

# Stores the scheduled appointment, user info, and answer results in DB
def storeInformation(appt_info, answer_info):
	sig_name = appt_info.get('sig_name', None)
	dob_date = appt_info.get('dob_date', None)
	delivery_date = appt_info.get('delivery_date', None)
	sig_image = appt_info.get('sig_image', None)
	phone_number = appt_info.get('phone_number', None)
	appt_id = appt_info.get('appt_id', None)

	# Format is for example: 03/02/2016
	# Store the patient info in the db
	#dob_datetime = datetime.strptime(dob_date_str, "%m/%d/%Y");
	#delivery_datetime = datetime.strptime(delivery_date_str, "%m/%d/%Y");
	p = Patient(name=sig_name, dob_date=dob_date, 
		delivery_date=delivery_date, phone_number=phone_number)

	# Update the appointment that was booked for this patient
	a = Appointment.objects.get(pk=appt_id)
	a.booked = True
	a.save()

	p.appointment = a

	# Store the patient's answers to the personalized care question
	answers = getAnswerValues(answer_info)

	personalized_care_answers = PersonalizedCareAnswers()
	personalized_care_answers.q1 = answers[0]
	personalized_care_answers.q2 = answers[1]
	personalized_care_answers.q3 = answers[2]
	personalized_care_answers.q4 = answers[3]
	personalized_care_answers.q5 = answers[4]
	personalized_care_answers.q6 = answers[5]
	personalized_care_answers.q7 = answers[6]
	personalized_care_answers.q8 = answers[7]
	personalized_care_answers.q9 = answers[8]
	personalized_care_answers.save()

	p.personalized_care_answers = personalized_care_answers

	p.save()

	return

def getAnswerValues(answer_info):
	answers = ['no answer', 'no answer', 'no answer', 'no answer', 'no answer',
		'no answer', 'no answer', 'no answer', 'no answer']
	likert_choices = ['not at all', 'not really', 'somewhat', 'important', 'very important']

	for key, value in answer_info.iteritems():
		try:
			question_number = int(key)
			# Yes/No question
			if (question_number >= 7 and question_number <= 9):
				if (value == 2):
					answers[question_number-1] = 'yes'
				elif (value == 0):
					answers[question_number-1] = 'don\'t know'
				else:
					answers[question_number-1] = 'no'
			# Likert question
			else:
				answers[question_number-1] = likert_choices[value+2]
		except ValueError:
			continue

	return answers

def storeAnswers(answer_info):
	
	answers = getAnswerValues(answer_info)

	a = PersonalizedCareAnswers()
	a.q1 = answers[0]
	a.q2 = answers[1]
	a.q3 = answers[2]
	a.q4 = answers[3]
	a.q5 = answers[4]
	a.q6 = answers[5]
	a.q7 = answers[6]
	a.q8 = answers[7]
	a.q9 = answers[8]
	a.save()

	return a

# Adds the appointment information to the pdf to be printed
def printAppointment(p, width, height, appt_info, answer_info):
	sig_name = appt_info.get('sig_name', None)
	delivery_date = appt_info.get('delivery_date', None)
	dob_date = appt_info.get('dob_date', None)
	sig_image = appt_info.get('sig_image', None)
	phone_number = appt_info.get('phone_number', None)
	appt_date = appt_info.get('appt_date', None)
	appt_time = appt_info.get('appt_time', None)

	if (sig_name == None or delivery_date == None or dob_date == None 
		or sig_image == None or phone_number == None or appt_date == None
		or appt_time == None):
		return False

	first_col_width = 100
	second_col_width = 250
	third_col_width = 400

	# Header
	current_height = height - 40
	drawHeader(p, width/2-95, current_height, 'Appointment Information')

	# First row
	top_height = current_height - 30
	bot_height = current_height - 45

	drawFieldLabel(p, first_col_width, top_height, 'Name')
	drawFieldValue(p, first_col_width, bot_height, sig_name)

	drawFieldLabel(p, second_col_width, top_height, 'Date of birth')
	drawFieldValue(p, second_col_width, bot_height, dob_date)

	drawFieldLabel(p, third_col_width, top_height, 'Phone number')
	drawFieldValue(p, third_col_width, bot_height, phone_number)

	# Second row
	top_height = bot_height - 30
	bot_height = bot_height - 45

	drawFieldLabel(p, first_col_width, top_height, 'Date of delivery')
	drawFieldValue(p, first_col_width, bot_height, delivery_date)

	drawFieldLabel(p, second_col_width, top_height, 'Appt date')
	drawFieldValue(p, second_col_width, bot_height, appt_date)

	drawFieldLabel(p, third_col_width, top_height, 'Appt time')
	drawFieldValue(p, third_col_width, bot_height, appt_time)

	# Third row
	top_height = bot_height - 30
	current_height = drawSignature(p, sig_image, first_col_width, top_height)

	# Fourth row
	top_height = current_height - 30

	drawQuestionsAndAnswer(p, answer_info, first_col_width, top_height)

	p.showPage()

	return True

# Adds the consent information to the pdf to be printed
def printConsentInfo(p, width, height, consent_info):
	participant_name = consent_info.get('participant_name', None)
	participant_date = consent_info.get('participant_date', None)
	participant_signature = consent_info.get('participant_sig', None)
	obtaining_name = consent_info.get('obtaining_name', None)
	obtaining_role = consent_info.get('obtaining_role', None)
	obtaining_date = consent_info.get('obtaining_date', None)
	obtaining_signature = consent_info.get('obtaining_sig', None)

	if (participant_name == None or participant_date == None 
		or participant_signature == None or obtaining_name == None
		or obtaining_role == None or obtaining_date == None
		or obtaining_signature == None):
		return False

	first_col_width = 100
	second_col_width = 250
	third_col_width = 400

	# Header
	current_height = height - 40
	drawHeader(p, width/2-80, current_height, 'Consent Information')

	# First row
	top_height = current_height - 30
	bot_height = current_height - 45

	drawFieldLabel(p, first_col_width, top_height, 'Name of participant')
	drawFieldValue(p, first_col_width, bot_height, participant_name)

	drawFieldLabel(p, third_col_width, top_height, 'Date')
	drawFieldValue(p, third_col_width, bot_height, participant_date)

	# Second row
	top_height = bot_height - 30
	current_height = drawSignature(p, participant_signature, first_col_width, top_height)

	# Third row
	top_height = current_height - 30
	bot_height = current_height - 45

	drawFieldLabel(p, first_col_width, top_height, 'Name of person obtaining consent')
	drawFieldValue(p, first_col_width, bot_height, obtaining_name)

	drawFieldLabel(p, third_col_width, top_height, 'Date')
	drawFieldValue(p, third_col_width, bot_height, obtaining_date)
	
	# Fourth row
	top_height = bot_height - 30
	bot_height = bot_height - 45

	drawFieldLabel(p, first_col_width, top_height, 'Role of person obtaining consent')
	drawFieldValue(p, first_col_width, bot_height, obtaining_role)

	# Fifth row
	top_height = bot_height - 30
	drawSignature(p, obtaining_signature, first_col_width, top_height)

	return True

def drawHeader(p, width, height, header):
	p.setFont('Helvetica-Bold', 16)
	p.drawString(width, height, header)
	return

def drawFieldLabel(p, width, height, label):
	p.setFont('Helvetica-Bold', 12)
	p.drawString(width, height, label)
	return

def drawFieldValue(p, width, height, value):
	p.setFont('Helvetica', 12)
	p.drawString(width, height, value)
	return

def drawSignature(p, signature, current_width, current_height):
	p.setFont('Helvetica-Bold', 12)
	p.drawString(100, current_height, 'Signature')
	
	img_width = 400
	img_height = 120
	img = Image(signature, width=img_width, height=img_height)
	img_table = Table(data=[[img]], colWidths=img_width, rowHeights=img_height,
    	style=[
	        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
	        ('BOX', (0, 0), (0, 0), 0.5, colors.black),
	        ('VALIGN', (0, 0), (0, 0), 'MIDDLE'),
	    ]
	)

	current_height = current_height - img_height - 10
	img_table.wrapOn(p, img_width, img_height)
	img_table.drawOn(p, current_width, current_height)

	return current_height

def	drawQuestionsAndAnswer(p, answer_info, first_col_width, top_height):
	questions = ['Getting birth control:', 'Breastfeeding support:', 'Checking on my mood after delivery:', 
		'Planning my next pregnancy:', 'Sexual activity after birth:', 
		'Discussing issues of bowel or bladder health:',
		'Did you have gestational diabetes during this pregnancy?',
		'Did you have high blood pressure during this pregnancy?',
		'Did you have a preterm delivery during this pregnancy?']
	answers = getAnswerValues(answer_info)

	bot_height = top_height - 15
	for i in xrange(0, len(questions)):
		drawFieldLabel(p, first_col_width, top_height, questions[i])
		drawFieldValue(p, first_col_width + 15, bot_height, answers[i])
		top_height -= 40
		bot_height -= 40

# Used to add appointments to the DB programatically
def createMockAppointments():
	appointment_dates = ["04/19/2016", "04/19/2016", "04/19/2016",
	"04/19/2016", "04/19/2016", "04/10/2016", "04/13/2016", "04/13/2016", "04/11/2016","05/02/2016","05/02/2016"]
	appointment_times = ["10am", "12pm", "2pm", "3pm", "5pm","12pm","2pm","4pm","10am","2pm","3pm"]
	for i in xrange(0,len(appointment_dates)):
		print i
		appt_datetime = datetime.strptime(
			appointment_dates[i] + " " + appointment_times[i] , "%m/%d/%Y %I%p")
		new_appointment = Appointment(unit_name="Blue U",
			appt_datetime=appt_datetime, appt_date=appointment_dates[i],
			appt_time=appointment_times[i])
		new_appointment.save()
	print "done"
	return
