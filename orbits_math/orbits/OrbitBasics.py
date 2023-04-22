# -*- coding: utf-8 -*-
"""
@author: Matthew Gunther

Basic orbits functions & classes
"""

import pathlib
import os
import time

import numpy as np
from scipy import constants as const
from matplotlib import pyplot as plt # used for testing
#from numba import jit
from scipy.integrate import solve_ivp

from mpi4py import MPI

from pymgrit.core.application import Application
from pymgrit.core.vector import Vector
from pymgrit.core.mgrit import Mgrit
from pymgrit.core import simple_setup_problem
from pymgrit.core import mgrit

import NumericalAnalysis as na
import MatlabOrbits as morb
import ValladoOrbits as vorb
import ExternalOrbits as xorb

## CONSTANTS ------------------------------------------------------------------

# Universal
c = const.c # speed of light, m/s
AU = 149597870.7 # astronomical unit, km
ly = c*const.year/const.kilo # light year, km

# Earth
muE = 398600 # Earth mu, km/s^3
rE = 6378 # Earth radius, km
gE = 9.81 # Earth surface gravity, m/s^2

# Luna
delta_Luna = 31.7 # angular diameter of Earth's moon
rho_Luna = 3344 # density of Earth's moon

# The Sun
mu_S = 1.32712442099e11 # gravitational parameter, km^3/s^2
g_S = 274       # surface gravity, m/s^2
m_S = 1.98892e30 # mass, kg
r_S = 696000    # radius, km
rho_S = 1408    # density, kg/m^3
L_S = 383e24    # luminosity, J/s (W)
M_S = 4.83      # absolute magnitude
SE_S = 63       # spectral emission, J/m^2
T_S = 5772      # effective surface temperature, K
delta_S = 32    # angular size, arcminutes
d_S = AU        # mean distance from Earth, km (=1AU)
dsun = d_S
Lsun = L_S
msun = -26.8    # apparent magnitude
rsun = r_S
Tsun = T_S

# Sol System
Sol_a = np.array([57.909e6,
                  108.209e6,
                  AU,
                  227.923e6,
                  2.768*AU,
                  778.57e6,
                  1433.529e6,
                  2872.463e6,
                  4495.06e6,
                  5869.656e6]) # Solar system semimajor axes, km
Sol_names = ['Mercury',
             'Venus',
             'Earth',
             'Mars',
             'Ceres',
             'Jupiter',
             'Saturn',
             'Uranus',
             'Neptune',
             'Pluto'] # Solar system planet names

## ----------------------------------------------------------------------------
## CONVERSION & MISC FUNCTIONS
## ----------------------------------------------------------------------------

def parse_datestr(string='00:00:00.0 am'):
    """
    parse date from string input
    """
    if string.split(' ')[0] != string: # true if there is a space
        if string.split(' ')[1] in ['a', 'A', 'am', 'AM']: ap = 'am'
        elif string.split(' ')[1] in ['p', 'P', 'pm', 'PM']: ap = 'pm' 
        is24 = False
        string = string.split(' ')[0] # discard am/pm
    elif string.split('a')[0] != string: # true if there is an 'a'
        ap = 'am'
        is24 = False
        string = string.split('a')[0] # discard am/pm
    elif string.split('p')[0] != string:  # true if there is a 'p'
        ap = 'pm'
        is24 = False
        string = string.split('p')[0] # discard am/pm
    else: # no am or pm supplied, must be 24hr format
        ap = ''
        is24 = True
    
    ls = string.split(':') # split by colon
    h = int(ls[0]) # hours
    m = int(ls[1]) # minutes
    if len(ls) > 2: # true if seconds supplied
        s = float(ls[2]) # seconds (handles ss and ss.s)
    else:
        s = 0. # 0 seconds if not supplied
    if len(ls) == 4: # true if hundredths of a second supplied as ss:ss
        s += float(ls[3])/100 # add hundredths to seconds
        
    return h, m, s, ap, is24

def time2str(h, m, s, ap):
    """
    format time of day into string
    """
    hstr = str(h)
    mstr = str(m)
    sstr = str(s)
    string = ':'.join([hstr, mstr, sstr])
    return ' '.join([string, ap])

def fd_str(string):
    """
    calculate fractional day from string
    """
    h, m, s, ap, is24 = parse_datestr(string)
    frac = morb.frac_day(h, m, s, ap, is24)
    return frac

def fd_str_sec(string):
    """
    calculate fractional day in seconds from string
    """
    frac_days = fd_str(string)
    frac_sec = frac_days*const.day
    return frac_sec

#@jit(nopython=True, parallel=True)
def ang_diam(d, D):
    """
    inputs: actual diameter (d), distance (D)
    outputs: angular diameter (delta) [arcmin]
    """
    delta = 2*np.arcsin(d/(2*D))
    return(np.rad2deg(delta)*60) # arcminutes
    
