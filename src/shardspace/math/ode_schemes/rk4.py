def rk4(f, h, y, t, misc, **kwargs):
	k0 = f(t, y, misc, **kwargs)
	k1 = f(t + h*0.5, y + h*(0.5*k0), misc, **kwargs)
	k2 = f(t + h*0.5, y + h*(0.5*k1), misc, **kwargs)
	k3 = f(t + h*1.0, y + h*(1.0*k2), misc, **kwargs)
	ynew = y + h*(0.16666666666666666*k0 + 0.3333333333333333*k1 + 0.3333333333333333*k2 + 0.16666666666666666*k3)
	return ynew
