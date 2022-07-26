# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 13:18:29 2022

@author: Matthew

Conversion of Matlab routines by David Vallado to python
Implementation of some additional routines from Vallado 4ed
"""

import numpy as np

"""
-------------------------------------------------------------------------------
CONSTANTS
-------------------------------------------------------------------------------
"""

"""
% ------------------------------------------------------------------------------
%
%                           function constmath
%
%  this function sets constants for mathematical operations. 
%
%  author        : david vallado                  719-573-2600    2 apr 2007
%
%  revisions
%
%  inputs        : description                    range / units
%    none
%
%  outputs       :
%    rad, twopi, halfpi;
%    ft2m, mile2m, nm2m, mile2ft, mileph2kmph, nmph2kmph;
%
%  locals        :
%                -
%
%  coupling      :
%    none.
%
% constmath;
% ------------------------------------------------------------------------------
"""
small = 1.0e-10

infinite  = 999999.9
undefined = 999999.1

#% -------------------------  mathematical  --------------------
rad    = 180.0 / np.pi
twopi  = 2.0 * np.pi
halfpi = np.pi * 0.5

#% -------------------------  conversions  ---------------------
ft2m    =    0.3048
mile2m  = 1609.344
nm2m    = 1852
mile2ft = 5280
mileph2kmph = 0.44704
nmph2kmph   = 0.5144444

"""
% ------------------------------------------------------------------------------
%
%                           function constastro
%
%  this function sets constants for various astrodynamic operations. 
%
%  author        : david vallado                  719-573-2600    2 apr 2007
%
%  revisions
%
%  inputs        : description                    range / units
%    none
%
%  outputs       :
%    re, flat, omegaearth, mu;
%    eccearth, eccearthsqrd;
%    renm, reft, tusec, tumin, tuday, omegaearthradptu, omegaearthradpmin;
%    velkmps, velftps, velradpmin;
%    degpsec, radpday;
%    speedoflight, au, earth2moon, moonradius, sunradius;
%
%  locals        :
%                -
%
%  coupling      :
%    none.
%
% constastro;
% ------------------------------------------------------------------------------
"""

#% -----------------------  physical constants  ----------------
#% WGS-84/EGM-96 constants used here
re         = 6378.137         #% km
flat       = 1.0/298.257223563
omegaearth = 7.292115e-5     #% rad/s
mu         = 398600.4418      #% km3/s2
mum        = 3.986004418e14   #% m3/s2

#% derived constants from the base values
eccearth = np.sqrt(2.0*flat - flat**2)
eccearthsqrd = eccearth**2

renm = re / nm2m
reft = re * 1000.0 / ft2m

tusec = np.sqrt(re**3 / mu)
tumin = tusec / 60.0
tuday = tusec / 86400.0

omegaearthradptu  = omegaearth * tusec
omegaearthradpmin = omegaearth * 60.0

velkmps = np.sqrt(mu / re)
velftps = velkmps * 1000.0/ft2m
velradpmin = velkmps * 60.0/re
#%for afspc
#%velkmps1 = velradpmin*6378.135/60.0   7.90537051051763
#%mu1 = velkmps*velkmps*6378.135        3.986003602567418e+005        
degpsec = (180.0 / np.pi) / tusec
radpday = 2.0 * np.pi * 1.002737909350795

speedoflight = 2.99792458e8 #% m/s
au = 149597870.0      #% km
earth2moon = 384400.0 #% km
moonradius =   1738.0 #% km
sunradius  = 696000.0 #% km

masssun   = 1.9891e30
massearth = 5.9742e24
massmoon  = 7.3483e22

"""
-------------------------------------------------------------------------------
FUNCTIONS
-------------------------------------------------------------------------------
"""

def mag( vec ):
    """
    % ------------------------------------------------------------------------------
    %
    %                            function mag
    %
    %  this function finds the magnitude of a vector.  the tolerance is set to
    %    0.000001, thus the 1.0e-12 for the squared test of underflows.
    %
    %  author        : david vallado                  719-573-2600   30 may 2002
    %
    %  revisions
    %    vallado     - fix tolerance to match coe, eq, etc            3 sep 2002
    %
    %  inputs          description                    range / units
    %    vec         - vector
    %
    %  outputs       :
    %    mag         - magnitude
    %
    %  locals        :
    %    none.
    %
    %  coupling      :
    %    none.
    %
    % mag = ( vec );
    % ----------------------------------------------------------------------------- }
    
    function mag = mag ( vec );
    """
    vec = np.array(vec).reshape(3)
    
    temp= vec[0]*vec[0] + vec[1]*vec[1] + vec[2]*vec[2]

    if abs( temp ) >= 1.0e-16:
        mag= np.sqrt( temp )
    else:
        mag= 0.0
    
    return mag

def angl( vec1, vec2 ):
    """
    % ------------------------------------------------------------------------------
    %
    %                            function angl
    %
    %  this function calculates the angle between two vectors.  the output is
    %    set to 999999.1 to indicate an undefined value.  be sure to check for
    %    this at the output phase.
    %
    %  author        : david vallado                  719-573-2600   27 may 2002
    %
    %  revisions
    %    vallado     - fix tolerances                                 5 sep 2002
    %
    %  inputs          description                    range / units
    %    vec1        - vector number 1
    %    vec2        - vector number 2
    %
    %  outputs       :
    %    theta       - angle between the two vectors  -pi to pi
    %
    %  locals        :
    %    temp        - temporary real variable
    %
    %  coupling      :
    %
    % [theta] = angl ( vec1,vec2 );
    % ----------------------------------------------------------------------------- }
    
    function [theta] = angl ( vec1,vec2 );
    """
    vec1 = np.array(vec1).reshape(3)
    vec2 = np.array(vec2).reshape(3)
    
    small     = 0.00000001
    undefined = 999999.1
    
    magv1 = mag(vec1)
    magv2 = mag(vec2)
    
    if magv1*magv2 > small**2:
        temp= np.dot(vec1,vec2) / (magv1*magv2)
        if abs( temp ) > 1.0:
            temp= np.sign(temp) * 1.0
        theta= np.arccos( temp )
    else:
        theta= undefined
    
    return theta

def semidiam(r_obj, r_sat2obj):
    """
    Vallado eq 5-11
    The semi-diameter is half the angular extent of an object viewed from a
    single location.
    Typical values for the Sun are .2666 deg (16 arcmin),
    and for the Moon, .259 deg (15 arcmin 54 arcsec)
    
    Inputs:
        r_obj = radius of viewed object
        r_sat2obj = vector from viewing location to object
    Outputs:
        alpha = semi-diameter (radians)
    """
    return np.arctan2(r_obj, np.linalg.norm(r_sat2obj))

def jday(yr, mon, day, hr, minute, sec):
    """
    % -----------------------------------------------------------------------------
    %
    %                           function jday.m
    %
    %  this function finds the julian date given the year, month, day, and time.
    %
    %  author        : david vallado                  719-573-2600   27 may 2002
    %
    %  revisions
    %                -
    %
    %  inputs          description                    range / units
    %    year        - year                           1900 .. 2100
    %    mon         - month                          1 .. 12
    %    day         - day                            1 .. 28,29,30,31
    %    hr          - universal time hour            0 .. 23
    %    min         - universal time min             0 .. 59
    %    sec         - universal time sec             0.0 .. 59.999
    %    whichtype   - julian .or. gregorian calender   'j' .or. 'g'
    %
    %  outputs       :
    %    jd          - julian date                    days from 4713 bc
    %    jdfrac      - julian date fraction of a day   0.0 to 1.0
    % 
    %  locals        :
    %    none.
    %
    %  coupling      :
    %    none.
    %
    %  references    :
    %    vallado       2007, 189, alg 14, ex 3-14
    %
    % [jd, jdfrac] = jday(yr, mon, day, hr, min, sec)
    % -----------------------------------------------------------------------------
    
    function [jd, jdfrac] = jday(yr, mon, day, hr, min, sec)
    """

    #% ------------------------  implementation   ------------------
    jd = ( 367.0 * yr
           - np.floor( (7 * (yr + np.floor( (mon + 9) / 12.0) ) ) * 0.25 )
           + np.floor( 275 * mon / 9.0 )
           + day + 1721013.5 )   #% use - 678987.0 to go to mjd directly
    jdfrac = (sec + minute * 60.0 + hr *3600.0) / 86400.0
    
    #% check jdfrac
    if jdfrac > 1.0:
        jd = jd + np.floor(jdfrac)
        jdfrac = jdfrac - np.floor(jdfrac)
    
    #%  - 0.5 * sign(100.0 * yr + mon - 190002.5) + 0.5;
    
    return jd, jdfrac

def rot1( vec, xval ):
    """
    % ------------------------------------------------------------------------------
    %
    %                                  rot1
    %
    %  this function performs a rotation about the 1st axis.
    %
    %  author        : david vallado                  719-573-2600   27 may 2002
    %
    %  revisions
    %                -
    %
    %  inputs          description                    range / units
    %    vec         - input vector
    %    xval        - angle of rotation              rad
    %
    %  outputs       :
    %    outvec      - vector result
    %
    %  locals        :
    %    c           - cosine of the angle xval
    %    s           - sine of the angle xval
    %    temp        - temporary extended value
    %
    %  coupling      :
    %    none.
    %
    % [outvec] = rot1 ( vec, xval );
    % ----------------------------------------------------------------------------- }
    
    function [outvec] = rot1 ( vec, xval );
    """
    vec = np.array(vec).reshape(3)
    
    temp= vec[2]
    c= np.cos( xval )
    s= np.sin( xval )
    
    outvec = np.zeros(3) # column vector
    outvec[2]= c*vec[2] - s*vec[1]
    outvec[1]= c*vec[1] + s*temp
    outvec[0]= vec[0]
    
    return outvec

def rot2( vec, xval ):
    """
    % ------------------------------------------------------------------------------
    %
    %                            function rot2
    %
    %  this function performs a rotation about the 2nd axis.
    %
    %  author        : david vallado                  719-573-2600   27 may 2002
    %
    %  revisions
    %                -
    %
    %  inputs          description                    range / units
    %    vec         - input vector
    %    xval        - angle of rotation              rad
    %
    %  outputs       :
    %    outvec      - vector result
    %
    %  locals        :
    %    c           - cosine of the angle xval
    %    s           - sine of the angle xval
    %    temp        - temporary extended value
    %
    %  coupling      :
    %    none.
    %
    % [outvec] = rot2 ( vec, xval );
    % ----------------------------------------------------------------------------- }
    
    function [outvec] = rot2 ( vec, xval );
    """
    vec = np.array(vec).reshape(3)
    
    temp= vec[2]
    c= np.cos( xval )
    s= np.sin( xval )
    
    outvec = np.zeros(3) # column vector
    outvec[2]= c*vec[2] + s*vec[0]
    outvec[0]= c*vec[0] - s*temp
    outvec[1]= vec[1]
    
    return outvec

def rot3( vec, xval ):
    """
    % ------------------------------------------------------------------------------
    %
    %                            function rot3
    %
    %  this function performs a rotation about the 3rd axis.
    %
    %  author        : david vallado                  719-573-2600   27 may 2002
    %
    %  revisions
    %                -
    %
    %  inputs          description                    range / units
    %    vec         - input vector
    %    xval        - angle of rotation              rad
    %
    %  outputs       :
    %    outvec      - vector result
    %
    %  locals        :
    %    c           - cosine of the angle xval
    %    s           - sine of the angle xval
    %    temp        - temporary extended value
    %
    %  coupling      :
    %    none.
    %
    % [outvec] = rot3 ( vec, xval );
    % ----------------------------------------------------------------------------- }
    
    function [outvec] = rot3 ( vec, xval );
    """
    vec = np.array(vec).reshape(3)
    
    temp= vec[1]
    c= np.cos( xval )
    s= np.sin( xval )
    
    outvec = np.zeros(3) # column vector
    outvec[1]= c*vec[1] - s*vec[0]
    outvec[0]= c*vec[0] + s*temp
    outvec[2]= vec[2]
    
    return outvec

def rot1mat( xval ):
    """
    % ------------------------------------------------------------------------------
    %
    %                                  rot1mat
    %
    %  this function sets up a rotation matrix for an input angle about the first
    %    axis.
    %
    %  author        : david vallado                  719-573-2600   10 jan 2003
    %
    %  revisions
    %                -
    %
    %  inputs          description                    range / units
    %    xval        - angle of rotation              rad
    %
    %  outputs       :
    %    outmat      - matrix result
    %
    %  locals        :
    %    c           - cosine of the angle xval
    %    s           - sine of the angle xval
    %
    %  coupling      :
    %    none.
    %
    % [outmat] = rot1mat ( xval );
    % ----------------------------------------------------------------------------- }
    
    function [outmat] = rot1mat ( xval );
    """
    c= np.cos( xval )
    s= np.sin( xval )
    
    outmat = np.zeros((3,3)) # 3x3 matrix
    outmat[0,0]= 1.0
    outmat[0,1]= 0.0
    outmat[0,2]= 0.0
    
    outmat[1,0]= 0.0
    outmat[1,1]= c
    outmat[1,2]= s
    
    outmat[2,0]= 0.0
    outmat[2,1]= -s
    outmat[2,2]= c
    
    return outmat

def rot2mat( xval ):
    """
    % ------------------------------------------------------------------------------
    %
    %                                  rot2mat
    %
    %  this function sets up a rotation matrix for an input angle about the second
    %    axis.
    %
    %  author        : david vallado                  719-573-2600   10 jan 2003
    %
    %  revisions
    %                -
    %
    %  inputs          description                    range / units
    %    xval        - angle of rotation              rad
    %
    %  outputs       :
    %    outmat      - matrix result
    %
    %  locals        :
    %    c           - cosine of the angle xval
    %    s           - sine of the angle xval
    %
    %  coupling      :
    %    none.
    %
    % [outmat] = rot2mat ( xval );
    % ----------------------------------------------------------------------------- }
    
    function [outmat] = rot2mat ( xval );
    """
    c= np.cos( xval )
    s= np.sin( xval )
    
    outmat = np.zeros((3,3)) # 3x3 matrix
    outmat[0,0]= c
    outmat[0,1]= 0.0
    outmat[0,2]= -s
    
    outmat[1,0]= 0.0
    outmat[1,1]= 1.0
    outmat[1,2]= 0.0
    
    outmat[2,0]= s
    outmat[2,1]= 0.0
    outmat[2,2]= c
    
    return outmat

def rot3mat( xval ):
    """
    % ------------------------------------------------------------------------------
    %
    %                                  rot3mat
    %
    %  this function sets up a rotation matrix for an input angle about the third
    %    axis.
    %
    %  author        : david vallado                  719-573-2600   10 jan 2003
    %
    %  revisions
    %                -
    %
    %  inputs          description                    range / units
    %    xval        - angle of rotation              rad
    %
    %  outputs       :
    %    outmat      - matrix result
    %
    %  locals        :
    %    c           - cosine of the angle xval
    %    s           - sine of the angle xval
    %
    %  coupling      :
    %    none.
    %
    % [outmat] = rot3mat ( xval );
    % ----------------------------------------------------------------------------- }
    
    function [outmat] = rot3mat ( xval );
    """
    c= np.cos( xval )
    s= np.sin( xval )
    
    outmat = np.zeros((3,3)) # 3x3 matrix
    outmat[0,0]= c
    outmat[0,1]= s
    outmat[0,2]= 0.0
    
    outmat[1,0]= -s
    outmat[1,1]= c
    outmat[1,2]= 0.0
    
    outmat[2,0]= 0.0
    outmat[2,1]= 0.0
    outmat[2,2]= 1.0
    
    return outmat

def newtonnu( ecc,nu ):
    """
    % ------------------------------------------------------------------------------
    %
    %                           function newtonnu
    %
    %  this function solves keplers equation when the true anomaly is known.
    %    the mean and eccentric, parabolic, or hyperbolic anomaly is also found.
    %    the parabolic limit at 168 is arbitrary. the hyperbolic anomaly is also
    %    limited. the hyperbolic sine is used because it's not double valued.
    %
    %  author        : david vallado                  719-573-2600   27 may 2002
    %
    %  revisions
    %    vallado     - fix small                                     24 sep 2002
    %
    %  inputs          description                    range / units
    %    ecc         - eccentricity                   0.0  to
    %    nu          - true anomaly                   -2pi to 2pi rad
    %
    %  outputs       :
    %    e0          - eccentric anomaly              0.0  to 2pi rad       153.02 deg
    %    m           - mean anomaly                   0.0  to 2pi rad       151.7425 deg
    %
    %  locals        :
    %    e1          - eccentric anomaly, next value  rad
    %    sine        - sine of e
    %    cose        - cosine of e
    %    ktr         - index
    %
    %  coupling      :
    %    arcsinh     - arc hyperbolic sine
    %    sinh        - hyperbolic sine
    %
    %  references    :
    %    vallado       2007, 85, alg 5
    %
    % [e0,m] = newtonnu ( ecc,nu );
    % ------------------------------------------------------------------------------
    
    function [e0,m] = newtonnu ( ecc,nu );
    """
    #% ---------------------  implementation   ---------------------
    e0= 999999.9
    m = 999999.9
    small = 0.00000001
    
    #% --------------------------- circular ------------------------
    if ( abs( ecc ) < small  ):
        m = nu
        e0= nu
    else:
        #% ---------------------- elliptical -----------------------
        if ( ecc < 1.0-small  ):
            sine= (np.sqrt( 1.0 -ecc*ecc ) * np.sin(nu)) / (1.0 +ecc*np.cos(nu))
            cose= ( ecc + np.cos(nu) ) / ( 1.0  + ecc*np.cos(nu) )
            e0  = np.arctan2( sine,cose )
            m   = e0 - ecc*np.sin(e0)
        else:
            #% -------------------- hyperbolic  --------------------
            if ( ecc > 1.0 + small  ):
                if (ecc > 1.0 ) & (abs(nu)+0.00001 < np.pi-np.arccos(1.0 /ecc)):
                    sine= (np.sqrt(ecc*ecc-1.0) * np.sin(nu)) / (1.0 + ecc*np.cos(nu))
                    e0  = np.arcsinh( sine )
                    m   = ecc*np.sinh(e0) - e0
            else:
                #% ----------------- parabolic ---------------------
                if ( abs(nu) < 168.0*np.pi/180.0  ):
                    e0= np.tan( nu*0.5  )
                    m = e0 + (e0*e0*e0)/3.0

    if ( ecc < 1.0  ):
        m = np.mod( m,2.0 *np.pi )
        if ( m < 0.0  ):
            m= m + 2.0 *np.pi
        e0 = np.mod( e0,2.0 *np.pi )

    return e0, m

def rv2coe(r,v, muin=mu):
    """
    %

    % ------------------------------------------------------------------------------
    %
    %                           function rv2coe
    %
    %  this function finds the classical orbital elements given the geocentric
    %    equatorial position and velocity vectors.
    %
    %  author        : david vallado                  719-573-2600   21 jun 2002
    %
    %  revisions
    %    vallado     - fix special cases                              5 sep 2002
    %    vallado     - delete extra check in inclination code        16 oct 2002
    %    vallado     - add constant file use                         29 jun 2003
    %    vallado     - add mu                                         2 apr 2007
    %
    %  inputs          description                    range / units
    %    r           - ijk position vector            km
    %    v           - ijk velocity vector            km / s
    %    mu          - gravitational parameter        km3 / s2
    %
    %  outputs       :
    %    p           - semilatus rectum               km
    %    a           - semimajor axis                 km
    %    ecc         - eccentricity
    %    incl        - inclination                    0.0  to pi rad
    %    omega       - longitude of ascending node    0.0  to 2pi rad
    %    argp        - argument of perigee            0.0  to 2pi rad
    %    nu          - true anomaly                   0.0  to 2pi rad
    %    m           - mean anomaly                   0.0  to 2pi rad
    %    arglat      - argument of latitude      (ci) 0.0  to 2pi rad
    %    truelon     - true longitude            (ce) 0.0  to 2pi rad
    %    lonper      - longitude of periapsis    (ee) 0.0  to 2pi rad
    %
    %  locals        :
    %    hbar        - angular momentum h vector      km2 / s
    %    ebar        - eccentricity     e vector
    %    nbar        - line of nodes    n vector
    %    c1          - v**2 - u/r
    %    rdotv       - r dot v
    %    hk          - hk unit vector
    %    sme         - specfic mechanical energy      km2 / s2
    %    i           - index
    %    e           - eccentric, parabolic,
    %                  hyperbolic anomaly             rad
    %    temp        - temporary variable
    %    typeorbit   - type of orbit                  ee, ei, ce, ci
    %
    %  coupling      :
    %    mag         - magnitude of a vector
    %    angl        - find the angl between two vectors
    %    newtonnu    - find the mean anomaly
    %
    %  references    :
    %    vallado       2007, 121, alg 9, ex 2-5
    %
    % [p,a,ecc,incl,omega,argp,nu,m,arglat,truelon,lonper ] = rv2coe (r,v);
    % ------------------------------------------------------------------------------
    
    function [p,a,ecc,incl,omega,argp,nu,m,arglat,truelon,lonper ] = rv2coe (r,v);
    """
    r = np.array(r).reshape(3)
    v = np.array(v).reshape(3)
    
    #constmath;
    #constastro;  % don't overwrite mu
    #muin = mu; % this is the km version
    #% -------------------------  implementation   -----------------
    magr = mag( r )
    magv = mag( v )
    #% ------------------  find h n and e vectors   ----------------
    hbar = np.cross( r,v )
    magh = mag( hbar )
    if ( magh > small ):
        nbar = np.zeros(3) # column vector
        nbar[0]= -hbar[1]
        nbar[1]=  hbar[0]
        nbar[2]=   0.0
        magn = mag( nbar )
        c1 = magv*magv - muin /magr
        rdotv= np.dot( r,v )
        ebar = np.zeros(3) # column vector
        for i in np.arange(0, 3): # i= 1 : 3
            ebar[i]= (c1*r[i] - rdotv*v[i])/muin
        ecc = mag( ebar )
        
        #% ------------  find a e and semi-latus rectum   ----------
        sme= ( magv*magv*0.5  ) - ( muin /magr )
        if ( abs( sme ) > small ):
            a= -muin  / (2.0 *sme)
        else:
            a= infinite
        p = magh*magh/muin
        
        #% -----------------  find inclination   -------------------
        hk= hbar[2]/magh
        incl= np.arccos( hk )
        
        #% --------  determine type of orbit for later use  --------
        #% ------ elliptical, parabolic, hyperbolic inclined -------
        typeorbit= 'ei'
        if ( ecc < small ):
            #% ----------------  circular equatorial ---------------
            if  (incl<small) | (abs(incl-np.pi)<small):
                typeorbit= 'ce'
            else:
                #% --------------  circular inclined ---------------
                typeorbit= 'ci'
        else:
            #% - elliptical, parabolic, hyperbolic equatorial --
            if  (incl<small) | (abs(incl-np.pi)<small):
                typeorbit= 'ee'
        
        #% ----------  find longitude of ascending node ------------
        if ( magn > small ):
            temp= nbar[0] / magn
            if ( abs(temp) > 1.0  ):
                temp= np.sign(temp)
            omega= np.arccos( temp )
            if ( nbar[1] < 0.0  ):
                omega= twopi - omega
        else:
            omega= undefined
        
        #% ---------------- find argument of perigee ---------------
        if (typeorbit == 'ei'):
            argp = angl( nbar,ebar)
            if ( ebar[2] < 0.0  ):
                argp= twopi - argp
        else:
            argp= undefined
        
        #% ------------  find true anomaly at epoch    -------------
        if ( typeorbit[0] == 'e' ):
            nu =  angl( ebar,r)
            if ( rdotv < 0.0  ):
                nu= twopi - nu
        else:
            nu= undefined
        
        #% ----  find argument of latitude - circular inclined -----
        if (typeorbit == 'ci'):
            arglat = angl( nbar,r )
            if ( r[2] < 0.0  ):
                arglat= twopi - arglat
            m = arglat
        else:
            arglat= undefined
        
        #% -- find longitude of perigee - elliptical equatorial ----
        if  ( ecc>small ) & (typeorbit == 'ee'):
            temp= ebar[0]/ecc
            if ( abs(temp) > 1.0  ):
                temp= np.sign(temp)
            lonper= np.arccos( temp )
            if ( ebar[1] < 0.0  ):
                lonper= twopi - lonper
            if ( incl > halfpi ):
                lonper= twopi - lonper
        else:
            lonper= undefined
        
        #% -------- find true longitude - circular equatorial ------
        if  ( magr>small ) & (typeorbit == 'ce'):
            temp= r[0]/magr
            if ( abs(temp) > 1.0  ):
                temp= np.sign(temp)
            truelon= np.arccos( temp )
            if ( r[1] < 0.0  ):
                truelon= twopi - truelon
            if ( incl > halfpi ):
                truelon= twopi - truelon
            m = truelon
        else:
            truelon= undefined
        
        #% ------------ find mean anomaly for all orbits -----------
        if ( typeorbit[0] == 'e' ):
            e, m = newtonnu(ecc,nu )

    else:
        p    = undefined
        a    = undefined
        ecc  = undefined
        incl = undefined
        omega= undefined
        argp = undefined
        nu   = undefined
        m    = undefined
        arglat = undefined
        truelon= undefined
        lonper = undefined

    return p, a, ecc, incl, omega, argp, nu, m, arglat, truelon, lonper

def coe2rv( p,ecc,incl,omega,argp,nu,arglat,truelon,lonper ):
    """
    %

    % ------------------------------------------------------------------------------
    %
    %                           function coe2rv
    %
    %  this function finds the position and velocity vectors in geocentric
    %    equatorial (ijk) system given the classical orbit elements.
    %
    %  author        : david vallado                  719-573-2600    9 jun 2002
    %
    %  revisions
    %    vallado     - add constant file use                         29 jun 2003
    %
    %  inputs          description                    range / units
    %    p           - semilatus rectum               km
    %    ecc         - eccentricity
    %    incl        - inclination                    0.0  to pi rad
    %    omega       - longitude of ascending node    0.0  to 2pi rad
    %    argp        - argument of perigee            0.0  to 2pi rad
    %    nu          - true anomaly                   0.0  to 2pi rad
    %    arglat      - argument of latitude      (ci) 0.0  to 2pi rad
    %    truelon     - true longitude            (ce) 0.0  to 2pi rad
    %    lonper      - longitude of periapsis    (ee) 0.0  to 2pi rad
    %
    %  outputs       :
    %    r           - ijk position vector            km
    %    v           - ijk velocity vector            km / s
    %
    %  locals        :
    %    temp        - temporary real*8 value
    %    rpqw        - pqw position vector            km
    %    vpqw        - pqw velocity vector            km / s
    %    sinnu       - sine of nu
    %    cosnu       - cosine of nu
    %    tempvec     - pqw velocity vector
    %
    %  coupling      :
    %    mag         - magnitude of a vector
    %    rot3        - rotation about the 3rd axis
    %    rot1        - rotation about the 1st axis
    %
    %  references    :
    %    vallado       2007, 126, alg 10, ex 2-5
    %
    % [r,v] = coe2rv ( p,ecc,incl,omega,argp,nu,arglat,truelon,lonper );
    % ------------------------------------------------------------------------------
    
    function [r,v] = coe2rv ( p,ecc,incl,omega,argp,nu,arglat,truelon,lonper );
    """
    #% -------------------------  implementation   -----------------
    #constmath;
    #constastro;

    #% -------------------------------------------------------------
    #%       determine what type of orbit is involved and set up the
    #%       set up angles for the special cases.
    #% -------------------------------------------------------------
    if ( ecc < small ):
        #% ----------------  circular equatorial  ------------------
        if (incl<small) | ( abs(incl-np.pi)< small ):
            argp = 0.0
            omega= 0.0
            nu   = truelon
        else:
            #% --------------  circular inclined  ------------------
            argp= 0.0
            nu  = arglat
    else:
        #% ---------------  elliptical equatorial  -----------------
        if ( ( incl<small) | (abs(incl-np.pi)<small) ):
            argp = lonper
            omega= 0.0

    #% ----------  form pqw position and velocity vectors ----------
    cosnu= np.cos(nu)
    sinnu= np.sin(nu)
    temp = p / (1.0  + ecc*cosnu)
    rpqw = np.zeros(3) # column vector
    rpqw[0]= temp*cosnu
    rpqw[1]= temp*sinnu
    rpqw[2]=     0.0
    if ( abs(p) < 0.0001):
        p= 0.0001
    vpqw = np.zeros(3)
    vpqw[0]=    -sinnu*np.sqrt(mu)  / np.sqrt(p)
    vpqw[1]=  (ecc + cosnu)*np.sqrt(mu) / np.sqrt(p)
    vpqw[2]=      0.0

    #% ----------------  perform transformation to ijk  ------------
    tempvec = rot3( rpqw   , -argp )
    tempvec = rot1( tempvec, -incl )
    r = rot3( tempvec, -omega )

    tempvec =rot3( vpqw   , -argp )
    tempvec =rot1( tempvec, -incl )
    v = rot3( tempvec, -omega )

    #r=r'; np array is 1d
    #v=v'; np array is 1d
    
    return r, v

def azl2radc(az, el, lat, lst, alt=False):
    """
    % azl2radc
    %
    % this function finds the rtasc decl values given the az-el
    %
    %
    %
    function [rtasc,decl] = azl2radc(az, el, lat, lst);
    
    'alt' flag added to toggle between approaches
    """
    rad = 180.0 / np.pi

    decl = (np.arcsin( np.sin(el)*np.sin(lat)
            + np.cos(el)*np.cos(lat)*np.cos(az) ))

    slha1 = -(np.sin(az)*np.cos(el)*np.cos(lat)) / (np.cos(decl)*np.cos(lat))
    clha1 = (np.sin(el) - np.sin(lat)*np.sin(decl)) / (np.cos(decl)*np.cos(lat))

    lha1 = np.arctan2(slha1, clha1)
    #%    fprintf(1,' lha1 %13.7f \n',lha1*rad);

    #% alt approach
    slha2 = -( np.sin(az)*np.cos(el) ) / ( np.cos(decl) )
    clha2 = (np.cos(lat)*np.sin(el) - np.sin(lat)*np.cos(el)*np.cos(az)) / np.cos(decl)

    lha2 = np.arctan2(slha2,clha2)
    #%    fprintf(1,' lha2 %13.7f \n',lha2*rad);
    
    if alt:
        rtasc = lst - lha2
    else:
        rtasc = lst - lha1
    
    return rtasc, decl

def sun( jd, radec=False ):
    """
    %

    % ------------------------------------------------------------------------------
    %
    %                           function sun
    %
    %  this function calculates the geocentric equatorial position vector
    %    the sun given the julian date.  this is the low precision formula and
    %    is valid for years from 1950 to 2050.  accuaracy of apparent coordinates
    %    is 0.01  degrees.  notice many of the calculations are performed in
    %    degrees, and are not changed until later.  this is due to the fact that
    %    the almanac uses degrees exclusively in their formulations.
    %
    %  author        : david vallado                  719-573-2600   27 may 2002
    %
    %  revisions
    %    vallado     - fix mean lon of sun                            7 mat 2004
    %
    %  inputs          description                    range / units
    %    jd          - julian date                    days from 4713 bc
    %
    %  outputs       :
    %    rsun        - ijk position vector of the sun au
    %    rtasc       - right ascension                rad
    %    decl        - declination                    rad
    %
    %  locals        :
    %    meanlong    - mean longitude
    %    meananomaly - mean anomaly
    %    eclplong    - ecliptic longitude
    %    obliquity   - mean obliquity of the ecliptic
    %    tut1        - julian centuries of ut1 from
    %                  jan 1, 2000 12h
    %    ttdb        - julian centuries of tdb from
    %                  jan 1, 2000 12h
    %    hr          - hours                          0 .. 24              10
    %    min         - minutes                        0 .. 59              15
    %    sec         - seconds                        0.0  .. 59.99          30.00
    %    temp        - temporary variable
    %    deg         - degrees
    %
    %  coupling      :
    %    none.
    %
    %  references    :
    %    vallado       2007, 281, alg 29, ex 5-1
    %
    % [rsun,rtasc,decl] = sun ( jd );
    % ------------------------------------------------------------------------------
    
    function [rsun,rtasc,decl] = sun ( jd );
    
    added 'radec' flag to optionally output right ascension and declination
    """
    twopi      =     2.0*np.pi
    deg2rad    =     np.pi/180.0
    show = 'n'
    
    #% -------------------------  implementation   -----------------
    #% -------------------  initialize values   --------------------
    tut1= ( jd - 2451545.0  )/ 36525.0

    if show == 'y':
        #fprintf(1,'tut1 %14.9f \n',tut1);
        pass

    meanlong= 280.460  + 36000.77*tut1
    meanlong= np.mod( meanlong,360.0  )  #%deg

    ttdb= tut1
    meananomaly= 357.5277233  + 35999.05034 *ttdb
    meananomaly= np.mod( meananomaly*deg2rad,twopi )  #%rad
    if ( meananomaly < 0.0  ):
        meananomaly= twopi + meananomaly

    eclplong= ( meanlong + 1.914666471 *np.sin(meananomaly)
                + 0.019994643 *np.sin(2.0 *meananomaly) ) #%deg
    eclplong= np.mod( eclplong,360.0  )  #%deg

    obliquity= 23.439291  - 0.0130042 *ttdb  #%deg

    eclplong = eclplong *deg2rad
    obliquity= obliquity *deg2rad

    #% --------- find magnitude of sun vector, )   components ------
    magr= ( 1.000140612  - 0.016708617 *np.cos( meananomaly )
                          - 0.000139589 *np.cos( 2.0 *meananomaly ) )   #% in au's

    rsun = np.zeros(3) # column vector
    rsun[0]= magr*np.cos( eclplong )
    rsun[1]= magr*np.cos(obliquity)*np.sin(eclplong)
    rsun[2]= magr*np.sin(obliquity)*np.sin(eclplong)

    if show == 'y':
        """
        fprintf(1,'meanlon %11.6f meanan %11.6f eclplon %11.6f obli %11.6f \n', ...
                meanlong,meananomaly/deg2rad,eclplong/deg2rad,obliquity/deg2rad);
        fprintf(1,'rs %11.9f %11.9f %11.9f \n',rsun);
        fprintf(1,'magr %14.7f \n',magr);
        """

    rtasc= np.arctan2( np.cos(obliquity)*np.tan(eclplong) )

    #% --- check that rtasc is in the same quadrant as eclplong ----
    if ( eclplong < 0.0  ):
        eclplong= eclplong + twopi    #% make sure it's in 0 to 2pi range
    
    if ( abs( eclplong-rtasc ) > np.pi*0.5  ):
        rtasc= rtasc + 0.5 *np.pi*round( (eclplong-rtasc)/(0.5 *np.pi))
    
    decl = np.arcsin( np.sin(obliquity)*np.sin(eclplong) )
    
    if radec:
        return rsun, rtasc, decl
    else:
        return rsun



"""
-------------------------------------------------------------------------------
EXAMPLES
-------------------------------------------------------------------------------
"""

def ex2_5():
    r_IJK = np.array([6524.834, 6862.875, 6448.296]) # position, ECI, km
    v_IJK = np.array([4.901327, 5.533756, -1.976341]) # velocity, ECI, km/s
    p, a, ecc, incl, omega, argp, nu, m, arglat, truelon, lonper = rv2coe(r_IJK, v_IJK)
    print('r_ECI = ', r_IJK, ' km')
    print('v_ECI = ', v_IJK, ' km/s')
    print('semiparameter        p       = ', p, ' km (correct = 11,067.79 km)')
    print('semimajor axis       a       = ', a, ' km (correct = 36127.343 km)')
    print('eccentricity         ecc     = ', ecc, ' (correct = 0.832853)')
    print('inclination          incl    = ', incl, ' deg (correct = 87.87 deg)')
    print('right ascension      omega   = ', omega, ' deg (correct = 227.898 deg)')
    print('argument of perigee  argp    = ', argp, ' deg (correct = 53.38 deg)')
    print('true anomaly         nu      = ', nu, ' deg (correct = 92.335 deg)')
    print('                     m       = ', m)
    print('argument of latitude arglat  = ', arglat, ' deg (correct = 145.60549 deg)')
    print('true longitude       truelon = ', truelon, ' deg (correct = 55.282587 deg)')
    print('longitude of perigee lonper  = ', lonper, 'deg (correct = 281.27 deg)')
    
    return p, a, ecc, incl, omega, argp, nu, m, arglat, truelon, lonper

def ex2_6():
    p, a, ecc, incl, omega, argp, nu, m, arglat, truelon, lonper = ex2_5()
    r_new, v_new = coe2rv(p, ecc, incl, omega, argp, nu, arglat, truelon, lonper)
    print('Try to get the same r_ECI, v_ECI back with coe2rv:')
    print('r_new = ', r_new, ' km')
    print('v_new = ', v_new, ' km/s')
    
def ex5_1():
    """
    %     -----------------------------------------------------------------
    %
    %                              Ex5_1.m
    %
    %  this file demonstrates example 5-1.
    %
    %                          companion code for
    %             fundamentals of astrodynamics and applications
    %                                 2007
    %                            by david vallado
    %
    %     (w) 719-573-2600, email dvallado@agi.com
    %
    %     *****************************************************************
    %
    %  current :
    %             7 jun 07  david vallado
    %                         original
    %  changes :
    %            13 feb 07  david vallado
    %                         original baseline
    %
    %     *****************************************************************
    """
    conv = np.pi / (180*3600)
    timezone = 0
    """
    year = 2006  #% need UTC that will give TDT on the 2 Apr 0 hr
    mon = 4
    day = 1
    hr = 23
    minute = 58
    second = 54.816
    [jd, jdfrac] = jday(year, mon, day, hr, minute, second);
    fprintf(1,'jd  %11.9f \n',jd+jdfrac );
    dat = 33;
    xp = 0.103267 * conv;
    yp = 0.373786 * conv;
    dut1 = 0.2653628;
    lod = 0.0009307;
    ddpsi = -0.55418 * conv;
    ddeps = -0.005137 * conv;

    [ut1, tut1, jdut1,jdut1frac, utc, tai, tt, ttt, jdtt,jdttfrac, tdb, ttdb, jdtdb,jdtdbfrac ] ...
         = convtime ( year, mon, day, hr, minute, second, timezone, dut1, dat );
    fprintf(1,'input data \n\n');
    fprintf(1,' year %5i ',year);
    fprintf(1,' mon %4i ',mon);
    fprintf(1,' day %3i ',day);
    fprintf(1,' %3i:%2i:%8.6f\n ',hr,minute,second );
    fprintf(1,' dut1 %8.6f s',dut1);
    fprintf(1,' dat %3i s',dat);
    fprintf(1,' xp %8.6f "',xp / conv);
    fprintf(1,' yp %8.6f "',yp / conv);
    fprintf(1,' lod %8.6f s\n',lod);
    fprintf(1,' ddpsi %8.6f " ddeps  %8.6f\n',ddpsi/conv, ddeps/conv);

    fprintf(1,'tt  %8.6f ttt  %16.12f jdtt  %18.11f ',tt,ttt,jdtt );
    [h,m,s] = sec2hms( tt );
    fprintf(1,'hms %3i %3i %8.6f \n',h,m,s);
   
    [rsun,rtasc,decl] = sun ( jd );
    fprintf(1,'sun  rtasc %14.6f deg decl %14.6f deg\n',rtasc*rad,decl*rad );
    fprintf(1,'sun newTOD %11.9f%11.9f%11.9f au\n',rsun );
    fprintf(1,'sun newTOD %14.4f%14.4f%14.4f km\n',rsun*149597870.0 );

    rsunaa = [0.9775113 0.1911521  0.0828717]*149597870.0; % astronomical alm value into km
    fprintf(1,'rs almanac ICRF %11.9f %11.9f %11.9f km \n',rsunaa);

    %ttt= ( jd - 2451545.0  )/ 36525.0;
    vmod = [0 0 0]';
    amod = [0 0 0]';
    [reci,veci,aeci] = mod2eci  ( rsun',vmod,amod,ttt );
    fprintf(1,'mod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',reci*149597870.0, mag(reci)*149597870.0 );
    db = reci*149597870.0-rsunaa';
    fprintf(1,'delta mod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',db, mag(db) );

    [reci,veci,aeci] = tod2eci  ( rsun',vmod,amod,ttt, ddpsi, ddeps );
    fprintf(1,'tod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',reci*149597870.0, mag(reci)*149597870.0 );
    db = reci*149597870.0-rsunaa';
    fprintf(1,'delta tod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',db, mag(db) );

    #%         [reci,veci,aeci] = eci2mod ( rsun',vmod,amod,ttt );
    #%         fprintf(1,'eci - mod  %11.9f %11.9f %11.9f %11.4f km  \n',reci*149597870.0, mag(reci)*149597870.0 );
    #%         db = reci*149597870.0-rsunaa';
    #%         fprintf(1,'delta eci - mod  %11.9f %11.9f %11.9f %11.4f km  \n',db, mag(db) );
    #% 
    #%         [reci,veci,aeci] = eci2tod ( rsun',vmod,amod,ttt, ddpsi, ddeps );
    #%         fprintf(1,'eci - tod  %11.9f %11.9f %11.9f %11.4f km  \n',reci*149597870.0, mag(reci)*149597870.0 );
    #%         db = reci*149597870.0-rsunaa';
    #%         fprintf(1,'delta eci - tod  %11.9f %11.9f %11.9f %11.4f km  \n',db, mag(db) );
    
    [hms] = hms2rad( 0,44,33.42 );
    [dms] = dms2rad( 4,47,18.3 );
    fprintf(1,'hms ast alm rtasc %11.9f decl %11.9f \n',hms*rad,dms*rad );


    % now try alamnac method
    [rsuna,rtasca,decla] = sunalmanac ( jd );
    fprintf(1,'\n\nsun  rtasc %14.6f deg decl %14.6f deg\n',rtasca*rad, decla*rad );
    fprintf(1,'sun ALM %11.9f%11.9f%11.9f au\n',rsuna );
    fprintf(1,'sun ALM %14.4f%14.4f%14.4f km\n',rsuna*149597870.0 );

    fprintf(1,'rs aa ICRF %11.9f %11.9f %11.9f km \n',rsunaa);

    %ttt= ( jd - 2451545.0  )/ 36525.0;
    vmod = [0 0 0]';
    amod = [0 0 0]';
    [reci,veci,aeci] = mod2eci  ( rsuna',vmod,amod,ttt );
    fprintf(1,'mod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',reci*149597870.0, mag(reci)*149597870.0 );
    db = reci*149597870.0-rsunaa';
    fprintf(1,'delta mod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',db, mag(db) );

    [reci,veci,aeci] = tod2eci  ( rsuna',vmod,amod,ttt, ddpsi, ddeps );
    fprintf(1,'tod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',reci*149597870.0, mag(reci)*149597870.0 );
    db = reci*149597870.0-rsunaa';
    fprintf(1,'delta tod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',db, mag(db) );

    #%         [reci,veci,aeci] = eci2mod ( rsuna',vmod,amod,ttt );
    #%         fprintf(1,'eci - mod  %11.9f %11.9f %11.9f %11.4f km  \n',reci*149597870.0, mag(reci)*149597870.0 );
    #%         db = reci*149597870.0-rsunaa';
    #%         fprintf(1,'delta eci - mod  %11.9f %11.9f %11.9f %11.4f km  \n',db, mag(db) );
    #% 
    #%         [reci,veci,aeci] = eci2tod ( rsuna',vmod,amod,ttt, ddpsi, ddeps );
    #%         fprintf(1,'eci - tod  %11.9f %11.9f %11.9f %11.4f km  \n',reci*149597870.0, mag(reci)*149597870.0 );
    #%         db = reci*149597870.0-rsunaa';
    #%         fprintf(1,'delta eci - tod  %11.9f %11.9f %11.9f %11.4f km  \n',db, mag(db) );

    [hms] = hms2rad( 0,44,33.42 );
    [dms] = dms2rad( 4,47,18.3 );
    fprintf(1,'hms ast alm rtasc %11.9f decl %11.9f \n',hms*rad,dms*rad );

    fprintf(1,'==============================================================\n');
    % previous edition example
    year = 1994;
    mon = 4;
    day = 1;
    hr = 23;
    minute = 58;
    second = 59.816;
    [jd,jdfrac] = jday(year, mon, day, hr, minute, second);
    fprintf(1,'jd  %11.9f \n',jd+jdfrac );
    dat = 28;
    xp = 0.174467 * conv;
    yp = 0.389967 * conv;
    dut1 = -0.0226192;
    lod = 0.0023867;
    ddpsi = -0.016790 * conv;
    ddeps = -0.007353 * conv;
    [ut1, tut1, jdut1,jdut1frac, utc, tai, tt, ttt, jdtt,jdttfrac, tdb, ttdb, jdtdb,jdtdbfrac ] ...
         = convtime ( year, mon, day, hr, minute, second, timezone, dut1, dat );
    fprintf(1,'input data \n\n');
    fprintf(1,' year %5i ',year);
    fprintf(1,' mon %4i ',mon);
    fprintf(1,' day %3i ',day);
    fprintf(1,' %3i:%2i:%8.6f\n ',hr,minute,second );
    fprintf(1,' dut1 %8.6f s',dut1);
    fprintf(1,' dat %3i s',dat);
    fprintf(1,' xp %8.6f "',xp / conv);
    fprintf(1,' yp %8.6f "',yp / conv);
    fprintf(1,' lod %8.6f s\n',lod);
    fprintf(1,' ddpsi %8.6f " ddeps  %8.6f\n',ddpsi/conv, ddeps/conv);

    fprintf(1,'tt  %8.6f ttt  %16.12f jdtt  %18.11f ',tt,ttt,jdtt );
    [h,m,s] = sec2hms( tt );
    fprintf(1,'hms %3i %3i %8.6f \n',h,m,s);
 
    [rsun,rtasc,decl] = sun ( jd );
    fprintf(1,'sun  rtasc %14.6f deg decl %14.6f deg\n',rtasc*rad,decl*rad );
    fprintf(1,'sun ICRS %11.9f%11.9f%11.9f au\n',rsun );
    fprintf(1,'sun ICRS %14.4f%14.4f%14.4f km\n',rsun*149597870.0 );

    rsunaa = [0.9772766 0.1922635  0.0833613]*149597870.0; % astronomical alm value into km
    fprintf(1,'rs almanac MOD %11.9f %11.9f %11.9f km \n',rsunaa);

    %ttt= ( jd - 2451545.0  )/ 36525.0;
    vmod = [0 0 0]';
    amod = [0 0 0]';
    [reci,veci,aeci] = mod2eci  ( rsun',vmod,amod,ttt );
    fprintf(1,'mod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',reci*149597870.0, mag(reci)*149597870.0 );
    db = reci*149597870.0-rsunaa';
    fprintf(1,'delta mod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',db, mag(db) );

    [reci,veci,aeci] = tod2eci  ( rsun',vmod,amod,ttt, ddpsi, ddeps );
    fprintf(1,'tod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',reci*149597870.0, mag(reci)*149597870.0 );
    db = reci*149597870.0-rsunaa';
    fprintf(1,'delta tod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',db, mag(db) );

    #%         [reci,veci,aeci] = eci2mod ( rsun',vmod,amod,ttt );
    #%         fprintf(1,'eci - mod  %11.9f %11.9f %11.9f %11.4f km  \n',reci*149597870.0, mag(reci)*149597870.0 );
    #%         db = reci*149597870.0-rsunaa';
    #%         fprintf(1,'delta eci - mod  %11.9f %11.9f %11.9f %11.4f km  \n',db, mag(db) );
    #% 
    #%         [reci,veci,aeci] = eci2tod ( rsun',vmod,amod,ttt, ddpsi, ddeps );
    #%         fprintf(1,'eci - tod  %11.9f %11.9f %11.9f %11.4f km  \n',reci*149597870.0, mag(reci)*149597870.0 );
    #%         db = reci*149597870.0-rsunaa';
    #%         fprintf(1,'delta eci - tod  %11.9f %11.9f %11.9f %11.4f km  \n',db, mag(db) );
    
    % now try alamnac method
    [rsuna,rtasca,decla] = sunalmanac ( jd );
    fprintf(1,'\n\nsun  rtasc %14.6f deg decl %14.6f deg\n',rtasca*rad, decla*rad );
    fprintf(1,'sun ALM %11.9f%11.9f%11.9f au\n',rsuna );
    fprintf(1,'sun ALM %14.4f%14.4f%14.4f km\n',rsuna*149597870.0 );

    fprintf(1,'rs aa ICRF %11.9f %11.9f %11.9f km \n',rsunaa);

    %ttt= ( jd - 2451545.0  )/ 36525.0;
    vmod = [0 0 0]';
    amod = [0 0 0]';
    [reci,veci,aeci] = mod2eci  ( rsuna',vmod,amod,ttt );
    fprintf(1,'mod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',reci*149597870.0, mag(reci)*149597870.0 );
    db = reci*149597870.0-rsunaa';
    fprintf(1,'delta mod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',db, mag(db) );

    [reci,veci,aeci] = tod2eci  ( rsuna',vmod,amod,ttt, ddpsi, ddeps );
    fprintf(1,'tod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',reci*149597870.0, mag(reci)*149597870.0 );
    db = reci*149597870.0-rsunaa';
    fprintf(1,'delta tod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',db, mag(db) );

    fprintf(1,'==============================================================\n');
    % another example tdt = 29+32.184 secs less than 4/2 at 0 hrs
    year = 1995;
    mon = 4;
    day = 1;
    hr = 23;
    minute = 58;
    second = 58.816;
    [jd,jdfrac] = jday(year, mon, day, hr, minute, second);
    fprintf(1,'jd  %11.9f \n',jd+jdfrac );
    dat = 29;
    xp = 0.034454 * conv;
    yp = 0.558299 * conv;
    dut1 = 0.1535663;
    lod = 0.0026897;
    ddpsi = -0.022953 * conv;
    ddeps = -0.008104 * conv;
    [ut1, tut1, jdut1,jdut1frac, utc, tai, tt, ttt, jdtt,jdttfrac, tdb, ttdb, jdtdb,jdtdbfrac ] ...
         = convtime ( year, mon, day, hr, minute, second, timezone, dut1, dat );
    fprintf(1,'input data \n\n');
    fprintf(1,' year %5i ',year);
    fprintf(1,' mon %4i ',mon);
    fprintf(1,' day %3i ',day);
    fprintf(1,' %3i:%2i:%8.6f\n ',hr,minute,second );
    fprintf(1,' dut1 %8.6f s',dut1);
    fprintf(1,' dat %3i s',dat);
    fprintf(1,' xp %8.6f "',xp / conv);
    fprintf(1,' yp %8.6f "',yp / conv);
    fprintf(1,' lod %8.6f s\n',lod);
    fprintf(1,' ddpsi %8.6f " ddeps  %8.6f\n',ddpsi/conv, ddeps/conv);

    fprintf(1,'ut1 %8.6f tut1 %16.12f jdut1 %18.11f ',ut1,tut1,jdut1 );
    [h,m,s] = sec2hms( ut1 );
    fprintf(1,'hms %3i %3i %8.6f \n',h,m,s);
    fprintf(1,'utc %8.6f ',utc );
    [h,m,s] = sec2hms( utc );
    fprintf(1,'hms %3i %3i %8.6f \n',h,m,s);
    fprintf(1,'tai %8.6f',tai );
    [h,m,s] = sec2hms( tai );
    fprintf(1,'hms %3i %3i %8.6f \n',h,m,s);
    fprintf(1,'tt  %8.6f ttt  %16.12f jdtt  %18.11f ',tt,ttt,jdtt );
    [h,m,s] = sec2hms( tt );
    fprintf(1,'hms %3i %3i %8.6f \n',h,m,s);
    fprintf(1,'tdb %8.6f ttdb %16.12f jdtdb %18.11f\n',tdb,ttdb,jdtdb );
  
    [rsun,rtasc,decl] = sun ( jd+jdfrac );
    fprintf(1,'sun  rtasc %14.6f deg decl %14.6f deg\n',rtasc*rad,decl*rad );
    fprintf(1,'sun ICRS %11.9f%11.9f%11.9f au\n',rsun );
    fprintf(1,'sun ICRS %14.4f%14.4f%14.4f km\n',rsun*149597870.0 );

    rsunaa = [0.9781158 0.1884327  0.0816997]*149597870.0; % astronomical alm value into km
    fprintf(1,'rs almanac MOD %11.9f %11.9f %11.9f km \n',rsunaa);

    %ttt= ( jd - 2451545.0  )/ 36525.0;
    vmod = [0 0 0]';
    amod = [0 0 0]';
    [reci,veci,aeci] = mod2eci  ( rsun',vmod,amod,ttt );
    fprintf(1,'mod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',reci*149597870.0, mag(reci)*149597870.0 );
    db = reci*149597870.0-rsunaa';
    fprintf(1,'delta mod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',db, mag(db) );

    [reci,veci,aeci] = tod2eci  ( rsun',vmod,amod,ttt, ddpsi, ddeps );
    fprintf(1,'tod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',reci*149597870.0, mag(reci)*149597870.0 );
    db = reci*149597870.0-rsunaa';
    fprintf(1,'delta tod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',db, mag(db) );

    #%         [reci,veci,aeci] = eci2mod ( rsun',vmod,amod,ttt );
    #%         fprintf(1,'eci - mod  %11.9f %11.9f %11.9f %11.4f km  \n',reci*149597870.0, mag(reci)*149597870.0 );
    #%         db = reci*149597870.0-rsunaa';
    #%         fprintf(1,'delta eci - mod  %11.9f %11.9f %11.9f %11.4f km  \n',db, mag(db) );
    #% 
    #%         [reci,veci,aeci] = eci2tod ( rsun',vmod,amod,ttt, ddpsi, ddeps );
    #%         fprintf(1,'eci - tod  %11.9f %11.9f %11.9f %11.4f km  \n',reci*149597870.0, mag(reci)*149597870.0 );
    #%         db = reci*149597870.0-rsunaa';
    #%         fprintf(1,'delta eci - tod  %11.9f %11.9f %11.9f %11.4f km  \n',db, mag(db) );
    
    % now try alamnac method
    [rsuna,rtasca,decla] = sunalmanac ( jd+jdfrac );
    fprintf(1,'\n\nsun  rtasc %14.6f deg decl %14.6f deg\n',rtasca*rad, decla*rad );
    fprintf(1,'sun ALM %11.9f%11.9f%11.9f au\n',rsuna );
    fprintf(1,'sun ALM %14.4f%14.4f%14.4f km\n',rsuna*149597870.0 );

    fprintf(1,'rs aa ICRF %11.9f %11.9f %11.9f km \n',rsunaa);

    %ttt= ( jd - 2451545.0  )/ 36525.0;
    vmod = [0 0 0]';
    amod = [0 0 0]';
    [reci,veci,aeci] = mod2eci  ( rsuna',vmod,amod,ttt );
    fprintf(1,'mod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',reci*149597870.0, mag(reci)*149597870.0 );
    db = reci*149597870.0-rsunaa';
    fprintf(1,'delta mod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',db, mag(db) );

    [reci,veci,aeci] = tod2eci  ( rsuna',vmod,amod,ttt, ddpsi, ddeps );
    fprintf(1,'tod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',reci*149597870.0, mag(reci)*149597870.0 );
    db = reci*149597870.0-rsunaa';
    fprintf(1,'delta tod - eci  %11.9f %11.9f %11.9f %11.4f km  \n',db, mag(db) );
    """

        

#ex2_5()