#@jit(nopython=True, parallel=True)
def grav2mass(g, r):
    """
    inputs: surface gravity (g, m/s^2), radius (r, km)
    outputs: mass (m, kg)
    """
    r_m = r*const.kilo # r in meters
    m = g*(r_m**2)/const.G # m in kg
    return(m)

#@jit(nopython=True, parallel=True)    
def gsurf(r, m):
    '''
    inputs: radius (r, km), mass (m, kg)
    outputs: surface gravity(g, m/s^2)
    '''
    r_m = r*const.kilo # r in meters
    g = m*const.G/(r_m**2) # g in m/s^2
    return g
    
#@jit(nopython=True, parallel=True)
def mass2mu(m):
    """
    inputs:  mass (m, kg)
    outputs: gravitational parameter (mu, km^3/s^2)
    """
    mu_ms = m*const.G # mu in m^3/s^2
    mu = mu_ms/(const.kilo**3) # mu in km^3/s^2
    return(mu)
    
#@jit(nopython=True, parallel=True)
def mu2mass(mu):
    """
    inputs: gravitational parameter (mu, km^3/s^2)
    outputs:  mass (m, kg)
    """
    mu_ms = mu*(const.kilo**3) # mu in m^3/s^2
    m = mu_ms/const.G # m in kg
    return(m)

#@jit(nopython=True, parallel=True)
def Vsphere(r):
    '''
    inputs: radius (r, m)
    outputs: volume (V, m^3)
    '''
    V = (4/3)*np.pi*(r**3) # V in m^3
    return(V)

#@jit(nopython=True, parallel=True)
def mass2dens(m, r):
    '''
    inputs:  mass    (m,   kg)
             radius  (r,   km)
    outputs: density (rho, kg/m^3)
    '''
    r_m = r*const.kilo # r in m
    rho = m/Vsphere(r_m) # rho in kg/m^3
    return(rho)
    
#@jit(nopython=True, parallel=True)
def dens2mass(r, rho):
    '''
    inputs:  radius  (r,   km)
             density (rho, kg/m^3)
    outputs: mass    (m,   kg)
    '''
    r_m = r*const.kilo # r in m
    m = rho*Vsphere(r_m) # mass in kg
    return m

#@jit(nopython=True, parallel=True)
def r2mu(r, rho):
    '''
    inputs:  radius          (r,   km)
             density         (rho, kg/m^3)
    outputs: grav. parameter (mu,  km^3/s^2)
    '''
    m = dens2mass(r, rho) # mass in kg
    mu = mass2mu(m) # mu in km^3/s^2
    return mu

#@jit(nopython=True, parallel=True)
def r2C(r):
    '''
    inputs:  radius        (r)
    outputs: circumference (C)
    '''
    return 2*np.pi*r

def xy2r(x, y):
    # Rectangular to polar coordinate conversion: r from (x, y)
    return np.sqrt(x**2 + y**2)
    
def xy2theta(x, y):
    # Rectangular to polar coordinate conversion: theta from (x,y)
    return np.arctan2(y, x)

def rect2polar(x, y):
    '''
    Rectangular to polar coordinate conversion
    
    inputs:  x coordinate     (x,     distance)
             y coordinate     (y,     distance)
    outputs: r coordinate     (r,     distance)
             theta coordinate (theta, rad)
    '''
    
    r     = xy2r(x, y)
    theta = xy2theta(x, y)
    
    return r, theta

def rtheta2x(r, theta):
    # Polar to rectangular coordinate conversion: x from (r, theta)
    return r*np.cos(theta)

def rtheta2y(r, theta):
    # Polar to rectangular coordinate conversion: y from (r, theta)
    return r*np.sin(theta)

def polar2rect(r, theta):
    '''
    Polar to rectangular coordinate conversion
    
    inputs:  r coordinate     (r,     distance)
             theta coordinate (theta, rad)
    outputs: x coordinate     (x,     distance)
             y coordinate     (y,     distance)
    '''
    
    x = rtheta2x(r, theta)
    y = rtheta2y(r, theta)
    
    return x, y

def xyz2r(x, y, z):
    # Cartesian x y z to spherical radius, r
    return np.sqrt(x**2 + y**2 + z**2)

def xyz2theta(x, y, z):
    # Cartesian x y z to spherical colatitude, theta (rad)
    return np.arctan2(np.sqrt(x**2 + y**2), z)

def xyz2phi(x, y, z):
    # Cartesian x y z to spherical longitude, phi (rad)
    if x >= 0: return np.arctan2(y, x)
    else:      return np.arctan2(y, x) + np.pi

def rect2sphere(x, y, z):
    '''
    Cartesian to spherical coordinate conversion
    
    inputs:  x coordinate     (x,     distance)
             y coordinate     (y,     distance)
             z coordinate     (z,     distance)
    outputs: r coordinate     (r,     distance)
             theta coordinate (theta, rad)
             phi coordinate   (phi,   rad)
    '''
    r =     xyz2r(x, y, z)
    theta = np.arccos(z/r)
    phi =   xyz2phi(x, y, z)
    
    return r, theta, phi

