# -*- coding: utf-8 -*-
"""
Matthew Gunther

This script analyzes various planetary & orbital parameters for Shardspace.
"""

import numpy as np
from scipy import constants as const
import orbits.OrbitBasics as ob
import Calendars as cal

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
ARRAH - CENTRAL BODY OF THE MATERIAL PLANE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

# Sol values (Earth's sun) for relative calcs
m_S = ob.m_S            # mass, kg
r_S = ob.r_S            # radius, km
T_S = ob.T_S            # effective surface temperature, K
L_S = ob.L_S            # luminosity, J/s (W)

m_A = 1.75 # let Arrah = 1.75 solar masses
m_A_kg = 1.75*m_S # Arrah mass in kg
mu_A = m_S*m_A*const.G/(const.kilo**3) # Arrah mu, km^3/s^2
Arrah_color = '#ffc18dff' # 3500K, from https://academo.org/demos/colour-temperature-relationship/
T_A = 3500      # temperature, K
Lrel = 1        # relative luminosity, L/Lsun
rrel = ((T_S/T_A)**2)*np.sqrt(Lrel/L_S) # relative stefan-boltzmann law
r_A = rrel*r_S # km

Arrah = ob.CentralBody('Arrah', mu = mu_A, r = r_A, m = m_A_kg, T = T_A)

'''
PLANETS OF THE MATERIAL PLANE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

names = ['Sarlona',
         'Khorvaire',
         'Ring of Siberys',
         'Xendrik',
         'Aerenal',
         'Argonnessen',
         'Frostfell',
         'Everice']

planets = ['Sarlona',
           'Khorvaire',
           'Xendrik',
           'Aerenal',
           'Argonnessen',
           'Frostfell',
           'Everice']
g = {'Sarlona':     9.5,
     'Khorvaire':   10,
     'Xendrik':     7.5,
     'Aerenal':     2,
     'Argonnessen': 20,
     'Frostfell':   5,
     'Everice':     5} # surface gravity, m/s^2
r = {'Sarlona':     3500,
     'Khorvaire':   4000,
     'Xendrik':     3000,
     'Aerenal':     1000,
     'Argonnessen': 50000,
     'Frostfell':   3000,
     'Everice':     3000} # radius, km

# randomly generated positions using
# treasuretools.roll('1d360')*np.pi/180
# true anomaly at epoch, radians
# Everice and Frostfell are at mutual L3 points (180deg separation)
# Everice = Frostfell - pi
# Aerenal is at Xen'drik's L4 point (60deg ahead)
# Aerenal = Xendrik + (60*pi/180)
theta = {'Sarlona':     5.6199601914217405,
         'Khorvaire':   0.,
         'Xendrik':     3.8571776469074686,
         'Aerenal':     4.904375198104066,
         'Argonnessen': 2.478367537831948,
         'Frostfell':   4.485496177625427,
         'Everice':     1.3439035240356336}

# create CentralBody objects for planets
CB = {}
for x in planets:
    CB[x] = ob.CentralBody(x, g = g[x], r = r[x])

# extract parameters of interest
C = {}; m = {}; mu = {}; rho = {}
for x in planets:
    C[x] = CB[x].C # circumference, km
    m[x] = CB[x].m # mass, kg
    mu[x] = CB[x].mu # gravitational parameter, km^3/s^2
    rho[x] = CB[x].rho # density, kg/m^3
    
# orbital semimajor axes of planets
# compare Eberron orbits to HZ
P_Khorvaire = 336*const.day # [s] Khorvaire's year is 336 days
# TRAPPIST-1
orb_T = np.array([24.0, 15.0, 9.0, 6.0, 4.0, 3.0, 2.0]) # number of orbits
n_orb = orb_T[1:len(planets)-1+1]
factor = 2
n_orb[4] = n_orb[4]/factor
n_orb[5] = n_orb[5]/(factor**2)
n_norm = n_orb/n_orb[1] # normalize to the 2nd planet (Khorvaire)
Pnorm = n_orb[1]/n_orb # TRAPPIST orbital period ratios
P_E = P_Khorvaire*Pnorm # [s] relative period of Eberron planets
P_E_days = P_E/const.day # [d]
a_vec = []
a_vec = np.zeros((len(names),1), dtype='float64')
for i in range(len(names)-2):
    a_vec[i] = ob.P2a(P_E[i], mu_A) # semimajor axes, km
a_vec[6:8] = a_vec[5] # correct Frostfell & Everice indices
a_vec[4:6] = a_vec[3:5] # correct Aerenal & Argonnessen indices

ArrahSystem = {'names':     names,
               'r':         a_vec,    
               'title':     'Eberron',
               'CB':        Arrah,
               'epoch_ta':  np.array(list(theta.items())),
               'epoch_date':cal.GalifarDate(d=1, m='Zarantyr', y=998)}

'''
for i in range(len(planets[:-1])):
    print(_names[i],':',round(a_vec[i][0]/ob.AU,2))
