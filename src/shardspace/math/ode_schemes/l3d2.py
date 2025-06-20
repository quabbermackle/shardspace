def l3d2(f, h, y, t, misc, **kwargs):
	k0 = f(t, y + h*(0.5*k0 + 0.5*k1), misc, **kwargs)
	k1 = f(t + h*1.0, y + h*(-0.5*k0 + 0.5*k1), misc, **kwargs)
	ynew = y + h*(0.5*k0 + 0.5*k1)
	return ynew
