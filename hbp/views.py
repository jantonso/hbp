from django.http import HttpResponse

from django.shortcuts import render, redirect

# The index that indicates the user has finished all the videos
finished_videos_index = 3

def index(request):
	return render(request, 'index.html', {})

def personalizedCare(request):
	if request.method == 'GET':
		return render(request, 'personalizedCare.html', {})
	elif request.method == 'POST':
		# Create session to keep track of if the user has watched all their required videos
		request.session['finished_videos'] = False
		# Do POST SHIT => redirect to important information
		return redirect('/iv/')

def informationalVideos(request, video_index=0):
	try:		
		finished_videos = False
		# Check to see if they have finished all their videos
		if (request.session.get('finished_videos', False)):
			finished_videos = True

		video_index = int(video_index)
		if (not finished_videos):
			# Update the session to reflect that they have finished all the videos
			if (video_index == finished_videos_index):
				request.session['finished_videos'] = True
				finished_videos = True

		return render(request, 'importantInformation.html', {'video_index': video_index, 
						'finished_videos': finished_videos})
	except ValueError as e:
		print e

def commitAndSchedule(request):
	if request.method == 'GET':
		return render(request, 'commitAndSchedule.html', {})
	elif request.method == 'POST':
		return redirect('/incentive/')

def incentive(request):
	if request.method == 'GET':
		return render(request, 'incentive.html', {})
	elif request.method == 'POST':
		return redirect('/final/')

def final(request):
	return render(request, 'final.html', {})
