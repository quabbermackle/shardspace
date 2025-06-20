def dirkc3(f, h, y, t, misc, **kwargs):
	k0 = f(t + h*0.7886751345948129, y + h*(0.7886751345948129*k0), misc, **kwargs)
	k1 = f(t + h*0.21132486540518713, y + h*(-0.5773502691896257*k0 + 0.7886751345948129*k1), misc, **kwargs)
	ynew = y + h*(0.5*k0 + 0.5*k1)
	return ynew
