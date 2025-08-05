from django.db import models

# Create your models here.
class LocationUpdate(models.Model):
    device_id = models.CharField(default='id_not_found')
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)