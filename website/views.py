from django.shortcuts import render
from django.http import Http404
from apps.geography.models import City, Country
from apps.tech_events.models import TechEvent
from website.utils import reshape_events
from datetime import datetime, timedelta
import pytz

from django.contrib.gis.measure import D

from django.views.decorators.cache import cache_page


@cache_page(60 * 15)
def home(request):
    countries = Country.objects.filter(is_active=True).order_by('name')
    d        = datetime.utcnow().replace(tzinfo=pytz.utc)
    today    = datetime.combine(d, datetime.min.time()).replace(tzinfo=pytz.utc)
    end_date = today + timedelta(days=31)

    ret = []
    for country in countries:
        carr = {
            'country' : country.name,
            'cities'  : [],
        }
        for city in country.cities.filter(is_active=True).all():
            t = TechEvent.objects.filter(location__distance_lte=(city.location, D(m=city.distance*1000))).filter(is_active=True).filter(begin_time__range=(today,end_date)).order_by('begin_time').count()
            carr['cities'].append({
                'name' : city.short_name,
                'slug' : city.slug,
                'count': t
            })
        ret.append(carr)

    return render(request,'website/home.html',{'countries' : ret })



@cache_page(60 * 15)
def city(request,city):
    try:
        c = City.objects.get(slug=city) 
    except City.DoesNotExist:
        raise Http404

    d        = datetime.utcnow().replace(tzinfo=pytz.utc)
    today    = datetime.combine(d, datetime.min.time()).replace(tzinfo=pytz.utc)
    end_date = today + timedelta(days=31)

    t = TechEvent.objects.filter(location__distance_lte=(c.location, D(m=c.distance*1000))).filter(is_active=True).filter(begin_time__range=(today,end_date)).order_by('begin_time')

    ret = {
        'city'             : c,
        'days'             : reshape_events(t)
    }

    return render(request,'website/events.html', ret)
