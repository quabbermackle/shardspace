import numpy as np

from Constants_Eberron import ArrahSystem as Eb
import orbits.OrbitBasics as ob
import orbits.Relativity as rel

mult_CS = 1.25

print(Eb.keys())
print(Eb['names'])
#print(Eb['epoch_date'])     # epoch date, GalifarDate object
#print(Eb['epoch_ta'])       # true anomaly at epoch, radians
#print(Eb['r'])              # semimajor axis (circular orbit radius), km

i_K = Eb['names'].index('Khorvaire')
#print('Khorvaire index:', i_K)
i_F = Eb['names'].index('Frostfell')
#print('Frostfell index:', i_F)
r_K = Eb['r'][i_K][0]
print('Khorvaire radius:', r_K)
r_F = Eb['r'][i_F][0]
#print('Frostfell radius:', r_F)
ta_K = float(Eb['epoch_ta'][i_K][1])
print('Khorvaire true anomaly:', ta_K)

x_K, y_K = ob.polar2rect(r_K, ta_K)
print('Khorvaire (x,y) =', x_K, y_K)

r_S = mult_CS * r_F
ta_S = 0.
#print('Sigil (r,theta) =', r_S, ta_S)
x_S, y_S = ob.polar2rect(r_S, ta_S)
print('Sigil (x,y) =', x_S, y_S)

dx = x_S - x_K
print('distance from Khorvaire to Sigil =', dx, 'km')

dt_K = []
accel = [.1, .5, 1, 5, 10] # possible SR
for a in accel:
    dt = rel.flip_ad2t(a, dx)
    dt_K.append(dt) # Khorvaire time elapsed for a flip & burn trajectory
    print('accel =', accel, 'Khorvaire duration =', dt)