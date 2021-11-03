# -*- coding: utf-8 -*-
"""
Matthew Gunther

This script analyzes various planetary & orbital parameters for Shardspace.
"""

import numpy as np
from scipy import constants as const
import OrbitBasics as ob

"""
Notes:
    C = circumference of a circle/sphere
    r = radius of a circle/sphere
    Vs = volume of a sphere
    mu = gravitational parameter (km^3/s^2)
    G = universal gravitational constant
    g = surface gravity (m/s^2)
    
    C = 2pi*r; r = C/2pi
    Vs = 4/3*pi*r^3
    mu = G*m
    g = mu/r^2; mu = g*r^2
    m = g*r^2/G = g*(C/2pi)^2/G
    
    Orbital elements
    a = semimajor axis (km)
    e = eccentricity
    i = inclination (deg)
    RAAN = right ascension of ascending node (deg)
    omega = argument of periapse
    theta = true anomaly (deg)
    M = mean anomaly (deg)
    E = eccentric anomaly (deg)
    r = orbital radius (km)
    ra = apoapse distance (km)
    rp = periapse distance (km)
    p = semiparameter (km)
    P = orbital period (s)
    b = semiminor axis (km)
    
    circular orbit
    r = rp = ra = a = p
    e, i, RAAN, & omega all = 0
    
    P = 2pi*sqrt(a^3/mu)
    a = cbrt(mu*(P/2pi)^2)
    mean orbital distance = a+b/2
    M = E - e*sin(E)
    cos(theta) = (cos(E)-e)/(1-e*cos(E))
    theta = M + (2e-(1/4)e^3)sin(M) + (5/4)e^2*sin(2M) + (13/12)e^3*sin(3M) + O(e^4)
    r = a*(1-e^2)/(1+e*cos(theta))
"""

'''
PLANETS OF THE MATERIAL PLANE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

planets = ['Sarlona',
           'Khorvaire',
           'Xendrik',
           'Aerenal',
           'Argonnessen',
           'Frostfell']
g = {'Sarlona':9.5,
     'Khorvaire':10,
     'Xendrik':7.5,
     'Aerenal':2,
     'Argonnessen':20,
     'Frostfell':5} # surface gravity, m/s^2
r = {'Sarlona':3500,
     'Khorvaire':4000,
     'Xendrik':3000,
     'Aerenal':1000,
     'Argonnessen':50000,
     'Frostfell':3000} # radius, km

CB = {}
for x in planets:
    CB[x] = ob.CentralBody(g = g[x], r = r[x])

C = {}; m = {}; mu = {}; rho = {}
for x in planets:
    C[x] = CB[x].C # circumference, km
    m[x] = CB[x].m # mass, kg
    mu[x] = CB[x].mu # gravitational parameter, km^3/s^2
    rho[x] = CB[x].rho # density, kg/m^3
print('circumference:')
print(C)
print(' ')
print('mass:')
print(m)
print(' ')
print('gravitational parameter:')
print(mu)
print(' ')
print('density:')
print(rho)
print(' ')

'''
MOONS OF KHORVAIRE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

moons = ['Zarantyr',
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
         'Vult']
D_mi = {'Zarantyr':1250,
         'Olarune':950,
         'Therendor':1100,
         'Eyre':1200,
         'Dravago':2000,
         'Nymm':900,
         'Lharvion':1350,
         'Barrakas':1500,
         'Rhaan':800,
         'Sypheros':1200,
         'Aryth':1000,
         'Vult':1800}
meandist_mi = {'Zarantyr':14300,
         'Olarune':22500,
         'Therendor':39000,
         'Eyre':52000,
         'Dravago':77500,
         'Nymm':95000,
         'Lharvion':125000,
         'Barrakas':144000,
         'Rhaan':168000,
         'Sypheros':193000,
         'Aryth':221000,
         'Vult':252000}
P = {'Zarantyr':11*const.week,
         'Olarune':8*const.week,
         'Therendor':6*const.week,
         'Eyre':9*const.week,
         'Dravago':13*const.week,
         'Nymm':4*const.week,
         'Lharvion':14*const.week,
         'Barrakas':15*const.week,
         'Rhaan':7*const.week,
         'Sypheros':5*const.week,
         'Aryth':12*const.week,
         'Vult':10*const.week}
M = {'Zarantyr':229.09,
         'Olarune':0,
         'Therendor':0,
         'Eyre':240,
         'Dravago':138.46,
         'Nymm':0,
         'Lharvion':154.29,
         'Barrakas':0,
         'Rhaan':308.57,
         'Sypheros':0,
         'Aryth':0,
         'Vult':0}
i = 15 # inclination, deg
omega = 90 # argument of periapse, deg

