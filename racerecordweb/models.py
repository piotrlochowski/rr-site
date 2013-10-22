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
    drivers = models.ManyToManyField(Driver, related_name='events', null=True, blank=True, default=None, through='EventDriver')

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


class EventDriver(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event)
    driver = models.ForeignKey(Driver)
    car = models.ForeignKey(Car, null=True, blank=True, default=None)
    start_number = models.SmallIntegerField()

    def __unicode__(self):
        return u'%s %s na %s' % (self.driver.last_name, self.driver.first_name, self.event.name)


class Trial(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    event = models.ForeignKey(Event, related_name='trials')

    def __unicode__(self):
        return u'%s' % (self.name)


#class TrialResult(models.Model):
#    id = models.AutoField(primary_key=True)
    #trial = models.ForeignKey(Trial)
    #best_time = models.TimeField(null=True, blank=True)
    #driver = models.ForeignKey(Driver, null=True, blank=True, default=None)
    #laps = models.OneToOneField(Lap)

    #def __unicode__(self):
    #    return u'Zaloga nr %s na próbie %s uzyskala najlepszy czas %s' % (self.startnumber, self.trial.name, self.besttime)


class Lap(models.Model):
    lap_nr = models.IntegerField()
    time = models.TimeField()
    penalty = models.SmallIntegerField(null=True, blank=True, default=None)
    penalty_value = models.BigIntegerField(null=True, blank=True, default=None)
    event_driver = models.ForeignKey(EventDriver, related_name='laps')

    def __unicode__(self):
        return u'%d uzyskał %s na %d przejeździe' % (self.event_driver.start_number, self.time, self.lap_nr)

    #return u'%d:Sd:sd' %(self.time)
