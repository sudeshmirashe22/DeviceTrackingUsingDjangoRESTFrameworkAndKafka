from django.contrib import admin
from .models import LocationUpdate

# Register your models here.
# admin.site.register(LocationUpdate)

@admin.register(LocationUpdate)
class LocationUpdate(admin.ModelAdmin):
    list_display = ('device_id','latitude', 'longitude', 'timestamp')