def rthetaphi2x(r, theta, phi):
    # Spherical r theta phi to Cartesian x
    return r * np.cos(phi) * np.sin(theta)

def rthetaphi2y(r, theta, phi):
    # Spherical r theta phi to Cartesian y
    return r * np.sin(phi) * np.sin(theta)

def sphere2rect(r, theta, phi):
    '''
    Spherical to Cartesian coordinate conversion
    
    inputs:  r coordinate     (r,     distance)
             theta coordinate (theta, rad)
             phi coordinate   (phi,   rad)
    outputs: x coordinate     (x,     distance)
             y coordinate     (y,     distance)
             z coordinate     (z,     distance)
    '''
    x = rthetaphi2x(r, theta, phi)
    y = rthetaphi2y(r, theta, phi)
    z = rtheta2x(r, theta)
    
    return x, y, z

def R_cart2sphere(theta, phi):
    # Rotation matrix: cartesian to spherical
    sintheta = np.sin(theta)
    costheta = np.cos(theta)
    sinphi   = np.sin(phi)
    cosphi   = np.cos(phi)
    R = np.array([
            [ sintheta*cosphi, sintheta*sinphi,  costheta],
            [ costheta*cosphi, costheta*sinphi, -sintheta],
            [-sinphi,          cosphi,           0       ]
            ])
    return R

def R_sphere2cart(theta, phi):
    # Rotation matrix: spherical to cartesian
    R = R_cart2sphere(theta, phi)
    # the matrix is orthogonal, therefore R^-1 = R^T
    return R.T

def Rx(theta):
    # Rotation matrix for angle theta about x-axis
    costheta = np.cos(theta)
    sintheta = np.sin(theta)
    R = np.array([
            [1, 0,         0       ],
            [0, costheta, -sintheta],
            [0, sintheta,  costheta]
            ])
    return R

def Ry(theta):
    # Rotation matrix for angle theta about y-axis
    costheta = np.cos(theta)
    sintheta = np.sin(theta)
    R = np.array([
            [ costheta, 0, sintheta],
            [ 0,        1, 0       ],
            [-sintheta, 0, costheta]
            ])
    return R

def Rz(theta):
    # Rotation matrix for angle theta about z-axis
    costheta = np.cos(theta)
    sintheta = np.sin(theta)
    R = np.array([
            [costheta, -sintheta, 0],
            [sintheta,  costheta, 0],
            [0,         0,        1]
            ])
    return R

def Rzyx(alpha, beta, gamma):
    # Rotation matrix of angles:
    #   gamma about z-axis
    #   beta  about y-axis
    #   alpha about x-axis
    R1 = Rz(gamma)
    R2 = Ry(beta)
    R3 = Rx(alpha)
    R = R1 @ R2 @ R3
    return R

def R2d(theta):
    # 2D rotation matrix through angle theta
    costheta = np.cos(theta)
    sintheta = np.sin(theta)
    R = np.array([
            [costheta, -sintheta],
            [sintheta,  costheta]
            ])
    return R


## ----------------------------------------------------------------------------
## ORBITS FUNCTIONS
## ----------------------------------------------------------------------------

#@jit(nopython=True, parallel=True)
def Me2theta(M, e):
    """
    inputs: mean anomaly (M), eccentricity (e)
    outputs: true anomaly (theta), approx error (err)
    """
    theta = M + (2*e - 0.25*e**3)*np.sin(np.deg2rad(M))
    + 1.25*e**2*np.sin(2*np.deg2rad(M)) + (13/12)*e**3*np.sin(3*np.deg2rad(M))
    err = e**4
    return([theta, err])
    
#@jit(nopython=True, parallel=True)
def meandist2a(md, e):
    '''
    inputs:  mean distance  (md)
             eccentricity   (e)
    outputs: semimajor axis (a)
    '''
    return md*2/(1+np.sqrt(1-(e**2)))

#@jit(nopython=True, parallel=True)
def a2rpra(a, e):
    '''
    inputs:  semimajor axis     (a)
             eccentricity       (e)
    outputs: radius of periapse (rp)
             radius of apoapse  (ra)
    '''
    rp = a*(1-e) # radius of periapse
    ra = a*(1+e) # radius of apoapse
    return(rp, ra)
    
#@jit(nopython=True, parallel=True)
def P2a(P, mu):
    '''
    inputs:  orbital period  (P,  sec)
             grav. parameter (mu, km^3/s^2)
    outputs: semimajor axis  (a,  km)
    '''
    return np.cbrt(mu*((P/(2*np.pi))**2))

