from django.core.exceptions import ValidationError
import requests

def validate_meetup_url_exists(value):
    r = requests.head(f"https://www.meetup.com/{value}/events/ical/")
    if r.status_code != 200:
        raise ValidationError(f"{value} is not a valid Meetup URL")
