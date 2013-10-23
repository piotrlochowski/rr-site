import datetime
from django.contrib.auth.models import User
from django.db.models import Min, Sum, Max
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from racerecordweb.models import Lap, Trial, Event, Driver, Car, TrialDriver
from tastypie.authorization import Authorization
import copy


class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all();
        resource_name = 'event'
        include_resource_uri = False

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                # Get rid of the "meta".
                del (data_dict['meta'])
                # Rename the objects.
                data_dict['events'] = copy.copy(data_dict['objects'])
                del (data_dict['objects'])
        return data_dict


class DriverResource(ModelResource):
    class Meta:
        queryset = Driver.objects.all();
        resource_name = 'driver'
        fields = ['last_name', 'first_name']
        include_resource_uri = False

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                # Get rid of the "meta".
                del (data_dict['meta'])
                # Rename the objects.
                data_dict['drivers'] = copy.copy(data_dict['objects'])
                del (data_dict['objects'])
        return data_dict


class TrialResource(ModelResource):
    event = fields.ForeignKey(EventResource, 'event')

    class Meta:
        queryset = Trial.objects.all()
        resource_name = 'trial'
        include_resource_uri = False
        filtering = {
            'name': ALL,
        }

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                # Get rid of the "meta".
                del (data_dict['meta'])
                # Rename the objects.
                data_dict['trials'] = copy.copy(data_dict['objects'])
                del (data_dict['objects'])
        return data_dict


class CarResource(ModelResource):
    class Meta:
        queryset = Car.objects.all();
        resource_name = 'car'
        include_resource_uri = False

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                # Get rid of the "meta".
                del (data_dict['meta'])
                # Rename the objects.
                data_dict['cars'] = copy.copy(data_dict['objects'])
                del (data_dict['objects'])
        return data_dict


class TrialDriverResource(ModelResource):
    #laps = fields.ToManyField(LapResource, 'laps', related_name="lap", full=True, null=True)
    driver = fields.ForeignKey(DriverResource, 'driver', full=True, null=True)
    event = fields.ForeignKey(EventResource, 'event', full=True, null=True)

    class Meta:
        queryset = TrialDriver.objects.all()
        resource_name = 'trial_driver'
        #excludes = ['id']
        include_resource_uri = False
        authorization = Authorization()
        filtering = {
            'driver': ['first_name', 'last_name'],
        }

    def dehydrate(self, bundle):
        #laps = Lap.objects.filter(trial_driver__id=bundle.obj.id,
        #                          trial_driver__driver__id=bundle.obj.driver.id)
        #times = Lap.objects.aggregate(Sum('time'), Min('time'), Max('time'))

        #aggregate(Avg('price'), Max('price'), Min('price'))

        #bundle.data['time_n-1'] = times['time__sum']-times['time__min']
        #bundle.data['time_best'] = times['time__max']

        times = bundle.obj.laps.all().aggregate(Sum('time'), Min('time'), Max('time'))

        bundle.data['time_n-1'] = times['time__sum']-times['time__min']
        bundle.data['time_best'] = times['time__max']
        del bundle.data['id']
        del bundle.data['event']
        return bundle

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                # Get rid of the "meta".
                del (data_dict['meta'])
                # Rename the objects.
                data_dict['trial_driver'] = copy.copy(data_dict['objects'])
                del (data_dict['objects'])
        return data_dict


class LapResource(ModelResource):
    trial_driver = fields.ForeignKey(TrialDriverResource, 'trial_driver', related_name='laps')
    #trial = fields.ForeignKey(Trial, 'trial', related_name='laps')

    class Meta:
        queryset = Lap.objects.all()
        resource_name = 'lap'
        excludes = ['penalty', 'penalty_value']
        include_resource_uri = True
        authorization = Authorization()


    def hydrate(self, bundle):
        (min, sec, msec) = [int(t) for t in bundle.data['time'].split(':')]
        bundle.data['time'] = int(
            (datetime.timedelta(minutes=min, seconds=sec, milliseconds=msec)).total_seconds() * 1000)
        trial = Trial.objects.get(id=bundle.data['trial_id'])
        trial_driver = TrialDriver.objects.get(event__id=bundle.data['event_id'],
                                               start_number=bundle.data['start_number'])
        #bundle.obj.lap_nr = bundle.data['lap_nr']
        bundle.obj.trial_driver = trial_driver
        bundle.obj.trial = trial
        del bundle.data['event_id']
        del bundle.data['trial_id']
        del bundle.data['start_number']
        return bundle

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                # Get rid of the "meta".
                del (data_dict['meta'])
                # Rename the objects.
                data_dict['laps'] = copy.copy(data_dict['objects'])
                del (data_dict['objects'])
        return data_dict

#class LocationResource(ModelResource):
#    class Meta:
#        queryset = Location.objects.all();
#        resource_name = 'location'
#        include_resource_uri = False
#
#    def alter_list_data_to_serialize(self, request, data_dict):
#        if isinstance(data_dict, dict):
#            if 'meta' in data_dict:
#                # Get rid of the "meta".
#                del(data_dict['meta'])
#                # Rename the objects.
#                data_dict['locations'] = copy.copy(data_dict['objects'])
#                del(data_dict['objects'])
#        return data_dict
