from datetime import datetime
from collections import OrderedDict

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def reshape_events(events):
    """
    Received a list of TechEvent objects and returns an ordered dictionary
    Args:
        events: Array of TechEvent model objects

    Returns:
        OrderedDict: Ordered dictionary of events sorted by day ascending

    Examples:
        Output:
            datetime.date(2017, 1, 24): {
                'date': 'Jan 24',
                'dow': 'Tuesday',
                'events': [
                    <TechEvent: TechEvent object>,
                    <TechEvent: TechEvent object>,
                    <TechEvent: TechEvent object>
                ]
            },
            datetime.date(2017, 1, 25): {
                'date': 'Jan 25',
                'dow': 'Wednesday',
                'events': [
                    <TechEvent: TechEvent object>,
                    <TechEvent: TechEvent object>
                ]
            },
    """
    out = {}

    # loop over all the events
    for e in events:
        k = e.begin_time.date()
        if k not in out:
            out[k] = {
                # Format: Mmm dd (Mar 09)
                'date': e.begin_time.strftime('%b %d'),

                # Day of week: (Monday)
                'dow': e.begin_time.strftime('%A'),
                'events': []
            }

        out[k]['events'].append(e)

    # sort the items
    return OrderedDict((datetime.strftime(k, '%d-%m-%Y'), v)
                       for k, v in sorted(out.items()))

def retry_request(url):
    """
    taken from here: https://stackoverflow.com/a/35504626/1646663

    :param url:
    :return:
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    }

    s = requests.Session()

    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])

    s.mount('https://', HTTPAdapter(max_retries=retries))

    return s.get(url, headers=headers)