from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

from location_field.models.spatial import LocationField

from apps.geography.models import Country

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    weight = models.IntegerField(blank=True,default=0)

    class Meta:
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name

class Company(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug        = models.CharField(max_length=100)
    weight      = models.IntegerField(blank=True,default=0)
    categories  = models.ManyToManyField('Category') 
    website     = models.URLField()
    twitter     = models.CharField(max_length=50)
    full_address= models.CharField(max_length=200)
    country     = models.ForeignKey('geography.Country')
    location    = LocationField(based_fields=[full_address],zoom=7,default='POINT(0.0 0.0)')
    objects     = models.GeoManager()
    
    class Meta:
        verbose_name_plural = 'Companies'

    def __unicode__(self):
        return self.name
