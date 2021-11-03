# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 19:00:39 2021

@author: Matthew
"""

import numpy as np
from scipy import constants as const
from matplotlib import pyplot as plt

import OrbitBasics as ob
import NumericalAnalysis as na

## ----------------------------------------------------------------------------
## CONSTANTS
## ----------------------------------------------------------------------------

c  = const.c                    # speed of light, m/s
AU = 149597870.7                # astronomical unit, km
ly = c*const.year/const.kilo    # light year, km

G = const.G # universal gravitational constant (m^3/kg/s)

## ----------------------------------------------------------------------------
## SPECIAL RELATIVITY
## ----------------------------------------------------------------------------

'''
# CONVENTIONS
all four-vectors are column vectors
Lorentz factor: gamma = 1/sqrt(1-v^2/c^2)
velocity ratio: beta = v/c
relativistic momentum: p = gamma*m*v
energy: E = gamma*m*c^2
invariant mass: minv 
relativistic mass: m = gamma*m (aka "observed mass")
KE = (gamma-1)*m*c^2
'''

# Minkowski metric
eta = np.eye(4)
eta[0,0] = -1 # metric with signature (-+++)
#print(eta)
eta_pos = eta * (-np.eye(4)) # metric with signature (+---)

'''
Position four-vector:
X = [ct, x, y, z] coordinate frame, at rest
X' = [ct', x', y', z'] proper frame, seen from coord frm as mov w speed v

Momentum four-vector:
P = [E/c, px, py, pz]

Lorentz transformation:
X' = Lambda * X
'''

## ----------------------------------------------------------------------------
## LIST OF RELATIVITY METRICS
## ----------------------------------------------------------------------------
'''

standard 2D metric
    Cartesian coordinates (x, y):
        ds**2 = dx**2 + dy**2 (Pythagorean theorem)
    
    2-sphere coordinates (theta, phi):
        dOmega**2 = dtheta**2 + (sin(theta)**2)*(dphi**2)


standard 3D metric
    Cartesian coordinates (x, y, z):
        ds**2 = dx**2 + dy**2 + dz**2
        
    spherical coordinates (r, theta, phi)
        ds**2 = dr**2 + (r**2)*(dOmega**2)
    

Minkowski metric
    flat spacetime (Special Relativity)

    x**2 + y**2 + z**2 + (ict)**2 = const       (-+++)
    -(ct)**2 + x**2 + y**2 + z**2 = const       (-+++)
    
    (c**2 * t**2) - x**2 - y**2 - z**2 = const  (+---)
    
    spacetime interval:
    (c**2)*(t1 - t2)**2 - (x1 - x2)**2 - (y1 - y2)**2 - (z1 - z2)**2

    ds**2 = -(c**2)*(dt**2) + dx**2 + dy**2 + dz**2     (-+++)

    coordinates (ct, x, y, z) (Standard Basis):
        eta = [-1 0 0 0           = [1  0  0  0
                0 1 0 0              0 -1  0  0
                0 0 1 0              0  0 -1  0
                0 0 0 1] (-+++)      0  0  0 -1] (+---)
    
    coordinates (t, x, y, z):
        eta = [-c**2 0 0 0
                0    1 0 0
                0    0 1 0
                0    0 0 1] (-+++)
        
    spherical coordinates (t, r, theta, phi):
        ds**2 = -(c**2)*(dt**2) + dr**2 + (r**2)*(dOmega**2)
        

Schwarzchild metric
    uncharged, non-rotating mass (General Relativity)
    static, spherically symmetric body of mass M in vacuum
    
    Schwarzchild radius:
        rs = 2*G*M / (c**2)

    Schwarzchild coordinates (t, r, theta, phi):
        anisotropic coordinates
            vel of light diff in radial and transverse directions
        
        ds**2 = - (1 - 2*G*M/(r * (c**2))) * (c**2) * (dt**2)
                + (1 - 2*G*M/(r * (c**2)))^-1 * dr**2
                + (r**2) * dOmega**2
        where G = univ grav constant, and M = mass of the grav source
        (-+++)
        
        ds**2 = -(c**2) * (dtau**2)
              = - (c**2) * (1 - rs/r) * (dt**2)
                + (1 - rs/r)^-1 * dr**2
                + r**2 * dOmega**2
        where tau is proper time, t is coordinate time,
            r is circumference/2pi of sphere centered around massive body,
            theta is colatitude (radians), phi is longitude (radians)
                
        -c**2 = (ds/dtau)**2 
              = A*(dr/dtau)**2 + (r**2)*(dphi/dtau)**2 + B*(dt/dtau)**2
                  where A = 1/(1 - rs/r), and B = (c**2)*(rs/r - 1)
        
    coordinates (ct, r, theta, phi):
        g_mu,nu = [
            -(1 - 2*G*M/(r * (c**2)))  0                          0     0
              0                       (1 - 2*G*M/(r * (c**2)))^-1 0     0
              0                        0                          r**2  0
              0                        0                          0    (r**2)*(sin(theta)**2) ]
        (-+++)
        
    isotropic spherical coordinates (t, r1, theta, phi) (Eddington):
        r  =  r1*(1 + G*m/(2*(c**2)*r1))             =  r1*(1 +  rs/4r1)
                (thus r1 = r - rs/4)
        dr = dr1*(1 - ((G*m)**2)/(4*(c**4)*(r1**2))) = dr1*(1 - (rs/4r1)**2)
        (1 - 2*G*m/((c**2)*r)) = (1 - G*m/(2*(c**2)*r1))**2 / (1 + G*m/(2*(c**2)*r1))**2
        (1 - rs/r) = ( (1 - rs/4r1)/(1 + rs/4r1) )**2
        
    isotropic rectangular coordinates (t, x, y, z) (Eddington):
        x = r1 * sin(theta) * cos(phi)
        y = r1 * sin(theta) * sin(phi)
        z = r1 * cos(theta)
        
        ds**2 =   (1 + G*m/(2*(c**2)*r1))**4 * (dx**2 + dy**2 + dz**2)
                - (c**2) * (dt**2) * (1 - G*m/(2*(c**2)*r1))**2 / (1 + G*m/(2*(c**2)*r1))**2
                
        ds**2 =   (1 +  rs/4r1)**4 * (dx**2 + dy**2 + dz**2)
                - (c**2) * (dt**2) * ( (1 - rs/4r1)/(1 + rs/4r1) )**2
                
        where r1 is defined by Eddington's isotropic spherical coordinates
        
    Eddington-Finkelstein coordinates
        ingoing: -(1 - rs/r)*(dv**2) + 2*dv*dr + (r**2)*(dOmega**2)
        outgoing: -(1 - rs/r)*(du**2) - 2*du*dr + (r**2)*(dOmega**2)
            where c has been set to 1
    
    Gullstrand-Painleve coordinates
        -(1 - rs/r)*(dT**2) +/- 2*sqrt(rs/r)*dT*dr + dr**2 + (r**2)*(dOmega**2)
            where c has been set to 1
    
    Isotropic coordinates
        -((1 - rs/(4*R))**2 / (1 - rs/(4*R))**2)*(dt**2)
        + ((1 + rs/(4*R))**4) * (dx**2 + dy**2 + dz**2)
            where R = sqrt(x**2 + y**2 + z**2)
            and c has been set to 1
            note - valid only outside event horizon: R > rs/4
    
    Kruskal-Szekeres coordinates
        -(4*(rs**3)/r) * exp(-r/rs) * (dT**2 - dR**2) + (r**2)*(dOmega**2)
            where T**2 - R**2 = (1 - r/rs) * exp(r/rs)
            and c has been set to 1
    
    Lemaitre coordinates
        -dT**2 + (rs/r)*(dR**2) + (r**2)*(dOmega**2)
            where r = ((3/2)*(R +/- T))^(2/3) * (rs^(1/3))
            and c has been set to 1
    
    Novikov coordinates
    
    Harmonic coordinates
        -((rho - rs/2)/(rho + rs/2))*(dt**2)
        + ((rho + rs/2)/(rho - rs/2))*(drho**2)
        + ((rho + rs/2)**2) * (dOmega**2)
            where rho = r - rs/2
            and c has been set to 1
    

Reissner-Nordstrom metric
    charged, non-rotating mass (General Relativity)
    static, spherically symmetric body of mass M_irr and charge Q in vacuum
    
    characteristic length scale:
        rQ**2 = (Q**2)*G / (4*pi*eps0*(c**4))
                    where eps0 is the electric constant
    
    total mass and irreducible mass:
        M_irr = (c**2 / G) * sqrt(rQ**2 / 2)
        M = M_tot = (Q**2 / (16*pi*eps0*G*M_irr)) + M_irr
    
    spherical coordinates (t, r, theta, phi):
        ds**2 = (c**2) * (dtau**2)
              =   (1 - rs/r + (rQ**2)/(r**2)) * (c**2) * (dt**2)
                - (1 - rs/r + (rQ**2)/(r**2))^-1 * (dr**2)
                - (r**2) * (dOmega**2)
                
    electromagnetic potential:
        A_alpha = [Q/r, 0, 0, 0]
    
    gravitational time dilation:
        gamma = sqrt(r**2 / (Q**2 + (r - 2*M)*r))
        
    equations of motion:
        can restrict to the equatorial plane because of symmetry
        use theta instead of phi for readability
        dimensionless natural units of G = M = c = K = 1, charge q
        derivatives with respect to proper time tau, ie adot = da/dtau
        tdoubledot =   2*(Q**2 - M*r)/(r*(r**2 - 2*M*r + Q**2))  * rdot * tdot
                     + q*Q/(r**2 - 2*m*r + Q**2)                 * rdot
        rdoubledot =   (r**2 - 2*M*r + Q**2)*(Q**2 - M*r)/(r**5) * (tdot)**2
                     + (M*r - Q**2)/(r*(r**2 - 2*M*r + Q**2))    * (rdot)**2
                     + (r**2 - 2*M*r + Q**2)/r                   * (thetadot)**2
                     + q*Q*(r**2 - 2*m*r + Q**2)/(r**4)          * tdot
        thetadoubledot = -2/r * thetadot * rdot
        gamma = (q*Q*(r**3) + E*(r**4)) / ((r**2)*(r**2 - 2*r + Q**2))
        specific orbital energy
            E = sqrt(Q**2 - 2*r*M + r**2)/(r*sqrt(1 - v**2)) + q*Q/r
        specific relative angular momentum
            L = v_perp*r / sqrt(1 - v**2)
        local velocity
            v = sqrt(((E**2 - 1)*(r**2) - Q**2 - r**2 + 2*r*M) / ((E**2)*(r**2)))


Kerr metric
    uncharged, rotating mass (General Relativity)
    

Kerr-Newman metric
    charged, rotating mass (General Relativity)


Alcubierre metric


de Sitter metric


anti-de Sitter metric


Friedmann-Lemaitre-Robertson-Walker metric


Isotropic coordinates


Lemaitre-Tolman metric (aka Bondi metric)


Peres metric


Rindler coordinates


Weyl-Lewis-Papapetrou coordinates


Godel metric


'''

def v2beta(v):
    # velocity as a ratio of the speed of light
    return v/c

def uvec2beta(u):
    # calculate beta from velocity 3-vector
    return na.vecnorm(u)/c

def beta2v(beta):
    # convert velocity ratio to velocity
    return beta*c

def gammav(v):
    # Lorentz factor given velocity magnitude
    return 1 / np.sqrt(1 - ((v/c)**2))

def gammauvec(u):
    # Lorentz factor given velocity 3-vector, u
    return 1 / np.sqrt(1 - (np.dot(u, u)/(c**2)))

def gammabeta(beta):
    # Lorentz factor given velocity ratio, beta = v/c
    return 1 / np.sqrt(1 - (beta**2))

def boost(u):
    # Boost matrix for Lorentz transformation from coord to proper frame
    # where the proper frame has 3-velocity u measured in the coord frame
    # the two frames are related by:
    # X' = B(u) * X
    #   where X is a four-vector in the coordinate frame,
    #   X' is the four-vector in the proper frame,
    #   and u is the velocity 3-vector
    # to go from X' to X instead, use:
    # X = B(-u) * X'
    
    gamma = gammauvec(u) # Lorentz factor
    vx = u[0] # x-velocity component
    vy = u[1] # y-velocity component
    vz = u[2] # z-velocity component
    v = np.sqrt(vx**2 + vy**2 + vz**2) # magnitude of velocity
    
    # repeated factors
    gm1 = gamma - 1
    mg_c = -gamma/c
    v2 = v**2
    
    B = np.array([
            [gamma, mg_c*vx,            mg_c*vy,            mg_c*vz           ],
            [0,     1+(gm1*(vx**2)/v2), gm1*vx*vy/v2,       gm1*vx*vz/v2      ],
            [0,     0,                  1+(gm1*(vy**2)/v2), gm1*vy*vz/v2      ],
            [0,     0,                  0,                  1+(gm1*(vz**2)/v2)]
            ])
    B = B + np.triu(B, 1).T # B is diagonally symmetric
    
    return B

def Rzyx4d(a, b, c):
    # Spatial rotation matrix for four-vectors
    R3 = ob.Rzyx(a, b, c)
    R = np.array([
            [1, 0,       0,       0      ],
            [0, R3[0,0], R3[0,1], R3[0,2]],
            [0, R3[1,0], R3[1,1], R3[1,2]],
            [0, R3[2,0], R3[2,1], R3[2,2]],
            ])
    return R

def Rx4d(theta):
    # Spatial rotation matrix for four-vectors
    R3 = ob.Rx(theta)
    R = np.array([
            [1, 0,       0,       0      ],
            [0, R3[0,0], R3[0,1], R3[0,2]],
            [0, R3[1,0], R3[1,1], R3[1,2]],
            [0, R3[2,0], R3[2,1], R3[2,2]],
            ])
    return R

def Ry4d(theta):
    # Spatial rotation matrix for four-vectors
    R3 = ob.Ry(theta)
    R = np.array([
            [1, 0,       0,       0      ],
            [0, R3[0,0], R3[0,1], R3[0,2]],
            [0, R3[1,0], R3[1,1], R3[1,2]],
            [0, R3[2,0], R3[2,1], R3[2,2]],
            ])
    return R

def Rz4d(theta):
    # Spatial rotation matrix for four-vectors
    R3 = ob.Rz(theta)
    R = np.array([
            [1, 0,       0,       0      ],
            [0, R3[0,0], R3[0,1], R3[0,2]],
            [0, R3[1,0], R3[1,1], R3[1,2]],
            [0, R3[2,0], R3[2,1], R3[2,2]],
            ])
    return R

def beta2zeta(beta):
    # calculates rapidity given velocity ratio beta = v/c
    return np.arctanh(beta)

def v2zeta(v):
    # calculates rapidity given velocity magnitude
    return np.arctanh(v/c)

def uvec2zeta(u):
    # calculates rapidity given velocity 3-vector
    return np.arctanh(na.vecnorm(u)/c)

def uvec2zetavec(uvec):
    # calculates rapidity as a vector given velocity vector
    
    v = na.vecnorm(uvec) # velocity magnitude
    
    if v !=0: uhat = uvec/v # unit vector of velocity
    else: uhat = np.array([0, 0, 0]) # zero vector if zero magnitude
    
    zeta = v2zeta(v) # rapidity magnitude
    
    return zeta*uhat # velocity vector

def zeta2beta(zeta):
    # convert rapidity to velocity ratio (beta = v/c)
    return np.tanh(zeta)

def zeta2v(zeta):
    # convert rapidity to velocity
    return np.tanh(zeta)*c

def zetavec2uvec(zetavec):
    # convert rapidity vector to velocity vector
    
    zeta = na.vecnorm(zetavec) # rapidity magnitude
    
    if zeta !=0: zetahat = zetavec/zeta # unit vector of rapidity
    else: zetahat = np.array([0, 0, 0]) # zero vector if zero magnitude
    
    v = zeta2v(zeta) # velocity magnitude
    
    return v*zetahat # rapidity vector

def deltabeta(beta0, dbeta):
    # calculate relativistic velocity change
    # converts velocities to rapidities, since rapidities are additive in SR
    # inputs are velocity ratios (beta = v/c)
    # outputs final relativistic velocity
    
    # convert to rapidity
    zeta0 = beta2zeta(beta0)
    dzeta = beta2zeta(dbeta)
    
    # rapidities are additive
    zeta = zeta0 + dzeta
    
    # convert back to relative velocity
    return zeta2beta(zeta)

def deltavrel(v0, dv):
    # relativistic change in velocity magnitude
    # converts velocity to rapidity, since rapidity is additive
    return deltabeta(v0/c, dv/c)*c

def deltavrel3d(u0vec, duvec):
    # relativistic change in velocity 3-vector
    # converts velocity to rapidity, since rapidity is additive
    
    # calculate rapidity vectors from velocity vectors
    zeta0vec = uvec2zetavec(u0vec)
    dzetavec = uvec2zetavec(duvec)
    
    # add rapidity vectors elementwise
    zetavec = zeta0vec + dzetavec
    
    # convert rapidity back to velocity
    return zetavec2uvec(zetavec)
    
    
def zboost(zeta):
    # boost along z axis with rapidity zeta
    coshzeta = np.coshzeta
    sinhzeta = np.sinhzeta
    B = np.array([
            [coshzeta, 0, 0, sinhzeta],
            [0,        1, 0, 0       ],
            [0,        0, 1, 0       ],
            [sinhzeta, 0, 0, coshzeta]
            ])
    return B

def angmom(r, m, omega):
    # Angular momentum of a spherical particle
    # r = radius
    # m = mass
    # omega = angular velocity (rad/s)
    # J = I*omega, sphere I = r^2 * m
    return (r**2) * m * omega

#def Meq(Mirr, a):

#def spinparam(J, M):

def rschwarz(m):
    # Schwarzchild radius for body of mass m (kg)
    return 2*G*m / (c**2) # (m)

def rschwarzkm(m):
    # Schwarzchild radius for body of mass m (kg)
    return rschwarz(m) / const.kilo # (km)

def rschwarz_mu(mu):
    # Schwarzchild radius for body with gravitational parameter mu (km^3/s^2)
    return 2*mu*(const.kilo**3) / (c**2) # (m)

def rschwarzkm_mu(mu):
    # Schwarzchild radius for body with gravitational parameter mu (km^3/s^2)
    return rschwarz(mu) / const.kilo # (km)

def christoffelschwarz(rs, r, theta):
    '''
    Calculates the Christoffel symbols of the Schwarzchild metric
    Inputs:     rs    = Schwarzchild radius (m)
                r     = radial distance (m)
                theta = colatitude (rad)
    Outputs:    nonzero Christoffel symbols with indices [t, r, theta, phi]
    '''
    stheta = np.sin(theta)
    rmrs = r - rs
    rsmr = rs - r
    
    Gamma = {}
    
    Gamma['t,r,t']          = rs / (2*r*(rmrs))
    
    Gamma['r,t,t']          = rs*(rmrs) / (2*(r**3))
    Gamma['r,r,r']          = -Gamma['t,r,t']
    Gamma['r,theta,theta']  = rsmr
    Gamma['r,phi,phi']      = (rsmr) * (stheta**2)
    
    Gamma['theta,r,theta']  = 1/r
    Gamma['theta,phi,phi']  = -stheta * np.cos(theta)
    
    Gamma['phi,r,phi']      = Gamma['theta,r,theta']
    Gamma['phi,theta,phi']  = np.arctan(theta)
    
    return Gamma

def schwarz2iso(r, rs):
    # convert radius in schwarzchild coordinates to isotropic spherical coords
    # r = r1*(1 + G*m/(2*(c**2)*r1))
    #   = r1*(1 + s/4r1)
    # thus r1 = r - rs/4
    return r - rs/4

def schwarz2rect(r, theta, phi, rs):
    # convert schwarzchild spherical coordinates to isotropic rectangular
    r1 = schwarz2iso(r, rs)
    stheta = np.sin(theta)
    x = r1 * stheta * np.cos(phi)
    y = r1 * stheta * np.sin(phi)
    z = r1 * np.cos(theta)
    return x, y, z

## ----------------------------------------------------------------------------
## EQUATIONS OF MOTION
## ----------------------------------------------------------------------------

def SR2body(t, s, CB):
    '''
    2-body equation of motion modified by Special Relativity
    Relativistic momentum: p = gamma*m*v
    F = dp/dt = gamma*m*dv/dt = -gamma*G*M*m*rhat/r^2
    a = dv/dt = -gamma*mu*r/norm(r)^3
    
    inputs:  initial state   (s[rx,ry,rz,vx,vy,vz],  [km(x3),km/s(x3)])
             time, t         (t,  s)
             central body object with attribute mu (grav param, km^3/s^2)
    outputs: d/dt(state)     (s1[vx,vy,vz,ax,ay,az], [km/s(x3),km/s^2(x3)])
    '''
    
    r = s[:3]
    v = s[3:]
    gamma = gammauvec(v)
    
    a = -gamma*CB.mu*r / (na.vecnorm(r)**3)
    
    s1 = np.array([v[0], v[1], v[2], a[0], a[1], a[2]])
    return s1

def schwarzsphere(tau, s, CB):
    
    # unpack state
    t       = s[0] # coordinate time,               sec
    r       = s[1] # proper radial distance,        m
    theta   = s[2] # proper colatitude,             rad
    phi     = s[3] # proper longitude,              rad
    dt      = s[4] # Lorentz factor,                sec/sec
    dr      = s[5] # proper radial velocity,        m/s
    dtheta  = s[6] # proper colatitudinal velocity, rad/s
    dphi    = s[7] # proper longitudinal velocity,  rad/s
    
    # unpack central body characteristics
    rs = CB.rs     # Schwarzchild radius,           m
    
    # calculate Christoffel symbols
    Gamma = christoffelschwarz(rs, r, theta)
    
    # Geodesic equations
    ddt     =     -(Gamma['t,r,t'] * dr * dt)
    ddr     = -(   (Gamma['r,t,t'] * (dt**2))
                 + (Gamma['r,r,r'] * (dr**2))
                 + (Gamma['r,theta,theta'] * (dtheta**2))
                 + (Gamma['r,phi,phi'] * (dphi**2)))
    ddtheta = -(   (Gamma['theta,r,theta'] * dr * dtheta)
                 + (Gamma['theta,phi,phi'] * (dphi**2)))
    ddphi   = -(   (Gamma['phi,r,phi'] * dr * dphi)
                 + (Gamma['phi,theta,phi'] * dtheta * dphi))
    
    # repack state
    ds = np.array([dt,  dr,  dtheta,  dphi,
                   ddt, ddr, ddtheta, ddphi])
            
    return ds

'''
def schwarzrect(tau, s, mu):
'''
'''
Schwarzchild geodesic equations of motion

inputs:  initial state    s[t,x,y,z,vt,vx,vy,vz] (column vector)
         delta t (proper) (tau, s)
         grav. parameter  (mu, km^3/s^2)
outputs: d/dt(state)      s1[vt,vx,vy,vz,at,ax,ay,az] (column vector)
'''
'''
rs = 2*mu / ((c/const.kilo)**2) # Schwarzchild radius (km)

# unpack state
#t      = s[0]
r, theta, phi = ob.rect2sphere(s[1], s[2], s[3])
dt     = s[4]
vxyz   = s[4:7]
R      = ob.R_cart2sphere(theta, phi)
vrtp   = R @ vxyz
dr     = vrtp[0]
dtheta = vrtp[1]
dphi   = vrtp[2]

# define w(r) and v(r) for brevity
w = 1 - (rs/r)
v = 1/w
dw_dr = rs / (r**2)
dv_dr = -rs / ((r-rs)**2)
#dw_dtau = dw_dr * dr_dtau
#dv_dtau = dv_dr * dr_dtau

# Schwarzchild geodesics
at     = -v * dw_dr * dt *dr
ar     = (   (-(1/(2*v)) * dv_dr * (dr**2))
           + ((r/v) * (dtheta**2))
           + ((r*(np.sin(theta)**2)/v) * (dphi**2))
           - (((c**2)/(2*v)) * dw_dr * (dt**2))
          )
atheta = (   (-(2/r) * dtheta * dr)
           + (np.sin(theta) * np.cos(theta) * (dphi**2))
          )
aphi   = (   (-(2/r) * dphi * dr)
           - ((2/np.tan(theta)) * dphi * dtheta)
          )

# pack new state
axyz = R.T @ np.array([ar, atheta, aphi])
s1 = np.array([dt, vxyz[0], vxyz[1], vxyz[2], at, axyz[0], axyz[1], axyz[2]])
return s1

def schwarzsphere(tau, s, mu):
'''
'''
Schwarzchild geodesic equations of motion

inputs:  initial state    s[t,r,theta,phi,dt,dr,dtheta,dphi]
         proper time      (tau, s)
         grav. parameter  (mu, km^3/s^2)
outputs: d/dtau(state)    s1[dt,dr,dtheta,dphi,ddt,ddr,ddtheta,ddphi]
'''
'''
rs = 2*mu / ((c/const.kilo)**2) # Schwarzchild radius (km)

# unpack state
#t     = s[0] # unused
r      = s[1]
theta  = s[2]
#phi    = s[3] # unused
dt     = s[4]
dr     = s[5]
dtheta = s[6]
dphi   = s[7]

# define w(r) and v(r) for brevity
w = 1 - (rs/r)
v = 1/w
dw_dr = rs / (r**2)
dv_dr = -rs / ((r-rs)**2)
#dw_dtau = dw_dr * dr_dtau
#dv_dtau = dv_dr * dr_dtau

# Schwarzchild geodesics
ddt     = -v * dw_dr * dt * dr
ddr     = (   (-(1/(2*v)) * dv_dr * (dr**2))
            + ((r/v) * (dtheta**2))
            + ((r*(np.sin(theta)**2)/v) * (dphi**2))
            - (((c**2)/(2*v)) * dw_dr * (dt**2))
           )
ddtheta = (   (-(2/r) * dtheta * dr)
            + (np.sin(theta) * np.cos(theta) * (dphi**2))
           )
ddphi   = (   (-(2/r) * dphi * dr)
            - ((2/np.tan(theta)) * dphi * dtheta)
           )

# pack new state
s1 = np.array([dt, dr, dtheta, dphi, ddt, ddr, ddtheta, ddphi])
return s1
'''

## ----------------------------------------------------------------------------
## TEST
## ----------------------------------------------------------------------------

# test orbit
alt = 500 # altitude, km
rx0 = ob.Earth.r + alt # initial x position, km
ry0 = 0
rz0 = 0
vx0 = 0
vy0 = ob.circvel(rx0, ob.Earth.mu) # initial y velocity, km/s
vz0 = 0

# initial state
s0 = np.array([rx0, ry0, rz0, vx0, vy0, vz0])
dt = 10
#tspan = [0, 1*const.hour]
tspan = [0, 1*ob.a2P(rx0, ob.Earth.mu)]

# integrate
t, rv = na.ode(ob.twobodyRV, s0, tspan, dt, scheme = na.rk4.integrator, misc=ob.Earth)

# plot
#plt.close()
fig, ax = plt.subplots()
ax.plot(rv[:,0], rv[:,1], '.-')
ax.set_aspect('equal')

# test Schwarzchild geodesics
t0 = 0
r0 = rx0
theta0 = 0
phi0 = 0
vt0 = 1
vr0 = 0
vtheta0 = 0
vphi0 = (2*np.pi) / ob.a2P(r0, ob.Earth.mu) # 2 pi radians per orbital period

s0sphere = np.array([t0, r0, theta0, phi0, vt0, vr0, vtheta0, vphi0])
dtau = 10
tauspan = [0, 10*ob.a2P(r0, ob.Earth.mu)]

# integrate
tausphere, statesphere = na.ode(schwarzsphere, s0sphere, tauspan, dtau, misc=ob.Earth)
tcoord = statesphere[:,0]
rsphere = statesphere[:,1]
thetasphere = statesphere[:,2]
phisphere = statesphere[:,3]
rx, ry, rz = schwarz2rect(rsphere, thetasphere, phisphere, ob.Earth.rs)

# plot
polfig, polax = plt.subplots(subplot_kw={'projection': 'polar'})
polax.plot(statesphere[:,3], statesphere[:,1], '.-')
polax.set_title('Schwarzchild spherical coordinates')
rectfig, rectax = plt.subplots()
rectax.plot(rx, ry, '.-')
rectax.set_title('Isotropic rectangular coordinates')
plt.show()

'''
fig0, ax0 = plt.subplots()
ax0.plot(tausphere, statesphere[:,0], '.-')
ax0.set_title('t vs tau')
fig1, ax1 = plt.subplots()
ax1.plot(tausphere, statesphere[:,1], '.-')
ax1.set_title('r vs tau')
fig2, ax2 = plt.subplots()
ax2.plot(tausphere, statesphere[:,2], '.-')
ax2.set_title('theta vs tau')
fig3, ax3 = plt.subplots()
ax3.plot(tausphere, statesphere[:,3], '.-')
ax3.set_title('phi vs tau')
plt.show()
'''