def Pa2mu(P, a):
    '''
    inputs:  orbital period  (P,  sec)
             semimajor axis  (a,  km)
    outputs: grav. parameter (mu, km^3/s^2)
    '''
    return (a**3) / ( (P / (2*np.pi))**2 )

#@jit(nopython=True, parallel=True)
def ab2e(a, b):
    '''
    intputs: semimajor axis (a)
             semiminor axis (b)
    outputs: eccentricity   (e)
    '''
    return np.sqrt((a**2 - b**2)/a)

#@jit(nopython=True, parallel=True)
def a2P(a, mu):
    '''
    inputs:  semimajor axis  (a,  km)
             grav. parameter (mu, km^3/s^2)
    outputs: orbital period  (P,  sec)
    '''
    return 2*np.pi*np.sqrt((a**3)/mu)

#@jit(nopython=True, parallel=True)
def circvel(r, mu):
    '''
    Orbital velocity for a circular orbit
    
    inputs:  radius          (r,  km)
             grav. parameter (mu, km^3/s^2)
    outputs: velocity        (v,  km/s)
    '''
    return np.sqrt(mu/r)

def rschwarz(m):
    # Schwarzchild radius for body of mass m (kg)
    return 2*const.G*m / (c**2) # (m)

def rschwarzkm(m):
    # Schwarzchild radius for body of mass m (kg)
    return rschwarz(m) / const.kilo # (km)

def rschwarz_mu(mu):
    # Schwarzchild radius for body with gravitational parameter mu (km^3/s^2)
    return 2*mu*(const.kilo**3) / (c**2) # (m)

def rschwarzkm_mu(mu):
    # Schwarzchild radius for body with gravitational parameter mu (km^3/s^2)
    return rschwarz(mu) / const.kilo # (km)

def ae2p(a, ecc):
    # calculate semiparameter from semimajor axis and eccentricity
    return a * (1 - ecc**2)

def orbtype(ecc, inc):
    # determine type of orbit (code snippet from Vallado rv2coe)
    
    #% ------ elliptical, parabolic, hyperbolic inclined -------
    typeorbit= 'ei'
    if ( ecc < vorb.small ):
        #% ----------------  circular equatorial ---------------
        if  (inc<vorb.small) | (abs(inc-np.pi)<vorb.small):
            typeorbit= 'ce'
        else:
            #% --------------  circular inclined ---------------
            typeorbit= 'ci'
    else:
        #% - elliptical, parabolic, hyperbolic equatorial --
        if  (inc<vorb.small) | (abs(inc-np.pi)<vorb.small):
            typeorbit= 'ee'
    
    return typeorbit

def rv2nbar(r, v):
    # calculate nbar vector from r, v (code snippet from Vallado coe2rv)
    hbar = np.cross( r,v )
    #magh = vorb.mag( hbar )
    #if ( magh > vorb.small ):
    nbar = np.zeros(3) # column vector
    nbar[0]= -hbar[1]
    nbar[1]=  hbar[0]
    nbar[2]=   0.0
    
    return nbar

def coe2rv(coe, arglat=0., truelon=0., lonper=0.):
    """
    wrapper for Vallado coe2rv(), restricted to classical orbital elements
    
    Inputs:
        coe = [a, ecc, inc, RAAN, omega, theta]
        arglat = argument of latitude, equals true anomaly for circular inclined
        truelon = true longitude, equals true anomaly for circular equatorial
        lonper = longitude of perigee, equals argument of perigee for elliptical equatorial
    
    Outputs:
        r = position vector, km
        v = velocity vector, km/s
    """
    a = coe[0] # semimajor axis
    ecc = coe[1] # eccentricity
    inc = coe[2] # inclination
    RAAN = coe[3] # right ascension
    omega = coe[4] # argument of perigee
    theta = coe[5] # true anomaly
    
    # calculate semiparameter
    p = ae2p(a, ecc)
    
    #% -------------------------------------------------------------
    #%       determine what type of orbit is involved and set up the
    #%       set up angles for the special cases.
    #% -------------------------------------------------------------
    if ( ecc < vorb.small ):
        #% ----------------  circular equatorial  ------------------
        if (inc<vorb.small) | ( abs(inc-np.pi)< vorb.small ):
            omega = 0.0
            RAAN  = 0.0
            theta = truelon
        else:
            #% --------------  circular inclined  ------------------
            omega = 0.0
            theta = arglat
    else:
        #% ---------------  elliptical equatorial  -----------------
        if ( ( inc<vorb.small) | (abs(inc-np.pi)<vorb.small) ):
            omega = lonper
            RAAN  = 0.0
    
    return vorb.coe2rv( p,ecc,inc,RAAN,omega,theta,arglat,truelon,lonper )

