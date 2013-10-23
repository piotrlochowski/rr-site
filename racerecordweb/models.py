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


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Wydarzenie', max_length=20)
    drivers = models.ManyToManyField(Driver, related_name='trials', null=True, blank=True, default=None, through='TrialDriver')


    def __unicode__(self):
        return u'%s' % (self.name)


class Car(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    capacity = models.CharField(max_length=10)
    power = models.IntegerField()
    year = models.IntegerField()
    plate = models.CharField(max_length=10)
    driver = models.ForeignKey(Driver)

    def __unicode__(self):
        return u'%s z %s nr rej. %s' % (self.name, self.year, self.plate)


class Trial(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    event = models.ForeignKey(Event, related_name='trials')
    #trial_driver = models.ForeignKey(TrialDriver, related_name='laps')
    drivers = models.ManyToManyField(Driver, related_name='trials', null=True, blank=True, default=None, through='TrialDriver')

    def __unicode__(self):
        return u'%s' % (self.name)


class TrialDriver(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event)
    driver = models.ForeignKey(Driver)
    trial = models.ForeignKey(Trial)
    car = models.ForeignKey(Car, null=True, blank=True, default=None)
    start_number = models.SmallIntegerField()

    def __unicode__(self):
        return u'%s %s na %s' % (self.driver.last_name, self.driver.first_name, self.event.name)


class Lap(models.Model):
    lap_nr = models.IntegerField()
    time = models.IntegerField()
    penalty = models.SmallIntegerField(null=True, blank=True, default=None)
    penalty_value = models.BigIntegerField(null=True, blank=True, default=None)
    #trial_driver = models.ForeignKey(TrialDriver, related_name='laps')
    trial = models.ForeignKey(Trial, related_name='laps')

    def __unicode__(self):
        return u'%d uzyskał %s na %d przejeździe' % (self.trial_driver.start_number, self.time, self.lap_nr)

    #return u'%d:Sd:sd' %(self.time)
