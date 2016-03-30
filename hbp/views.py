from django.http import HttpResponse

from django.shortcuts import render, redirect

from .forms import DeliveryDateForm, SignatureForm

# Indicates that the user has finished all the videos
finished_videos_index = 10

# Session values
# 	=> required_videos = list of required videos for the user to watch
#	=> appointment = {delivery_date, name, date_of_birth, 
#					  signature, appointment_info, phone_number}

def index(request):
	return render(request, 'index.html', {})

# User answers questions about postpartum needs
def personalizedCare(request):
	if request.method == 'GET':
		return render(request, 'personalizedCare.html', {})
	elif request.method == 'POST':
		# Add a list of the required videos to the session
		request.session['required_videos'] = [1, 4, 6, 8, 10]
		return redirect('/iv/')

# User watches informational videos 
def informationalVideos(request, video_index=0):
	try:	
		video_index = int(video_index)
		# Check to see if they have finished all their required videos
		next_video = 0
		finished_videos = True
		required_videos = request.session.get('required_videos')
		# They jumped directly to this page
		if (required_videos == None):
			return redirect('/')	
		# They still have required videos to watch		
		elif (len(required_videos) != 0):
			next_video = required_videos[0]
			finished_videos = False
			# Remove the next video from the list of required videos
			request.session['required_videos'] = required_videos[1:]

		return render(request, 'importantInformation.html', {'video_index': video_index, 
						'finished_videos': finished_videos, 'next_video': next_video})
	except ValueError as e:
		print e
		return redirect('/')

# Displays intro message for commit and schedule page
def commitAndScheduleIntro(request):
	return render(request, 'commitAndScheduleIntro.html', {})

# User enters in delivery date 
def commitAndScheduleDeliveryDate(request):
	if request.method == 'GET':
		form = DeliveryDateForm()
		return render(request, 'commitAndScheduleDeliveryDate.html', {'form': form})
	elif request.method == 'POST':
		# Process the DeliveryDateForm data
		form = DeliveryDateForm(request.POST)
		if form.is_valid():
			delivery_day = form.cleaned_data['delivery_day']
			delivery_month = form.cleaned_data['delivery_month']
			delivery_year = form.cleaned_data['delivery_year']

			# Keep track of the user's appointment info in the session
			delivery_date = delivery_month + '/' + delivery_day + '/' + delivery_year
			request.session['appointment'] = {'delivery_date': delivery_date}

			return redirect('/cs/calendar/')
		else:
			# form is invalid, need to display errors to the user
			print form.errors
			return redirect('/')

# User selects an appt from calendar 
def commitAndScheduleCalendar(request):
	return render(request, 'commitAndScheduleCalendar.html', {})

# User signs and confirms appt 
def commitAndScheduleSignature(request):
	if request.method == 'GET':
		form = SignatureForm()
		return render(request, 'commitAndScheduleSignature.html', {'form': form})
	elif request.method == 'POST':
		# Process the SignatureForm data
		form = SignatureForm(request.POST, request.FILES)
		if form.is_valid():
			sig_name = form.cleaned_data['sig_name']
			dob_day = form.cleaned_data['dob_day']
			dob_month = form.cleaned_data['dob_month']
			dob_year = form.cleaned_data['dob_year']
			sig_image = form.cleaned_data['sig_image']
			print len(sig_image)

			# Add user's appointment info to the session
			dob_date = dob_month + '/' + dob_day + '/' + dob_year
			temp_appointment = request.session['appointment']
			temp_appointment.update({'sig_name': sig_name, 
				'dob_date': dob_date})
			request.session['appointment'] = temp_appointment
			return redirect('/incentive/')
		else:
			# form is invalid, need to display errors to the user
			print form.errors
			return redirect('/')

# Displays incentive message and user provides phone number
def incentive(request):
	print request.session.get('appointment')
	if request.method == 'GET':
		return render(request, 'incentive.html', {})
	elif request.method == 'POST':
		return redirect('/final/')

# Displays final message to the user
def final(request):
	return render(request, 'final.html', {})
