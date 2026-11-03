#!/usr/bin/env python3
"""
simulation.py
Proof-of-concept integration of the chiral field equation in a flat FLRW background.
CCCM: Chiral Cyclic Cosmological Model

Equation solved:
    d^2 chi / dN^2 + (3 - Q/2) dchi/dN + (1/H^2) dV/dchi = noise
where N = ln(a), Q = d ln(H^2)/dN, and H(z) = H0 * sqrt(Omega_m (1+z)^3 + Omega_L).
"""

import numpy as np
from scipy.integrate import solve_ivp

# Cosmological parameters (Planck 2018)
H0 = 67.4          # km/s/Mpc
Omega_m = 0.315
Omega_L = 0.685
chi0 = 1e-9        # equilibrium chirality
alpha = 2.0        # symmetry-breaking depth
Gamma_over_H = 0.1 # damping coefficient / H

def V(chi):
    """Symmetry-breaking potential."""
    return (chi / chi0)**4 - alpha * (chi / chi0)**2

def dV_dchi(chi):
    return 4.0 * chi**3 / chi0**4 - 2.0 * alpha * chi / chi0**2

def H_z(z):
    return H0 * np.sqrt(Omega_m * (1.0 + z)**3 + Omega_L)

def z_of_N(N):
    return np.exp(-N) - 1.0

def dydN(N, y):
    chi, dchi = y
    z = z_of_N(N)
    Hz = H_z(z)
    # Friedman acceleration factor Q = d ln H^2 / dN
    a = np.exp(N)
    Q = -3.0 * Omega_m / (Omega_m + Omega_L * a**3)
    # Noise term: small stochastic kick (representing quantum fluctuation)
    noise = 1e-12 * np.random.normal()
    d2chi = -(3.0 - 0.5 * Q + Gamma_over_H) * dchi - dV_dchi(chi) / Hz**2 + noise
    return [dchi, d2chi]

# Initial conditions at z=1e12 -> N = -ln(1+z)
N_start = -np.log(1.0 + 1e12)
N_end = 0.0  # z=0
N_eval = np.linspace(N_start, N_end, 100000)

# Seed: chi ~ 0 with tiny fluctuation
y0 = [1e-10, 0.0]

sol = solve_ivp(dydN, [N_start, N_end], y0, t_eval=N_eval, method='RK45', rtol=1e-8)

z_out = z_of_N(sol.t)
chi_out = sol.y[0]

print(f"Initial chi = {chi_out[0]:.3e}")
print(f"Final chi at z=0 = {chi_out[-1]:.3e}")

# Save output
np.savetxt("chi_evolution.txt", np.column_stack([z_out, chi_out]),
           header="z chi", comments="", fmt="%.6e")
