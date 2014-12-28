from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

from location_field.models.spatial import LocationField

class Country(models.Model):
    NORTH_AMERICA = 'NA'
    SOUTH_AMERICA = 'SA'
    EUROPE        = 'EU'
    MIDDLE_EAST   = 'ME'
    ASIA          = 'AS'
    OCEANIA       = 'AU'
    AFRICA        = 'AF'
    REGION_CHOICES = (
        ( NORTH_AMERICA, 'North America'),
        ( SOUTH_AMERICA, 'South America'),
        (        EUROPE, 'Europe'       ),
        (   MIDDLE_EAST, 'Middle East'  ),
        (          ASIA, 'Asia'         ),
        (       OCEANIA, 'Oceania'      ),
        (        AFRICA, 'Africa'       ),
    )

    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=False)
    weight = models.IntegerField()
    region = models.CharField(max_length=2, choices=REGION_CHOICES, default=NORTH_AMERICA)

    class Meta:
        verbose_name_plural = "Countries"

    def __unicode__(self):
        return self.name



class City(models.Model):
    short_name  = models.CharField(max_length=50)
    long_name   = models.CharField(max_length=50)
    country     = models.ForeignKey('Country')
    slug        = models.SlugField(unique=True)
    distance    = models.IntegerField()
    is_active   = models.BooleanField(default=False)
    location    = LocationField(based_fields=[long_name],zoom=7,default='POINT(0.0 0.0)')
    objects     = models.GeoManager()

    class Meta:
        verbose_name_plural = "Cities"

    def __unicode__(self):
        return self.long_name


