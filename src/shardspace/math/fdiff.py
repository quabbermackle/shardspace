"""
Created on Sat Jun 28 10:26 2025

@author: Matthew

Finite difference codes
Mostly follows LeVeque - Finite Difference Methods for Ordinary and Partial Differential Equations
"""

import numpy as np
from scipy import special

def fdcoeffV(k:int, xbar:float, x:np.ndarray):
    """
    Returns:
        np.ndarray: row vector containing finite difference coefficients
        
    % Compute coefficients for finite difference approximation for the
    % derivative of order k at xbar based on grid values at points in x.
    %
    % WARNING: This approach is numerically unstable for large values of n since
    % the Vandermonde matrix is poorly conditioned.  Use fdcoeffF.m instead,
    % which is based on Fornberg's method.
    %
    % This function returns a row vector c of dimension 1 by n, where n=length(x),
    % containing coefficients to approximate u^{(k)}(xbar), 
    % the k'th derivative of u evaluated at xbar,  based on n values
    % of u at x(1), x(2), ... x(n).  
    %
    % If U is a column vector containing u(x) at these n points, then 
    % c*U will give the approximation to u^{(k)}(xbar).
    %
    % Note for k=0 this can be used to evaluate the interpolating polynomial 
    % itself.
    %
    % Requires length(x) > k.  
    % Usually the elements x(i) are monotonically increasing
    % and x(1) <= xbar <= x(n), but neither condition is required.
    % The x values need not be equally spaced but must be distinct.  
    %
    % From  http://www.amath.washington.edu/~rjl/fdmbook/  (2007)
    """
    
    x = np.array(x)
    
    n = len(x)
    if k >= n: 
        raise Exception("Error: length(x) must be larger than k")
    
    A = np.ones((n,n))
    xrow = (x[:] - xbar).reshape((1,n))    # displacements x-xbar as a row vector.
    
    for i in range(1,n):
        A[i,:] = (xrow**(i)) / special.factorial(i)
        
    b = np.zeros((n,1))                 # b is right hand side
    b[k] = 1                            # so k’th derivative term remains
    c = np.linalg.solve(A, b)           # solve system for coefficients
    
    return c.reshape((1,n))             # row vector

def fdcoeff_index_uniform(order:int, indexes:np.ndarray):
    # Input the indices of the 1D stencil, with xbar assumed = 0
    # Outputs a nicely formatted string showing the difference formula
    
    c = fdcoeffV(k=order, xbar=0, x=indexes)
    p = len(indexes) - order
    
    xstr = [     f' + {np.abs(_x)}*h'   if np.sign(_x) == 1 and _x != 1.0
            else f' + h'                if np.sign(_x) == 1 and _x == 1.0
            else f' - {np.abs(_x)}*h'   if np.sign(_x) == -1 and _x != -1.0
            else f' - h'                if np.sign(_x) == -1 and _x == -1.0
            else  '' for _x in indexes]
    
    cstr = [     f' + {np.abs(_c[0])}*u(xbar{_x})'  if np.sign(_c) == 1 and _c[0] != 1.0
            else f' + u(xbar{_x})'                  if np.sign(_c) == 1 and _c[0] == 1.0
            else f' - {np.abs(_c[0])}*u(xbar{_x})'  if np.sign(_c) == -1 and _c[0] != -1.0
            else f' - u(xbar{_x})'                  if np.sign(_c) == -1 and _c[0] == -1.0
            else '' for _c, _x in zip(c.T, xstr)]
    # cstr[0].lstrip(' +')
    
    out = ''.join([f'D^({k})(xbar) = h**(-{k}) * ('] + cstr + [f'), Order({p}) or better'])
    
    return out, c

if __name__ == '__main__':
    
    # test fdcoeffV
    xbar = 1
    h = 1
    x = np.array([xbar-2*h, xbar-h, xbar])
    k = 1
    c = fdcoeffV(k,xbar,x)
    print(c)
    
    # 1st derivatives ---------------------------------------
    
    # 1st order one-sided +
    out, _ = fdcoeff_index_uniform(1, [1, 0])
    print(out)
    
    # 1st order one-sided -
    out, _ = fdcoeff_index_uniform(1, [0, -1])
    print(out)
    
    # 2nd order centered
    out, _ = fdcoeff_index_uniform(1, [1, -1])
    print(out)
    
    # 3rd order
    out, _ = fdcoeff_index_uniform(1, [1, 0, -1, -2])
    print(out)
    
    # Example 1.2, 2nd order
    idx = np.array([0, -1, -2])
    out, c = fdcoeff_index_uniform(k, idx)
    print(out)
    
    # 2nd derivatives --------------------------------------------
    k = 2
    
    # 2nd order centered
    out, _ = fdcoeff_index_uniform(k, [-1, 0, 1])
    print(out)
    
    # 3rd derivatives ---------------------------------------------
    k = 3
    
    # 1st order uncentered
    out, _ = fdcoeff_index_uniform(k, [2, 1, 0, -1])
    print(out)
    
    # 2nd order centered
    out, _ = fdcoeff_index_uniform(k, [2, 1, -1, -2])
    print(out)
    