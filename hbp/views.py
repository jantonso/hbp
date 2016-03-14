from django.http import HttpResponse

from django.shortcuts import render, redirect

def index(request):
	return render(request, 'index.html', {})

def personalizedCare(request):
	if request.method == 'GET':
		return render(request, 'personalizedCare.html', {})
	elif request.method == 'POST':
		# Do POST SHIT => redirect to important information
		return redirect('/iv/')

def informationalVideos(request, video_index=0):
	try:
		video_index = int(video_index)
		return render(request, 'importantInformation.html', {'video_index': video_index})
	except ValueError as e:
		print e
