# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 17:10:05 2021

@author: Matthew Gunther (TheKingofCrimsonesia)
"""

import math
import numpy as np
from scipy import constants as const
import matplotlib.pyplot as plt
plt.close('all')

import OrbitBasics as ob
from OrbitBasics import dist
import Constants_Eberron as eberron
CB = eberron.CB # dict of CentralBody objects
planets = eberron.planets[:-1]

# Universal constants
c = const.c # speed of light, m/s
AU = ob.AU  # astronomical unit, km
ly = ob.ly  # light year, km

'''
Stellar Parameters
'''

# constants for Sol, Earth's sun
mu_S = ob.mu_S          # gravitational parameter, km^3/s^2
g_S = ob.g_S            # surface gravity, m/s^2
m_S = ob.m_S            # mass, kg
r_S = ob.r_S            # radius, km
rho_S = ob.rho_S        # density, kg/m^3
L_S = ob.L_S            # luminosity, J/s (W)
M_S = ob.M_S            # absolute magnitude
SE_S = ob.SE_S          # spectral emission, J/m^2
T_S = ob.T_S            # effective surface temperature, K
delta_S = ob.delta_S    # angular size, arcminutes
d_S = AU                # mean distance from Earth, km (=1AU)
dsun = d_S
Lsun = L_S
msun = ob.msun          # apparent magnitude
rsun = r_S
Tsun = T_S
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
             'Ceres',
             'Jupiter',
             'Saturn',
             'Uranus',
             'Neptune',
             'Pluto'] # Solar system planet names

# Stefan-Boltzmann law:
# L = 4*pi*sigma*(r**2)*(T**4)
#     L, Luminosity (J/s, aka Watts)
#     r, Radius (m)
#     T, Effective Temperature (K)
def T2F(T):
    # F = energy flux, W/m^2
    return const.sigma*(T**4) # W/m^2
def F2T(F):
    return math.pow(F/const.sigma, 0.25) # K
def rT2L(r, T):
    return 4*np.pi*const.sigma*(r**2)*(T**4) # W
def TL2r(T, L):
    return math.sqrt(L/(4*np.pi*const.sigma*(T**4))) # m
def rL2T(r, L):
    return math.pow((L/(4*np.pi*const.sigma*(r**2))), 0.25) # K

# mass-luminosity relation
# (L/Lsun) = (M/Msun)**a
def Mrel_to_Lrel(Mrel):
    if Mrel < 0.43:
        Lrel = 0.23*(Mrel**2.3)
    elif Mrel < 2:
        Lrel = Mrel**4
    elif Mrel < 55:
        Lrel = 1.4*(Mrel**3.5)
    else:
        Lrel = 32000*Mrel
    return Lrel
#def MtoL_alt(Mrel):
    # only valid for 0.2 < Mrel < 0.85
    #return Mrel**(()+()+()+()+0.215)

# parallax and distance
def p2d(p):
    # p = parallax angle, arcseconds
    # d = distance, parsecs
    return 1/p # pc
def p2d_km(p):
    # p = parallax angle, arcseconds
    # d = distance, km
    return p2d(p)*dist.pc # km

# luminosity distance formula
def Ld2b(L, d):
    # L = luminosity, W (J/s)
    # d = distance, m
    # b = brightness, W/m^2
    return L/(4*np.pi*(d**2)) # W/m^2
def Ld2b_km(L, d):
    return Ld2b(L, d*const.kilo) # W/m^2
def db2L(d, b):
    return 4*np.pi*(d**2)*b # W
def db2L_km(d, b):
    return db2L(d*const.kilo, b) # W
def db2L_rel(drel, brel):
    # drel = relative distance, d/dsun
    # brel = relative brightness, b/bsun
    # Lrel = relative luminosity, L/Lsun
    return (drel**2)*brel # L/Lsun
def Ld2b_rel(Lrel, drel):
    return Lrel/(drel**2) # b/bsun
bsun = Ld2b(Lsun, dsun) # brightness of Sun at Earth, W/m^2

# apparent magnitude and brightness ratio
# m1-m2 = -2.5log(b1/b2)
# m = apparent magnitude, relative at Earth
# b = brightness, W/m^2
def m2brel(m1, m2):
    # return brightness ratio, brel = b1/b2
    return 10**(m1-m2) # b1/b2
def m2b(m1, m2, b2):
    # return brightness in W/m^2
    return b2*m2brel(m1, m2) # W/m^2
def m2brel_S(m):
    # assume Sun for m2, b2
    # return brightness ratio, brel = b/bsun
    return m2b(m, msun) # b/bsun
def m2b_S(m):
    # assume Sun for m2, b2
    # return brightness in W/m^2
    return m2b(m, msun, bsun) # W/m^2

# apparent and absolute magnitude
# M = absolute magnitude, brightness at 10 pc
# m-M = distance modulus
def md2M(m, d):
    # m = apparent magnitude
    # d = distance in pc
    return m-(5*np.log10(d))+5 # M
def md2M_km(m, d):
    return md2M(m, d/dist.pc) # M
def mM2d(m, M):
    # m = apparent magnitude
    # M = absolute magnitude
    # returns distance in pc
    return 10**((m-M+5)/5) # pc
def mM2d_km(m, M):
    return mM2d(m, M)*dist.pc # km

# Wien's law
def T2lmax(T):
    # T = temperature, K
    # lmax = peak wavelength, nm
    return 2900000/T # nm
def lmax2T(lmax):
    return 2900000/lmax # K

# relative stefan-boltzmann law
# rrel = r/rsun
# Trel = T/Tsun
# Lrel = L/Lsun
def TL2rrel(T, L):
    return ((Tsun/T)**2)*math.sqrt(L/Lsun) # r/rsun
def TL2rrel_km(T, L):
    return TL2rrel(T, L)*rsun # km

'''
Habitable Zone Calculations
'''

def HZcalc(teff=5780.0, Lrel=1.0, e=0.0, type='gh'):
    '''
    from Kopperapu et al, "Habitable Zones - New Estimates"
    '''
    # teff = stellar effective temperature, K (2600 < teff < 7200)
    # Lrel = relative luminosity (L/Lsun)
    # e = orbital eccentricity of planet
    
    seffsun  = np.array([1.776, 1.107, 0.356, 0.320, 1.188, 0.99])
    A = np.array([2.136e-4, 1.332e-4, 6.171e-5, 5.547e-5, 1.433e-4, 1.209e-4])
    B = np.array([2.533e-8, 1.580e-8, 1.698e-9, 1.526e-9, 1.707e-8, 1.404e-8])
    C = np.array([-1.332e-11, -8.308e-12, -3.198e-12, -2.874e-12, -8.968e-12, -7.418e-12])
    D = np.array([-3.097e-15, -1.931e-15, -5.575e-16, -5.011e-16, -2.084e-15, -1.713e-15])
    # i = 0 --> Recent Venus
    # i = 1 --> Runaway Greenhouse
    # i = 2 --> Maximum Greenhouse
    # i = 3 --> Early Mars
    # i = 4 --> Runaway Greenhouse for 5 ME
    # i = 5 --> Runaway Greenhouse for 0.1 ME
    
    # SOLAR FLUX - TEMPERATURE DEPENDENCE
    # use Runaway Greenhouse for inner HZ edge
    # use Maximum Greenhouse for outer HZ edge
    seff = np.array([0.0,0.0])
    tstar = teff-5780 # K
    if type=='gh': idx = [1,2] # greenhouse limits
    elif type=='vm': idx = [0,3] # recent Venus/early Mars limits
    for i in [0,1]:
        seff[i] = seffsun[idx[i]] + A[idx[i]]*tstar + B[idx[i]]*tstar**2 + C[idx[i]]*tstar**3 + D[idx[i]]*tstar**4
    
    # SOLAR FLUX - ECCENTRICITY DEPENDENCE
    seff = seff/math.sqrt(1 - e**2)
    
    # HABITABLE ZONE EDGE DISTANCES
    d = (Lrel/seff)**0.5 # AU
    
    return d # AU

def Mr2Prel(M, r):
    # M = planetary mass, kg
    # r = planetary radius, km
    # Prel = relative atmospheric pressure, P/P0 (P0 = Earth pressure)
    M0 = 5.9724e24 # Earth mass, kg
    r0 = 6371 # Earth mean radius, km
    return ((M/M0)**2) * ((r0/r)**4) # Prel

'''
Orbital Resonance
'''
# TRAPPIST-1
orb_T = np.array([24.0, 15.0, 9.0, 6.0, 4.0, 3.0, 2.0]) # number of orbits

# Laplacian
# double 1:2:4 chain
P_L = np.array([1.0, 2.0, 4.0, 8.0, 16.0, 32.0]) # orbital periods

'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

#print('Earth:')
HZ_E = HZcalc() # AU
#print('inner HZ =',str(round(HZ_E[0],3)),'AU')
#print('outer HZ =',str(round(HZ_E[1],3)),'AU')
#print(' ')

# constants for Arrah, Eberron's sun
#print('Arrah:')
#r_A = 1000000   # radius, km
#L_A = 300e24    # luminosity, J/s (W)

#T_A = rL2T(r_A*const.kilo, L_A)
#print('T =',str(T_A))

#lmax = T2lmax(T_A)
#print('peak wavelength =',str(lmax))

#print(' ')
# ----- USE THESE VALUES ----------------
T_A = 3500      # temperature, K
Lrel = 1        # relative luminosity, L/Lsun
#print('for T =',str(T_A))
#print('and L = Lsun,')

rrel = TL2rrel(T_A, Lsun)
r_A = rrel*rsun # km
#print('r =',str(round(rrel,2)),'times rsun')
#print('(',str(round(r_A,-3)),'km )')

lmax = T2lmax(T_A)
#print('peak wavelength =',str(round(lmax)))

HZ_A = HZcalc(T_A, Lrel) # runaway & max greenhouse limits
#print('inner HZ =',str(round(HZ_A[0],3)),'AU')
#print('outer HZ =',str(round(HZ_A[1],3)),'AU')
HZ_Avm = HZcalc(T_A, Lrel, type='vm') # recent Venus & early Mars limits
#print('Venus HZ =',str(round(HZ_Avm[0],3)),'AU')
#print('Mars HZ =',str(round(HZ_Avm[1],3)),'AU')
'''
HZ_X = HZcalc(T_A, Lrel, e=0.1)
print('eccentric Xendrik:')
print('inner HZ =',str(round(HZ_X[0],3)),'AU')
print('outer HZ =',str(round(HZ_X[1],3)),'AU')
'''
#print(' ')

#print('Relative atmospheric pressure:')
for i in planets:
    Prel = Mr2Prel(CB[i].m, CB[i].r)
    #print(i,':',Prel)
#print(' ')

'''
# orbital resonance
fund = 110.0 # A2, Hz
tones_T = fund*orb_T # TRAPPIST tones, Hz
tones_L = 2*fund*P_L # Laplacian tones, Hz
print('Orbital resonance tones [Hz]:')
print('TRAPPIST-1:')
print(tones_T)
print('Laplacian:')
print(tones_L)
'''

# compare Eberron orbits to HZ
names = ['Sarlona',
         'Khorvaire',
         'Ring',
         'Xendrik',
         'Argonnessen',
         'Frostfell']
P_Khorvaire = 336*const.day # [s] Khorvaire's year is 336 days
#scale = np.array(1.)
#n_orb = np.zeros_like(names, dtype='float64')
#for i in range(1,len(planets)+1):
#    n_orb[i-1] = orb_T[i-1]/(scale**i) # outer 6 TRAPPIST planets
n_orb = orb_T[1:len(planets)+1]
factor = 2
n_orb[4] = n_orb[4]/factor
n_orb[5] = n_orb[5]/(factor**2)
n_norm = n_orb/n_orb[1] # normalize to the 2nd planet (Khorvaire)
Plapl = P_L/P_L[1] # Laplacian orbital periods
Pnorm = n_orb[1]/n_orb # TRAPPIST orbital period ratios
#Pnorm = Plapl # override TRAPPIST with Laplacian
P_E = P_Khorvaire*Pnorm # [s] relative period of Eberron planets
P_E_days = P_E/const.day # [d]


print('Eberron orbital distances')
print('number of orbits relative to 1 Khorvaire orbit:')
for i in range(len(names)):
    print(names[i],':',round(n_norm[i],2))
print('orbital period ratios:')
for i in range(len(planets)):
    print(names[i],':',round(Pnorm[i],2))
print('orbital period [days]:')
for i in range(len(planets)):
    print(names[i],':',round(P_E_days[i],2))
print(' ')


'''
m_vec = np.linspace(0.1, 2, 20) # let Arrah's mass range from 0.1 to 2 mSun
mu_vec = m_S*m_vec*const.G/(const.kilo**3) # Arrah mu range, km^3/s^2
a_vec = np.zeros((len(names),len(mu_vec)))
for i in range(len(names)):
    a_vec[i,:] = ob.P2a(P_E[i], mu_vec) # semimajor axes, km
    plt.plot(a_vec[i,:]/AU, m_vec, label=names[i])
plt.plot(Sol_a/AU, np.ones_like(Sol_a), 'ko', label='Solar System')

plt.axvline(HZ_A[0], c='m', ls='--', label='Inner HZ limit')
plt.axvline(HZ_A[1], c='c', ls='--', label='Outer HZ limit')
plt.axvline(HZ_Avm[0], c='r', ls='--', label='Venus HZ limit')
plt.axvline(HZ_Avm[1], c='b', ls='--', label='Mars HZ limit')
'''

m_A = 1.75 # let Arrah = 1.75 solar masses
mu_A = m_S*m_A*const.G/(const.kilo**3) # Arrah mu, km^3/s^2
a_vec = []
a_vec = np.zeros((len(names),1), dtype='float64')
for i in range(len(names)):
    a_vec[i] = ob.P2a(P_E[i], mu_A) # semimajor axes, km
    #plt.plot(a_vec[i]/AU, m_A, 'kx')
'''
plt.xlabel('orbital distance, AU')
plt.ylabel('Arrah mass, mSun')
plt.xscale('log')
plt.legend()
plt.show()
'''


print('Eberron final parameters:')
print('Arrah mass = ',m_A,'solar masses')
print('Arrah mu =',round(mu_A/1e9,2),'x10^9 km^3/s^2')
print('semimajor axes [AU]:')
for i in range(len(planets)):
    print(names[i],':',round(a_vec[i][0]/AU,2))
print(' ')
print('semimajor axes [km]:')
for i in range(len(planets)):
    print(names[i],':',round(a_vec[i][0],2))
print(' ')
