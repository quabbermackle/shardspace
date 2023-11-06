# script for testing automatic differentiation routines

from nderiv import *

if __name__=='__main__':
    # unit tests
    '''
    testscalar = 1
    testvector = np.array([2,3,4])
    testarray = np.concatenate([np.atleast_1d(testscalar), testvector])
    print(testarray)
    '''

    test = nderiv(np.array([2, 1, 0]), 3)
    print(test.val(), test.dvec, test.order)
    print('test = ', test)
    print(str(test))

    testsum = lambda x : 3 + x
    print(testsum(2))
    test2 = nderiv(3, order=3)
    print('addition test: ', testsum(test))
    print((test + test2))

    testsub = lambda x : 3 - x
    print('subtraction test: ', testsub(test))
    print((test - test2))

    testmul = lambda x,y : x * y
    print('multiplication test: ', testmul(3, test))
    print((test * test2))
    print((test * test))

    print('division test: ', (test / test2))

    print('exponent test: ', (test ** 2))

    print('total test: ', (test + test2 * (test / test2)))

    print('exp test: ', exp(test), '; numpy: ', np.exp(2))

    print('log test: ', log(test), '; numpy: ', np.log(2))

    #print('0th order test: ', nderiv(value=1, order=0))

    print('sin test: ', sin(test), '; numpy: ', np.sin(2))

    print('cos test: ', cos(test), '; numpy: ', np.cos(2))

    testxy = lambda x,y : (x**2 - cos(y))*((5*x*y + 7))
    print('(x^2 - cos(y)) * (5xy + 7): ', testxy(test, test2))

    # example from documentation on the auto_diff package
    x_auto_diff = nderiv([3, 1], order=1)
    print('auto_diff test: ')
    print(f'x = {x_auto_diff} (should be val=3, der=1)')
    y = x_auto_diff**2
    print(f'y = x**2 = {y} (should be val=9, der=6)')
    z = sin(y)
    zval = np.sin(y.val())
    zder = np.cos(y.val())*y.derivs()[0]
    print(f'z = sin(y) = {z} (should be val={zval}, der={zder}')

    # example from Fraysse and Suarel
    #f = lambda x : sin(x) + x**2
    #f0 = lambda x : np.sin(x) + x**2
    #f1 = lambda x : np.cos(x) + 2*x
    #f2 = lambda x : -np.sin(x) + 2
    #f3 = lambda x : -np.cos(x)
    print('\n\nanalytical test:')
    x = 2
    y = 3
    print(f'x = {x}, const = {y}\n')
    x3 = nderiv([x,1], order=3) # independent variable
    y3 = nderiv(y, order=3) # dependent variable
    
    print('x + const')
    f = x3 + y
    f0 = x + y
    f1 = 1
    f2 = 0
    f3 = 0
    print('autodiff:')
    print(f)
    print(f'analytical: [{f0}, {f1}, {f2}, {f3}]\n')

    print('x - const')
    f = x3 - y
    f0 = x - y
    f1 = 1
    f2 = 0
    f3 = 0
    print('autodiff:')
    print(f)
    print(f'analytical: [{f0}, {f1}, {f2}, {f3}]\n')

    print('const + x')
    f = y + x3
    f0 = y + x
    f1 = 1
    f2 = 0
    f3 = 0
    print('autodiff:')
    print(f)
    print(f'analytical: [{f0}, {f1}, {f2}, {f3}]\n')

    print('const - x')
    f = y - x3
    f0 = y - x
    f1 = -1
    f2 = 0
    f3 = 0
    print('autodiff:')
    print(f)
    print(f'analytical: [{f0}, {f1}, {f2}, {f3}]\n')

    print('x * const')
    f = x3 * y
    f0 = x * y
    f1 = y
    f2 = 0
    f3 = 0
    print('autodiff:')
    print(f)
    print(f'analytical: [{f0}, {f1}, {f2}, {f3}]\n')

    print('const * x')
    f = y * x3
    f0 = y * x
    f1 = y
    f2 = 0
    f3 = 0
    print('autodiff:')
    print(f)
    print(f'analytical: [{f0}, {f1}, {f2}, {f3}]\n')

    print('-x + const')
    f = -x3 + y
    f0 = -x + y
    f1 = -1
    f2 = 0
    f3 = 0
    print('autodiff:')
    print(f)
    print(f'analytical: [{f0}, {f1}, {f2}, {f3}]\n')

    print('x / const')
    f = x3 / y
    f0 = x / y
    f1 = 1 / y
    f2 = 0
    f3 = 0
    print('autodiff:')
    print(f)
    print(f'analytical: [{f0}, {f1}, {f2}, {f3}]\n')

    print('const / x')
    f = y / x3
    f0 = y * (x**-1)
    f1 = (-1*y) * (x**-2)
    f2 = (-2*-1*y) * (x**-3)
    f3 = (-3*-2*-1*y) * (x**-4)
    print('autodiff:')
    print(f)
    print(f'analytical: [{f0}, {f1}, {f2}, {f3}]\n')

    '''
    order = 3
    print('order = ', order)
    for n in range(order+1):
        print('n = ', n)
        for i in range(n+1):
            print('i = ', i)
    '''