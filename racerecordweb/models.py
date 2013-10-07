# coding=ISO-8859-2
from django.db import models

# Create your models here.

class Driver(models.Model):
	id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	#cars = models.ForeignKey(Car)
	
	def __unicode__(self):
		return u'%s %s' % (self.last_name, self.first_name)

class Car (models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=20)
	capacity = models.CharField(max_length=10)
	power = models.IntegerField()
	year = models.IntegerField()
	plate = models.CharField(max_length= 10)
	driver = models.ForeignKey(Driver)
	
	def __unicode__(self):
		return u'%s z %s nr rej. %s' %(self.name, self.year, self.plate)
	
class Location(models.Model):
	id = models.AutoField(primary_key=True)
	city = models.CharField('Miejscowosc', max_length=20)
	
	def __unicode__(self):
		return u'%s' %(self.city)
	
class Trial(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	location = models.ForeignKey(Location)
	
	def __unicode__(self):
		return u'%s' %(self.name)

class TrialResult(models.Model):
	id = models.AutoField(primary_key=True)
	trial = models.ForeignKey(Trial)
	besttime = models.TimeField()
	startnumber = models.IntegerField()
	driver = models.ForeignKey(Driver)
	car = models.ForeignKey(Car)
	#laps = models.OneToOneField(Lap)
	
	def __unicode__(self):
		return u'Przejazdy nr %s na próbie %s' %(self.startnumber, self.trial.name)
	
class Lap(models.Model):
	id = models.AutoField(primary_key=True)
	lap_nr = models.IntegerField()
	time = models.TimeField()
	penalty = models.TimeField('Time sanction value')
	penalty_value = models.CharField(max_length=10)
	trial_result = models.ForeignKey(TrialResult, related_name='laps')
	
	def __unicode__(self):
		return u'%d uzyskał %s na %d przejeździe' %(self.trial_result.startnumber, self.time, self.lap_nr)
		#return u'%d:Sd:sd' %(self.time)
