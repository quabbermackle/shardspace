'''
Defines nderiv class for automatic differentiation of Nth order derivatives.
This is accomplished by operator overloading.
Designed for cython and numpy.

Matthew Gunther
04/04/2023
'''

import cython as cy
import numpy as np
#cimport numpy as cnp

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
template for operator overload functions in nderiv class

    def __add__(self, other):
        # add other to self
        if type(self) != nderiv and type(other) != nderiv:
            # neither are nderiv
            return self + other
        else:
            # convert to nderiv as needed
            if type(self) != nderiv: self = nderiv(self)
            if type(other) != nderiv: other = nderiv(other)
            order = max(self.order, other.order)
            dvec = np.zeros(order+1)
            self.pad_dvec(order)
            other.pad_dvec(order)
            for i in range(order+1):
                # Levi Eq. 25, add values and derivatives of each order
                dvec[i] = self[i] + other[i]
            return nderiv(dvec, order)
'''

class nderiv():
    __name__ = 'nderiv'
    
    __doc__ =   '''
                Implements the rules for automatic differentiation outlined in
                Levi, Nadav - Numerical integration of ODE's with Automatic differentiation
                The value is stored as nderiv.val, a float
                The derivatives up to order n are stored as nderiv.dvec, a numpy array
                The order of the derivatives to calculate is nderiv.order, an int
                '''

    def __init__(   self,
                    dvec:np.array = np.array([cy.float(0), cy.float(0)]),
                    order:cy.int = cy.int(1)):
        '''
        initialize variable, x, to differentiate with respect to with
            dvec = [x, 1, ...], length = order + 1
        initialize independent variables and constants with
            dvec = [x, 0, ...], length = order + 1
        '''
        # dvec contains value and all derivs up to specified order
        # value is dvec[0], 1st order deriv is dvec[1], etc
        self.dvec = np.atleast_1d(dvec)
        self.order: cy.int = cy.int(order)
        if len(self.dvec) > self.order+1:
            order = len(self.dvec) - 1 # uses dvec length to define order
        self.pad_dvec(self.order)

    def __repr__(self): #also called when invoking self.__str__()
        # representation for printouts
        return f'val, derivs to order {self.order}: {self.val()}, {self.derivs()}'

    def __len__(self): return self.dvec.__len__()

    def __getitem__(self, key): return self.dvec.__getitem__(key)

    def __setitem__(self, key, value): self.dvec.__setitem__(key, value)

    def __delitem__(self, key): self.dvec.__delitem__(key)

    def __iter__(self): return self.dvec.__iter__()

    def val(self):
        # method to extract value in a more readable way than indexing dvec manually
        return self[0]

    def derivs(self):
        # method to extract derivs in a more readable way than indexing dvec manually
        return self[1:]

    def pad_dvec(self, order):
        if len(self) < order+1:
            # add zeros so len(dvec) = order + 1
            self.dvec = np.pad(self.dvec, (0, order+1-len(self)), constant_values=0)

    def __add__(self, other):
        # add other to self
        if type(self) != nderiv and type(other) != nderiv:
            # neither are nderiv
            return self + other
        else:
            # convert to nderiv as needed
            if type(self) != nderiv: self = nderiv(self)
            if type(other) != nderiv: other = nderiv(other)
            order = max(self.order, other.order)
            dvec = np.zeros(order+1)
            self.pad_dvec(order)
            other.pad_dvec(order)
            for i in range(order+1):
                # Levi Eq. 25, add values and derivatives of each order
                dvec[i] = self[i] + other[i]
            return nderiv(dvec, order)

    def __radd__(self, other):
        # add self to other
        if type(self) != nderiv and type(other) != nderiv:
            # neither are nderiv
            return other + self
        else:
            # convert to nderiv as needed
            if type(self) != nderiv: self = nderiv(self)
            if type(other) != nderiv: other = nderiv(other)
            order = max(self.order, other.order)
            dvec = np.zeros(order+1)
            self.pad_dvec(order)
            other.pad_dvec(order)
            for i in range(order+1):
                # Levi Eq. 25, add values and derivatives of each order
                dvec[i] = other[i] + self[i]
            return nderiv(dvec, order)
    
    def __sub__(self, other):
        # subtract other from self
        if type(self) != nderiv and type(other) != nderiv:
            # neither are nderiv
            return self - other
        else:
            # convert to nderiv as needed
            if type(self) != nderiv: self = nderiv(self)
            if type(other) != nderiv: other = nderiv(other)
            order = max(self.order, other.order)
            dvec = np.zeros(order+1)
            self.pad_dvec(order)
            other.pad_dvec(order)
            # Levi Eq. 25, subtract values and derivatives of each order
            for i in range(order+1):
                dvec[i] = self[i] - other[i]
            return nderiv(dvec, order)
    
    def __rsub__(self, other):
        # subtract self from other
        if type(self) != nderiv and type(other) != nderiv:
            # neither are nderiv
            return other - self
        else:
            # convert to nderiv as needed
            if type(self) != nderiv: self = nderiv(self)
            if type(other) != nderiv: other = nderiv(other)
            order = max(self.order, other.order)
            dvec = np.zeros(order+1)
            self.pad_dvec(order)
            other.pad_dvec(order)
            # Levi Eq. 25, subtract values and derivatives of each order
            for i in range(order+1):
                dvec[i] = other[i] - self[i]
            return nderiv(dvec, order)

    def __mul__(self, other):
        # multiply self by other
        if type(self) != nderiv and type(other) != nderiv:
            # neither are nderiv
            return self * other
        else:
            # convert both to nderiv as needed
            if type(self) != nderiv: self = nderiv(self)
            if type(other) != nderiv: other = nderiv(other)
            order = max(self.order, other.order)
            dvec = np.zeros(order+1)
            self.pad_dvec(order)
            other.pad_dvec(order)
            # Levi Eq. 26, product rule generalized to nth derivative
            for n in range(order+1):
                for i in range(n+1):
                    dvec[n] += self[i] * other[n - i]
            return nderiv(dvec, order)

    def __rmul__(self, other):
        # multiply other by self
        if type(self) != nderiv and type(other) != nderiv:
            # neither are nderiv
            return other * self
        else:
            # convert both to nderiv as needed
            if type(self) != nderiv: self = nderiv(self)
            if type(other) != nderiv: other = nderiv(other)
            order = max(self.order, other.order)
            dvec = np.zeros(order+1)
            self.pad_dvec(order)
            other.pad_dvec(order)
            # Levi Eq. 26, product rule generalized to nth derivative
            for n in range(order+1):
                for i in range(n+1):
                    dvec[n] += other[i] * self[n - i]
            return nderiv(dvec, order)

    def __truediv__(self, other):
        # divide self by other
        if type(self) != nderiv and type(other) != nderiv:
            # neither are nderiv
            return self / other
        else:
            # convert both to nderiv as required
            if type(self) != nderiv: self = nderiv(self)
            if type(other) != nderiv: other = nderiv(other)
            order = max(self.order, other.order)
            dvec = np.zeros(order+1)
            self.pad_dvec(order)
            other.pad_dvec(order)
            # Levi Eq. 27, quotient rule generalized to nth derivative
            q0_inv = 1 / other[0]
            for n in range(order+1):
                for i in range(1, n+1):
                    dvec[n] += dvec[n - i] * other[i]
                dvec[n] = q0_inv * (self[n] - dvec[n])
            return nderiv(dvec, order)

    def __rtruediv__(self, other):
        # divide other by self
        if type(self) != nderiv and type(other) != nderiv:
            # neither are nderiv
            return other / self
        else:
            # convert both to nderiv as required
            if type(self) != nderiv: self = nderiv(self)
            if type(other) != nderiv: other = nderiv(other)
            order = max(self.order, other.order)
            dvec = np.zeros(order+1)
            self.pad_dvec(order)
            other.pad_dvec(order)
            # Levi Eq. 27, quotient rule generalized to nth derivative
            q0_inv = 1 / self[0]
            for n in range(order+1):
                for i in range(1, n+1):
                    dvec[n] += dvec[n - i] * self[i]
                dvec[n] = q0_inv * (other[n] - dvec[n])
            return nderiv(dvec, order)
    
    def __pow__(self, other):
        # raise self to the power of other
        if type(self) != nderiv and type(other) != nderiv:
            # neither are nderiv
            return self ** other
        if type(other) == nderiv:
            raise RuntimeError('Can only raise nderiv to a constant!')
        if other == 1.:
            return self # Levi Eq. 30 doesn't handle constant = 1
        else:
            # Levi Eq. 30, requires other to be a constant != 1
            dvec = np.zeros(self.order+1)
            dvec[0] = self.val() ** other
            p0_inv = 1 / self[0]
            for n in range(1, self.order+1):
                for i in range(n):
                    dvec[n] += ((other * n) - ((other + 1) * i)) * dvec[i] * self[n - i]
                dvec[n] = (p0_inv / n) * dvec[n]
            return nderiv(dvec, self.order)
    
    def __lt__(self, other):
        if type(self) != nderiv and type(other) != nderiv:
            return self < other
        elif type(self) == nderiv and type(other) != nderiv:
            return self.val() < other
        elif type(self) != nderiv and type(other) == nderiv:
            return self < other.val()
        else:
            return self.val() < other.val()
    def __le__(self, other):
        if type(self) != nderiv and type(other) != nderiv:
            return self <= other
        elif type(self) == nderiv and type(other) != nderiv:
            return self.val() <= other
        elif type(self) != nderiv and type(other) == nderiv:
            return self <= other.val()
        else:
            return self.val() <= other.val()
    def __eq__(self, other):
        if type(self) != nderiv and type(other) != nderiv:
            return self == other
        elif type(self) == nderiv and type(other) != nderiv:
            return self.val() == other
        elif type(self) != nderiv and type(other) == nderiv:
            return self == other.val()
        else:
            return self.val() == other.val()
    def __ne__(self, other):
        if type(self) != nderiv and type(other) != nderiv:
            return self != other
        elif type(self) == nderiv and type(other) != nderiv:
            return self.val() != other
        elif type(self) != nderiv and type(other) == nderiv:
            return self != other.val()
        else:
            return self.val() != other.val()
    def __gt__(self, other):
        if type(self) != nderiv and type(other) != nderiv:
            return self > other
        elif type(self) == nderiv and type(other) != nderiv:
            return self.val() > other
        elif type(self) != nderiv and type(other) == nderiv:
            return self > other.val()
        else:
            return self.val() > other.val()
    def __ge__(self, other):
        if type(self) != nderiv and type(other) != nderiv:
            return self >= other
        elif type(self) == nderiv and type(other) != nderiv:
            return self.val() >= other
        elif type(self) != nderiv and type(other) == nderiv:
            return self >= other.val()
        else:
            return self.val() >= other.val()

    def __neg__(self): return self*-1

    def __int__(self): return int(self[0])
    def __float__(self): return float(self[0])

    def exp(self): return exp(self)

    def log(self): return log(self)

    def sin(self): return sin(self)

    def cos(self): return cos(self)
    
def exp(p:nderiv):
    # raise e to the power of p
    if type(p) != nderiv:
        # fall back to numpy if called with another type
        return np.exp(p)
    else:
        # Levi Eq. 28
        dvec = np.zeros(p.order+1)
        dvec[0] = np.exp(p.val())
        for n in range(1, p.order+1):
            for i in range(n):
                dvec[n] += (n - i) * dvec[i] * p[n - i]
            dvec[n] = (1 / np.math.factorial(n)) * dvec[n]
        return nderiv(dvec, p.order)

def log(p:nderiv):
    # natural logarithm of p
    if type(p) != nderiv:
        # fall back to numpy
        return np.log(p)
    else:
        # Levi Eq. 29
        dvec = np.zeros(p.order+1)
        dvec[0] = np.log(p.val())
        p0_inv = 1 / p.dvec[0]
        for n in range(1, p.order+1):
            for i in range(1, n):
                dvec[n] += (n - i) * p[i] * dvec[n - i]
            dvec[n] = p0_inv * (p[n] - ((1 / np.math.factorial(n)) * dvec[n]))
        return nderiv(dvec, p.order)

def cos(p:nderiv):
    # cosine of p, assumes p in radians
    if type(p) != nderiv:
        # fall back to numpy
        return np.cos(p)
    else:
        # Levi Eq. 31
        dvec = np.zeros(p.order+1)
        dvec[0] = np.cos(p.val())
        if p.order-1 == 0:
            # stop recursion at order 0 (no derivatives)
            sinp = [np.sin(p.val())]
        else:
            # recursive call to nderiv.sin
            psub1 = nderiv(p.dvec[:-1], p.order-1) # decrement order to prevent recursion loop
            sinp = sin(psub1) # note this is nderiv sin
        for n in range(1, p.order+1):
            for i in range(n):
                dvec[n] += (n - i) * sinp[i] * p[n - i]
            dvec[n] = (-1 / np.math.factorial(n)) * dvec[n]
        return nderiv(dvec, p.order)

def sin(p:nderiv):
    # sine of p, assumes p in radians
    if type(p) != nderiv:
        # fall back to numpy
        return np.sin(p)
    else:
        # Levi Eq. 32
        dvec = np.zeros(p.order+1)
        dvec[0] = np.sin(p.val())
        if p.order-1 == 0:
            # stop recursion at order 0 (no derivatives)
            cosp = [np.cos(p.val())]
        else:
            # recursive call to nderiv.cos
            psub1 = nderiv(p.dvec[:-1], p.order-1) # decrement order to prevent recursion loop
            cosp = cos(psub1) # note this is nderiv sin
        for n in range(1, p.order+1):
            for i in range(n):
                dvec[n] += (n - i) * cosp[i] * p[n - i]
            dvec[n] = (1 / np.math.factorial(n)) * dvec[n]
        return nderiv(dvec, p.order)

def sqrt(x:nderiv):
    # square root of x
    if type(x) != nderiv:
        # fall back to numpy
        return np.sqrt(x)
    else:
        return x ** 0.5

# trig functions defined in terms of sin() and cos()

def tan(x:nderiv): return sin(x) / cos(x)

def cot(x:nderiv): return cos(x) / sin(x)

def csc(x:nderiv): return 1 / sin(x)

def sec(x:nderiv): return 1 / cos(x)

def cot(x:nderiv): return 1 / tan(x)

# hyperbolic trig functions defined in terms of exp()

def sinh(x:nderiv): return (exp(x) - exp(-x)) / 2

def cosh(x:nderiv): return (exp(x) + exp(-x)) / 2

def tanh(x:nderiv): return (exp(2*x) - 1) / (exp(2*x) + 1)

def coth(x:nderiv): return (exp(2*x) + 1) / (exp(2*x) - 1)

def sech(x:nderiv): return 2 / (exp(x) + exp(-x))

def csch(x:nderiv): return 2 / (exp(x) - exp(-x))

# inverse hyperbolic trig functions defined in terms of log()

def arcsinh(x:nderiv): return log(x + (x**2 + 1)**0.5)

def arccosh(x:nderiv): return log(x + (x**2 - 1)**0.5)

def arctanh(x:nderiv): return 0.5 * log((1 + x) / (1 - x))

def arccoth(x:nderiv): return 0.5 * log((x + 1) / (x - 1))

def arcsech(x:nderiv): return log((1/x) + ((1/(x**2)) - 1)**0.5)

def arccsch(x:nderiv): return log((1/x) + ((1/(x**2)) + 1)**0.5)