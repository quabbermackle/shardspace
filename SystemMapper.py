# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 02:16:05 2021

@author: Matthew

This file defines objects to plot Spelljammer system maps and display orbits
within them.

Created specifically for Shardspace, an Eberron/Spelljammer combo. Color scheme
and fonts match those of other maps created for this setting.
"""

from matplotlib import pyplot as plt
from matplotlib import patches as patch
from matplotlib import font_manager as fm
from scipy import constants as const
import numpy as np
from numba import jit
import pathlib as pl
from os import path

import OrbitBasics as ob

'''
-------------------------------------------------------------------------------
CONSTANTS
-------------------------------------------------------------------------------
'''

Mmi2km = 1e6*const.mile/1e3 # conversion factor, million miles to km

d_inner = round(20*Mmi2km) # km, dist of spaces on the inner track
d_outer = round(400*Mmi2km) # km, dist of spaces on the outer track

rmax_inner = round(300*Mmi2km) # km, outer radius of inner track
rmin_outer = round(200*Mmi2km) # inner radius of outer track

nr_in = int(np.ceil(rmax_inner/d_inner)) # number of radial gridlines in inner plot
ntheta_in = 6*np.arange(1, nr_in) # number of angular gridlines at each radial one
thetagrid_in = []
for i in range(nr_in-1):
    thetagrid_in.append(np.linspace(0, 360, ntheta_in[i]+1))

space = '#030058ff' # background space color (deep purple)
brass = '#db8627ff' # orange brass color for orbit tracks etc
sphere = '#7397d4ff' # sky blue for crystal sphere
directory = path.dirname(path.abspath(__file__)) # directory of current file
fontpath = directory + '\\Eberron.ttf' # system file path to Eberron font
ebfont = fm.FontProperties(fname = fontpath) # use this to set Eberron font

#print(rmax_inner/d_inner)
#print(ntheta_in)
#print(thetavec_in)

'''
-------------------------------------------------------------------------------
CLASSES
-------------------------------------------------------------------------------
'''

class SystemMap:
    def __init__(self, planets = ob.SolSystem):
        # planets must be a dict with keys for 'names', 'r' (orbital radii),
        # and 'CB' - an instance of a CentralBody object
        # this assumes all planets have circular orbits
        self.planets = planets
        self.names = planets['names']
        self.r = planets['r']
        self.cb = planets['CB']
        
        # epoch date
        if 'epoch' in planets.keys(): self.epoch = planets['epoch']
        else:
            self.epoch = 0
            self.planets['epoch'] = self.epoch
        
        # epoch positions
        if 'epochxy' in planets.keys(): self.epochxy = planets['epochxy']
        else:
            self.epochxy = np.zeros((len(self.r), 2))
            for i in range(len(self.r)):
                self.epochxy[i,:] = [0, self.r[i]] # [x, y] rect coord, km
            self.planets['epochxy'] = self.epochxy
        
        # define outer track outer limits
        self.rmax = max(planets['r']) # km, largest orbital radius
        nr_out = int(np.floor(2*self.rmax/d_outer)) # num out radial grids
        self.rsphere = nr_out*d_outer # km, celestial sphere radius
        
        # create 1x2 subplots
        self.fig, (self.inner, self.outer) = plt.subplots(1, 2) # fig & ax obj
        self.fig.tight_layout() # apply tight layout to whole figure
        self.mng = plt.get_current_fig_manager()
        self.mng.window.showMaximized() # maximize the window
        
        # set titles
        if 'title' in planets.keys():
            self.title = planets['title'] # name of system, ie 'Solar System'
            self.fig.suptitle(self.title, fontproperties = ebfont,
                              fontsize = 48)
        else: self.title = ''
        self.inner.set_title('Inner System', fontproperties = ebfont,
                             fontsize = 24)
        self.outer.set_title('Outer System', fontproperties = ebfont,
                             fontsize = 24)
        
        # set up axes
        for x in [self.inner, self.outer]:
            x.set_aspect('equal') # square aspect ratio
            x.set_axis_off()
            
        # set axes limits
        self.inner.set_xlim(-rmax_inner, rmax_inner)
        self.inner.set_ylim(-rmax_inner, rmax_inner)
        self.outer.set_xlim(-self.rsphere, self.rsphere)
        self.outer.set_ylim(-self.rsphere, self.rsphere)
        
        # plot background color
        self.inner.add_artist(patch.Circle((0,0), radius = rmax_inner,
                                           ec = (0,0,0,0), fc = space))
        self.outer.add_artist(patch.Circle((0,0), radius = self.rsphere,
                                           ec = (0,0,0,0), fc = space))
        
        # plot limiting radii
        self.inner.add_artist(patch.Circle((0,0), radius = rmax_inner,
                                           ec = 'black', fc = (0,0,0,0)))
        self.inner.add_artist(patch.Circle((0,0), radius = rmin_outer,
                                           ec = 'grey', fc = (0,0,0,0),
                                           lw = 2))
        self.outer.add_artist(patch.Circle((0,0), radius = rmin_outer,
                                           ec = 'grey', fc = 'grey'))
        self.outer.add_artist(patch.Circle((0,0), radius = self.rsphere,
                                           ec = sphere, fc = (0,0,0,0),
                                           lw = 10))
        
        # show correspondence between inner and outer plots
        '''
        for x in [self.inner, self.outer]:
            x.add_artist(patch.ConnectionPatch(
                    (0, rmin_outer), (0, rmin_outer), coordsA = 'data',
                    coordsB = 'data', axesA = self.inner, axesB = self.outer,
                    color = 'grey', lw = 2))
            x.add_artist(patch.ConnectionPatch(
                    (0, -rmin_outer), (0, -rmin_outer),  coordsA = 'data',
                    coordsB = 'data', axesA = self.inner, axesB = self.outer,
                    color = 'grey', lw = 2))
        '''
        
        # plot wedge patches to create inner grid
        self.rgrid_in = d_inner*np.arange(1, nr_in)
        self.thetagrid_in = thetagrid_in
        for ir in range(nr_in-1):
            for jtheta in range(ntheta_in[ir]):
                w = patch.Wedge((0,0),
                                r = self.rgrid_in[ir] + d_inner,
                                width = d_inner,
                                theta1 = self.thetagrid_in[ir][jtheta],
                                theta2 = self.thetagrid_in[ir][jtheta+1],
                                ec = (1, 1, 1, 0.2),
                                fc = (0, 0, 0, 0))
                self.inner.add_artist(w)
        
        # plot wedge patches to create outer grid
        self.rgrid_out = d_outer*np.arange(1, self.rsphere/d_outer)
        ntheta_out = 6*np.arange(1, nr_out) # num ang gridline at each rad
        self.thetagrid_out = []
        for i in range(nr_out-1):
            self.thetagrid_out.append(np.linspace(0, 360, ntheta_out[i]+1))
        for ir in range(nr_out-1):
            for jtheta in range(ntheta_out[ir]):
                w = patch.Wedge((0,0),
                                r = self.rgrid_out[ir] + d_outer,
                                width = d_outer,
                                theta1 = self.thetagrid_out[ir][jtheta],
                                theta2 = self.thetagrid_out[ir][jtheta+1],
                                ec = (1, 1, 1, 0.2),
                                fc = (0, 0, 0, 0))
                self.outer.add_artist(w)
        
        # plot planetary orbits
        for i in range(len(self.names)):
            # create Circle artists for current planet, then add to axes
            D = self.r[i] # diameter
            cin = patch.Circle((0,0), radius = D, lw = 3,
                               ec = brass, fc = (0, 0, 0, 0))
            cout = patch.Circle((0,0), radius = D, lw = 3,
                                ec = brass, fc = (0, 0, 0, 0))
            if self.r[i] < rmax_inner: self.inner.add_artist(cin)
            if self.r[i] > rmin_outer: self.outer.add_artist(cout)
            
        # plot central body in inner system
        self.inner.plot(0, 0, '.', ms = 30)
        self.inner.annotate(self.cb.name, (0,0), xytext = (10,-5),
                            textcoords = 'offset points', color = 'white',
                            fontproperties = ebfont, fontsize = 16)
        
    def showdate(self, date, label=True):
       
        # plot at epoch time
        if date == self.epoch: self.xy = self.epochxy
        # ephemeris calculation to plot at any time
        else: self.xy = ephemeris(date, self)
            
        # plot current x,y coordinates
        for i in range(len(self.r)):
            if self.r[i] < rmax_inner:
                self.inner.plot(self.xy[i,0], self.xy[i,1], '.', ms = 15)
                if label:
                    self.inner.annotate(
                            self.names[i], self.xy[i,:], xytext = (5,2),
                            textcoords='offset points', color = 'white',
                            fontproperties = ebfont, fontsize = 16)
            if self.r[i] > rmin_outer:
                self.outer.plot(self.xy[i,0], self.xy[i,1], '.', ms = 15)
                if label:
                    self.outer.annotate(
                            self.names[i], self.xy[i,:], xytext = (5,2),
                            textcoords='offset points', color = 'white',
                            fontproperties = ebfont, fontsize = 16)
        
    def showepoch(self):
        self.showdate(date = self.epoch)
     
'''
-------------------------------------------------------------------------------
FUNCTIONS
-------------------------------------------------------------------------------
'''

def ephemeris(t, system):
    '''
    2D circular ephemeris calculation
    inputs: t      = time since epoch
            system = object with attributes:
                        r       = vector of planetary radii
                        epoch   = epoch time
                        epochxy = coordinates at epoch time
                        cb      = CentralBody object with attributes:
                                    mu  = gravitational parameter
                                    xyz = coordinates at time t
    outputs: xy = coordinates of each planet at time t
    ''' 
    
    r  = system.r             # radii of planets in circular orbits, km
    t0 = system.epoch         # epoch time, sec
    x0 = system.epochxy[:, 0] # x coordinates of planets at epoch time, km
    y0 = system.epochxy[:, 1] # y coordinates of planets at epoch time, km
    mu = system.cb.mu         # grav parameter of central body, km^3/s^2
    a  = system.cb.xyz[0]     # x coordinate of central body at time t, km
    b  = system.cb.xyz[1]     # y coordinate of central body at time t, km
    
    theta0 = ob.xy2theta(x0, y0) # theta coordinates at epoch time, rad
    thetadot = np.sqrt(mu / (r**3)) # angular rates, rad/sec
    dtheta = (t - t0) * thetadot # angular distances since epoch, sec
    
    theta = theta0 + dtheta # theta coordinates at current time t
    
    x = a + ob.rtheta2x(r, theta) # x coordinates at time t
    y = b + ob.rtheta2y(r, theta) # y coordinates at time t
    
    xy = np.zeros((len(system.r), 2))
    xy[:, 0] = x
    xy[:, 1] = y
    
    return xy

'''
-------------------------------------------------------------------------------
TEST
-------------------------------------------------------------------------------
'''

test = SystemMap()
test.showepoch()
test.showdate(1*const.year)
plt.show()
#print(test.rsphere/d_outer)

'''
fig, ax = plt.subplots()
e = patch.Ellipse((0,0), width = 1, height=1, fc = (0, 0, 0, 0), ec = '#db8627ff')
ax.add_artist(e)
w = patch.Wedge((0,0), 1, 0, 45, width=0.5)
ax.add_artist(w)
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
plt.show()
'''