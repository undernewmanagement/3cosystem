from django.apps import AppConfig
from django.db.models.signals import post_save

from tech_events import signals
from tech_events.models import MeetupGroup


class TechEventsAppConfig(AppConfig):
    name = 'tech_events'
    verbose_name = 'Events'

    def ready(self):
        post_save.connect(signals.meetup_group_post_save, sender=MeetupGroup)
