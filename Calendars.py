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
L2D = 21*T2D # Aerenal luenir to days (63)
TH2D = 12*L2D # Aerenal thuelir to days (756 = 1 Xendrik year)
R2D = 3*TH2D # Aerenal rueln to days (2268)
N2D = 2*R2D # Aerenal nuerlnir to days (4536)
S2D = 112 # Sovereign season to days
SW2D = 16 # Sovereign week to days
WC2D = 3 # Quor Tarai waking cycle to days
SC2D = 14 # Quor Tarai sleeping cycle to days
DR2D = 5 # kalashtar Days of Remembrance to days
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
               'Vult':     'Windwhisper'} # druidic month names
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
               'Vult':     'Uarth'} # dwarven month names
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
    if n == 1: s2 = 'st' # 1st
    elif n == 2: s2 = 'nd' # 2nd
    elif n == 3: s2 = 'rd' # 3rd
    else: s2 = 'th' # 0th, or 4th and up
    string = s + s2
    return string

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
        elif cal=='Druidic': m = druidmonths[self.month]
        elif cal=='Dwarven': m = dwarfmonths[self.month]
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

class AereniDate:
    # Aerenal Calendar (Qabalrin Wheel?)
    def __init__(self, d=1, t=7, l=9, th=2, r=1, n=2962):
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
        l = str(self.luenir)
        th = str(self.thuelir)
        r = str(self.rueln)
        n = str(self.nuerlnir)
        string = t + '-' + l + '-' + th + '-' + r + '-' + n + ' NA'
        if verbose: return d + ' of ' + string # add day to date
        else: return string
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
        dN = self.nuerlnir*N2D # AD of 1st day of current year
        return dN + self.days()
    def GD(self):
        # Galifaran day (similar to Julian Day)
        # number of days since 1 Zarantyr 0 YK
        Y0 = galifar2aereni(GalifarDate(y=0)) # year 0 YK in the Aereni calendar
        GD = self.AD() - Y0.AD() + 1 # days since Y0
        return GD
    
class SovereignDate:
    # Sovereign Book of Seasons (old Sarlonan - Pyrine)
    # celebrates the Celestial Week
    def __init__(self, w=1, d='Aureday', s='Yearbirth', y=998):
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
    dA = 40000*Y2D # years since landing on Aeren in days
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
        year = year - 1
    season = seasonnames[math.floor(dayofyear/S2D)]
    dayofseason = np.mod(dayofyear, S2D)
    week = math.floor(dayofseason/SW2D)+1
    dayofweek = np.mod(dayofseason, SW2D)
    day = sdaynames[dayofweek]
    return SovereignDate(w=week, d=day, s=season, y=year)

# TEST
    
'''
test1 = GalifarDate(d=20, m='Olarune', y=994)
print(test1.disp(dofw=True, cal='Druidic'))
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