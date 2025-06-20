def dirk3four(f, h, y, t, misc, **kwargs):
	k0 = f(t + h*0.5, y + h*(0.5*k0), misc, **kwargs)
	k1 = f(t + h*0.6666666666666666, y + h*(0.16666666666666666*k0 + 0.5*k1), misc, **kwargs)
	k2 = f(t + h*0.5, y + h*(-0.5*k0 + 0.5*k1 + 0.5*k2), misc, **kwargs)
	k3 = f(t + h*1.0, y + h*(1.5*k0 + -1.5*k1 + 0.5*k2 + 0.5*k3), misc, **kwargs)
	ynew = y + h*(1.5*k0 + -1.5*k1 + 0.5*k2 + 0.5*k3)
	return ynew
