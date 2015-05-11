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
from django.db.models import Max

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
	# Get data about gardenbeds from database and create home page
	max_x = GardenBed.objects.all().aggregate(Max('gardenbed_posx'))
	max_y = GardenBed.objects.all().aggregate(Max('gardenbed_posy'))
	gardenbed_posx_max = max_x['gardenbed_posx__max']
	gardenbed_posy_max = max_y['gardenbed_posy__max']
	gardenbeds_list = []
	for y in xrange(gardenbed_posy_max):
		for x in xrange(gardenbed_posx_max):
			gardenbeds = GardenBed.objects.filter(gardenbed_posx=x+1, gardenbed_posy=y+1)
			if (len(gardenbeds) == 0):
				gardenbeds_list.append(GardenBed(gardenbed_posx=x+1, gardenbed_posy=y+1))
			else:
				for g in gardenbeds:
					gardenbeds_list.append(g)	
	return render_to_response('home.html', {'gardenbeds' : gardenbeds_list, 'gardenbed_posx_max' : gardenbed_posx_max,
		'gardenbed_posy_max' : gardenbed_posy_max})