# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http.response import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response, redirect
#from mainpageapp.models import Plant, Mix, GardenBed
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib import auth

# Create your views here.
def load_robot(request):
	return render_to_response('robot.html')