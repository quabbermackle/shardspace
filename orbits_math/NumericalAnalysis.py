# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 12:00:13 2021

@author: Matthew
"""

import numpy as np
import random as rng
from numba import jit

# define Butcher tableaus
# the tableau must either be square or have exactly 1 more row than columns
# the order of each method is stored in the bottom left [i=#rows,0]
Butcher = {
        # ---------------------------------------------------------------------
        # EXPLICIT
        # ---------------------------------------------------------------------
        'euler':np.array([ # forward Euler 1st order
            [0, 0],
            [1, 1]
            ]),
        'midpoint':np.array([ # 2nd order
            [0,   0,   0],
            [1/2, 1/2, 0],
            [2,   0,   1]
            ]),
        'heun2':np.array([ # (explicit) trapezoid / modified Euler / Lobatto IIIC* 2nd order, not A-, B-, or L-stable
            [0, 0,   0  ],
            [1, 1,   0  ],
            [2, 1/2, 1/2]
            ]),
        'ralston2':np.array([ # Ralston 2nd order, minimum local error bound
            [0,   0,   0  ],
            [2/3, 2/3, 0  ],
            [2,   1/4, 3/4]
            ]),
        'kutta3':np.array([ # Kutta 3rd order
            [0,    0,   0,   0  ],
            [1/2,  1/2, 0,   0  ],
            [1,   -1,   2,   0  ],
            [3,    1/6, 2/3, 1/6]
            ]),
        'heun3':np.array([ # 3rd order
            [0,   0,   0,   0  ],
            [1/3, 1/3, 0,   0  ],
            [2/3, 0,   2/3, 0  ],
            [3,   1/4, 0,   3/4]
            ]),
        'ralston3':np.array([ # Ralston 3rd order (used in embedded Bogacki-Shampine)
            [0,   0,   0,   0  ],
            [1/2, 1/2, 0,   0  ],
            [3/4, 0,   3/4, 0  ],
            [3,   2/9, 1/3, 4/9]
            ]),
        'ssprk3':np.array([ # Strong Stability Preserving Runge-Kutta 3rd order
            [0,   0,   0,   0  ],
            [1,   1,   0,   0  ],
            [1/2, 1/4, 1/4, 0  ],
            [3,   1/6, 1/6, 2/3]
            ]),
        'rk4':np.array([ # Runge-Kutta 4th order; the "original"
            [0,   0,   0,   0,   0  ],
            [1/2, 1/2, 0,   0,   0  ],
            [1/2, 0,   1/2, 0,   0  ],
            [1,   0,   0,   1,   0  ],
            [4,   1/6, 1/3, 1/3, 1/6]
            ]),
        'ralston4':np.array([ # Ralston 4th order, minimum truncation error
            [ 0,         0,         0,          0,           0       ],
            [.4,        .4,         0,          0,           0       ],
            [.45573725, .29697761, .15875964,   0,           0       ],
            [ 1,        .21810040, -3.05096516, 3.83286476,  0       ],
            [ 4,        .17476028, -.55148066,  1.20553560, .17118478]
            ]),
        'kutta4':np.array([ # Kutta 4th order / 3/8ths rule
            [0,    0,    0,   0,   0  ],
            [1/3,  1/3,  0,   0,   0  ],
            [2/3, -1/3,  1,   0,   0  ],
            [1,    1,   -1,   1,   0  ],
            [4,    1/8,  3/8, 3/8, 1/8]
            ]),
        # ---------------------------------------------------------------------
        # Embedded
        # ---------------------------------------------------------------------
        'he12':np.array([ # Heun-Euler 2nd order embedded
            [0, 0,   0  ],
            [1, 1,   0  ],
            [0, 1/2, 1/2], # b,  2nd order
            [1, 1,   0  ]  # b*, 1st order
            ]),
        'rkf12':np.array([ # Runge-Kutta-Fehlberg 2nd order embedded
            [0,   0,     0,       0    ],
            [1/2, 1/2,   0,       0    ],
            [1,   1/256, 255/256, 0    ],
            [0,   1/512, 255/256, 1/512], # b,  2nd order
            [1,   1/256, 255/256, 0    ]  # b*, 1st order
            ]),
        'bs23':np.array([ # Bogacki-Shampine 3rd order embedded
            [0,   0,    0,   0,   0  ],
            [1/2, 1/2,  0,   0,   0  ],
            [3/4, 0,    3/4, 0,   0  ],
            [1,   2/9,  1/3, 4/9, 0  ],
            [0,   2/9,  1/3, 4/9, 0  ], # b,  3rd order
            [2,   7/24, 1/4, 1/3, 1/8]  # b*, 2nd order
            ]),
        'rkf45':np.array([ # Runge-Kutta-Fehlberg 5th order embedded
            [0,      0,          0,          0,           0,            0,     0   ],
            [1/2,    1/2,        0,          0,           0,            0,     0   ],
            [3/8,    3/32,       9/32,       0,           0,            0,     0   ],
            [12/13,  1932/2197, -7200/2197,  7296/2197,   0,            0,     0   ],
            [1,      439/216,   -8,          3680/513,   -845/4104,     0,     0   ],
            [1/2,   -8/27,       2,         -3544/2565,   1859/4104,   -11/40, 0   ],
            [0,      16/135,     0,          6656/12825,  28561/56430, -9/50,  2/55], # b,  5th order
            [4,      25/216,     0,          1408/2565,   2197/4104,   -1/5,   0   ]  # b*, 4th order
            ]),
        'ck45':np.array([ # Cash-Karp 5th order embedded
            [0,     0,           0,        0,           0,            0,         0       ],
            [1/5,   1/5,         0,        0,           0,            0,         0       ],
            [3/10,  3/40,        9/40,     0,           0,            0,         0       ],
            [3/5,   3/10,       -9/10,     6/5,         0,            0,         0       ],
            [1,    -11/54,       5/2,     -70/27,       35/27,        0,         0       ],
            [7/8,   1631/55296,  175/512,  575/13824,   44275/110592, 253/4096,  0       ],
            [0,     37/378,      0,        250/621,     125/594,      0,         512/1771], # b,  5th order
            [4,     2825/27648,  0,        18575/48384, 13525/55296,  277/14336, 1/4     ]  # b*, 4th order
            ]),
        'DoPr45':np.array([ # Dormand-Prince 5th order embedded
            [0,    0,           0,          0,           0,        0,            0,        0   ],
            [1/5,  1/5,         0,          0,           0,        0,            0,        0   ],
            [3/10, 3/40,        9/40,       0,           0,        0,            0,        0   ],
            [4/5,  44/45,      -56/15,      32/9,        0,        0,            0,        0   ],
            [8/9,  19372/6561, -25360/2187, 64448/6561, -212/729,  0,            0,        0   ],
            [1,    9017/3168,  -355/33,     46732/5247,  49/176,  -5103/18656,   0,        0   ],
            [1,    35/384,      0,          500/1113,    125/192, -2187/6784,    11/84,    0   ],
            [0,    35/384,      0,          500/1113,    125/192, -2187/6784,    11/84,    0   ], # b,  5th order
            [4,    5179/57600,  0,          7571/16695,  393/640, -92097/339200, 187/2100, 1/40]  # b*, 4th order
            ]),
        # ---------------------------------------------------------------------
        # IMPLICIT
        # ---------------------------------------------------------------------
        'bwdeuler':np.array([ # backward Euler 1st order
            [1, 1],
            [1, 1]
            ]),
        'gl2':np.array([ # implicit midpoint / Gauss-Legendre 2nd order (also diagonally implicit [DIRK] & symplectic)
            [1/2, 1/2],
            [2,   1  ]
            ]),
        'cranknicolson':np.array([ # Crank-Nicolson /implicit trapezoid 2nd order, A-stable
            [0, 0,   0  ],
            [1, 1/2, 1/2],
            [2, 1/2, 1/2]
            ]),
        'gl4':np.array([ # Gauss-Legendre 4th order (embedded?)
            [1/2 - np.sqrt(3)/6, 1/4,                1/4 - np.sqrt(3)/6],
            [1/2 + np.sqrt(3)/6, 1/4 + np.sqrt(3)/6, 1/4               ],
            [0,                  1/2,                1/2               ],
            [4,                  1/2 + np.sqrt(3)/2, 1/2 - np.sqrt(3)/2]
            ]),
        'gl6':np.array([ # Gauss-Legendre 6th order (embedded?)
            [1/2 - np.sqrt(15)/10,  5/36,                  2/9 - np.sqrt(15)/15,  5/36 - np.sqrt(15)/30],
            [1/2,                   5/36 + np.sqrt(15)/24, 2/9,                   5/36 - np.sqrt(15)/24],
            [1/2 + np.sqrt(15)/10,  5/36 + np.sqrt(15)/30, 2/9 + np.sqrt(15)/15,  5/36                 ],
            [0,                     5/18,                  4/9,                   5/18                 ],
            [6,                    -5/6,                   8/3,                  -5/6                  ]
            ]),
        # ---------------------------------------------------------------------
        # Diagonally Implicit Runge-Kutta (DIRK)
        # ---------------------------------------------------------------------
        'dirkks2':np.array([ # Kraaijevanger-Spijker 2nd order
            [1/2,  1/2, 0  ],
            [3/2, -1/2, 2  ],
            [2,   -1/2, 3/2]
            ]),
        'dirkc3':np.array([ # Crouzeix 3rd order
            [1/2 + np.sqrt(3)/6,  1/2 + np.sqrt(3)/6, 0                 ],
            [1/2 - np.sqrt(3)/6, -np.sqrt(3)/3,       1/2 + np.sqrt(3)/6],
            [3,                   1/2,                1/2               ]
            ]),
        'dirk3four':np.array([ # 3rd order (four stages), L-stable
            [1/2,  1/2,  0,   0,   0  ],
            [2/3,  1/6,  1/2, 0,   0  ],
            [1/2, -1/2,  1/2, 1/2, 0  ],
            [1,    3/2, -3/2, 1/2, 1/2],
            [3,    3/2, -3/2, 1/2, 1/2]
            ]),
        # ---------------------------------------------------------------------
        # Lobatto methods
        # ---------------------------------------------------------------------
        'l3a2':np.array([ # Lobatto IIIA 2nd order (embedded trapezoid?), collocation method, A- but not L- or B-stable
            [0, 0,   0  ],
            [1, 1/2, 1/2],
            [0, 1/2, 1/2],
            [2, 1,   0  ]
            ]),
        'l3a4':np.array([ # Lobatto IIIA 4th order (embedded?), collocation method, A- but not L- or B-stable
            [0,    0,    0,    0   ],
            [1/2,  5/24, 1/3, -1/24],
            [1,    1/6,  2/3,  1/6 ],
            [0,    1/6,  2/3,  1/6 ],
            [4,   -1/2,  2,   -1/2 ]
            ]),
        'l3b2':np.array([ # 2nd order (embedded?), discontinuous collocation, A- but not L- or B-stable
            [0, 1/2, 1  ],
            [1, 1/2, 0  ],
            [0, 1/2, 1/2],
            [2, 1,   0  ]
            ]),
        'l3b4':np.array([ # Lobatto IIIB 4th order (embedded?), discontinuous collocation, A- but not L- or B-stable
            [0,    1/6, -1/6,  0  ],
            [1/2,  1/6,  1/3,  0  ],
            [1,    1/6,  5/6,  0  ],
            [0,    1/6,  2/3,  1/6],
            [4,   -1/2,  2,   -1/2]
            ]),
        'l3c2':np.array([ # Lobatto IIIC 2nd order (embedded?), discontinuous collocation, L- and B-stable
            [0, 1/2, -1/2],
            [1, 1/2,  1/2],
            [0, 1/2,  1/2],
            [2, 1,    0  ]
            ]),
        'l3c4':np.array([ # Lobatto IIIC 4th order (embedded?), discontinuous collocation, L- and B-stable
            [0,    1/6, -1/3,   1/6 ],
            [1/2,  1/6,  5/12, -1/12],
            [1,    1/6,  2/3,   1/6 ],
            [0,    1/6,  2/3,   1/6 ],
            [4,   -1/2,  2,    -1/2 ]
            ]),
        'butcher':np.array([ # Butcher / Lobatto IIIC* 4th order, not A-, B-, or L-stable
            [0,   0,   0,   0  ],
            [1/2, 1/4, 1/4, 0  ],
            [1,   0,   1,   0  ],
            [4,   1/6, 2/3, 1/6]
            ]),
        'l3d2':np.array([ # Lobatto IIID 2nd order, L-, B-stable
            [0,  1/2, 1/2],
            [1, -1/2, 1/2],
            [2,  1/2, 1/2]
            ]),
        'l3d4':np.array([ # Lobatto IIID 4th order, L-, B-stable
            [0,   1/6,  1,    -1/6],
            [1/2, 1/12, 5/12,  0  ],
            [1,   1/2,  1/3,   1/6],
            [4,   1/6,  2/3,   1/6]
            ]),
        'r1a3':np.array([ # Radau IA 3rd order, A-stable
            [0,   1/4, -1/4 ],
            [2/3, 1/4,  5/12],
            [3,   1/4,  3/4 ]
            ]),
        'r1a5':np.array([ # Radau IA 5th order, A-stable
            [0,                   1/9, (-1 - np.sqrt(6))/18,      (-1 + np.sqrt(6))/18     ],
            [3/5 - np.sqrt(6)/10, 1/9, 11/45 +  7*np.sqrt(6)/360, 11/45 - 43*np.sqrt(6)/360],
            [3/5 + np.sqrt(6)/10, 1/9, 11/45 + 43*np.sqrt(6)/360, 11/45 -  7*np.sqrt(6)/360],
            [5,                   1/9, 4/9   +    np.sqrt(6)/36,  4/9   -    np.sqrt(6)/36 ]
            ]),
        'r2a3':np.array([ # Radau IIA 3rd order, A-stable
            [1/3, 5/12, -1/12],
            [1,   3/4,   1/4 ],
            [3,   3/4,   1/4 ]
            ]),
        'r2a5':np.array([ # Radau IIA 5th order, A-stable
            [2/5 - np.sqrt(6)/10, 11/45  -   7*np.sqrt(6)/360,  37/225 - 169*np.sqrt(6)/1800, -2/225 + np.sqrt(6)/75],
            [2/5 + np.sqrt(6)/10, 37/225 + 169*np.sqrt(6)/1800, 11/45  +   7*np.sqrt(6)/360,  -2/225 - np.sqrt(6)/75],
            [1,                   4/9    -     np.sqrt(6)/36,   4/9    +     np.sqrt(6)/36,    1/9                  ],
            [5,                   4/9    -     np.sqrt(6)/36,   4/9    +     np.sqrt(6)/36,    1/9                  ]
            ]),
        }
Butcher['fwde1']     =  Butcher['euler']
Butcher['trap']      =  Butcher['heun2']
Butcher['threeeighthsrule']  =  Butcher['kutta4']
Butcher['fehlberg']  =  Butcher['rkf12']
Butcher['bosh23']    =  Butcher['bs23']
Butcher['DOPRI45']   =  Butcher['DoPr45']
Butcher['dp45']      =  Butcher['DoPr45']
Butcher['dopri45']   =  Butcher['DoPr45']
Butcher['bwde1']     =  Butcher['bwdeuler']
Butcher['gale2']     =  Butcher['gl2']
Butcher['dirk2']     =  Butcher['gl2']
Butcher['l3cstar2']   =  Butcher['heun2']
Butcher['l3cstarb4']  =  Butcher['butcher']

#@jit(nopython=True, parallel=True)
def rk2generic(alpha):
    # generic second-order Runge-Kutta method
    # given alpha, returns the Butcher tableau
    ratio = 1 / (2*alpha)
    b = np.array([
            [0,     0,       0    ],
            [alpha, alpha,   0    ],
            [2,     1-ratio, ratio]
            ])
    return b

#@jit(nopython=True, parallel=True)
def rk3generic(alpha):
    # generic third-order Runge-Kutta method (Sanderse & Veldman 2019)
    # given alpha, returns the Butcher tableau
    if alpha in [0, 2/3, 1]: raise('alpha =/= 0, 2/3, or 1')
    diff = 1 - alpha
    ratio = diff / (alpha * (3*alpha - 2) )
    b1 = .5 - (1 / (6*alpha) )
    b2 = 1 / (6*alpha*diff)
    b3 = (2 - 3*alpha) / (6*diff)
    b = np.array([
            [0,     0,        0,     0 ],
            [alpha, alpha,    0,     0 ],
            [1,     1+ratio, -ratio, 0 ],
            [3,     b1,       b2,    b3]
            ])
    return b

#@jit(nopython=True, parallel=True)
def pareschirussodirk2(x):
    # Pareschi-Russo two-stage 2nd order DIRK method
    # A-stable only if x >= 1/4
    # L-stable only if x = 1 +/- sqrt(2)/2
    # given x, returns the Butcher tableau
    b = np.array([
            [x,     x,       0  ],
            [1 - x, 1 - 2*x, x  ],
            [2,     1/2,     1/2]
            ])
    return b

#@jit(nopython=True, parallel=True)
def dirk2generic(x):
    # generic two-stage 2nd order DIRK method
    # A-stable only if x >= 1/4
    # L-stable only if x = 1 +/- sqrt(2)/2
    # given x, returns the Butcher tableau
    b = np.array([
            [x, x,   0  ],
            [1, 1-x, x  ],
            [2, 1/2, 1/2]
            ])
    return b

#@jit(nopython=True, parallel=True)
def dirk3(x):
    # three-stage 3nd order DIRK method
    # x = 0.4358665215
    # L-stable
    # given x, returns the Butcher tableau
    y = -(3*x**2)/2 + 4*x - 1/4
    z =  (3*x**2)/2 - 5*x + 5/4
    b = np.array([
            [x,       x,       0, 0],
            [(1+x)/2, (1-x)/2, x, 0],
            [1,       y,       z, x],
            [3,       y,       z, x]
            ])
    return b

#@jit(nopython=True, parallel=True)
def norsettdirk4(x):
    # three-stage, 4th order DIRK method
    # x = 1.06858 or 0.30254 or 0.12889
    # x1 = 1.06858 gives best stability for IVPs
    # given x, returns the Butcher tableau
    y = 3*(1 - 2*x)**2
    b = np.array([
            [x,   x,       0,       0      ],
            [1/2, 1/2 - x, x,       0      ],
            [1-x, 2*x,     1 - 4*x, x      ],
            [4,   1/(2*y), (y-1)/y, 1/(2*y)]
            ])
    return b

Butcher['dirkqz2'] = pareschirussodirk2(1/4) # Qin-Zhang
Butcher['dirkpr2pos'] = pareschirussodirk2(1 + np.sqrt(2)/2)
Butcher['dirkpr2neg'] = pareschirussodirk2(1 - np.sqrt(2)/2)
Butcher['dirk2pos'] = dirk2generic(1 + np.sqrt(2)/2)
Butcher['dirk2neg'] = dirk2generic(1 - np.sqrt(2)/2)
Butcher['dirk3'] = dirk3(.4358665215)
Butcher['dirkn4'] = norsettdirk4(1.06858)

# class to parse Butcher tableaus into integration schemes
class Scheme:
    def __init__(self, tableau = Butcher['rk4']):
        # store tableau
        self.tableau = tableau
        
        # order of scheme
        self.order = tableau[tableau.shape[0]-1, 0]
        
        # number of stages
        self.s = tableau.shape[1]-1
        
        # determine if scheme is embedded
        # (if nrows = ncols+1, scheme is embedded)
        if tableau.shape[0] == self.s + 2: self.embedded = True
        else: self.embedded = False
        
        # decompose Butcher tableau
        self.a = tableau[:self.s, 1:] # a1...as (Runge-Kutta matrix)
        self.c = tableau[:self.s, 0 ] # c1...cs (nodes)
        self.b = tableau[ self.s, 1:] # b1...bs (weights)
        if self.embedded: self.bstar = tableau[self.s+1, 1:] # bstar1...bstars
        
        # determine if scheme is implicit
        # (if a is lower triangular, scheme is explicit)
        if np.allclose(self.a, np.tril(self.a, -1)): self.implicit = False
        else: self.implicit = True
        
        # determine all k factors
        self.k = []
        #self.k[0] = 'f(t, y)'
        jmax = self.s
        for i in range(self.s):
            if not self.implicit: jmax = i
            
            # generate sum of a[i,j]*k[j]
            ysum = []
            for j in range(jmax):
                if self.a[i, j] != 0:
                    ysum.append(str(self.a[i, j]) + '*k' + str(j))
            if ysum == []: ystr = 'y'
            else:          ystr = 'y + h*(' + ' + '.join(ysum) + ')'
            
            # generate k[i]
            if self.c[i] == 0: tstr = 't'
            else:              tstr = 't + h*' + str(self.c[i])
            self.k.append('k' + str(i) + ' = f(' + ', '.join([tstr, ystr, 'misc', '**kwargs']) + ')')
            
        # generate formula for ynew
        ksum = []
        for i in range(self.s):
            if self.b[i] != 0:
                ksum.append(str(self.b[i]) + '*k' + str(i))
        kstr = ' + '.join(ksum)
        self.ynew = 'y + h*(' + kstr + ')'
        
        # store string of full scheme
        self.text = '\n'.join(self.k) + '\n' + 'ynew = ' + self.ynew
        
    def integrator(self, f, h, y, t, misc, **kwargs):
        for line in self.k: exec(line)
        exec('ynew = ' + self.ynew, globals(), locals())
        return locals()['ynew']
        
# generate scheme for all predefined tableaus
for b in Butcher.keys():
    exec(b+' = Scheme(Butcher[b])')
    #print(b)
    #print(locals()[b].text)
    #print('\n')
        
# Misc functions

#@jit(nopython=True, parallel=True)
def vecnorm(e=np.ndarray(0), type='2'):
    if type=='2':
        x = 0.
        for i in range(len(e)):
            x += abs(e[i])**2
        return np.sqrt(x)
    elif type=='1':
        x = 0.
        for i in range(len(e)):
            x += abs(e[i])
        return x
    elif type=='inf':
        return e.max()

#@jit(nopython=True, parallel=True)
def Newton(f, df, x0, tol=1e-6, maxit=1000):
    '''
    Newton-Rhapson root-finding algorithm
    
    INPUTS:
    f     - real-valued function handle
    df    - function handle of the derivative of f
    x0    - initial guess
    tol   - tolerance for convergence
    maxit - maximum # of iterations
    
    OUTPUTS:
    x1    - the root of f
    '''
    
    for i in range(maxit):
        y = f(x0)
        dy = df(x0)
        
        x1 = x0 - (y / dy)
        
        if abs(x1 - x0)<tol: return x1
        else: x0 = x1
        
    print('Newton\'s method failed to converge')
    return x1

#@jit(nopython=True, parallel=True)
def rk4basic(f, k, u0, t0, e=False, misc=[], **kwargs):
    '''
    Runge-Kutta scheme: 4th order
    
    INPUTS:
    f   - function handle
    k   - step size
    u0  - initial state (numpy array)
    t0  - initial time
    e   - output error? T=yes, F=no
    
    OUTPUTS:
    u1  - state at time t0+k
    err - error in state (optional)
    '''
    
    # Intermediate stages
    y1 = u0
    y2 = u0 + 0.5*k*f(t0        , y1, misc, **kwargs)
    y3 = u0 + 0.5*k*f(t0 + (k/2), y2, misc, **kwargs)
    y4 = u0 +     k*f(t0 + (k/2), y3, misc, **kwargs)
    
    # New state
    u1 = u0 + (k/6)*(  f(t0        , y1, misc, **kwargs) + 
                     2*f(t0 + (k/2), y2, misc, **kwargs) + 
                     2*f(t0 + (k/2), y3, misc, **kwargs) + 
                       f(t0 +  k   , y4, misc, **kwargs)  )
    
    err = k**4 # 4th order error
    
    if e: return u1, err
    return u1

#@jit(nopython=True, parallel=True)
def ode(f, s0, tspan, dt, scheme=rk4basic, misc=[], **kwargs):
    t = np.linspace(tspan[0], tspan[1], 1+round((tspan[1]-tspan[0])/dt))
    s = np.zeros((len(t), len(s0)))
    s[0] = s0
    for i in range(1, len(t)):
        s[i] = scheme(f, dt, s[i-1], t[i-1], misc, **kwargs)
    return t, s

# Particle Swarm Optimizer
#@jit(nopython=True, parallel=True)
def pso(J, a=np.array([]), b=np.array([]), N=100, imax=100, dr=[], ineq=[]):
    '''
    n-parameter minimization using particle swarm theory
    follows algorithm on p267 of Conway - Spacecraft Trajectory Optimization
    
    inputs: J    = cost function, J(Chi) = cost
            a    = lower bounds (a[i] <= Chi[i]), 1d numpy array
            b    = upper bounds (Chi[i] >= b[i]), 1d numpy array
            N    = number of particles
            imax = number of iterations
            dr   = equality constraints, dr(Chi) = 0
            ineq = inequality constraints, ineq(Chi) = boolean vector
    
    output: Y    = globally best solution after it iterations
    '''
    Chi = np.zeros((len(a),N)) # particle position
    w = Chi # particle velocity
    psi = np.ones((N,1))*np.inf # position cost
    psinew = np.zeros_like(psi)
    
    d = b - a # velocity bounds, 1d numpy array
    
    # generate N particles for:
    # Chi, uniform distribution over [a, b]
    # w, uniform distribution over [-d, d]
    for i in range(len(a)):
        for j in range(N):
            Chi[i,j] = rng.uniform(a[i], b[i])
            w[i,j] = rng.uniform(-d[i], d[i])
    
    # iterate for specified number of iterations
    for j in range(imax):
    
        # a) evaluate J & determine local best
        for i in range(N):
            psinew[i] = J(Chi[:,i]) # evaluate the objective function
        l = psinew < psi # test if new cost is lower than previous local best
        psi[l] = psinew[l] # if new is better, make it the local best
        
        # b) determine global best
        
        # c) update velocity vector
        
        # d) update position vector
        
    
    return Y

# TEST

'''
def func(x): return x**2 - 2
def dfunc(x): return 2*x
guess = 1

root = Newton(func, dfunc, guess)
print(root)
'''

'''
test = Scheme()
print(test.text)
print('\n')

test2 = Scheme(Butcher['euler'])
print(test2.text)
'''