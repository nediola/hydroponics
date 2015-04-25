from django.db import models

class Plant(models.Model):
	class Meta():
		db_table = 'plant'
	plant_name = models.CharField(max_length=256, unique=True)
	plant_description = models.TextField()

class Mix(models.Model):
	class Meta():
		db_table = 'mix'
	mix_name = models.CharField(max_length=256, unique=True)
	mix_description = models.CharField(max_length=256)

class GardenBed(models.Model):
	class Meta():
		db_table = 'gardenbed'
	gardenbed_plant = models.ForeignKey(Plant)
	gardenbed_mix = models.ForeignKey(Mix)