from django.core.management.base import BaseCommand, CommandError
from apps.tech_events.management.commands._firehose_utils import format_event, clean_json
from apps.tech_events.models import MeetupGroup
from apps.tech_events.models import TechEvent, ParseError
from icalendar import Calendar
import time
import socket
import requests
from retrying import retry


class Command(BaseCommand):
    help = 'Refresh all the meetup.com tech events'

    sleep_secs = 1

    # http://arstechnica.com/information-technology/2010/04/tutorial-use-twitters-new-real-time-stream-api-in-python/2/
    STREAM_URL = "http://stream.meetup.com/2/open_events?since_count=5000"

    def handle(self, *args, **options):

        """Connect to the remote API and start processing data"""

        while True:
            try:
                r = requests.get(self.STREAM_URL, stream=True, timeout=300)
                for line in r.iter_lines():
                    if line:
                        self.on_receive(line)

            except requests.exceptions.ChunkedEncodingError:
                self.stdout.write("CHUNKED ENCODING: Incomplete read")
                r.close()
                self.sleep()

            except requests.exceptions.ConnectionError:
                self.stdout.write("TIMEOUT: No response for over 300 seconds. Will sleep %s secs.", self.sleep_secs*2)
                r.close()
                self.sleep()

            except socket.error:
                self.stdout.write("SOCKET: Most likely connection reset by peer")
                self.sleep()

            except socket.timeout:
                self.stdout.write('SOCKET TIMEOUT: Restarting the connection')
                r.close()
                self.sleep()

    def sleep(self):
        """Custom sleep timer for used when connecting to API. Exponential back-off up to 256 seconds then resets"""

        time.sleep(self.sleep_secs)
        self.sleep_secs *= 2
        if self.sleep_secs > 256:
            self.sleep_secs = 1

    def on_receive(self, data):

        try:
            content = clean_json(data)
            [self.process_event(i) for i in content]

        except ValueError as e:
            self.process_error(str(e), 'no payload')

    def get_or_create_meetup_group(self, e):
        """Given the url name, retrieve the meetup group. If it does not exit then create it"""

        urlname = e['group']['urlname']
        name = e['group']['name']

        group, created = MeetupGroup.objects.get_or_create(
            url=urlname,
            defaults = {
                'name': (name[:190] + '..') if len(name) > 190 else name,
                'location': 'srid=4326;POINT(%s %s)' % (e['group']['group_lon'], e['group']['group_lat']),
                'is_blacklisted': False
            }
        )

        return group.id

    def save_event(self, e):
        """Save an event to the database"""

        # process event and format to dict
        event = format_event(e)

        # attach the meetup_group to the event
        event['meetup_group_id'] = self.get_or_create_meetup_group(e)

        # get the tech event
        TechEvent.objects.update_or_create(uniqid=e['id'], defaults=event)
        # cur.execute('SELECT * FROM tech_events_techevent WHERE uniqid = %s', (e['id'],))

        # if cur.rowcount == 0:
        #
        #     columns = ', '.join(event.keys())
        #     vals = tuple(event.values())
        #     cur.execute("INSERT INTO tech_events_techevent (%s) VALUES %s", (AsIs(columns), vals,))
        #
        # else:
        #
        #     updates = ', '.join(['%s = %%(%s)s' % (k, k) for k in event.keys() if k != 'uniqid'])
        #     query = "UPDATE tech_events_techevent SET %s WHERE uniqid = %%(uniqid)s" % updates
        #     cur.execute(query, event)

    def process_event(self, e):
        """Called each time there is new data coming in from the long HTTP poll process"""

        status = e['status']
        group_join_mode = e['group']['join_mode']
        category = e.get('group',{}).get('category',{}).get('shortname',None)

        if status in ['canceled', 'deleted']:

            TechEvent.objects.filter(uniqid=e['id']).delete()
            self.stdout.write("Deleted event: %s - %s" % (e['id'], e['group']['name']))

        elif status == 'upcoming' and group_join_mode == 'open' and category == 'tech':

            self.save_event(e)
            self.stdout.write("Processed '%s'" % e['group']['urlname'])


    def process_error(self, message, payload):
        """Log any errors it receives"""

        # TODO: move this to sentry
        self.stdout.write("PARSE ERROR (%s) - (%s)", message, payload)
        ParseError.objects.create(error_message=message, payload=payload)