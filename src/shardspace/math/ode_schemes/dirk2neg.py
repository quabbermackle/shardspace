def dirk2neg(f, h, y, t, misc, **kwargs):
	k0 = f(t + h*0.2928932188134524, y + h*(0.2928932188134524*k0), misc, **kwargs)
	k1 = f(t + h*1.0, y + h*(0.7071067811865476*k0 + 0.2928932188134524*k1), misc, **kwargs)
	ynew = y + h*(0.5*k0 + 0.5*k1)
	return ynew
