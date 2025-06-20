def r1a3(f, h, y, t, misc, **kwargs):
	k0 = f(t, y + h*(0.25*k0 + -0.25*k1), misc, **kwargs)
	k1 = f(t + h*0.6666666666666666, y + h*(0.25*k0 + 0.4166666666666667*k1), misc, **kwargs)
	ynew = y + h*(0.25*k0 + 0.75*k1)
	return ynew
