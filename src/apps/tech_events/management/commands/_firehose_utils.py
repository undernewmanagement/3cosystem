import time
import json


def clean_json(data):
    """Received a string comprised of one or more json objects and
    concatenated them into a single json array"""

    if data is None:
        return []

    data = data.encode() if type(data) is str else data

    # is this json string already a properly formatted array?
    try:
        s = json.loads(data)
        if isinstance(s, list):
            return s
    except ValueError:
        pass

    d = data.decode().strip().replace('\n', ',')
    d = '[' + d + ']'
    d = d.encode()
    return json.loads(d)


def format_event(e):
    """Process venue information"""
    if 'venue' in e:
        v = e['venue']
        address = '%s %s %s' % (
            v.get('address_1', ''),
            v.get('address_2', ''),
            v.get('address_3', '')
        )
        city = v.get('city', '')
        postal_code = v.get('zip', '')
        country = v.get('country', '')
        location = (v.get('lon', '0.0'), v.get('lat', '0.0'))
    else:
        address = 'See event listing for location info'
        city = ''
        postal_code = ''
        country = ''
        location = (e['group']['group_lon'], e['group']['group_lat'])

    # we trim the string lengths to avoid DB errors
    return {
        'uniqid': e['id'][:50],
        'name': e['group']['name'][:255],
        'url': e['event_url'][:200],

        # TODO - make this adjusted for timezones as well
        'begin_time': time.strftime('%Y-%m-%d %H:%M:%S%z', time.gmtime(e.get('time') / 1000.0)),
        'source': 'MU',
        'is_active': True,
        'meetup_group_id': None,
        'address': address[:255],
        'city': city[:100],
        'postal_code': postal_code[:20],
        'country': country[:50],
        'location': 'srid=4326;POINT(%s %s)' % location
    }