def rv2coe(r, v, mu=muE, extras=False):
    """
    wrapper for Vallado rv2coe(), restricted to classical orbital elements
    
    Inputs:
        r = position vector, km
        v = velocity vector, km/s
        mu = gravitational parameter, km^3/s^2, default Earth
        extras = True to return (coe, extra)
            where extra = [p: semiparameter, km
                           m: mean anomaly, rad
                           arglat: argument of latitude, rad, circular inclined
                           truelon: true longitude, rad, circular equatorial
                           lonper: longitude of perigee, rad, elliptical equatorial]
    
    Outputs:    
    coe = [a: semimajor axis, km
           ecc: eccentricity
           inc: inclination, rad
           RAAN: right ascension, rad
           omega: argument of perigee, rad
           theta: true anomaly, rad]
    """
    p,a,ecc,inc,RAAN,omega,theta,m,arglat,truelon,lonper = vorb.rv2coe(r,v,mu)
    coe = [a, ecc, inc, RAAN, omega, theta] # classical orbital elements
    extra = [p, m, arglat, truelon, lonper]
    if extras: return coe, extra
    else: return coe

## ----------------------------------------------------------------------------
## EQUATIONS OF MOTION
## ----------------------------------------------------------------------------
    
#@jit(nopython=True, parallel=True)
def twobodyRV(t, s, CB, **kwargs):
    '''
    two-body equations of motion
    F = dp/dt = ma = -GMm*rhat/r^2
    a = -mu*rhat/r^2 = -mu*r/norm(r)^3
    
    inputs:  initial state   (s[rx,ry,rz,vx,vy,vz],  [km(x3),km/s(x3)])
             time, t         (t,  s)
             central body object with attribute mu (grav param, km^3/s^2)
    outputs: d/dt(state)     (s1[vx,vy,vz,ax,ay,az], [km/s(x3),km/s^2(x3)])
    '''
    
    r = s[:3]
    v = s[3:]
    
    a = -CB.mu*r / (na.vecnorm(r)**3)
    
    s1 = np.array([v[0], v[1], v[2], a[0], a[1], a[2]])
    return s1

def twobodypert(t, s, CB, **kwargs):
    '''
    two-body equations of motion + perturbational acceleration
    F = dp/dt = ma = -GMm*rhat/r^2
    a = -mu/rhat/r^r + pert = -mu*r/norm(r)^3 + pert
    
    inputs:  initial state   (s[rx,ry,rz,vx,vy,vz],  [km(x3),km/s(x3)])
             time, t         (t,  s)
             central body object with attribute mu (grav param, km^3/s^2)
             pert            function handle for perturbational acceleration
    outputs: d/dt(state)     (s1[vx,vy,vz,ax,ay,az], [km/s(x3),km/s^2(x3)])
    '''
    if 'pert' not in kwargs.keys(): pert = lambda x: 0
    else: pert = kwargs['pert']
    
    r = s[:3]
    v = s[3:]
    
    apert = pert(t, s, CB, **kwargs)
    
    a = (-CB.mu*r / (na.vecnorm(r)**3)) + apert
    
    s1 = np.array([v[0], v[1], v[2], a[0], a[1], a[2]])
    return s1

def accel_inline(t, s, CB, **kwargs):
    '''
    perturbational acceleration equation
    acceleration is directed either parallel or antiparallel to velocity
    
    *args must include:     scale = -1 to 1 (antiparallel to parallel)
                            mag = magnitude of accel (km/s^2)
    '''
    if 'scale' not in kwargs.keys(): scale = 1 # default parallel
    else: scale = kwargs['scale']
    if 'mag' not in kwargs.keys(): mag = 0 # no accel if no mag input
    else: mag = kwargs['mag']
    v = s[3:] # velocity vector
    vhat = v / na.vecnorm(v) # velocity unit vector
    accel = scale * mag * vhat # acceleration vector aligned with velocity
    return accel

## ----------------------------------------------------------------------------
## CLASSES
## ----------------------------------------------------------------------------
    
# distance unit conversion
#@jit(nopython=True, parallel=True)
class dist:
    def ly2m(d):
        # 1 light year = 9.46e15 m
        return d*c*const.year # m
    def m2ly(d):
        return d/(c*const.year) # ly
    def AU2km(d):
        # 1 AU = 149.6e6 km
        return d*AU # km
    def km2AU(d):
        # 1 km = 1/149.6e6 AU
        return d/AU # AU
    def pc2AU(d):
        # 1 parsec = 648000/pi AU
        return d*648000/np.pi # AU
    def AU2pc(d):
        return d/(648000/np.pi) # pc
    def pc2ly(d):
        # 1 parsec ~ 3.26 light years
        #return d*3.26156 # ly
        return d*dist.m2ly(dist.AU2km(dist.pc2AU(1))*const.kilo) # ly
    def ly2pc(d):
        return d/dist.m2ly(dist.AU2km(dist.pc2AU(1))*const.kilo) # pc
    pc = AU2km(pc2AU(1)) # parsec in km
    ly = ly2m(1)/const.kilo # light year in km
    AU = AU2km(1) # 1 AU in km

