from django.contrib import admin
from django import forms
from racerecordsite.racerecordweb import models


#class DriverAdmin(admin.ModelAdmin):
#    pass


class DriverForm(forms.ModelForm):
    start_nr = forms.IntegerField()

    class Meta:
        model = models.Driver

    #def save(self, commit=True):
    #    # do something with self.cleaned_data['temp_id']
    #    super(DriverForm, self).save(commit=commit)


class DriverAdmin(admin.ModelAdmin):
    exclude = ['start_nr']
    form = DriverForm


class TrialInline(admin.TabularInline):
    model = models.Trial


#class DriverInline(admin.TabularInline):
#    model = models.Driver


class EventAdmin(admin.ModelAdmin):
    inlines = [
        TrialInline,
        #DriverInline,
    ]


admin.site.register(models.Driver, DriverAdmin)
admin.site.register(models.Car)
admin.site.register(models.Trial)
admin.site.register(models.TrialResult)
admin.site.register(models.Lap)
admin.site.register(models.Event, EventAdmin)