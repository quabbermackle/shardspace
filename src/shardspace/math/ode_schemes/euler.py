def euler(f, h, y, t, misc, **kwargs):
	k0 = f(t, y, misc, **kwargs)
	ynew = y + h*(1*k0)
	return ynew