'''

'''
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
#print('Khorvaire GEO orbit:')
PGEO = const.day # Khorvaire day = 24 hours
rGEO = ob.P2a(PGEO, mu['Khorvaire'])
#print(rGEO)
#print('Xendrik GEO orbit:')
rGEO = ob.P2a(PGEO, mu['Xendrik'])
#rGEO = ob.P2a(PGEO, mu_E)
#print(rGEO)
#print(' ')
e = 0.2 # eccentricity
#print('e = '+str(e))
#print(' ')
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

'''
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
'''

#print('RAAN of moons:')
RAAN = {}
y = 360./12.
for x in np.arange(12):
    z = (x*y) - 90
    if z<0: z = z + 360
    #print(moons[x]+' - '+str(z))
    RAAN[moons[x]] = z
#print(' ')

#print('theta of moons:')
#print(theta)
#print(' ')

moonCOEs = np.zeros((len(moons), 6))
loop = 0
for x in moons:
    coe = np.array([a[x], e, i, RAAN[x], omega, theta[x]])
    moonCOEs[loop,:] = coe
    loop += 1

'''
PLANES OF THE ASTRAL SEA~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

planes = ['Lamannia',
          'Mabar',
          'Irian',
          'Risia',
          'Fernia',
          'Syrania',
          'Shavarath',
          'Dolurrh',
          'Thelanis',
          'Daanvi',
          'Kythri',
          'Xoriat',
          'Dal Quor']

P_yr = {'Lamannia':    1,
        'Mabar':       1,
        'Irian':       3,
        'Risia':       5,
        'Fernia':      5,
        'Syrania':     10,
        'Shavarath':   36,
        'Dolurrh':     100,
        'Thelanis':    225,
        'Daanvi':      400,
        'Kythri':      400,
        'Xoriat':      10000,
        'Dal Quor':    40000} # orbital period, years

# calculate mass required for Lamannia to orbit at 20AU radius
mu_req = ob.Pa2mu(P_yr['Lamannia']*P_Khorvaire, 20*ob.dist.AU) # mu required for 20 AU Lamannia orbit
m_req = ob.mu2mass(mu_req) # mass required for 20 AU Lamannia orbit
if __name__=='__main__': print('m_req =', m_req, ' kg')

#m_Eberron = 1500*m_S # effective mass of the Material Plane as seen by objects in the Astral Sea
m_Eberron = m_req
mu_Eberron = ob.mass2mu(m_Eberron)
r_Eberron = 1.25*ArrahSystem['r'][-1][0]
if __name__=='__main__':
    print(ArrahSystem['names'][-1], 'radius:', ArrahSystem['r'][-1][0], 'km =', ob.dist.km2AU(ArrahSystem['r'][-1][0]), ' AU')
    print('Eberron radius:', r_Eberron, 'km =', ob.dist.km2AU(r_Eberron), ' AU')
Eberron = ob.CentralBody('Eberron', mu = mu_Eberron, r = r_Eberron, m = m_Eberron)

a_planes = {}
P_sec = {}
if __name__=='__main__': print('Planar Orbits')
for i in planes:
    P_sec[i] = P_yr[i]*P_Khorvaire # orbital periods, sec
    a_planes[i] = ob.P2a(P_sec[i], mu_Eberron) # semimajor axes, km
    a_AU = ob.dist.km2AU(a_planes[i])
    if __name__=='__main__': print(i, ':', a_planes[i], 'km =', a_AU, 'AU')

#print(np.array(list(a_planes.values())).flatten())
AstralSystem_All = {'names': planes,
                    'r': np.array(list(a_planes.values())),
                    'title': 'Astral Sea',
                    'CB': Eberron}
AstralSystem = {'names': planes[:-2],
                'r': np.array(list(a_planes.values()))[:-2],
                'title': 'Astral Sea',
                'CB': Eberron
                }

'''
DAANVI - THE PERFECT ORDER
'''

# central body is 1Hz pulsar
m_Daanvi = 1.5*m_S # mass, kg
L_Daanvi = 5*L_S # luminosity

'''
DAL QUOR - THE REGION OF DREAMS
'''

# everything orbits il-Lashtavar
m_ilLashtavar = m_S # mass, kg

'''
DOLURRH - THE REALM OF THE DEAD
'''

# brown dwarf star
m_Dolurrh = 0.08*m_S # mass, kg
T_Dolurrh = 1000 # temperature, Kelvin
L_Dolurrh = 0.1*L_S # luminosity

'''
FERNIA - THE SEA OF FIRE
'''

# red supergiant
m_Fernia = 10*m_S # mass, kg
T_Fernia = 2500 # temperature, Kelvin
r_Fernia = 100*r_S # radius, km

'''
IRIAN - THE ETERNAL DAWN
'''

# large sun-like star
T_Irian = 6000 # temperature, Kelvin
m_Irian = 5*m_S # mass, kg
r_Irian = 10*r_S # radius, km
L_Irian = 10*L_S # luminosity

# The Amaranthine City
# 12 moons in orbit
r_Amaranthine = 10*ob.Earth.r # radius, km

'''
KYTHRI - THE CHURNING CHAOS
'''

# center is nebula with dozens of small T Tauri stars
# accelerated lifespans end within weeks of formation
m_Kythri = 0.1*m_S # mass, kg
Tmin_Kythri = 2500 # min temperature, Kelvin
Tmax_Kythri = 7500 # max temperature, Kelvin

'''
MABAR - THE ENDLESS NIGHT
'''

# black hole
m_Mabar = 100*m_S # mass, kg
rSch_Mabar = ob.rschwarz(m_Mabar) # schwarzchild radius, km
if __name__=='__main__': print('Mabar schwarzchild radius: ', rSch_Mabar, ' km = ', ob.dist.km2AU(rSch_Mabar), ' AU')
L_Mabar = 0.01*L_S # luminosity of accretion disk

'''
RISIA - THE PLAIN OF ICE
'''

# small blue star
m_Risia = 0.1*m_S # mass, kg
T_Risia = 6500 # temperature, Kelvin
r_Risia = 0.1*r_S # radius, km

'''
SHAVARATH - THE ETERNAL BATTLEGROUND
'''

# Baator
m_Baator = 0.5*m_S # mass, kg
T_Baator = 4000 # temperature, Kelvin

# Justice
m_Justice = 0.5*m_S # mass, kg
T_Justice = 5500 # temperature, Kelvin

# The Abyss

'''
SYRANIA - THE AZURE SKY
'''

'''
THELANIS - THE FAERIE COURT
'''

'''
XORIAT - THE REALM OF MADNESS
'''