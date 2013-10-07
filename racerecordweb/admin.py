from django.contrib import admin
from racerecordsite.racerecordweb import models

class DriverAdmin(admin.ModelAdmin):
	pass

admin.site.register(models.Driver, DriverAdmin)
admin.site.register(models.Car)
admin.site.register(models.Trial)
admin.site.register(models.TrialResult)
admin.site.register(models.Lap)
admin.site.register(models.Location)