from django.shortcuts import render
from django.http import Http404
from apps.geography.models import City, Country
from apps.tech_events.models import TechEvent
from apps.companies.models import Category, Company
from website.utils import reshape_events
from datetime import datetime, timedelta
import pytz

from django.contrib.gis.measure import D

from django.views.decorators.cache import cache_page


@cache_page(60 * 15)
def home(request):
    countries = Country.objects.filter(is_active=True).order_by('name')
    d = datetime.utcnow().replace(tzinfo=pytz.utc)
    today = datetime.combine(d, datetime.min.time()).replace(tzinfo=pytz.utc)
    end_date = today + timedelta(days=31)

    ret = []

    for country in countries:

        carr = {
            'country': country.name,
            'cities': [],
        }

        for city in country.cities.filter(is_active=True).all():

            t = TechEvent.objects\
                    .filter(location__distance_lte=(city.location, D(m=city.distance*1000)))\
                    .filter(is_active=True)\
                    .filter(meetup_group__is_blacklisted=False)\
                    .filter(begin_time__range=(today, end_date))\
                    .order_by('begin_time').count()

            carr['cities'].append({
                'name': city.short_name,
                'slug': city.slug,
                'count': t
            })

        ret.append(carr)

    return render(request, 'website/home.html', {
        'countries': ret,
        'meta': {
            'description': 'We have the biggest, baddest list of local tech and startup events in over 65 cities',
            'title': 'Local startup and tech events in your city | 3cosystem'
        }
    })


@cache_page(60 * 15)
def city(request, city):
    """
    View all the events for a city. Results are cached for 15 minutes
    Args:
        request: django request object
        city: the name of the city (slug)

    Returns:

    """
    try:
        c = City.objects.get(slug=city) 
    except City.DoesNotExist:
        raise Http404

    d = datetime.utcnow().replace(tzinfo=pytz.utc)
    today = datetime.combine(d, datetime.min.time()).replace(tzinfo=pytz.utc)
    end_date = today + timedelta(days=31)

    t = TechEvent.objects\
            .filter(location__distance_lte=(c.location, D(m=c.distance*1000)))\
            .filter(is_active=True)\
            .filter(meetup_group__is_blacklisted=False)\
            .filter(begin_time__range=(today, end_date)).order_by('begin_time')

    ret = {
        'city': c,
        'days': reshape_events(t),
        'meta': {
            'description': "%s has %d tech and startup events scheduled over the next 30 days" % (c.short_name, len(t)),
            'title': "%d upcoming tech and startup events in %s" % (len(t), c.short_name)
        }
    }

    return render(request, 'website/events.html', ret)


def city_ecosystem(request, city):

    try:
        c = City.objects.get(slug=city) 
    except City.DoesNotExist:
        raise Http404

    categories = Category.objects.order_by('-weight').all()

    grid = []
    for category in categories:
        block = {
            'name': category.name,
            'idea': Company.objects.filter(cities=c).filter(stages__name='Idea').filter(categories=category).all(),
            'startup': Company.objects.filter(cities=c).filter(stages__name='Startup').filter(categories=category).all(),
            'growth': Company.objects.filter(cities=c).filter(stages__name='Growth').filter(categories=category).all()
        }
        grid.append(block)
        
    ret = {
        'city': c,
        'grid': grid,
        'meta': {
            'description': "description here %s" % c.short_name,
            'title': "Discover the tech and startup ecosystem in %s" % c.short_name
        }
    }
    return render(request, 'website/ecosystem.html', ret)


def sitemap(request):
    cities = City.objects.filter(is_active=True).all()
    return render(request, 'sitemap.xml', {'cities': cities})

