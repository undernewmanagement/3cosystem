from django.core.exceptions import ValidationError
import requests

def validate_meetup_url_exists(value):
    r = requests.head('http://www.meetup.com/%s/events/ical/' % (value,))
    if r.status_code != 200:
        raise ValidationError(u'%s is not a valid Meetup URL' % value)
