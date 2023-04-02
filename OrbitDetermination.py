# Matthew Gunther
# November 2022

def KF(xhat_0, Xstar_0, P_0):
    
    pass

"""
Kalman filter (sequential computation algorithm)
nomenclature & algorithm from Tapley, Schutz, and Born

Given xhat_k-1, P_k-1, Xstar_k-1, and Rk,
and the observation Y_k, at t_k

input xhat_0
input Xstar_0
input P_0

Notation:
Xhat    = estimated state
X       = true state
Xstar   = nominal state
Y       = observations
y       = observation deviation vector
x       = state deviation vector
Htilde  = mapping matrix, y to x
eps     = random vector of noise in observations
Phi     = state transition matrix, maps x at t0 to t (matrizant)
          linear term in Taylor expansion of state vector at t about state vector at reference time t0

Kalman filter recursively uses these equations:
Eq 4.7.1:   xbar_k = Phi(t_k, t_j) * xhat_j
            Pbar_k = Phi(t_k, t_j) * P_j * Phi^T(t_k, t_j)
Eq 4.7.11:  K = Pbar * H^T * (H*Pbar*H^T + R)^-1
Eq 4.7.12:  P = (I - K*H)
    alt:    P = (I - K*H) * Pbar * (I - K*H)^T + K*R*K^T
Eq 4.7.16:  xhat = xbar + K * (y - H*xbar)

Algorithm:
(1) Integrate from t_k-1 to tk
dXstar = F(Xstar, t)
dPhi(t, t_k-1) = A(t) * Phi(t, t_k-1)
Xstar(t_k-1) = Xstar_k-1
Phi(t_k-1, t_k-1) = I

(2) Compute
xbar_k = Phi(t_k, t_k-1) * xhat_k-1
Pbar_k = Phi(t_k, t_k-1) * P_k-1 * PhiT(t_k, t_k-1)

(3) Compute
y_k = Y_k - G(Xstar_k, t_k)
Htilde_k = pdG(Xstar_k, t_k) / pdX

(4) Compute the measurement update
K_k = Pbar_k * HtildeT_k * ((Htilde_k * Pbar_k * HtildeT_k) + R_k)^-1
xhat_k = xbar_k + K_k * (y_k - Htilde_k * xbar_k)
P_k = (I - K_k * Htilde_k) * Pbar_k

(5) replace k with k+1 and return to (1)

Algorithm (same as above)
initialize at t0
Set i = 1
Set values of t_i-1 = t0 and Xstar(t_i-1) = Xstar0
xhat_i-1 = xbar0
P_i-1 = Pbar0

(A) Read the next observation: t_i, Y_i, R_i

Integrate reference trajectory and state transition matrix
    from t_i-1 to t_i
dXstar = F(Xstar(t), t) with initial conditions Xstar(t_i-1)
A(t) = (pdF(X, t) / pdX)*
    where * means evaluated on the nominal trajectory
dPhi(t, t_i-1) = A(t) * Phi(t, t_i-1)
    with initial conditions Phi(t_i-1, t_i-1) = I
This gives Xstar(t_i), Phi(t_i, t_i-1)

Time Update
xbar_i = Phi(t_i, t_i-1) * xhat_i-1
Pbar_i = Phi(t_i, t_i-1) * P_i-1 * PhiT(t_i, t_i-1)

Compute: observation deviation, observation-state matrix, gain matrix
y_i = Y_i - G(Xstar_i, t_i)
Htilde_i = (pdG(X, t_i) / pdX)*
K_i = Pbar_i * HtildeT_i * (Htilde_i * Pbar_i * HtildeT_i + R_i)^-1

Measurement Update
xhat_i = xbar_i + K_i * (y_i - Htilde_i * xbar_i)
P_i = (I - K_i * Htilde_i) * Pbar_i
i = i + 1
Thus: t_i becomes t_i-1, Xstar(t_i) becomes Xstar(t_i-1)

Have all observations been read?
No: to (A)
Yes: STOP

Algorithm 3 (https://thekalmanfilter.com/kalman-filter-python-example/)
X = state
P = covariance matrix, sigma^2 on diagonal
A, Phi = state transition matrix
H = state to measurement transition matrix
R = input measurement variance
Q = system noise covariance matrix
x_p = predicted state
P_p = predicted state covariance matrix

propagate existing state and covariance through time
x_p = A*x
P_p = A*P*A^T + Q

K = Kalman gain
S = the innovation
S = H*P_p*H^T + R
K = P * H^T * S^-1

x = new state
P = new state covariance estimate
x = x_p + K*(z - H*x_p)
P = P_p - K*H*P_p

State transition matrix
[   deltaX    ]     [dX/dX0    dX/dY0    dX/dXdot0    dX/dYdot0    dX/dZdot0    ] [deltaX0   ]
[   deltaY    ]     [dY/dX0    dY/dY0    dY/dXdot0    dY/dYdot0    dY/dZdot0    ] [deltaY0   ]
[   deltaZ    ]  =  [dZ/dX0    dZ/dY0    dZ/dXdot0    dZ/dYdot0    dZ/dZdot0    ] [deltaZ0   ]
[   deltaXdot ]     [dXdot/dX0 dXdot/dY0 dXdot/dXdot0 dXdot/dYdot0 dXdot/dZdot0 ] [deltaXdot0]
[   deltaYdot ]     [dYdot/dX0 dYdot/dY0 dYdot/dXdot0 dYdot/dYdot0 dYdot/dZdot0 ] [deltaYdot0]
[   deltaZdot ]     [dZdot/dX0 dZdot/dY0 dZdot/dXdot0 dZdot/dYdot0 dZdot/dZdot0 ] [deltaZdot0]

Eq. 4.2.6
xdot(t) = A(t) * x(t)
y_i = Htilde_i * x_i + eps_i
where
A(t) = [pdF(t)/pdX(t)]*
Htilde_i = [pdG/pdX]*_i
x(t) = X(t) - Xstar(t)
x_i = X(t_i) - Xstar(t_i)
y_i = Y_i - G(Xstar_i, t_i)

d2rvec = -mu * rvec / rnorm^3
    d2X = -mu * X / r^3
    d2Y = -mu * Y / r^3
    d2Z = -mu * Z / r^3

State Vector
X = [ X ; Y ; Z ; dX ; dY ; dZ ]

Xdot =  [dX]  = [F1] = [dX]
        [dY]  = [F2] = [dY]
        [dZ]  = [F3] = [dZ]
        [d2X] = [F4] = [-mu*X/r^3]
        [d2Y] = [F5] = [-mu*Y/r^3]
        [d2Z] = [F6] = [-mu*Z/r^3]

A(t) = pdF(Xstar, t) / pdX = [dF1/dX dF1/dY ... dF1/ddZ]
                             [dF2/dX ...        dF2/ddZ]
                             [...       ...     ...    ]
                             [dF6/dX    ...     dF6/ddZ]

Observation Vector
Y = [rta ; dec]

Htilde = pdY/pdX = [drta/dX drta/dY ... drta/ddZ]
                   [ddec/dX ddec/dY ... ddec/ddZ]

General solution to
xdot(t) = A(t) *x(t)
is:
x(t) = Phi(t, t_k) * x_k    Eq. 4.2.7

Phi is the state transition matrix, which has properties
    1. Phi(tk, tk) = I
    2. Phi(ti, tk) = Phi(ti, tj) * Phi(tj, tk)
    3. Phi(ti, tk) = Phi^-1(tk, ti)


"""