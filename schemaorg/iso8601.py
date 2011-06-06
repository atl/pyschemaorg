"""ISO 8601 date time string parsing

Copyright (c) 2007 Michael Twomey

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Basic usage:
>>> import iso8601
>>> iso8601.parse_date("2007-01-25T12:00:00Z")
datetime.datetime(2007, 1, 25, 12, 0, tzinfo=<iso8601.iso8601.Utc ...>)
>>>

"""

from datetime import datetime, timedelta, tzinfo, date, time
import re

__all__ = ["parse_date", "ParseError"]

# Adapted from http://delete.me.uk/2005/03/iso8601.html
ISO8601_REGEX = re.compile(r"((?P<year>[0-9]{4})(-(?P<month>[0-9]{1,2})(-(?P<day>[0-9]{1,2}))?)?)?"
 r"((T?(?P<hour>[0-9]{2})(:(?P<minute>[0-9]{2})(:(?P<second>[0-9]{2})(\.|,(?P<fraction>[0-9]+))?)?)?)?"
 r"(?P<timezone>Z|(([-+])([0-9]{2}):([0-9]{2})))?)?"
)

TIMEZONE_REGEX = re.compile("(?P<prefix>[+-])(?P<hours>[0-9]{2}).(?P<minutes>[0-9]{2})")

class ParseError(Exception):
    """Raised when there is a problem parsing a date string"""

# Yoinked from python docs
ZERO = timedelta(0)
class Utc(tzinfo):
    """UTC
    
    """
    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO
UTC = Utc()

class FixedOffset(tzinfo):
    """Fixed offset in hours and minutes from UTC
    
    """
    def __init__(self, offset_hours, offset_minutes, name):
        self.__offset = timedelta(hours=offset_hours, minutes=offset_minutes)
        self.__name = name

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return ZERO
    
    def __repr__(self):
        return "<FixedOffset %r>" % self.__name

class TruncDate(object):
    def __init__(self, year, *args):
        if len(args) == 0 or args[0] == 0:
            self.date_resolution = 'year'
            self.date = date(year, 1, 1)
            self.resolution = timedelta(days=365)
            self._strformat = '%Y'
        elif len(args) == 1 or args[1] == 0:
            self.date_resolution = 'month'
            self.date = date(year, args[0], 1)
            self.resolution = timedelta(days=28)
            self._strformat = '%Y-%m'
        else:
            self.date_resolution = 'day'
            self.date = date(year, *args)
            self.resolution = timedelta(days=1)
            self._strformat = '%Y-%m-%d'
    
    def isoformat(self):
        return self.date.strftime(self._strformat)
    
    def __str__(self):
        return self.isoformat()
    

def parse_timezone(tzstring, default_timezone=UTC):
    """Parses ISO 8601 time zone specs into tzinfo offsets
    
    """
    if tzstring == "Z":
        return default_timezone
    if tzstring is None:
        return None
    m = TIMEZONE_REGEX.match(tzstring)
    prefix, hours, minutes = m.groups()
    hours, minutes = int(hours), int(minutes)
    if prefix == "-":
        hours = -hours
        minutes = -minutes
    return FixedOffset(hours, minutes, tzstring)

def parse_date(datestring, default_timezone=UTC):
    """Parses ISO 8601 dates into datetime objects
    
    The timezone is parsed from the date string. However it is quite common to
    have dates without a timezone (not strictly correct). In this case the
    default timezone specified in default_timezone is used. This is UTC by
    default.
    """
    if not isinstance(datestring, basestring):
        raise ParseError("Expecting a string %r" % datestring)
    m = ISO8601_REGEX.match(datestring)
    if not m:
        raise ParseError("Unable to parse date string %r" % datestring)
    groups = m.groupdict()
    tz = parse_timezone(groups["timezone"], default_timezone=default_timezone)
    if groups["fraction"] is None:
        groups["fraction"] = 0
    else:
        groups["fraction"] = int(float("0.%s" % groups["fraction"]) * 1e6)
    if groups['year'] and groups['hour']:
        return datetime(int(groups["year"]), int(groups["month"]), int(groups["day"]),
            int(groups["hour"]), int(groups["minute"] or 0), int(groups["second"] or 0),
            int(groups.get("fraction")), tz)
    elif groups['year'] and not groups['hour']:
        return TruncDate(int(groups["year"] or 0), int(groups["month"] or 0), int(groups["day"] or 0))
    elif not groups['year'] and groups['hour']:
        return time(int(groups.get("hour")), int(groups["minute"] or 0), int(groups["second"] or 0),
            int(groups.get("fraction")), tz)
