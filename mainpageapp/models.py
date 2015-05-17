from django.db import models
from django.forms import ModelForm

class Plant(models.Model):
	class Meta():
		db_table = 'plant'
	plant_name = models.CharField(max_length=256, unique=True)
	plant_description = models.TextField()
	plant_image_path = models.CharField(max_length=512, unique=True)

class Ingredient(models.Model):
	class Meta():
		db_table = 'ingredient'
	ingredient_name = models.CharField(max_length=256, unique=True)
	ingredient_description = models.TextField()

class Proportion(models.Model):
	class Meta():
		db_table = 'proportion'
	proportion_ingredient = models.ForeignKey(Ingredient, blank=True, null=True)
	proportion_ingredient_amount = models.IntegerField(default=0)

class Mix(models.Model):
	class Meta():
		db_table = 'mix'
	mix_name = models.CharField(max_length=256, unique=True)
	mix_description = models.CharField(max_length=256)
	mix_proportions = models.ManyToManyField(Proportion, blank=True)

class GardenBed(models.Model):
	class Meta():
		db_table = 'gardenbed'
	gardenbed_posx = models.IntegerField(default=0)
	gardenbed_posy = models.IntegerField(default=0)
	gardenbed_name = models.CharField(max_length=256, unique=True)
	gardenbed_time = models.CharField(max_length=512, blank=True, null=True)
	gardenbed_plant = models.ForeignKey(Plant, blank=True, null=True)
	gardenbed_mix = models.ForeignKey(Mix, blank=True, null=True)
	
	def get_gardenbed_posx(self):
		return self.gardenbed_posx
		
	def get_gardenbed_posy(self):
		return self.gardenbed_posy
