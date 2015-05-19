# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, redirect
from mainpageapp.models import Task
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.core.context_processors import csrf
from django.contrib import auth
import json

def load_base(request):
	return render_to_response('base.html')

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
		tasks = Task.objects.filter(task_sent_to_base=0)
		for t in tasks:
			tasks_for_base.append(t.task_json)
			gardenbed_ids[t.task_gardenbed_id] = 1
			t.task_sent_to_base = 1
			t.save() #FIXME TEMP TO DEBUG. ADD: save()
		shell['gardenbed_ids'] = gardenbed_ids.keys()
		shell['tasks'] = tasks_for_base
		return JsonResponse(shell)
	else:
		return JsonResponse({'error':'unsupported type of request'}) 