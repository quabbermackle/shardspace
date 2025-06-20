def kutta4(f, h, y, t, misc, **kwargs):
	k0 = f(t, y, misc, **kwargs)
	k1 = f(t + h*0.3333333333333333, y + h*(0.3333333333333333*k0), misc, **kwargs)
	k2 = f(t + h*0.6666666666666666, y + h*(-0.3333333333333333*k0 + 1.0*k1), misc, **kwargs)
	k3 = f(t + h*1.0, y + h*(1.0*k0 + -1.0*k1 + 1.0*k2), misc, **kwargs)
	ynew = y + h*(0.125*k0 + 0.375*k1 + 0.375*k2 + 0.125*k3)
	return ynew
