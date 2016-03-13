from django.http import HttpResponse

from django.shortcuts import render

def index(request):
	return render(request, 'index.html', {})

def personalizedCare(request):
	if request.method == 'GET':
		return render(request, 'personalizedCare.html', {})
	elif request.method == 'POST':
		# Do POST SHIT => redirect to important information
		return render(request, 'importantInformation.html', {})

 
