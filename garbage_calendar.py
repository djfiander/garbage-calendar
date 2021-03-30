#! /bin/env python3

from datetime import date, timedelta, datetime
import uuid
import sys

tomorrow = timedelta(days=1)
tumble = 6
Saturday = 5
Sunday = 6
seps = str.maketrans('', '', '-: ')

# The first garbage day
start = date(2020, 10, 1)

# statutory holidays. The generator stops when there are no more
# holidays in the list.
holidays = [date(2020, 10, 12), # Thanksgiving - moveable
            date(2020, 12, 25), # fixed
            date(2020, 12, 28), # fixed
            date(2021,  1,  1), # fixed
            date(2021,  2, 15), # family day - moveable
            date(2021,  4,  2), # Easter - moveable
            date(2021,  4,  5), # Easter - moveable
            date(2021,  5, 24), # Victoria day - moveable
            date(2021,  7,  1), # fixed
            date(2021,  8,  2), # Civic holiday - moveable
            date(2021,  9,  6) # Labour day - moveable
]

# The first day of each yard waste collection week.
yard_waste = [date(2020, 10, 13),
              date(2020, 11,  2),
              date(2020, 11, 23),
              date(2021,  4,  6),
              date(2021,  5, 17),
              date(2021,  6, 28),
              date(2021,  8,  9),
              date(2021,  9, 20)]

event = """BEGIN:VEVENT
DTSTART;VALUE=DATE:{start_date}
DTEND;VALUE=DATE:{end_date}
DTSTAMP:""" + \
    datetime.utcnow().isoformat(timespec='seconds').translate(seps) + 'Z' + \
"""
SEQUENCE:0
SUMMARY:{summary}
TRANSP:TRANSPARENT
UID:{uid}
END:VEVENT"""

def format_date(d):
    return d.isoformat().translate(seps)

def print_event(date, summary):
    print(event.format(start_date=format_date(date),
                       end_date=format_date(date+tomorrow),
                       summary=summary,
                       uid=uuid.uuid1()))

def isholiday(d):
    global holidays
    global holiday_month

    while len(holidays) > 0 and d > holidays[0]:
        holidays.pop(0)

    if len(holidays) == 0 or d != holidays[0]:
        return False

    holiday_month = d.month
    holidays.pop(0)
    return True


def next_saturday(d):
    while d.weekday() != Saturday:
        d += tomorrow
    return d

print("""BEGIN:VCALENDAR
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:PUBLISH
PRODID:-//FastMail/1.0/EN
X-WR-CALNAME:Garbage
X-WR-TIMEZONE:America/Toronto""")

for d in yard_waste:
    print(event.format(summary="Yard Waste",
                       start_date=format_date(d),
                       end_date=format_date(next_saturday(d)),
                       uid=uuid.uuid1()))

next = start
holiday_month = 0

while len(holidays) > 0 or next.month == holiday_month:
    last = next

    print_event(next, "Garbage")

    for i in range(0, tumble):
        next = next + tomorrow
        while next.weekday() in (Saturday, Sunday) or isholiday(next):
            next = next + tomorrow

print_event(last, "Update garbage calendar")
print("END:VCALENDAR")
