def ralston2(f, h, y, t, misc, **kwargs):
	k0 = f(t, y, misc, **kwargs)
	k1 = f(t + h*0.6666666666666666, y + h*(0.6666666666666666*k0), misc, **kwargs)
	ynew = y + h*(0.25*k0 + 0.75*k1)
	return ynew
