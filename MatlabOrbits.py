# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 20:06:45 2022

@author: Matthew Gunther

Conversion to python of orbital dynamics code written in undergrad & grad
courses between 2017-2020.
"""

import numpy as np

'''
-------------------------------------------------------------------------------
HELPER FUNCTIONS
written to support matlab conversions
-------------------------------------------------------------------------------
'''

RAD2DEG = 180/np.pi # 180 degrees per pi radians
DEG2RAD = np.pi/180 # pi radians per 180 degrees

def frac_day(h=0, m=0, s=0, ap='am', is24=False):
    """
    Calculate the fraction of the day since midnight
    inputs: hours (h), minutes (m), seconds (s), am/pm (ap), 24hour (is24)
    output: fraction of the day
    """
    if not is24: # check if 12 or 24hour format used
        if ap == 'pm': h += 12 # 12hour, pm: add 12 hours
    hfrac = h/24 # hours as fraction of the length of a day in hours
    mfrac = m/1440 # minutes as frac of len of day in mins
    sfrac = s/86400 # secs as frac of len of day in secs
    return hfrac + mfrac + sfrac

def monthnumber(days, leap=False, returnsum=False):
    """
    # use number of days to find Gregorian month
    """
    if leap: # leap year
        monthlen = [0,31,29,31,30,31,30,31,31,30,31,30,31]
    else: # non-leap year
        monthlen = [0,31,28,31,30,31,30,31,31,30,31,30,31]
    daysum = [-1]
    for ii in np.arange(0, len(monthlen)-1):
        daysum.append(sum(monthlen[0:ii+2]))
        if (days <= daysum[ii+1]) and (days > daysum[ii]):
            month = ii
    if returnsum:
        return month, daysum
    else:
        return month

'''
-------------------------------------------------------------------------------
MATLAB FUNCTIONS
written by Matthew Gunther except where specified otherwise
-------------------------------------------------------------------------------
'''

def JulianDay(year, month, day):
    """
    function [J0] = JulianDay(year,month,day)
    %JULIANDAY calculates the julian day number
    %   Inputs:
    %       year = calendar year (yyyy)
    %       month = calendar month (mm)
    %       day = calendar day (dd)
    %   Ouputs:
    %       J0 = Julian day number [days]
    
    % Calculate Julian day at 0h UT
    J0=367*year - floor(1.75*(year + floor((month+9)/12))) +...
        floor(275*month/9) + day + 1721013.5;
    
    end
    """
    J0 = (367*year - np.floor(1.75*(year + np.floor((month+9)/12)))
            + np.floor(275*month/9) + day + 1721013.5)
    return J0

def JD2Cal(JD):
    """
    function [ year,month,day,hour,minute,second ] = JD2Cal( JD )
    % JD2Cal calculates a calendar date from a Julian date
    % INPUTS: JD, julian date (days) (JD>J2000.0)
    % OUTPUTS: year, month, day, hour, minute, second, in UT time
    
    % from integer of JD, get year, month, and day
    """
    # subtract J2000.0 from int(JD) to get days since J2000.0
    daystot = np.floor(JD)-2451545
    
    # convert days to years since J2000.0
    years = np.floor(daystot/365)
    
    # calendar year is 2000 plus number of years since J2000.0
    year = 2000+years
    
    # number of days into year is the input JD - JD of year calculated
    days = np.floor(JD) - np.floor(JulianDay(year,0,0))
    
    # is this year a leap year?
    # if year number is divisible by 4, then yes
    leap = 0;
    if year/4 == np.floor(year/4):
        leap = 1
    
    # use number of days to find Gregorian month
    month = monthnumber(days, leap)
    
    # day of month is input JD - JD of calculated year and month
    day = np.floor(JD) - np.floor(juliandate(year,month,1));
    
    # from fraction of JD, get hour, minute, second, in UT time
    UTfrac = JD - np.floor(JD) # [days]
    
    # convert UT fraction to hours and floor to get hour of the day
    # gives hour from 0:23
    hour = np.floor(UTfrac*24)
    
    # find fraction in minutes, subtract minutes of hour to get minutes in hour
    minute = np.floor(UTfrac*24*60) - (hour*60)
    
    # find fraction of minute, convert to sec to get sec in min
    # returns a float to include fraction of sec
    second = ((UTfrac*24*60*60) - np.floor(UTfrac*24*60*60))*60
    return year,month,day,hour,minute,second

def juliandate(year,month=1,day=1,hour=0,minute=0,second=0,epoch='none'):
    '''
    function [ JD ] = JulianDateCalc( year,month,day,hour,minute,second )
    %JULIANDATE Translates standard date into Julian Date
    %   Calculates J0 using calendar date, then JD using UT, then adjusts to an
    %   epoch if supplied.
    %   Outputs JD in days
    '''
    # Convert calendar date to julian date
    # use year, month, and day to calculate J0
    J0 = JulianDay(year, month, day)
    # convert UT time from hours/minutes/seconds to fraction
    UT = frac_day(hour, minute, second)
    # use UT fraction to calculate JD
    JD = J0 + UT
    # adjust epoch if necessary
    if epoch == 'J2000':
        JD = JD - 2452545
    elif type(epoch) in [int, float]:
        JD = JD - juliandate(epoch, 1, 1, 12)
    return JD

def COEs_rad(r0, v0, mu=398600., use_h=False):
    """
    python updates:
        added 'mu' as an input with a default value of Earth gravity
        added 'use_h' flag
            False: return semimajor axis, 'a', as first COE
            True: return specific angular momentum, 'h', as first COE
    
    original Matlab code:
    function [COEout] = COEs_rad( r0,v0 )
    %COES Calculates the classical orbital elements given r0 and v0
    %   Inputs:
    %       position, r0(km)
    %       velocity, v0(km/s)
    %   Outputs: 
    %       specific angular momentum (h)
    %       inclination (inc)
    %       right ascension of the ascending node (RAAN)
    %       eccentricity (ecc)
    %       argument of perigee (omega)
    %       true anomaly (theta)
    %           (all angles output in radians)
    
    % if no mu input, assume Earth orbit
    """
    
    # ensure inputs are numpy arrays and floats
    for x in range(len(r0)): r0[x] = np.float64(r0[x])
    for x in range(len(v0)): v0[x] = np.float64(v0[x])
    mu = np.float64(mu)
    r0 = np.array(r0).reshape(3)
    v0 = np.array(v0).reshape(3)
    
    # Distance
    rmag = np.linalg.norm(r0)
    
    # Speed
    vmag = np.linalg.norm(v0)
    
    # Energy
    E = (vmag**2)/2 - (mu/rmag) # km^2/s^2
    
    # Semimajor Axis
    a = -mu / (2*E) # km
    
    # Radial Velocity
    vr = np.dot(r0, v0)/rmag
    
    # h, Specific Angular Momentum
    hvect = np.cross(r0, v0)
    hmag = np.linalg.norm(hvect)
    
    # inc, Inclination
    inc = np.arccos(hvect[2]/hmag)
    
    # Node Line in Equatorial Plane
    Nvect = np.cross([0,0,1], hvect)
    Nmag = np.linalg.norm(Nvect)
    
    # RAAN
    RAAN = np.arccos(Nvect[0]/Nmag)
    if Nvect[1] < 0:
        RAAN = (2*np.pi) - RAAN
    
    # ecc, Eccentricity
    eccvect = (1/mu) * ((((vmag**2) - (mu/rmag)) * r0) - (rmag * vr * v0))
    eccmag = np.linalg.norm(eccvect)
    
    # omega, Argument of Perigee
    omega = np.arccos(np.dot(Nvect, eccvect) / (Nmag * eccmag))
    if eccvect[2] < 0:
        omega = (2*np.pi) - omega
    
    # theta, True Anomaly
    theta = np.arccos(np.dot(eccvect, r0) / (eccmag * rmag))
    if vr < 0:
        theta = (2*np.pi) - theta
    
    h = hmag
    ecc = eccmag
    
    if use_h: COEout = np.array([ h,ecc,inc,RAAN,omega,theta ]) # use h
    else: COEout = np.array([ a,ecc,inc,RAAN,omega,theta ]) # use a
    
    return COEout

def COEs_to_Inertial_rad(coe, mu=398600.):
    """
    function [ r,v ] = COEs_to_Inertial_rad( coe,mu )
    %COES_TO_INERTIAL_DEG Calculates state vector in an inertial frame given COEs
    %   Inputs angular momentum (h), eccentricity (ecc), inclination (inc),
    %   right ascension of the ascending node (RAAN), argument of perigee
    %   (omega), true anomaly (theta), and gravitational parameter (mu).
    %   All angles input in radians.
    %   Outputs state vector in ECI frame (r_eci,v_eci).
    
    % if no mu input, assume Earth orbit
    """

    h     = coe[0]
    ecc   = coe[1]
    inc   = coe[2]
    RAAN  = coe[3]
    omega = coe[4]
    theta = coe[5]
    
    # precalculate sin(theta) and cos(theta)
    stheta = np.sin(theta)
    ctheta = np.cos(theta)
    
    # first find state vector in perifocal frame
    r_peri = ( ((h**2) / mu) * (1 / (1 + ecc*ctheta))
                * np.array([[ctheta, stheta, 0]]).T )
    v_peri = (mu / h) * np.array([[-stheta, ecc+ctheta, 0]]).T
    
    # then find rotation matrix from perifocal frame to ECI
    Q_X_xbar = (Czcalc_rad(omega) * Cxcalc_rad(inc) * Czcalc_rad(RAAN)).T
    
    # finally, rotate state vector in perifocal to ECI
    r = Q_X_xbar @ r_peri # matrix multiply with @, np.dot, or np.matmul
    v = Q_X_xbar @ v_peri
    
    return r, v

def Cxcalc_rad(phid):
    """
    function [ Cx ] = Cxcalc_rad( phid )
    %CX Calculates rotation matrix Cx
    %   Input is rotation angle phi (yaw) in radians.
    """
    cphi = np.cos(phid)
    sphi = np.sin(phid)
    Cx   = np.array([[1,0,0], [0,cphi,sphi], [0,-sphi,cphi]])
    
    return Cx

def Czcalc_rad(psid):
    """
    function [ Cz ] = Czcalc_rad( psid )
    %CZ Calculates rotation matrix Cz
    %   Input is rotation angle phi (roll) in radians.
    """
    cpsi = np.cos(psid)
    spsi = np.sin(psid)
    Cz   = np.array([[cpsi,spsi,0], [-spsi,cpsi,0], [0,0,1]])
    
    return Cz

"""
TESTING------------------------------------------------------------------------
"""

if __name__ == "__main__":
    '''
    coes = COEs_rad([7000, 1, -1], [0.001, np.sqrt(398600/7000), -0.001])
    print('coes = ', coes)
    
    r, v = COEs_to_Inertial_rad(coes)
    print('r = ', r)
    print('v = ', v)
    '''
    
    # Vallado ex 2-5
    r_IJK = np.array([6524.834, 6862.875, 6448.296]) # position, ECI, km
    v_IJK = np.array([4.901327, 5.533756, -1.976341]) # velocity, ECI, km/s
    mu = 398600
    
    coe = COEs_rad(r_IJK, v_IJK, mu, use_h=True)
    h = coe[0]
    ecc = coe[1]
    inc = coe[2]
    RAAN = coe[3]
    omega = coe[4]
    theta = coe[5]
    
    r = np.linalg.norm(r_IJK)
    v = np.linalg.norm(v_IJK)
    E = (v**2)/2 - (mu/r) # km^2/s^2
    a = -mu / (2*E) # km
    
    rnew, vnew = COEs_to_Inertial_rad(coe)
    
    print('r_ECI = ', r_IJK, ' km')
    print('v_ECI = ', v_IJK, ' km/s')
    print('r = ', r, 'km (correct = 11456.57 km)')
    print('v = ', v, 'km/s (correct = 7.651888 km/s)')
    print('angular momentum     h       = ', h, 'km^2/s (correct = 66420.1 km^2/s)')
    #print('semiparameter        p       = ', p, ' km (correct = 11,067.79 km)')
    print('semimajor axis       a       = ', a, ' km (correct = 36127.343 km)')
    print('eccentricity         ecc     = ', ecc, ' (correct = 0.832853)')
    print('inclination          inc     = ', inc*RAD2DEG, ' deg (correct = 87.87 deg)')
    print('right ascension      RAAN    = ', RAAN*RAD2DEG, ' deg (correct = 227.898 deg)')
    print('argument of perigee  omega   = ', omega*RAD2DEG, ' deg (correct = 53.38 deg)')
    print('true anomaly         theta   = ', theta*RAD2DEG, ' deg (correct = 92.335 deg)')
    #print('                     m       = ', m)
    #print('argument of latitude arglat  = ', arglat, ' deg (correct = 145.60549 deg)')
    #print('true longitude       truelon = ', truelon, ' deg (correct = 55.282587 deg)')
    #print('longitude of perigee lonper  = ', lonper, 'deg (correct = 281.27 deg)')
    print('rnew = ', rnew, ' km')
    print('vnew = ', vnew, ' km/s')












