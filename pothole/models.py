
from django.db import models
from datetime import datetime
# Create your models here.

class PolylineData(models.Model):
	filename = models.CharField(max_length=30, blank=True)
	score = models.DecimalField(max_digits=9, decimal_places=6)

	def __str__(self):
            return ('#' + str(self.id) + ' File: ' + str(self.filename) + ' - Score: ' + str(self.score))

class Pothole(models.Model):
	rpi_id=models.CharField(max_length=30, blank=True)
	timestamp = models.DateTimeField(default=datetime.now, blank=True)

	def __str__(self):
            return ('#' + str(self.id) + ' TS: ' + str(self.timestamp).split()[0])

class Location(models.Model):
	p_id=models.ForeignKey(Pothole, on_delete=models.CASCADE, null=True, blank=True)
	latitude=models.DecimalField(max_digits=9, decimal_places=6)
	longitude=models.DecimalField(max_digits=9, decimal_places=6)

	def __str__(self):
            return ('#' + str(self.p_id) + '-Lat: ' + str(self.latitude) + '-Lon: ' + str(self.longitude))

class Image(models.Model):
	p_id=models.ForeignKey(Pothole, on_delete=models.SET_NULL, null=True)
	#image=models.ImageField()
	
	def camera_sample():
		pass

	def __str__(self):
            return ('#' + str(self.p_id) + ' Image')

class Intensity(models.Model):
	p_id=models.ForeignKey(Pothole, on_delete=models.SET_NULL, null=True)
	breadth=models.FloatField(blank=True)
	depth=models.FloatField(blank=True)

	def __str__(self):
            return ('#' + str(self.p_id) + ' Dimensions')

class Accelerometer(models.Model):
	p_id=models.ForeignKey(Pothole, on_delete=models.SET_NULL, null=True)
	xaxis=models.FloatField(blank=True)
	yaxis=models.FloatField(blank=True)
	zaxis=models.FloatField(blank=True)

	def __str__(self):
            return ('#' + str(self.p_id) + ' accelerometer data')

