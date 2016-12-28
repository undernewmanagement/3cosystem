from datetime import datetime
from collections import OrderedDict


def reshape_events(events):
    out = {}
    for e in events:
        k = e.begin_time.date()
        if k not in out:
            out[k] = {
                'date': e.begin_time.strftime('%b %d'),
                'dow': e.begin_time.strftime('%A'),
                'events': []
            }

        out[k]['events'].append(e)

    return OrderedDict((datetime.strftime(k, '%d-%m-%Y'), v)
                       for k, v in sorted(out.items()))
