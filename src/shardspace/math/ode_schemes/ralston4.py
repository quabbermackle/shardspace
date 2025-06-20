def ralston4(f, h, y, t, misc, **kwargs):
	k0 = f(t, y, misc, **kwargs)
	k1 = f(t + h*0.4, y + h*(0.4*k0), misc, **kwargs)
	k2 = f(t + h*0.45573725, y + h*(0.29697761*k0 + 0.15875964*k1), misc, **kwargs)
	k3 = f(t + h*1.0, y + h*(0.2181004*k0 + -3.05096516*k1 + 3.83286476*k2), misc, **kwargs)
	ynew = y + h*(0.17476028*k0 + -0.55148066*k1 + 1.2055356*k2 + 0.17118478*k3)
	return ynew
