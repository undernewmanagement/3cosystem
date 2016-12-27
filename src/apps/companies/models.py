from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

from location_field.models.spatial import LocationField

from apps.geography.models import City

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    weight = models.IntegerField(blank=True,default=0)

    class Meta:
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name

class Stage(models.Model):
    name = models.CharField(max_length=100)
    weight = models.IntegerField(blank=True,default=0)
    
    def __unicode__(self):
        return self.name

class Company(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    slug        = models.CharField(max_length=100)
    weight      = models.IntegerField(blank=True,default=0)
    categories  = models.ManyToManyField('Category') 
    stages      = models.ManyToManyField('Stage') 
    website     = models.URLField()
    twitter     = models.CharField(max_length=50)
    full_address= models.CharField(max_length=200)
    cities      = models.ManyToManyField('geography.City')
    is_active   = models.BooleanField(default=False)
    location    = LocationField(based_fields=[full_address],zoom=7,default='POINT(0.0 0.0)')
    objects     = models.GeoManager()
    
    class Meta:
        verbose_name_plural = 'Companies'

    def __unicode__(self):
        return self.name
