def dirkks2(f, h, y, t, misc, **kwargs):
	k0 = f(t + h*0.5, y + h*(0.5*k0), misc, **kwargs)
	k1 = f(t + h*1.5, y + h*(-0.5*k0 + 2.0*k1), misc, **kwargs)
	ynew = y + h*(-0.5*k0 + 1.5*k1)
	return ynew
