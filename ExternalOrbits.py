# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 21:41:25 2022

@author: Matthew

Compilation of external orbital dynamics code.
Some has been converted from Matlab to python.

https://orbital-mechanics.space/reference/julian-date.html
"""

from datetime import date, datetime, time, timezone, timedelta

"""
-------------------------------------------------------------------------------
CODE FROM https://orbital-mechanics.space/reference/julian-date.html
-------------------------------------------------------------------------------
"""

def gregorian_to_julian_day_number(month, day, year):
    """Convert the given proleptic Gregorian date to the equivalent Julian Day Number."""
    if month < 1 or month > 12:
        raise ValueError("month must be between 1 and 12, inclusive")
    if day < 1 or day > 31:
        raise ValueError("day must be between 1 and 31, inclusive")
    A = int((month - 14) / 12)
    B = 1461 * (year + 4800 + A)
    C = 367 * (month - 2 - 12 * A)
    E = int((year + 4900 + A) / 100)
    JDN = int(B / 4) + int(C / 12) - int(3 * E / 4) + day - 32075
    return JDN

def gregorian_to_julian_date(dt):
    """Convert a Gregorian date to a Julian Date."""
    JDN = gregorian_to_julian_day_number(dt.month, dt.day, dt.year)
    JDT = JDN + (dt.hour - 12) / 24 + dt.minute / 1_440 + dt.second / 86_400 + dt.microsecond / 86_400_000_000
    return JDT

def julian_day_number_to_gregorian(jdn):
    """Convert the Julian Day Number to the proleptic Gregorian Year, Month, Day."""
    L = jdn + 68569
    N = int(4 * L / 146_097)
    L = L - int((146097 * N + 3) / 4)
    I = int(4000 * (L + 1) / 1_461_001)
    L = L - int(1461 * I / 4) + 31
    J = int(80 * L / 2447)
    day = L - int(2447 * J / 80)
    L = int(J / 11)
    month = J + 2 - 12 * L
    year = 100 * (N - 49) + I + L
    return year, month, day

def julian_date_to_gregorian(jd):
    """Convert a decimal Julian Date to the equivalent proleptic Gregorian date and time."""
    jdn = int(jd)
    if jdn < 1_721_426:
        raise ValueError("Julian Day Numbers less than 1,721,426 are not supported, "
                         "because Python's date class cannot represent years before "
                         "AD 1.")
    year, month, day = julian_day_number_to_gregorian(jdn)
    offset = timedelta(days=(jd % 1), hours=+12)
    dt = datetime(year=year, month=month, day=day, tzinfo=timezone.utc)
    return dt + offset

"""
TESTING------------------------------------------------------------------------
"""
"""
today = date(year=2020, month=12, day=7)
jdn = gregorian_to_julian_day_number(today.month, today.day, today.year)
print(today)
print(jdn)

evening = datetime.combine(today, time(hour=18, minute=12, second=43, microsecond=674805), tzinfo=timezone.utc)
print(evening)
jdt_evening = gregorian_to_julian_date(evening)
print(jdt_evening)
morning = evening.replace(hour=6, minute=0, second=0, microsecond=0)
print(morning)
jdt_morning = gregorian_to_julian_date(morning)
print(jdt_morning)

gregorian_evening = julian_date_to_gregorian(jdt_evening)
print(gregorian_evening)
gregorian_morning = julian_date_to_gregorian(jdt_morning)
print(gregorian_morning)

print(julian_day_number_to_gregorian(0))
"""