# central gravitational body
#@jit(nopython=True, parallel=True)
class CentralBody:
    def __init__(self, name = '', **inputs):
        '''
        inputs must include either m, mu, or both g and r
        '''
        
        self.name = name
        
        # m = mass, kg
        if 'm' in inputs: self.m = inputs['m']
        elif 'mu' in inputs: self.m = mu2mass(inputs['mu'])
        elif 'g' in inputs and 'r' in inputs:
            self.m = grav2mass(inputs['g'], inputs['r'])
        
        # mu = gravitational parameter, km^3/s^2
        if 'mu' in inputs: self.mu = inputs['mu']
        elif 'm' in inputs: self.mu = mass2mu(inputs['m'])
        elif 'g' in inputs and 'r' in inputs:
            self.mu = mass2mu(self.m)
        
        # r = radius, km
        if 'r' in inputs: self.r = inputs['r']
        
        # rs = Schwarzchild radius, m
        if 'rs' in inputs: self.rs = inputs['rs']
        else: self.rs = rschwarz_mu(self.mu)
        
        # C = circumference, km
        if 'C' in inputs: self.C = inputs['C']
        elif 'r' in inputs: self.C = r2C(inputs['r'])
        
        # g = surface gravity, m/s^2
        if 'g' in inputs: self.g = inputs['g']
        
        # rho = density, kg/m^3
        if 'rho' in inputs: self.rho = inputs['rho']
        elif 'm' in inputs and 'r' in inputs:
            self.rho = mass2dens(inputs['m'], inputs['r'])
        elif 'g' in inputs and 'r' in inputs:
            self.rho = mass2dens(self.m, inputs['r'])
        
        # T = temperature, K
        if 'T' in inputs: self.T = inputs['T']
        
        # delta = angular size at viewing body, arcminutes
        if 'delta' in inputs: self.delta = inputs['delta']
        elif 'r' in inputs and 'd' in inputs:
            self.delta = ang_diam(2*inputs['r'], inputs['d'])
        
        # d = distance from viewing body, km
        if 'd' in inputs: self.d = inputs['d']
        
        # x,y,z coordinates (zero if at center of coordinate system)
        if 'xyz' in inputs: self.xyz = inputs['xyz']
        else: self.xyz = np.array([0, 0, 0]) # assume zero if not supplied
        
# built-in class instances
Earth = CentralBody('Earth', mu = muE, r = rE, g = gE)
Sun = CentralBody('Sun', mu = mu_S, g = g_S, r = r_S, m = m_S, rho = rho_S, T = T_S, 
                  delta = delta_S, d = d_S)


SolSystem = {'names':Sol_names,
             'r'    :Sol_a,    
             'title':'Solar System',
             'CB'   :Sun}

# PyMGRIT orbit trajectory calculation
# Test my own implementation of a 3d orbit trajectory calculator
class VectorRV(Vector):
    """
    Class for vectors representing 3D space as R, V
    R = [x, y, z]       <- position
    V = [vx, vy, vz]    <- velocity
    """

    def __init__(self, values=np.zeros(6)):
        # initialize vector, default zeroes
        super().__init__()
        self.x  = values[0]
        self.y  = values[1]
        self.z  = values[2]
        self.vx = values[3]
        self.vy = values[4]
        self.vz = values[5]
    
    
    def __add__(self, other):
        # addition of self with another Vector
        tmp = VectorRV()
        tmp.set_values(self.get_values() + other.get_values())
        return tmp

    def __sub__(self, other):
        # subtraction of self with another Vector
        tmp = VectorRV()
        tmp.set_values(self.get_values() - other.get_values())
        return tmp

    def __mul__(self, other):
        # multiplication of self by scalar
        tmp = VectorRV()
        tmp.set_values(self.get_values() * other)

    def norm(self):
        # vector norm of self
        return np.linalg.norm(self.get_values())

    def set_values(self, values):
        # overwrite data values with input numpy array
        self.x  = values[0]
        self.y  = values[1]
        self.z  = values[2]
        self.vx = values[3]
        self.vy = values[4]
        self.vz = values[5]

    def get_values(self):
        # return vector data as numpy array
        return np.array([self.x, self.y, self.z, self.vx, self.vy, self.vz])

    def clone(self):
        # duplicate self into another Vector object
        tmp = VectorRV()
        tmp.set_values(self.get_values())
        return tmp

    def clone_zero(self):
        # create a Vector object initialized with zeros
        return VectorRV()

    def clone_rand(self):
        # create a Vector object initialized with random numbers
        tmp = VectorRV()
        tmp.set_values(np.random.rand(6))
        return tmp

    def pack(self):
        # define data to be communicated
        return np.array([self.x, self.y, self.z, self.vx, self.vy, self.vz])

    def unpack(self, values):
        # unpack data after receiving it
        self.x  = values[0]
        self.y  = values[1]
        self.z  = values[2]
        self.vx = values[3]
        self.vy = values[4]
        self.vz = values[5]

    def plot(self):
        # plot position in XY plane into current axes
        plt.plot(self.x, self.y, color='red', marker='.')

