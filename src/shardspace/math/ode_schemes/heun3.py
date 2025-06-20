def heun3(f, h, y, t, misc, **kwargs):
	k0 = f(t, y, misc, **kwargs)
	k1 = f(t + h*0.3333333333333333, y + h*(0.3333333333333333*k0), misc, **kwargs)
	k2 = f(t + h*0.6666666666666666, y + h*(0.6666666666666666*k1), misc, **kwargs)
	ynew = y + h*(0.25*k0 + 0.75*k2)
	return ynew
