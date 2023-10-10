from django.db import models
from django.core.validators import MaxValueValidator, RegexValidator


class Location(models.Model):
    state_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=5)
    lat = models.FloatField()
    lng = models.FloatField()


class Cargo(models.Model):
    pickup_location = models.ForeignKey(Location, related_name='cargo_pickup', on_delete=models.CASCADE)
    delivery_location = models.ForeignKey(Location, related_name='cargo_delivery', on_delete=models.CASCADE)
    weight = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10000)])
    description = models.CharField(max_length=1000)


class Truck(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    number = models.CharField(max_length=5, unique=True, validators=[RegexValidator(r"\d{4}[A-Z]{1}")])
    load_capacity = models.PositiveSmallIntegerField(validators=[MaxValueValidator(10000)])

    @property
    def zipcode(self):
        return self.location.zipcode
