def l3cstarb4(f, h, y, t, misc, **kwargs):
	k0 = f(t, y, misc, **kwargs)
	k1 = f(t + h*0.5, y + h*(0.25*k0 + 0.25*k1), misc, **kwargs)
	k2 = f(t + h*1.0, y + h*(1.0*k1), misc, **kwargs)
	ynew = y + h*(0.16666666666666666*k0 + 0.6666666666666666*k1 + 0.16666666666666666*k2)
	return ynew
