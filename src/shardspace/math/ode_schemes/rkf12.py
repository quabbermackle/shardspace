def rkf12(f, h, y, t, misc, **kwargs):
	k0 = f(t, y, misc, **kwargs)
	k1 = f(t + h*0.5, y + h*(0.5*k0), misc, **kwargs)
	k2 = f(t + h*1.0, y + h*(0.00390625*k0 + 0.99609375*k1), misc, **kwargs)
	ynew = y + h*(0.001953125*k0 + 0.99609375*k1 + 0.001953125*k2)
	return ynew
