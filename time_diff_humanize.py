# -*- coding: utf-8 -*-
from datetime import datetime

INTERVALS = [1, 60, 3600, 86400, 604800, 2419200, 29030400]
NAMES = [('second', 'seconds'),
         ('minute', 'minutes'),
         ('hour', 'hours'),
         ('day', 'days'),
         ('week', 'weeks'),
         ('month', 'months'),
         ('year', 'years')]


def time_diff_start():
    return datetime.now()


def time_diff_end(t_start):
    time_diff = (datetime.now() - t_start)
    time_diff_seconds = time_diff.seconds
    if time_diff_seconds > 5:
        diff = humanize_time(time_diff_seconds, 'seconds')
    else:
        microseconds = str(time_diff.microseconds)
        if len(microseconds) < 6:
            for i in range(6-len(microseconds)):
                microseconds = '0' + microseconds
        diff = str(time_diff_seconds) + '.' + str(microseconds) + ' seconds'
    return diff


def humanize_time(amount, units):
    """
    Divide `amount` in time periods.
    Useful for making time intervals more human readable.

    >>> humanize_time(173, 'hours')
    [(1, 'week'), (5, 'hours')]
    >>> humanize_time(17313, 'seconds')
    [(4, 'hours'), (48, 'minutes'), (33, 'seconds')]
    >>> humanize_time(90, 'weeks')
    [(1, 'year'), (10, 'months'), (2, 'weeks')]
    >>> humanize_time(42, 'months')
    [(3, 'years'), (6, 'months')]
    >>> humanize_time(500, 'days')
    [(1, 'year'), (5, 'months'), (3, 'weeks'), (3, 'days')]
    """
    result = []

    unit = map(lambda a: a[1], NAMES).index(units)
    # Convert to seconds
    amount = amount * INTERVALS[unit]

    for i in range(len(NAMES)-1, -1, -1):
      a = amount / INTERVALS[i]
      if a > 0:
         result.append( (a, NAMES[i][1 % a]) )
         amount -= a * INTERVALS[i]

    result = smart_str(result).replace("'"," ").replace("(","").replace(")","").replace(",","")

    return result
