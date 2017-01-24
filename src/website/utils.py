from datetime import datetime
from collections import OrderedDict


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
