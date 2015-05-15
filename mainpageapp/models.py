from django.db import models

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

class Mix(models.Model):
	class Meta():
		db_table = 'mix'
	mix_name = models.CharField(max_length=256, unique=True)
	mix_description = models.CharField(max_length=256)

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