from django.contrib import admin
from mainpageapp.models import Plant, GardenBed, Mix

# Register your models here.
admin.site.register(Plant)
admin.site.register(GardenBed)
admin.site.register(Mix)