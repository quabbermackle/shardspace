def gl4(f, h, y, t, misc, **kwargs):
	k0 = f(t + h*0.21132486540518713, y + h*(0.25*k0 + -0.038675134594812866*k1), misc, **kwargs)
	k1 = f(t + h*0.7886751345948129, y + h*(0.5386751345948129*k0 + 0.25*k1), misc, **kwargs)
	ynew = y + h*(0.5*k0 + 0.5*k1)
	return ynew
