# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 16:45:41 2021

@author: Matthew
"""

import numpy as np
from scipy import constants as const
import math
from numba import jit

Y2D = 336 # Khorvaire year to days
M2D = 28 # Khorvaire month to days
W2D = 7 # Galifar week to days
T2D = 3 # Aerenal tuern to days
L2D = 21*T2D # Aerenal luenir to days (63) (12 per Xendrik year)
TH2D = 12*L2D # Aerenal thuelir to days (756 = 1 Xendrik year, 2.25 Khorvaire years)
R2D = 3*TH2D # Aerenal rueln to days (2268) (6.75 Khorvaire years)
N2D = 2*R2D # Aerenal nuerlnir to days (4536) (6 Xendrik years, 13.5 Khorvaire years)
S2D = 112 # Sovereign season to days
SW2D = 16 # Sovereign week to days
WC2D = 3 # Quor Tarai waking cycle to days
SC2D = 14 # Quor Tarai sleeping cycle to days
DR2D = 5 # kalashtar Days of Remembrance to days
Y2DDR = 67*DR2D # kalashtar year, 67 Days of Remembrance
Y2DHARP = 365 # Toril, Harptos calendar year to days
M2DHARP = 30 # Toril, Harptos calendar month to days
W2DHARP = 10 # Toril, Harptos calendar week (tenday) to days

DAY = const.day # one Khorvaire day, sec
YEAR = Y2D*const.day # one Khorvaire year, sec
MONTH = M2D*const.day # one Khorvaire month, sec
WEEK = const.week # one Galifar week, sec
TUERN = T2D*const.day # one Aerenal tuern, sec
LUENIR = L2D*const.day # one Aerenal luenir, sec
THUELIR = TH2D*const.day # one Aerenal thuelir, sec (1 Xendrik year)
RUELN = R2D*const.day # one Aerenal rueln, sec
NUERLNIR = N2D*const.day # one Aerenal nuerlnir, sec
SEASON = S2D*const.day # one Sovereign season, sec
SWEEK = SW2D*const.day # one Sovereign week, sec
WAKING = WC2D*const.day # one waking cycle, sec
SLEEPING = SC2D*const.day # one sleeping cycle, sec
REMEMBRANCE = DR2D*const.day # one Days of Remembrance period, sec
YEARHARP = Y2DHARP*const.day # one Toril year, sec
MONTHHARP = M2DHARP*const.day # one Toril month, sec
WEEKHARP = W2DHARP*const.day # one Toril week (tenday), sec

caldesc = {'Galifar': """
               In the common calendar of Khorvaire, days are 24
               hours long, divided into day and night. Seven days make
               up a week, four weeks a month, and twelve months a
               year. The months correspond to the twelve moons of
               Eberron, and the prominent moon carries the name of the
               month in which its orbit brings it closest to the planet.
               The seven days of the week, in order, are Sul, Mol,
               Zol, Wir, Zor, Far, Sar.
               The common calendar of Khorvaire tracks the years
               since the founding of the kingdom of Gali far, using
               the abbreviation YK. The last king of Galifar, Jarot
               ir'Wynarn, died on 1 2 Therendor 894 YK. The Day of
               Mourning occurred a century later, on 20 Olarune 994
               YK. Our Eberron campaign begins on 1 Zarantyr 998 YK.
               
               Month    Name
               ----------------------------------
               1        Zarantyr (mid-winter)
               2        Olarune (late winter)
               3        Therendor (early spring)
               4        Eyre (mid-spring)
               5        Dravago (late spring)
               6        Nymm (early summer)
               7        Lharvion (mid-summer)
               8        Barrakas (late summer)
               9        Rhaan (early autumn)
               10       Sypheros (mid-autumn)
               11       Aryth (late autumn)
               12       Vult (early winter)
               
               Eberron - Rising from the Last War, p.7
               
               GM's note:
               One Khorvaire year equals one orbit around Arrah, and
               is 336 days long, which is 92% of an Earth year.
               A 20-year old Khorvairian would be 18.4 years old by
               Earth reckoning. The Code of Galifar recognizes
               adulthood at 20.
               """,
           'Gatekeeper': '',
           'Mror': '',
           'Talenta': '',
           'Aereni': """
               The Aereni calendar is a strange affair, practically
               unreadable to anyone not raised with it. It measures
               time in repeating cycles. For instance, while the calendar
               acknowledges the concept of “days,” they are not considered
               important measurements of time in their own
               right. Rather, they are the component parts to overlapping
               cycles called tuernai (singular tuern), which consist of
               three days each and are the primary unit of measurement
               on the Aereni calendar. A similar overlapping cycle of
               twenty-one tuernai equals a luenir, roughly three months
               on the Galifar calendar. This process continues, with
               luenirai overlapping to eventually form the Aereni year,
               years forming cycles called ruelnai, and ruelnai forming
               nuerlnirai (roughly analogous to a decade). Only then does
               the calendar restart. Specific holidays vary by family and
               the deathdays of ancestors.
               
               The Khorvaire year is 336 days (one orbit around Arrah).
               The Aerenal year is 756 days, which is 2.25 Khorvaire years
               (2 years 3 months). The Aereni measure this as one thuelir.
               
               The Aereni calendar counts the number of nuerlnirai since
               their ancestors made landfall on Aerenal as they fled
               the destruction of Xen'drik. Aeren Kriaddal, the oracle
               whose visions catalyzed the effort, did not live to see
               their new home. The elves named the planetoid Aerenal
               in their honor, and abbreviate their calendar as "NA",
               "Nuerlnir of Aeren".
               
               Our campaign starts on 1 Zarantyr 998 YK, which is:
               the 2nd of 7-9-2-1-2962 NA
               2nd day, 7th tuern, 9th luenir, 2nd thuelir, 1st rueln
               in the 2962nd nuerlnir of Aeren
               
               Unit     Equivalent   Days   Note
               ----------------------------------------------------------------
               Tuern                 3      252 per Aereni year
               Luenir   21 tuernai   63     12 per Aereni year
               Thuelir  12 luenirai  756    1 Aereni year, 2.25 Khorvaire years
               Rueln    3 thuelirai  2268   6.75 Khorvaire years (6y 9mo)
               Nuerlnir 2 ruelnai    4536   6 Aereni years, 13.5 Khorvaire years
               
               -Faiths of Eberron, p.141
               """,
           'Sovereign': """
               Worship of the Sovereign Host predates the formation
               of the great kingdom of Galifar. Thus, while all Vassals
               use the standard Galifar calendar in day-to-day
               life, they measure days of religious significance on
               the far older Sovereign Book of Seasons (or simply the
               Sovereign calendar).
               The original Vassals divided the year into three
               seasons, rather than four. Yearbirth, the first season,
               was associated with the dragon Siberys. Yeargrowth, the
               second season, was associated with Eberron. Finally,
               Yeardeath was associated with Khyber.
               Each season was divided into seven “weeks” of sixteen
               days each. Each day of the week was devoted to one of the
               fifteen gods of the original Sovereign Host, with an
               additional day at the end of the week devoted to the
               pantheon as a single unit.
               Additionally, each god has a favored season during
               which their festivals are particularly important.
               In the modern era, the names of the days formerly
               devoted to the Dark Six have been renamed after the
               Five Kingdoms and Galifar itself.
               The new year on the Sovereign calendar corresponds
               with the first day of the month of Therendor on the
               Galifar calendar.
               The weeks do not carry any names of their own. To
               indicate a specific day, someone using the Sovereign
               calendar adds a numeric value to the day in question.
               For instance, saying “Yearbirth Thranday the fourth”
               or “fourth Thranday of Yearbirth” indicates Thranday
               during the fourth week of the Yearbirth season.
               
               Day of the       Associated              Favored
               Celestial Week   Deity                   Season
               ---------------------------------------------------
               Aureday          Aureon                  Yeargrowth
               Karrnday         (Formerly the Fury)     Yeargrowth
               Kolday           Kol Korran              Yearbirth
               Baliday          Balinor                 Yeargrowth
               Thranday         (Formerly the Mockery)  Yeardeath
               Olladay          Olladra                 Yearbirth
               Galday           (Formerly the Shadow)   Yeardeath
               Bolday           Boldrei                 Yeargrowth
               Brelday          (Formerly the Keeper)   Yeardeath
               Onaday           Onatar                  Yearbirth
               Araday           Arawai                  Yearbirth
               D’arrday         Dol Arrah               Yeargrowth
               Aunday           (Formerly the Traveler) Yearbirth
               Dornday          Dol Dorn                Yeardeath
               Cyrday           (Formerly the Devourer) Yeardeath
               Hostday          The Sovereign Host      Yearbirth
               
               Faiths of Eberron, p.21-22
               """,
           'Qabalrin': """
               The Blood of Vol has been around since long before the
               formation of Galifar, and thus does not use the standard
               calendar to mark either religious observances or the passage
               of time. The faith follows the oldest active calendar
               on Eberron, called the Qabalrin Wheel. Named after
               the elf civilization that developed it on Xen’drik millennia
               ago, it was the only calendar of record for much of
               Eberron’s early history. Like its modern counterpart, the
               Qabalrin Wheel is divided into months that correspond
               to the moons of Eberron, but unlike the Galifar calendar,
               it still recognizes the thirteenth moon (believed
               lost to the cosmos when the giants sealed off the plane of
               Xoriat so many centuries ago). The Wheel has thirteen
               months rather than the standard twelve, with the last—
               Crya, associated with the lost Mark of Death—coming
               after Vult and before Zarantyr on the Galifar calendar.
               This renders the Qabalrin Wheel year one month longer
               than the Galifar year.
               The Blood of Vol liturgical calendar reckons time
               from the year when the House of Vol was betrayed, forcing
               its last scion into an eternity of undeath. To Seekers in the
               know, 998 YK corresponds to 2398 FH (the 2398th year
               since the Fall of the House). Many Seekers do not use this
               convention, of course, and even those who do still use the
               Galifar calendar for dealings outside the faith.
               
               Faiths of Eberron, p.80
               """,
           'Adar': """
               In the private lives of all kalashtar and lightspeakers,
               wherever they live, a year consists of sixty-seven periods
               of five days each. Each ancestor quori has five of its own
               Days of Remembrance, with the Void of Taratai coming
               last in the sequence. This calendar was established just
               after the exodus, when the fugitive quori fled into Adar,
               and it did not take into account the regular celestial
               events of Eberron.
               Among the people of Adar and Khorvaire, the
               kalashtar use the usual calendar. They still practice Days
               of Remembrance, but these days shift in the year to keep
               time with a cycle that doesn’t contain 335 days. Only
               the Void of Taratai observances are regular in Adar and
               Khorvaire, set when the last of Taratai’s line disappeared
               from Adar—at the end of Zarantyr and the beginning of
               Olarune. The other Days of Remembrance are observed
               privately as they occur, except when they overlap the
               Void. Any such period is interrupted by those fi ve days,
               restarting after they end.
               
               -Faiths of Eberron, p.129
               """
          }

Gm = {'Zarantyr': 1,
      'Olarune':  2,
      'Therendor':3,
      'Eyre':     4,
      'Dravago':  5,
      'Nymm':     6,
      'Lharvion': 7,
      'Barrakas': 8,
      'Rhaan':    9,
      'Sypheros': 10,
      'Aryth':    11,
      'Vult':     12} # Galifar month names
monthnames = ['Zarantyr',
              'Olarune',
              'Therendor',
              'Eyre',
              'Dravago',
              'Nymm',
              'Lharvion',
              'Barrakas',
              'Rhaan',
              'Sypheros',
              'Aryth',
              'Vult'] # Galifar month names
druidmonths = {'Zarantyr': 'Frostmantle',
               'Olarune':  'Thornrise',
               'Therendor':'Treeborn',
               'Eyre':     'Rainsong',
               'Dravago':  'Arrowfar',
               'Nymm':     'Sunstride',
               'Lharvion': 'Glitterstream',
               'Barrakas': 'Havenwild',
               'Rhaan':    'Stormborn',
               'Sypheros': 'Harrowfall',
               'Aryth':    'Silvermoon',
               'Vult':     'Windwhisper'} # Gatekeeper (druidic) month names
dwarfmonths = {'Zarantyr': 'Aruk',
               'Olarune':  'Lurn',
               'Therendor':'Ulbar',
               'Eyre':     'Kharn',
               'Dravago':  'Ziir',
               'Nymm':     'Dwarhuun',
               'Lharvion': 'Jond',
               'Barrakas': 'Sylar',
               'Rhaan':    'Razagul',
               'Sypheros': 'Thazm',
               'Aryth':    'Drakhadur',
               'Vult':     'Uarth'} # Mror (dwarven) month names
talentamonths = {'Zarantyr': 'Fang',
                 'Olarune':  'Wind',
                 'Therendor':'Ash',
                 'Eyre':     'Hunt',
                 'Dravago':  'Song',
                 'Nymm':     'Dust',
                 'Lharvion': 'Claw',
                 'Barrakas': 'Blood',
                 'Rhaan':    'Horn',
                 'Sypheros': 'Heart',
                 'Aryth':    'Spirit',
                 'Vult':     'Smoke'} # Talenta month names
Gd = {'Sul':1,
      'Mol':2,
      'Zol':3,
      'Wir':4,
      'Zor':5,
      'Far':6,
      'Sar':7} # Galifar week names
daynames = ['Sul','Mol','Zol','Wir','Zor','Far','Sar'] # Galifar day names
Ss = {'Yearbirth': 1,
      'Yeargrowth':2,
      'Yeardeath': 3} # Sovereign seasons
seasonnames = ['Yearbirth','Yeargrowth','Yeardeath'] # Sovereign seasons
Sd = {'Aureday': 1,
      'Karrnday':2,
      'Kolday':  3,
      'Baliday': 4,
      'Thranday':5,
      'Olladay': 6,
      'Galday':  7,
      'Bolday':  8,
      'Brelday': 9,
      'Onaday':  10,
      'Araday':  11,
      'Darrday': 12,
      'Aunday':  13,
      'Dornday': 14,
      'Cyrday':  15,
      'Hostday': 16} # Sovereign week days
sdaynames = ['Aureday',
             'Karrnday',
             'Kolday',
             'Baliday',
             'Thranday',
             'Olladay',
             'Galday',
             'Bolday',
             'Brelday',
             'Onaday',
             'Araday',
             'Darrday',
             'Aunday',
             'Dornday',
             'Cyrday',
             'Hostday'] # Sovereign week days
Sf = {'Aureday': 'Yeargrowth',
      'Karrnday':'Yeargrowth',
      'Kolday':  'Yearbirth',
      'Baliday': 'Yeargrowth',
      'Thranday':'Yeardeath',
      'Olladay': 'Yearbirth',
      'Galday':  'Yeardeath',
      'Bolday':  'Yeargrowth',
      'Brelday': 'Yeardeath',
      'Onaday':  'Yearbirth',
      'Araday':  'Yearbirth',
      'Darrday': 'Yeargrowth',
      'Aunday':  'Yearbirth',
      'Dornday': 'Yeardeath',
      'Cyrday':  'Yeardeath',
      'Hostday': 'Yearbirth'} # Sovereign favored seasons
Hm = {'Hammer':   1,
      'Alturiak': 2,
      'Ches':     3,
      'Tarsakh':  4,
      'Mirtul':   5,
      'Kythorn':  6,
      'Flamerule':7,
      'Eleasias': 8,
      'Eleint':   9,
      'Marpenoth':10,
      'Uktar':    11,
      'Nightal':  12} # Harptos calendar month names & numbers
Hmonthnames = ['Hammer',
               'Alturiak',
               'Ches',
               'Tarsakh',
               'Mirtul',
               'Kythorn',
               'Flamerule',
               'Eleasias',
               'Eleint',
               'Marpenoth',
               'Uktar',
               'Nightal'] # Harptos calendar month names
Hcommonmonths = {'Hammer':   'Deepwinter',
                 'Alturiak': 'The Claw of Winter',
                 'Ches':     'The Claw of the Sunsets',
                 'Tarsakh':  'The Claw of the Storms',
                 'Mirtul':   'The Melting',
                 'Kythorn':  'The Time of Flowers',
                 'Flamerule':'Summertide',
                 'Eleasias': 'Highsun',
                 'Eleint':   'The Fading',
                 'Marpenoth':'Leaffall',
                 'Uktar':    'The Rotting',
                 'Nightal':  'The Drawing Down'} # Harptos common month names
Hannuals = ['Midwinter',
            'Greengrass',
            'Midsummer',
            'Highharvesttide',
            'The Feast of the Moon'] # Harptos annual holidays
Hquadrennial = 'Shieldmeet' # Harptos quadrennial holiday
Hyear = ['Hammer',
         'Midwinter',
         'Shieldmeet',
         'Alturiak',
         'Ches',
         'Tarsakh',
         'Greengrass',
         'Mirtul',
         'Kythorn',
         'Flamerule',
         'Midsummer',
         'Eleasias',
         'Eleint',
         'Highharvesttide',
         'Marpenoth',
         'Uktar',
         'The Feast of the Moon',
         'Nightal'] # Harptos calendar year

def ordinal(n=0):
    # return the input number as an ordinal string
    # ie select from list 0th, 1st, 2nd, 3rd, 4th, etc
    s = str(n)
    s2 = ''
    if abs(n)>20: # handle numbers >20 recursively
        s2 = ordinal(np.mod(abs(n), 10))[1:]
    elif abs(n) == 1: s2 = 'st' # 1st
    elif abs(n) == 2: s2 = 'nd' # 2nd
    elif abs(n) == 3: s2 = 'rd' # 3rd
    else: s2 = 'th' # 0th, or 4th and up
    string = s + s2
    return string

def val2key(d, val):
    # search {'string': int} dictionary backwards
    # given value val, return matching key from d
    return list(d.keys())[list(d.values()).index(val)]

def wrap(x, y, xmax, base=0):
    # wrap number in x into y given max value of x, xmax
    # base is min number in set, ie [base, base+1, ... xmax-1, xmax]
    if x > xmax:
        _y, xnew = np.divmod(x, xmax)
        ynew = y + _y
        #xnew += base
        return xnew, ynew
    else: return x, y

class GalifarDate:
    # Galifar Calendar (common calendar of Khorvaire)
    def __init__(self, d=1, m='Zarantyr', y=998):
        self.day = d
        self.month = m
        self.year = y
    def disp(self, dofw=False, cal='Galifar', verbose=False):
        # return the date as a string
        if verbose:
            dofw=True
            d = ordinal(self.day)
            y = ordinal(self.year)
            epoch = ' Year of the Kingdom'
        else:
            d = str(self.day)
            epoch = ' YK'
            y = str(self.year)
        if cal=='Galifar': m = self.month
        elif cal=='Gatekeeper': m = druidmonths[self.month]
        elif cal=='Mror': m = dwarfmonths[self.month]
        elif cal=='Talenta': m = talentamonths[self.month]
        string = d + ' ' + m + ' ' + y + epoch
        if dofw:
            _d = self.day
            while _d > 7:
                _d = _d - 7 # constrain day to range 1-7
            dw = daynames[_d-1]
            return dw + ', ' + string # add day of week to date
        else: return string
    def days(self):
        # convert date to day of year
        dm = (Gm[self.month]-1)*M2D # elapsed months to days
        return dm + self.day
    def GD(self):
        # Galifaran day (similar to Julian Day)
        # number of days since 1 Zarantyr 0 YK
        dY = self.year*Y2D # GD of 1 Zarantyr, current year
        return dY + self.days()
    def increment(self, d=1, m=0, y=0):
        # add specified amount of time to current date
        self.day += d
        if self.day > 28:
            _m, _d = np.divmod(self.day, 28)
            self.day = _d
            m += _m
        mnum = Gm[self.month]
        mnew = mnum + m
        if mnew > 12:
            _y, _m = np.divmod(mnew, 12)
            self.year += _y
            self.month = val2key(Gm, _m)
        else: self.month = val2key(Gm, mnew)
        self.year += y
    def add_day(self, days=1):
        # wrapper for self.increment()
        self.increment(d=days)
    def add_month(self, months=1):
        # wrapper for self.increment()
        self.increment(d=0, m=months)
    def add_year(self, years=1):
        # wrapper for self.increment()
        self.increment(d=0, y=years)

class AereniDate:
    # Aerenal Calendar (Qabalrin Wheel?)
    def __init__(self, d=2, t=7, l=9, th=2, r=1, n=2999):
        self.day = d
        self.tuern = t
        self.luenir = l
        self.thuelir = th
        self.rueln = r
        self.nuerlnir = n
    def disp(self, verbose=False):
        # return the date as a string
        d = ordinal(self.day)
        t = str(self.tuern)
        t_o = ordinal(self.tuern)
        l = str(self.luenir)
        l_o = ordinal(self.luenir)
        th = str(self.thuelir)
        th_o = ordinal(self.thuelir)
        r = str(self.rueln)
        r_o = ordinal(self.rueln)
        n = str(self.nuerlnir)
        n_o = ordinal(self.nuerlnir)
        # standard date: 2nd of 7-9-2-1-2962 NA
        string = t + '-' + l + '-' + th + '-' + r + '-' + n + ' NA'
        string = d + ' of ' + string # add day to date
        # verbose date:
        # 2nd day, 7th tuern, 9th luenir, 2nd thuelir, 1st rueln
        # in the 2962nd nuerlnir of Aeren
        vstr = d + ' day, ' + t_o + ' tuern, ' + l_o + ' luenir, '
        vstr += th_o + ' thuelir, ' + r_o + ' rueln in the '
        vstr += n_o + ' nuerlnir of Aeren'
        if verbose: return vstr # verbose date format
        else: return string # standard date format
    def days(self):
        # convert date to day of nuerlnir
        dr = self.rueln*R2D # elapsed ruelnai to days
        dth = self.thuelir*TH2D # elapsed thuelirai to days
        dl = self.luenir*L2D # elapsed luenirai to days
        dt = self.tuern*T2D # elapsed tuernai to days
        return dr + dth + dl + dt + self.day
    def AD(self):
        # Aerenalian day (similar to Julian Day)
        # number of days since 1 1-1-1-1-0 NA
        dN = self.nuerlnir*N2D # AD of 1st day of current nuerlnir
        return dN + self.days()
    def GD(self):
        # Galifaran day (similar to Julian Day)
        # number of days since 1 Zarantyr 0 YK
        Y0 = galifar2aereni(GalifarDate(y=0)) # year 0 YK in the Aereni calendar
        GD = self.AD() - Y0.AD() + 1 # days since Y0
        return GD
    def increment(self, d=1, t=0, l=0, th=0, r=0, n=0):
        # add specified amount of time to current date
        self.day += d
        self.day, self.tuern = wrap(self.day, self.tuern, 3, 1)
        self.tuern += t
        self.tuern, self.luenir = wrap(self.tuern, self.luenir, 21, 1)
        self.luenir += l
        self.luenir, self.thuelir = wrap(self.luenir, self.thuelir, 12, 1)
        self.thuelir += th
        self.thuelir, self.rueln = wrap(self.thuelir, self.rueln, 3, 1)
        self.rueln += r
        self.rueln, self.nuerlnir = wrap(self.rueln, self.nuerlnir, 2, 1)
        self.nuerlnir += n
    
class SovereignDate:
    # Sovereign Book of Seasons (old Sarlonan - Pyrine)
    # celebrates the Celestial Week
    def __init__(self, w=4, d='Brelday', s='Yeardeath', y=998):
        self.week = w
        self.day = d
        self.season = s
        self.year = y
    def disp(self, fav=False):
        # return the date as a string
        w = ordinal(self.week)
        string1 = w+' '
        string2 = self.day+' of '+self.season+' '+str(self.year)+' YK'
        if fav:
            if Sf[self.day]==self.season:
                string1 += 'Favored '
        return string1 + string2
    def days(self):
        # convert date to day of year
        ds = (Ss[self.season]-1)*S2D # elapsed seasons to days
        dw = (self.week-1)*SW2D # elapsed weeks to days
        offset = GalifarDate(m='Therendor').days()-1 # the Sovereign year starts on 1 Therendor
        d = ds + dw + Sd[self.day] + offset
        if d>Y2D: d = d - Y2D # wrap to next year if day of year > 336
        return d
    def GD(self):
        # Galifaran day (similar to Julian Day)
        # number of days since 1 Zarantyr 0 YK
        dY = self.year*Y2D # GD of 1 Zarantyr, current year
        return dY + self.days()

#@jit(nopython=True, parallel=True)
def GD2date(GD = GalifarDate().GD()):
    year = math.floor(GD/Y2D) # years since 0 YK
    _day = np.mod(GD, Y2D) # remaining days
    month = math.floor(_day/M2D) # months since start of current year
    day = np.mod(_day, M2D) # remaining days
    return GalifarDate(d=day, m=monthnames[month], y=year)

#@jit(nopython=True, parallel=True)    
def galifar2aereni(YK = GalifarDate()):
    dA = (40499*Y2D) + (6*M2D) # days since landing on Aeren
    dY = (YK.year-998)*Y2D # years from 998 YK in days
    dM = (Gm[YK.month]-1)*M2D # months from year start in days
    _day = dA + dY + dM + YK.day # total days since landing on Aeren
    nuerlnir = math.floor(_day/N2D) # nuerlnirai since Aeren landing
    _day = np.mod(_day, N2D) # remaining days
    rueln = math.floor(_day/R2D) # ruelnai since Aeren landing
    _day = np.mod(_day, R2D) # remaining days
    thuelir = math.floor(_day/TH2D) # thuelirai since Aeren landing
    _day = np.mod(_day, TH2D) # remaining days
    luenir = math.floor(_day/L2D) # luenirai since Aeren landing
    _day = np.mod(_day, L2D) # remaining days
    tuern = math.floor(_day/T2D) # tuernai since Aeren landing
    day = np.mod(_day, T2D)+1 # remaining days
    return AereniDate(d=day, t=tuern, l=luenir, th=thuelir, r=rueln, n=nuerlnir)

#@jit(nopython=True, parallel=True)
def aereni2galifar(NA = AereniDate()):
    Y0 = galifar2aereni(GalifarDate(y=0)) # year 0 YK in the Aereni calendar
    GD = NA.AD() - Y0.AD() + 1 # days since Y0
    return GD2date(GD)

#@jit(nopython=True, parallel=True)
def sovereign2galifar(SK = SovereignDate()):
    return GD2date(SK.GD())

#@jit(nopython=True, parallel=True)
def galifar2sovereign(YK = GalifarDate()):
    year = YK.year
    dayofyear = YK.days()
    offset = GalifarDate(m='Therendor').days() # the Sovereign year starts on 1 Therendor
    dayofyear = dayofyear - offset # day of year relative to Sovereign year start
    if dayofyear<0: # wrap to previous year
        dayofyear = dayofyear + Y2D
    season = seasonnames[math.floor(dayofyear/S2D)]
    dayofseason = np.mod(dayofyear, S2D)
    week = math.floor(dayofseason/SW2D)+1
    dayofweek = np.mod(dayofseason, SW2D)
    day = sdaynames[dayofweek]
    return SovereignDate(w=week, d=day, s=season, y=year)

# TEST
    
#test = GalifarDate()
#test.add_month()

'''
test1 = GalifarDate(d=20, m='Olarune', y=994)
print(test1.disp(dofw=True, cal='Gatekeeper'))
print('day of year: '+str(test1.days()))
print('GD '+str(test1.GD()))

test2 = galifar2aereni(test1)
print(test2.disp(True))
print('day of nuerlnir: '+str(test2.days()))

test3 = GD2date(test1.GD())
print(test3.disp())

test4 = aereni2galifar(test2)
print(test4.disp())

test5 = SovereignDate(s='Yeardeath')
print(test5.disp(True))

test6 = sovereign2galifar(test5)
print(test6.disp(True))

print(' ')
test7 = aereni2galifar(galifar2aereni(GalifarDate()))
print(test7.disp(True))

test8 = galifar2aereni(aereni2galifar(AereniDate()))
print(test8.disp(True))

test9 = galifar2sovereign(sovereign2galifar(SovereignDate()))
print(test9.disp(True))

test10 = sovereign2galifar(galifar2sovereign(GalifarDate()))
print(test10.disp(True))
'''