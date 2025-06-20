def bwde1(f, h, y, t, misc, **kwargs):
	k0 = f(t + h*1, y + h*(1*k0), misc, **kwargs)
	ynew = y + h*(1*k0)
	return ynew
