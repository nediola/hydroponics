# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, redirect
from mainpageapp.models import Plant, Mix, GardenBed
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf

# Create your views here.

def authenticate(request):
	view = 'auth'
	return render_to_response('auth.html', {'name':view, 'username':auth.get_user(request).username})

def login(request):
	args = {}
	#args.update(csrf(request))
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request, user)
			return redirect('/')
		else:
			args['login_error'] = "User not found"
    		return render_to_response('auth.html', args)
	else:
		return render_to_response('main.html', args)
	
	return

def logout(request):
	auth.logout(request)
	args = {}
	return redirect('/')