def dirk2(f, h, y, t, misc, **kwargs):
	k0 = f(t + h*0.5, y + h*(0.5*k0), misc, **kwargs)
	ynew = y + h*(1.0*k0)
	return ynew
