# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, redirect
from mainpageapp.models import Task, Base, Tank, Ingredient
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core.context_processors import csrf
from django.contrib import auth
import json

def load_base(request):
	args = {}
	base = Base.objects.get(id=1)
	if (base.base_temperature and
		base.base_humidity and
		base.base_sensor_time):
		args['temperature'] = base.base_temperature
		args['humidity'] = base.base_humidity
		args['sensor_time'] = base.base_sensor_time 
	args['tanks'] = Tank.objects.all()
	ingredients = Ingredient.objects.all()
	args['ingredients'] = ingredients
	return render_to_response('base.html', args)

def get_tasks(request):
	shell = {}
	tasks_for_base = []
	gardenbed_ids = {}
	if request.method == 'POST':
		base_login = request.POST['login']
		base_password = request.POST['password']
		base = auth.authenticate(username=base_login, password=base_password)
		if base is None:
			return JsonResponse({'error':'access denied'})
		if ('temperature' in request.POST and 
			'humidity' in request.POST and
			'sensor_time' in request.POST):
			base = Base.objects.get(id=1)
			base.base_temperature = request.POST['temperature']
			base.base_humidity = request.POST['humidity']
			base.base_sensor_time = request.POST['sensor_time']
			base.save()
		tasks = Task.objects.filter(task_sent_to_base=0)
		for t in tasks:
			tasks_for_base.append(t.task_json)
			gardenbed_ids[t.task_gardenbed_id] = 1
			t.task_sent_to_base = 1
			t.save #FIXME TEMP TO DEBUG. ADD: save()
		shell['gardenbed_ids'] = gardenbed_ids.keys()
		shell['tasks'] = tasks_for_base
		return JsonResponse(shell)
	else:
		return JsonResponse({'error':'unsupported type of request'})

def set_tanks(request):
	if request.method =='POST':
		tank_id = request.POST['tank_id']
		tank = Tank.objects.get(id=tank_id)
		tank.tank_ingredient_id = request.POST['tank_ingredient']
		tank.tank_current_volume = request.POST['tank_current_volume']
		tank.tank_max_volume = request.POST['tank_max_volume']
		tank.save()
	return redirect('/base/')