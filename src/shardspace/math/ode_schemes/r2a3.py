def r2a3(f, h, y, t, misc, **kwargs):
	k0 = f(t + h*0.3333333333333333, y + h*(0.4166666666666667*k0 + -0.08333333333333333*k1), misc, **kwargs)
	k1 = f(t + h*1.0, y + h*(0.75*k0 + 0.25*k1), misc, **kwargs)
	ynew = y + h*(0.75*k0 + 0.25*k1)
	return ynew
