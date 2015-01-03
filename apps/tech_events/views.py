from django.shortcuts import render

from apps.tech_events.models import TechEvent
from apps.geography.model import City

def events_for_city(request,city):
    try:
        city = City.objects.get(name=city)
    except City.DoesNotExist:
        raise Http404
