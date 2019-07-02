from django.contrib.gis.db import models
from location_field.models.spatial import LocationField
from .validators import *
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import requests
from bs4 import BeautifulSoup

from icalendar import Calendar
from website.utils import retry_request


class MeetupGroup(models.Model):

    url = models.CharField(max_length=100, unique=True, validators=[validate_meetup_url_exists])
    name = models.CharField(max_length=100)
    is_blacklisted = models.BooleanField(default=False)
    location = models.PointField(null=True)

    class Meta:
        verbose_name_plural = "Meetup Groups"

    def __unicode__(self):
        return self.url


class TechEvent(models.Model):

    MEETUP = 'MU'
    EVENTBRITE = 'EB'
    ICAL = 'IC'
    CUSTOM = 'CU'

    SOURCE_CHOICES = (
        (MEETUP, 'Meetup.com'),
        (EVENTBRITE, 'EventBrite'),
        (ICAL, '.ics calendar'),
        (CUSTOM, 'Custom one-off event'),
    )

    uniqid = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    url = models.URLField()
    begin_time = models.DateTimeField('begin time')
    source = models.CharField(max_length=2,
                              choices=SOURCE_CHOICES,
                              default=CUSTOM)
    meetup_group = models.ForeignKey(MeetupGroup,
                                     null=True,
                                     blank=True,
                                     on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=50, null=True)
    location = LocationField(
                    based_fields=[address, city, postal_code],
                    zoom=7,
                    default='POINT (0.0 0.0)'
                )

    class Meta:
        verbose_name_plural = "Events"

    def __unicode__(self):
        return self.name


class ParseError(models.Model):

    created_at = models.DateField()
    error_message = models.TextField()
    payload = models.TextField()
    is_resolved = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Firehose Parse Errors'

    def __unicode__(self):
        return self.error_message


@receiver(pre_save, sender=MeetupGroup)
def meetup_group_pre_save(sender, instance, **kwargs):

    if instance.is_blacklisted is False:

        url = 'https://www.meetup.com/%s' % instance.url

        r = retry_request(url)

        html = BeautifulSoup(r.text, features="html.parser")

        res = html.findAll('meta', attrs={"property": "geo.position"})
        (lat, lng) = res[0]['content'].split(';')

        instance.name = html.h1.a.text[:255]

        instance.location = 'POINT(%s %s)' % (lng, lat)


@receiver(post_save, sender=MeetupGroup)
def meetup_group_post_save(sender, instance, **kwargs):
    """
    Download the current calendar for meetup groups just added using the
    admin.
    """

    # If the meetup group is blacklisted, then we should delete all related
    # tech events.
    if instance.is_blacklisted is True:
        TechEvent.objects.filter(meetup_group_id=instance.id).delete()

    else:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
        }
        group_calendar_url = 'http://www.meetup.com/%s/events/ical/' % instance.url

        r = requests.get(group_calendar_url, headers=headers)
        c = Calendar.from_ical(r.text)

        for i in c.walk():
            if i.name == 'VEVENT':

                uniqid = i['UID'].replace('event_', '').\
                         replace('@meetup.com', '')
                (lat, lng) = i['GEO'].to_ical().split(';')

                updated_values = {
                    'begin_time': i.get('DTSTART').dt,
                    'url': i['URL'][:200],
                    'name': i['SUMMARY'],
                    'source': 'MU',
                    'meetup_group_id': instance.id,
                    'is_active': True,
                    'address': i.get('LOCATION', 'See event page for details')[:255],
                    'city': '',
                    'postal_code': '',
                    'country': '',
                    'location': 'POINT (%s %s)' % (lng, lat)
                }

                TechEvent.objects.update_or_create(
                        uniqid=uniqid,
                        defaults=updated_values)
