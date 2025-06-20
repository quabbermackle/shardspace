def bs23(f, h, y, t, misc, **kwargs):
	k0 = f(t, y, misc, **kwargs)
	k1 = f(t + h*0.5, y + h*(0.5*k0), misc, **kwargs)
	k2 = f(t + h*0.75, y + h*(0.75*k1), misc, **kwargs)
	k3 = f(t + h*1.0, y + h*(0.2222222222222222*k0 + 0.3333333333333333*k1 + 0.4444444444444444*k2), misc, **kwargs)
	ynew = y + h*(0.2222222222222222*k0 + 0.3333333333333333*k1 + 0.4444444444444444*k2)
	return ynew
