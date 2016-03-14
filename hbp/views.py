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

def informationalVideos(request):
	return render(request, 'importantInformation.html', {})