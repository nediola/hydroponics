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
from django.http import JsonResponse
import json

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
			gardenbeds = GardenBed.objects.filter(gardenbed_posx=x+1, gardenbed_posy=y+1) #FIXME it is awful
			if (len(gardenbeds) == 0):
				gardenbeds_list.append(GardenBed(gardenbed_posx=x+1, gardenbed_posy=y+1))
			else:
				for g in gardenbeds:
					gardenbeds_list.append(g)	
	return render_to_response('home.html', {'gardenbeds' : gardenbeds_list, 'gardenbed_posx_max' : gardenbed_posx_max,
		'gardenbed_posy_max' : gardenbed_posy_max})

def get_params(request):
	if (request.method == "POST" and request.is_ajax()):
		str_json = request.body
		decoded_json = json.loads(str_json)
		req_type = decoded_json['type']
		if (req_type == 'gardenbed'):
			return JsonResponse(get_gardenbed_json(decoded_json['gardenbed_id']))
		if (req_type == 'plants_mixs'):
			return JsonResponse(get_plants_mixs_json())
		if (req_type == 'plant_description'):
			return JsonResponse(get_plant_description_json(decoded_json['plant_id']))
		return JsonResponse({'error':'unknown type of request'})

def get_gardenbed_json(gardenbed_id):
	resp_data = {}
	gardenbed = GardenBed.objects.get(id=gardenbed_id)
	resp_data['gardenbed_name'] = gardenbed.gardenbed_name
	resp_data['gardenbed_plant_id'] = gardenbed.gardenbed_plant.id
	resp_data['gardenbed_plant_description'] = gardenbed.gardenbed_plant.plant_description
	resp_data['gardenbed_time'] = gardenbed.gardenbed_time
	resp_data['gardenbed_mix_id'] = gardenbed.gardenbed_mix.id
	return resp_data

def get_plants_mixs_json():
	resp_data = {}
	mixs_names = {}
	mixs = Mix.objects.all()
	for m in mixs:
		mixs_names[m.id] = m.mix_name
	resp_data['mixs'] = mixs_names
	plant_names = {}
	plants = Plant.objects.all()
	for p in plants:
		plant_names[p.id] = p.plant_name
	resp_data['plants'] = plant_names
	return resp_data

def get_plant_description_json(plant_id):
	resp_data = {}
	plant = Plant.objects.get(id=plant_id)
	resp_data['plant_description'] = plant.plant_description
	return resp_data

def set_params(request):
	if (request.method == "POST" and request.is_ajax()):
		str_json = request.body
		decoded_json = json.loads(str_json)
		req_type = decoded_json['type']
		if (req_type == 'set_gardenbed'):
			return JsonResponse(set_gardenbed_json(decoded_json))
		return JsonResponse({'error':'unknown type of request'})

def set_gardenbed_json(decoded_json):
	gardenbed = GardenBed.objects.get(id=decoded_json['gardenbed_id'])
	gardenbed.gardenbed_plant = Plant.objects.get(id=decoded_json['gardenbed_plant_id'])
	gardenbed.gardenbed_mix = Mix.objects.get(id=decoded_json['gardenbed_mix_id'])
	gardenbed.gardenbed_time = decoded_json['gardenbed_time']
	gardenbed.save() # this will update only
	return {'status':'Saved'}