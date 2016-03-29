from django.http import HttpResponse

from django.shortcuts import render, redirect

# Indicates that the user has finished all the videos
finished_videos_index = 10

def index(request):
	return render(request, 'index.html', {})

# User answers questions about postpartum needs
def personalizedCare(request):
	if request.method == 'GET':
		return render(request, 'personalizedCare.html', {})
	elif request.method == 'POST':
		# Add a list of the required videos to the session
		request.session['required_videos'] = [1, 4, 6, 8, 10]
		# Do POST SHIT => redirect to important information
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

# Displays intro message for commit and schedule page
def commitAndScheduleIntro(request):
	return render(request, 'commitAndScheduleIntro.html', {})

# User enters in delivery date 
def commitAndScheduleDeliveryDate(request):
	if request.method == 'GET':
		return render(request, 'commitAndScheduleDeliveryDate.html', {})
	elif request.method == 'POST':
		return redirect('/cs/calendar/')

# User selects an appt from calendar 
def commitAndScheduleCalendar(request):
	return render(request, 'commitAndScheduleCalendar.html', {})

# User signs and confirms appt 
def commitAndScheduleSignature(request):
	if request.method == 'GET':
		return render(request, 'commitAndScheduleSignature.html', {})
	elif request.method == 'POST':
		return redirect('/incentive/')

# Displays incentive message and user provides phone number
def incentive(request):
	if request.method == 'GET':
		return render(request, 'incentive.html', {})
	elif request.method == 'POST':
		return redirect('/final/')

# Displays final message to the user
def final(request):
	return render(request, 'final.html', {})
