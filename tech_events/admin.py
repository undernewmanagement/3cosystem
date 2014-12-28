from django.contrib import admin
from tech_events.models import MeetupGroup, TechEvent, ParseError

admin.site.register(MeetupGroup)
admin.site.register(TechEvent)
admin.site.register(ParseError)

# Register your models here.
