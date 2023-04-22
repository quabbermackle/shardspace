'''
Defines basic dual class for automatic differentiation of 1st derivatives.
This is accomplished by operator overloading.
Designed for cython and numpy.

Matthew Gunther
04/04/2023
'''

import cython as cy
import numpy as np
#cimport numpy as cnp

# template for overloaded function
'''
    def __function__(self, other):
        if type(self) != dual and type(other) != dual:
            # neither are duals
            return self
        elif type(self) != dual and type(other) == dual:
            # self is a scalar, other is a dual
            val = self.val
            deriv = self.deriv
            return dual(val, deriv)
        elif type(self) == dual and type(other) != dual:
            # other is a scalar, self is a dual
            val = self.val
            deriv = self.deriv
            return dual(val, deriv)
        elif type(self) == dual and type(other) == dual:
            # both are duals
            val = self.val
            deriv = self.deriv
            return dual(val, deriv)
'''

class dual(float):
    '''
    This is a basic class implementing dual numbers for automatic differentiation.
    Only calculates the first derivative.
    The value is accessed as dual.val, derivative as dual.deriv
    '''
    
    def __init__(self, val, deriv=0.):
        '''
        initialize variable to differentiate with respect to with
            deriv = 1
        initialize independent variables and constants with
            deriv = 0
        '''

        super().__init__(val)
        self.val = val
        self.deriv = deriv
    
    def __add__(self, other):
        if type(self) != dual and type(other) != dual:
            # neither are duals
            return self + other
        elif type(self) != dual and type(other) == dual:
            # self is a scalar, other is a dual
            val = self + other.val
            deriv = other.deriv # deriv of scalar is 0
            return dual(val, deriv)
        elif type(self) == dual and type(other) != dual:
            # other is a scalar, self is a dual
            val = self.val + other
            deriv = self.deriv # deriv of scalar is 0
            return dual(val, deriv)
        elif type(self) == dual and type(other) == dual:
            # both are duals
            val = self.val + other.val
            deriv = self.deriv + other.deriv
            return dual(val, deriv)
    
    def __sub__(self, other):
        if type(self) != dual and type(other) != dual:
            # neither are duals
            return self - other
        elif type(self) != dual and type(other) == dual:
            # self is a scalar, other is a dual
            val = self - other.val
            deriv = other.deriv # deriv of scalar is 0
            return dual(val, deriv)
        elif type(self) == dual and type(other) != dual:
            # other is a scalar, self is a dual
            val = self.val - other
            deriv = self.deriv # deriv of scalar is 0
            return dual(val, deriv)
        elif type(self) == dual and type(other) == dual:
            # both are duals
            val = self.val - other.val
            deriv = self.deriv - other.deriv
            return dual(val, deriv)
        
    def __mul__(self, other):
        if type(self) != dual and type(other) != dual:
            # neither are duals
            return self * other
        elif type(self) != dual and type(other) == dual:
            # self is a scalar
            val = self * other.val
            deriv = self * other.deriv
            return dual(val, deriv)
        elif type(self) == dual and type(other) != dual:
            # other is a scalar
            val = self.val * other
            deriv = self.deriv * other
            return dual(val, deriv)
        elif type(self) == dual and type(other) == dual:
            # both are duals
            val = self.val * other.val
             # product rule, f'g + fg'
            deriv = (self.deriv * other.val) + (self.val * other.deriv)
            return dual(val, deriv)
    
    def __truediv__(self, other):
        if type(self) != dual and type(other) != dual:
            # neither are duals
            return self / other
        elif type(self) != dual and type(other) == dual:
            # self is a scalar
            val = self / other.val
            deriv = self / other.deriv
            return dual(val, deriv)
        elif type(self) == dual and type(other) != dual:
            # other is a scalar
            val = self.val / other
            deriv = self.deriv / other
            return dual(val, deriv)
        elif type(self) == dual and type(other) == dual:
            # both are duals
            val = self.val / other.val
             # quotient rule, (f'g - fg')/g^2
            deriv = ((self.deriv * other.val) - (self.val * other.deriv)) / (other.val ** 2)
            return dual(val, deriv)
        return
    
    def __pow__(self, other):
        if type(self) != dual and type(other) != dual:
            # neither are duals
            return self ** other
        elif type(self) != dual and type(other) == dual:
            # self is a scalar
            val = self ** other.val
            deriv = (self ** other.val) * np.log(self) * other.deriv
            return dual(val, deriv)
        elif type(self) == dual and type(other) != dual:
            # other is a scalar
            val = self.val ** other
            deriv = other * (self.val ** (other - 1)) * self.deriv
            return dual(val, deriv)
        elif type(self) == dual and type(other) == dual:
            # both are duals
            return exp(other * log(self)) # use overloaded log, *, and exp
    
    def __neg__(self):
        return dual(-1., 0.) * self
    
    def __abs__(self):
        if type(self) != dual:
            return np.abs(self)
        else:
            val = np.abs(self.val)
            deriv = self.deriv * np.sign(self.val)
            return dual(val, deriv)

def exp(x=dual):
    val = np.exp(x.val)
    deriv = np.exp(x.val) * x.deriv
    return dual(val, deriv)

def log(x=dual):
    val = np.log(x.val)
    deriv = x.deriv / x.val
    return dual(val, deriv)

def sqrt(x=dual):
    return

def sin(x=dual):
    val = np.sin(x.val)
    deriv = np.cos(x.val) * x.deriv
    return dual(val, deriv)

def cos(x=dual):
    val = np.cos(x.val)
    deriv = -np.sin(x.val) * x.deriv
    return dual(val, deriv)

def tan(x=dual):
    val = np.tan(x.val)
    deriv = (np.sec(x.val) ** 2) * x.deriv
    return dual(val, deriv)

def cot(x=dual):
    val = np.cot(x.val)
    deriv = -(np.csc(x.val) ** 2) * x.deriv
    return dual(val, deriv)

def sec(x=dual):
    val = np.sec(x.val)
    deriv = np.sec(x.val) * np.tan(x.val) * x.deriv
    return

def csc(x=dual):
    val = np.csc(x.val)
    deriv = -np.csc(x.val) * np.cot(x.val) * x.deriv
    return dual(val, deriv)

def asin(x=dual):
    return

def acos(x=dual):
    return

def atan(x=dual):
    return