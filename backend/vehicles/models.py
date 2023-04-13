from django.contrib.gis.db.models import PointField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Vehicle(models.Model):
    license_plate = models.CharField(max_length=6)
    battery_level = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ]
    )
    in_use = models.BooleanField()
    model = models.CharField(max_length=30)
    location = PointField(geography=True)


class Shift(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class Swap(models.Model):
    class Meta:
        unique_together = ('shift', 'vehicle')
        indexes = [
            models.Index(fields=['shift_id', 'vehicle_id'], name='search_shift_vehicle')
        ]

    shift = models.ForeignKey(Shift, on_delete=models.DO_NOTHING, related_name='swaps')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.DO_NOTHING, related_name='swaps')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