mu_E = ob.Earth.mu # Earth gravitational parameter, km^3/s^2
print('Khorvaire GEO orbit:')
PGEO = const.day # Khorvaire day = 24 hours
rGEO = ob.P2a(PGEO, mu['Khorvaire'])
print(rGEO)
print('Xendrik GEO orbit:')
rGEO = ob.P2a(PGEO, mu['Xendrik'])
#rGEO = ob.P2a(PGEO, mu_E)
print(rGEO)
print(' ')
e = 0.2 # eccentricity
print('e = '+str(e))
print(' ')
delta_earthmoon = ob.delta_Luna # angular diameter of Earth's moon
rho_earthmoon = ob.rho_Luna # density of Earth's moon
rho_moons = 3000 # density of Khorvaire's moons, kg/m^3
rho_earth = 5514 # density of Earth

D = {}; meandist = {}; a = {}; rp = {}; ra = {}; delta_p = {}; delta_a = {}
delta_ratio = {}; delta_earthratio_p = {}; delta_earthratio_a = {}; b = {}
P_X = {}; P_E = {}; theta = {}; err = {}; R = {}; mu_moons = {}; g_moons = {}
m_moons = {}; grel = {};
#e = {};
for x in moons:
    D[x] = D_mi[x]*const.mile/const.kilo # D in km
    R[x] = D[x]/2 # radius in km
    m_moons[x] = ob.dens2mass(R[x], rho_earth) # mass in kg
    mu_moons[x] = ob.r2mu(R[x], rho_moons) # gravitational parameter in km^3/s^2
    g_moons[x] = ob.gsurf(R[x], m_moons[x]) # surface gravity in m/s^2
    grel[x] = g_moons[x]/g['Khorvaire'] # surface gravity in g's
    meandist[x] = meandist_mi[x]*const.mile/const.kilo # meandist in km
    
    # method 1 (mean dist and e given)
    a[x] = ob.meandist2a(meandist[x], e)
    # method 2 (mean dist and P given)
    #a[x] = P2a(P[x], mu['Khorvaire']) # semimajor axes, km
    #a[x] = P2a(P[x], mu['Xendrik'])
    #a[x] = P2a(P[x], mu_E)
    #b[x] = (2*meandist[x])-a[x] # semiminor axes, km
    #e[x] = ab2e(a[x], b[x]) # eccentricity
    
    P[x] = ob.a2P(a[x], mu['Khorvaire'])/const.day # orbital period, days
    P_X[x] = ob.a2P(a[x], mu['Xendrik'])/const.day
    P_E[x] = ob.a2P(a[x], mu_E)/const.day
    [rp[x], ra[x]] = ob.a2rpra(a[x], e) # radius at apoapse and periapse, km
    delta_p[x] = ob.ang_diam(D[x], rp[x]) # angular diameter at periapse, arcminutes
    delta_a[x] = ob.ang_diam(D[x], ra[x]) # angular diameter at apoapse, arcminutes
    delta_ratio[x] = delta_p[x]/delta_a[x] # max/min angular diameter ratio
    delta_earthratio_p[x] = delta_p[x]/delta_earthmoon # ratio to Earth's moon (31.7 arcmin)
    delta_earthratio_a[x] = delta_a[x]/delta_earthmoon # ratio to Earth's moon
    [theta[x], err[x]] = ob.Me2theta(M[x], e) # true anomaly, deg
print('diameter of moons:')
print(D)
print(' ')
print('radius of moons [km]')
print(R)
print(' ')
print('mu of moons [km^3/s^2]')
print(mu_moons)
print(' ')
print('surface gravity of moons [m/s^2]')
print(g_moons)
print(' ')
print('surface gravity [g\'s]:')
print(grel)
print(' ')
print('mean distance of moons:')
print(meandist)
print(' ')
print('semimajor axes of moons:')
print(a)
print(' ')
#print('semiminor axes of moons:')
#print(b)
#print(' ')
#print('eccentricity of moons:')
#print(e)
#print(' ')
print('orbital period of moons (days):')
print(P)
print(' ')
print('rp and ra of moons:')
print('rp:')
print(rp)
print('ra:')
print(ra)
print(' ')
print('ang diam of moons:')
print('max (rp):')
print(delta_p)
#print('min (ra):')
#print(delta_a)
#print('max/min ratio:')
#print(delta_ratio)
print('ratio to Earth\'s moon:')
print('max (rp):')
print(delta_earthratio_p)
#print('min (ra):')
#print(delta_earthratio_a)
#print(' ')

print('RAAN of moons:')
RAAN = {}
y = 360./12.
for x in np.arange(12):
    z = (x*y) - 90
    if z<0: z = z + 360
    print(moons[x]+' - '+str(z))
    RAAN[moons[x]] = z
print(' ')

print('theta of moons:')
print(theta)
print(' ')

moonCOEs = np.zeros((len(moons), 6))
loop = 0
for x in moons:
    coe = np.array([a[x], e, i, RAAN[x], omega, theta[x]])
    moonCOEs[loop,:] = coe
    loop += 1