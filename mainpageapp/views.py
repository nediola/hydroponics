# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, redirect
from mainpageapp.models import Plant, Mix, GardenBed
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib import auth

def enter(request):
	if request.user.is_authenticated():
		return redirect('/home')
	else:
		return redirect('/auth')

def authenticate(request):
	return render_to_response('auth.html')

def login(request):
	args = {}
	#args.update(csrf(request))
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request, user)
			return redirect('/home')
		else:
			args['login_error'] = "User not found"
    		return render_to_response('auth.html', args)
	else:
		args['login_error'] = "Not POST request"
    	return render_to_response('auth.html', args)

def logout(request):
	auth.logout(request)
	return redirect('/')

def home(request):
	return render_to_response('home.html')
	

    