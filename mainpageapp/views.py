# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, redirect
from mainpageapp.models import Plant, Mix, GardenBed, Ingredient
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib import auth
from django.db.models import Max
from django.http import JsonResponse
import json
import string

gardenbed_y_names = list(string.ascii_uppercase)

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
				#create new gardenbed
				gardenbed_name = str(x+1) + gardenbed_y_names[y]
				empty_gardenbed = GardenBed.objects.create(gardenbed_posx=x+1, gardenbed_posy=y+1, 
					gardenbed_name = gardenbed_name)
				#empty_gardenbed = GardenBed(gardenbed_posx=x+1, gardenbed_posy=y+1)
				gardenbeds_list.append(empty_gardenbed)
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
		if (req_type == 'ingredients'):
			return JsonResponse(get_ingredients_json())
		if (req_type == 'ingredient_description'):
			return JsonResponse(get_ingredient_description_json(decoded_json['ingredient_id']))
		return JsonResponse({'error':'unknown type of request'})

def get_gardenbed_json(gardenbed_id):
	resp_data = {}
	gardenbed = GardenBed.objects.get(id=gardenbed_id)
	resp_data['gardenbed_name'] = gardenbed.gardenbed_name
	if gardenbed.gardenbed_plant is not None:
		resp_data['gardenbed_plant_id'] = gardenbed.gardenbed_plant.id
		resp_data['gardenbed_plant_description'] = gardenbed.gardenbed_plant.plant_description
	if gardenbed.gardenbed_time is not None:
		resp_data['gardenbed_time'] = gardenbed.gardenbed_time
	if gardenbed.gardenbed_mix is not None:
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

def get_ingredients_json():
	resp_data = {}
	ingredients_names = {}
	ingredients = Ingredient.objects.all()
	for i in ingredients:
		ingredients_names[i.id] = i.ingredient_name
	resp_data['ingredients'] = ingredients_names
	return resp_data

def get_ingredient_description_json(ingredient_id):
	resp_data = {}
	ingredient = Ingredient.objects.get(id=ingredient_id)
	resp_data['ingredient_description'] = ingredient.ingredient_description
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
	if (decoded_json['gardenbed_plant_id']):
		gardenbed.gardenbed_plant = Plant.objects.get(id=decoded_json['gardenbed_plant_id'])
	else:
		gardenbed.gardenbed_plant = None
	if (decoded_json['gardenbed_mix_id']):
		gardenbed.gardenbed_mix = Mix.objects.get(id=decoded_json['gardenbed_mix_id'])
	else:
		gardenbed.gardenbed_mix = None
	if (decoded_json['gardenbed_time']):
		gardenbed.gardenbed_time = decoded_json['gardenbed_time']
	else:
		gardenbed.gardenbed_time = None
	gardenbed.save()
	return {'status':'Saved'}

def set_plants(request):
	if (request.method == "POST" and request.is_ajax()):
		str_json = request.body
		decoded_json = json.loads(str_json)
		req_type = decoded_json['type']
		if (req_type == 'new'):
			return JsonResponse(set_plants_new_json(decoded_json))
		if (req_type == 'save'):
			return JsonResponse(set_plants_save_json(decoded_json))
		if (req_type == 'delete'):
			return JsonResponse(set_plants_delete_json(decoded_json))
		return JsonResponse({'error':'unknown type of request'})

def set_plants_new_json(decoded_json):
	print decoded_json
	plant = Plant.objects.create(
		plant_name=decoded_json['plant_name'],
		plant_description=decoded_json['plant_description'],
		plant_image_path = decoded_json['plant_image_path']
	)
	return {'status':'Added', 'id':plant.id}

def set_plants_save_json(decoded_json):
	plant = Plant.objects.get(id=decoded_json['plant_id'])
	if (decoded_json['plant_description']):
		plant.plant_description = decoded_json['plant_description']
	if (decoded_json['plant_image_path']):
		plant.plant_image_path = decoded_json['plant_image_path']
	plant.save()
	return {'status':'Saved'}

def set_plants_delete_json(decoded_json):
	plant = Plant.objects.get(id=decoded_json['plant_id'])
	plant.delete()
	return {'status':'Deleted'}

def set_ingredients(request):
	if (request.method == "POST" and request.is_ajax()):
		str_json = request.body
		decoded_json = json.loads(str_json)
		req_type = decoded_json['type']
		if (req_type == 'new'):
			return JsonResponse(set_ingredients_new_json(decoded_json))
		if (req_type == 'save'):
			return JsonResponse(set_ingredients_save_json(decoded_json))
		if (req_type == 'delete'):
			return JsonResponse(set_ingredients_delete_json(decoded_json))
		return JsonResponse({'error':'unknown type of request'})

def set_ingredients_new_json(decoded_json):
	print decoded_json
	ingredient = Ingredient.objects.create(
		ingredient_name=decoded_json['ingredient_name'],
		ingredient_description=decoded_json['ingredient_description']
	)
	return {'status':'Added', 'id':ingredient.id}

def set_ingredients_save_json(decoded_json):
	ingredient = Ingredient.objects.get(id=decoded_json['ingredient_id'])
	if (decoded_json['ingredient_description']):
		ingredient.ingredient_description = decoded_json['ingredient_description']
	ingredient.save()
	return {'status':'Saved'}

def set_ingredients_delete_json(decoded_json):
	ingredient = Ingredient.objects.get(id=decoded_json['ingredient_id'])
	ingredient.delete()
	return {'status':'Deleted'}