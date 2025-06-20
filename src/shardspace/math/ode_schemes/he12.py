def he12(f, h, y, t, misc, **kwargs):
	k0 = f(t, y, misc, **kwargs)
	k1 = f(t + h*1.0, y + h*(1.0*k0), misc, **kwargs)
	ynew = y + h*(0.5*k0 + 0.5*k1)
	return ynew
