from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource, ALL,ALL_WITH_RELATIONS
from racerecordweb.models import Lap, TrialResult, Trial, Event, Driver, Car
from tastypie.authorization import Authorization
import copy

class LocationResource(ModelResource):
    class Meta:
        queryset = Event.objects.all();
        resource_name = 'location'
        include_resource_uri = False
        
    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                # Get rid of the "meta".
                del(data_dict['meta'])
                # Rename the objects.
                data_dict['locations'] = copy.copy(data_dict['objects'])
                del(data_dict['objects'])
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
                del(data_dict['meta'])
                # Rename the objects.
                data_dict['drivers'] = copy.copy(data_dict['objects'])
                del(data_dict['objects'])
        return data_dict


class TrialResource(ModelResource):
    location = fields.ForeignKey(LocationResource, 'location')

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
                del(data_dict['meta'])
                # Rename the objects.
                data_dict['trials'] = copy.copy(data_dict['objects'])
                del(data_dict['objects'])
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
                del(data_dict['meta'])
                # Rename the objects.
                data_dict['cars'] = copy.copy(data_dict['objects'])
                del(data_dict['objects'])
        return data_dict

class TrialResultResource(ModelResource):
    laps = fields.ToManyField('racerecordweb.api.LapResource', 'laps', full=True)
    driver = fields.ForeignKey(DriverResource, 'driver', full=True, null=True)
    trial = fields.ForeignKey(TrialResource, 'trial', full=True, null=True)
    car = fields.ForeignKey(CarResource, 'car', full=True, null=True)

    class Meta:
        queryset = TrialResult.objects.all()
        resource_name = 'trial_result'
        excludes = ['id']
        include_resource_uri = True
        authorization= Authorization()
        filtering = {
            'driver': ['first_name', 'last_name'],
        }

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                # Get rid of the "meta".
                del(data_dict['meta'])
                # Rename the objects.
                data_dict['trial_results'] = copy.copy(data_dict['objects'])
                del(data_dict['objects'])
        return data_dict

class LapResource(ModelResource):
    trial_result = fields.ForeignKey(TrialResultResource, 'trial_result')

    class Meta:
        queryset = Lap.objects.all()
        resource_name = 'lap'
        excludes = ['id']
        include_resource_uri = True
        authorization= Authorization()
        filtering = {
            'trial_result': ['startnumber', 'driver'],
        }

    def hydrate(self, bundle):
        trial = Trial.objects.get(id=bundle.data['trial_id'])
        (tr, isNew) = TrialResult.objects.get_or_create(startnumber=bundle.data['startnumber'], trial__id=bundle.data['trial_id'], defaults={'trial': trial})
        #objects_filter = TrialResult.objects.filter(startnumber=bundle.data['startnumber'], trial__id=bundle.data['trial_id'])[0]
        bundle.obj.trial_result_id = tr.id
        del bundle.data['startnumber']
        return bundle

    def alter_list_data_to_serialize(self, request, data_dict):
        if isinstance(data_dict, dict):
            if 'meta' in data_dict:
                # Get rid of the "meta".
                del(data_dict['meta'])
                # Rename the objects.
                data_dict['laps'] = copy.copy(data_dict['objects'])
                del(data_dict['objects'])
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
