import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import requests

from models import TechEvent
from icalendar import Calendar
from BeautifulSoup import BeautifulSoup


def meetup_group_pre_save(sender, instance, **kwargs):
    url       = 'http://www.meetup.com/%s' % instance.url
    r         = requests.get(url)
    html      = BeautifulSoup(r.text)
    geo_tag   = html.findAll(attrs={"name":"geo.position"})
    (lat,lng) = geo_tag[0]['content'].split(';')

    
    

def meetup_group_post_save(sender, instance, **kwargs):
    '''
    This signal will download the current calendar for meetup groups
    just added using the admin.
    '''
    group_calendar_url = 'http://www.meetup.com/%s/events/ical/' % instance.url

    r = requests.get(group_calendar_url)
    c = Calendar.from_ical(r.text)

    for i in c.walk():
        if i.name=='VEVENT':

            (lat,lng) = i['GEO'].to_ical().split(';')
            t = TechEvent.objects.create(
                uniqid     = i['UID'].replace('event_','').replace('@meetup.com',''),
                begin_time = i.get('DTSTART').dt,
                url        = i['URL'],
                name       = i['SUMMARY'],
                source     = 'MU',
                meetup_group_id = instance.id,
                is_active   = True,
                address     = i.get('LOCATION','See event page for details'),
                city        = '',
                postal_code = '',
                country     = '',
                location    = 'POINT (%s %s)' % (lng,lat)
            )












#            print "SUMMARY     : %s" % i['SUMMARY']
#            print "BEGIN TIME  : %s" % i.get('DTSTART').dt
#            print "UID         : %s" % i['UID']
#            print "STATUS      : %s" % i['STATUS']
#            print "URL         : %s" % i['URL']
#            print "GEO         : %s" % i['GEO'].to_ical()
#            print "DESCRIPTION : %s" % i['DESCRIPTION']
#            print "LOCATION    : %s" % i.get('LOCATION','See event page for details')
#            print '-------------------'
