import datetime
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from racerecordweb.models import Lap, Trial, Event, Driver, Car, EventDriver
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


class EventDriverResource(ModelResource):
    #laps = fields.ToManyField('racerecordweb.api.LapResource', 'laps', full=True, null=True)
    driver = fields.ForeignKey(DriverResource, 'driver', full=True, null=True)
    event = fields.ForeignKey(EventResource, 'event', full=True, null=True)

    class Meta:
        queryset = EventDriver.objects.all()
        resource_name = 'event_driver'
        excludes = ['id']
        include_resource_uri = True
        authorization = Authorization()
        filtering = {
            'driver': ['first_name', 'last_name'],
        }

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                # Get rid of the "meta".
                del (data_dict['meta'])
                # Rename the objects.
                data_dict['event_driver'] = copy.copy(data_dict['objects'])
                del (data_dict['objects'])
        return data_dict


class LapResource(ModelResource):
    event_driver = fields.ForeignKey(EventDriverResource, 'event_driver')

    class Meta:
        queryset = Lap.objects.all()
        resource_name = 'lap'
        excludes = ['penalty', 'penalty_value']
        include_resource_uri = True
        authorization = Authorization()


    def hydrate(self, bundle):
        (min, sec, msec) = [int(t) for t in bundle.data['time'].split(':')]
        bundle.data['time'] = int((datetime.timedelta(minutes=min, seconds=sec, milliseconds=msec)).total_seconds() * 1000)
        trial = Trial.objects.get(id=bundle.data['trial_id'])
        event_driver = EventDriver.objects.get(event__id=bundle.data['event_id'],
                                                   start_number=bundle.data['start_number'])
        #bundle.obj.lap_nr = bundle.data['lap_nr']
        bundle.obj.event_driver = event_driver
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