class PyMGRITOrbit3D(Application):
    """ 
    Application for calculating two-body orbital trajectories in 3D,
        a = -mu*r/norm(r)^3
        s = [x, y, z, vx, vy, vz]
        ds/dt = [vx, vy, vz, ax, ay, az]
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        """
        t_start = other.t_start
        t_stop  = other.t_stop
        nt      = other.nt
        s0      = other.s0
        CB      = other.CB
        EOM     = other.EOM
        method  = other.method
        """

        # set the class used for each time point
        self.vector_template = VectorRV()

        # set the initial condition
        self.vector_t_start = VectorRV()
        if 's0' in kwargs.keys():
            self.vector_t_start.set_values(kwargs['s0'].get_values())
        #self.vector_t_start.set_values(s0.get_values())
        
        # set the equations of motion to use
        self.EOM = twobodyRV # default basic two-body, no perturbations
        if 'EOM' in kwargs.keys():
            self.EOM = kwargs['EOM']
        #self.EOM = EOM

        # set the central body
        self.CB = Earth # default to Earth gravitational parameter
        if 'CB' in kwargs.keys():
            self.CB = kwargs['CB']
        #self.CB = CB

        # set the integration method
        # must be a string recognized in scipy solve_ivp(, method='str')
        # OR an OdeSolver class
        self.method = 'LSODA' # default to Adams/BDF (FORTRAN wrapper)
        if 'method' in kwargs.keys():
            self.method = kwargs['method']
        #self.method = method

    def step(self, u_start: VectorRV, t_start: float, t_stop:  float, *args, **kwargs) -> VectorRV:
        # use scipy to take one time step
        res = solve_ivp(fun     = self.EOM,
                        y0      = u_start.get_values(),
                        args    = (self.CB),
                        t_span  = np.array([t_start, t_stop]),
                        t_eval  = np.array([t_start, t_stop]),
                        method  = self.method)
        ret = VectorRV()
        ret.set_values(res.y[:, -1])
        return ret

class Orbit3D():
    def __init__(self, *args, **kwargs):
        # set up PyMGRIT problem with:

        # initial state [R, V]
        if 's0' in kwargs.keys(): self.s0 = VectorRV(kwargs['s0'])
        else: self.s0 = VectorRV(np.zeros(6))

        # [t_start, t_stop], sec
        if 'tspan' in kwargs.keys():
            self.t_start    = kwargs['tspan'][0]
            self.t_stop     = kwargs['tspan'][1]
        else: 
            self.t_start = 0.
            self.t_stop = 1.

        # number of time steps
        if 'nt' in kwargs.keys(): self.nt = kwargs['nt']
        else: self.nt = 100

        # central body
        if 'CB' in kwargs.keys(): self.CB = kwargs['CB']
        else: self.CB = Earth
        
        # equations of motion
        if 'EOM' in kwargs.keys(): self.EOM = kwargs['EOM']
        else: self.EOM = twobodyRV

        # integration method
        if 'method' in kwargs.keys(): self.method = kwargs['method']
        else: self.method = 'LSODA'

        # tolerance
        if 'tol' in kwargs.keys(): self.tol = kwargs['tol']
        else: self.tol = 1e-12

        # number of MGRIT levels
        if 'level' in kwargs.keys(): self.level = kwargs['level']
        else: self.level = 2   
        
        # MGRIT level coarsening
        if 'coarsening' in kwargs.keys(): self.coarsening = kwargs['coarsening']
        else: self.coarsening = 10
        
        self.orbit      = None
        self.multilevel = None
        self.mgrit      = None
        self.info       = {}
        self.t          = np.array
        self.s          = np.ndarray
        self.R          = self.s
        self.V          = self.s
        self.setup(*args, **kwargs)

    def setup(self, *args, **kwargs):
        # construct multilevel hierarchy and set up Mgrit solver
        self.orbit = PyMGRITOrbit3D(t_start=self.t_start, t_stop=self.t_start, nt=self.nt, *args, **kwargs)
        self.multilevel = simple_setup_problem(problem    = self.orbit,
                                               level      = self.level,
                                               coarsening = self.coarsening)
        self.mgrit = Mgrit(problem = self.multilevel,
                           tol     = self.tol)

    def solve(self):
        # run the Mgrit solver and return the output
        self.info = self.mgrit.solve()
        self.t = np.array()
        self.s = np.ndarray()
        for i in self.mgrit.index_local[0]:
            self.t.append(self.mgrit.t[0][i]) # extract time steps
            self.s.append(self.u[0][i]) # extract state
        self.R = self.s[:, :3] # position
        self.V = self.s[:, 3:] # velocity
        return self.info

## ----------------------------------------------------------------------------
## TEST
## ----------------------------------------------------------------------------

if __name__ == "__main__":
    
    # test two-body EOM
    alt = 500 # altitude, km
    rx0 = rE + alt # initial x position, km
    ry0 = 0
    rz0 = 0
    vx0 = 0
    vy0 = circvel(rx0, muE) # initial y velocity, km/s
    vz0 = 0
    
    # initial state
    s0 = np.array([rx0, ry0, rz0, vx0, vy0, vz0])
    dt = 10
    #tspan = [0, 1*const.hour]
    tspan = [0, 1*a2P(rx0, muE)]
    
    # integrate
    print(na.rk4.text)
    #t, rv = na.ode(twobodyRV, s0, tspan, dt, na.rk4.integrator, Earth)
    
    # plot
    plt.close()
    #fig, ax = plt.subplots()
    #ax.plot(rv[:,0], rv[:,1], '.-')
    #ax.set_aspect('equal')
    
    # accel
    mag = 0.001 # km/s^2
    scale = 1
    
    # integrate
    #t, rv = na.ode(twobodypert, s0, tspan, dt, scheme = na.rk4.integrator,
    #               misc=Earth, pert=accel_inline, mag=mag, scale=scale)
    
    # plot
    #fig, ax = plt.subplots()
    #ax.plot(rv[:,0], rv[:,1], '.-')
    #ax.set_aspect('equal')
    
    test1 = morb.juliandate(2022, 7, 16, 19, 0, 0)
    print(test1)
    test2 = morb.JulianDay(2022, 7, 16)
    print(test2)
    test3 = morb.JD2Cal(test1)
    print(test3)
    test4 = morb.JD2Cal(test2)
    print(test4)
    
    # Vallado ex 2-5
    r_IJK = np.array([6524.834, 6862.875, 6448.296]) # position, ECI, km
    v_IJK = np.array([4.901327, 5.533756, -1.976341]) # velocity, ECI, km/s
    mu = 398600
    
    coe = rv2coe(r_IJK, v_IJK, muE)
    a = coe[0]
    ecc = coe[1]
    inc = coe[2]
    RAAN = coe[3]
    omega = coe[4]
    theta = coe[5]
    
    r = np.linalg.norm(r_IJK)
    v = np.linalg.norm(v_IJK)
    E = (v**2)/2 - (mu/r) # km^2/s^2
    a = -mu / (2*E) # km
    
    rnew, vnew = coe2rv(coe)
    
    print('RV <-> COE test:')
    print('r_ECI = ', r_IJK, ' km')
    print('v_ECI = ', v_IJK, ' km/s')
    print('r = ', r, 'km (correct = 11456.57 km)')
    print('v = ', v, 'km/s (correct = 7.651888 km/s)')
    #print('angular momentum     h       = ', h, 'km^2/s (correct = 66420.1 km^2/s)')
    #print('semiparameter        p       = ', p, ' km (correct = 11,067.79 km)')
    print('semimajor axis       a       = ', a, ' km (correct = 36127.343 km)')
    print('eccentricity         ecc     = ', ecc, ' (correct = 0.832853)')
    print('inclination          inc     = ', inc*vorb.rad, ' deg (correct = 87.87 deg)')
    print('right ascension      RAAN    = ', RAAN*vorb.rad, ' deg (correct = 227.898 deg)')
    print('argument of perigee  omega   = ', omega*vorb.rad, ' deg (correct = 53.38 deg)')
    print('true anomaly         theta   = ', theta*vorb.rad, ' deg (correct = 92.335 deg)')
    #print('mean anomaly         m       = ', m, ' deg')
    #print('argument of latitude arglat  = ', arglat, ' deg (correct = 145.60549 deg)')
    #print('true longitude       truelon = ', truelon, ' deg (correct = 55.282587 deg)')
    #print('longitude of perigee lonper  = ', lonper, 'deg (correct = 281.27 deg)')
    print('rnew = ', rnew, ' km')
    print('vnew = ', vnew, ' km/s')
    print('\n')

    '''
    print('PyMGRIT test:')
    print(VectorRV().get_values())

    # integrate
    #TestOrbit = Orbit3D(s0, tspan, 100, Earth, twobodyRV, 'LSODA', 1e-12, 2, 10)
    TestOrbit = Orbit3D(s0=s0, tspan=tspan)
    TestOrbit.solve()
    
    # plot
    fig, ax = plt.subplots()
    ax.plot(TestOrbit.R[0], TestOrbit.R[1], '.-')
    ax.set_aspect('equal')
    '''

    h, m, s, ap, is24 = parse_datestr('12:25 am')
    string = time2str(h, m, s, ap)
    print(string)
    print(fd_str(string))
    
    plt.show()
