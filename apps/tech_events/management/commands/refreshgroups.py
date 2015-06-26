import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from django.core.management.base import BaseCommand, CommandError
from apps.tech_events.models import MeetupGroup
from apps.tech_events.models import TechEvent

import requests
from icalendar import Calendar

    
class Command(BaseCommand):
    help = 'Refresh all the meetup.com tech events'

    def handle(self, *args, **options):
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36', }

        for instance in MeetupGroup.objects.all().filter(is_blacklisted=False):
            self.stdout.write('Getting "%s"' % instance.name)
            group_calendar_url = 'http://www.meetup.com/%s/events/ical/' % instance.url

            r = requests.get(group_calendar_url,headers=headers)

            try:
                c = Calendar.from_ical(r.text)
                for i in c.walk():
                    if i.name=='VEVENT':

                        uniqid    = i['UID'].replace('event_','').replace('@meetup.com','')
                        (lat,lng) = i['GEO'].to_ical().split(';')

                        updated_values = {
                        'begin_time'      : i.get('DTSTART').dt,
                        'url'             : i['URL'],
                        'name'            : i['SUMMARY'],
                        'source'          : 'MU',
                        'meetup_group_id' : instance.id,
                        'is_active'       : True,
                        'address'         : i.get('LOCATION','See event page for details'),
                        'city'            : '',
                        'postal_code'     : '',
                        'country'         : '',
                        'location'        : 'POINT (%s %s)' % (lng,lat)
                        }

                        t = TechEvent.objects.update_or_create(uniqid=uniqid, defaults=updated_values)

            except ValueError:
                self.stdout.write('[ERROR] - Getting "%s"' % instance.name)
                

