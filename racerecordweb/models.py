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


class TrialDriver(models.Model):
    id = models.AutoField(primary_key=True)
    trial = models.ForeignKey(Trial)
    driver = models.ForeignKey(Driver)
    car = models.ForeignKey(Car, null=True, blank=True, default=None)
    start_number = models.SmallIntegerField()


    def __unicode__(self):
        return u'%s %s na %s' % (self.driver.last_name, self.driver.first_name, self.trial.name)


class Lap(models.Model):
    lap_nr = models.IntegerField()
    time = models.IntegerField()
    penalty = models.SmallIntegerField(null=True, blank=True, default=None)
    penalty_value = models.BigIntegerField(null=True, blank=True, default=None)
    event_driver = models.ForeignKey(EventDriver, related_name='laps')
    trial_driver = models.ForeignKey(TrialDriver, related_name='laps', null=True, blank=True, default=None)
    trial = models.ForeignKey(Trial, related_name='laps')

    def __unicode__(self):
        return u'%d uzyskał %s na %d przejeździe próby %s' % (self.event_driver.start_number, self.time, self.lap_nr, self.trial.name)

    def save(self, force_insert=False, force_update=False, using=None):
        create = TrialDriver.objects.get_or_create(start_number=self.event_driver.start_number, trial__id=self.trial.id,
                                                   defaults={'start_number': self.event_driver.start_number,
                                                             'trial': self.trial, 'driver': self.event_driver.driver,
                                                             'car': self.event_driver.car})[0]
        self.trial_driver= create
        return super(Lap, self).save(force_insert, force_update, using)



