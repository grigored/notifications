import datetime

import pytz


def get_decimal_separator(locale):
    if locale == 'cs_CZ':
        return ','
    return '.'


def format_decimal(decimal, locale, default=None):
    return format_decimal_precision(decimal, locale, 3, default=default)


def format_decimal_precision(decimal, locale, precision, default=None):
    separator = get_decimal_separator(locale)
    try:
        string = (('%.' + str(precision) + 'f') % decimal)
        if precision > 0:
            string = string.rstrip('0').rstrip('.')
            if separator == ',':
                string = string.replace('.', ',')
        return string
    except:
        return default


def format_date(timestamp, timezone_string=None, timezone_obj=None, locale='en_US'):
    if timestamp is None:
        return '--'

    time_formatter = '%d/%m/%Y'
    if locale == 'en_US':
        time_formatter = '%m/%d/%Y'

    timezone = timezone_obj or pytz.timezone(timezone_string)

    return datetime.datetime.fromtimestamp(
        timestamp,
        timezone
    ).strftime(time_formatter)


def format_date_time(timestamp, timezone_string=None, timezone_obj=None, locale='en_US'):
    if timestamp is None:
        return '--'

    time_formatter = '%d/%m/%Y %H:%M'
    if locale == 'en_US':
        time_formatter = '%m/%d/%Y %I:%M %p'

    timezone = timezone_obj or pytz.timezone(timezone_string)

    return datetime.datetime.fromtimestamp(
        timestamp,
        timezone
    ).strftime(time_formatter)
