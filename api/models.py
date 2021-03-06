from django.db import models


class EarthQuake(models.Model):
    origin_time = models.DateTimeField()
    magnitude = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    depth = models.IntegerField()
    region_city = models.CharField(max_length=200)
    region_state = models.CharField(max_length=200)

    def __str__(self):
        return self.region_state
