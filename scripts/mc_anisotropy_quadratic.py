#!/usr/bin/env python3
"""Monte Carlo verification of the quadratic anisotropy lemma.
Repository: https://github.com/SFST-2026/T5
"""
import numpy as np
np.random.seed(42)

R0, M0, N = 0.5, 6*np.pi**5, 100000
print("Monte Carlo anisotropy sensitivity study")
print(f"R0={R0}, M0=6pi^5={M0:.6f}, N={N}\n")
print(f"{'sigma_R':>10} {'M_spread(ppm)':>14} {'P(<10ppm)':>10} {'source':>14}")
for sR in [1e-4, 1e-5, 1e-6]:
    dev = []
    for _ in range(N):
        Rj = np.random.normal(R0, sR, 5)
        Rj *= (R0**5 / np.prod(Rj))**0.2  # volume-preserving projection
        dev.append((6*(2*np.pi)**5*np.prod(Rj) - M0)/M0*1e6)
    d = np.array(dev)
    # Also compute without volume-preserving (global scale dominates)
    dev2 = []
    for _ in range(N):
        Rj = np.random.normal(R0, sR, 5)
        dev2.append((6*(2*np.pi)**5*np.prod(Rj) - M0)/M0*1e6)
    d2 = np.array(dev2)
    print(f"{sR:>10.0e} {np.std(d2):>10.0f} (total) "
          f"{np.mean(np.abs(d2)<10)*100:>5.0f}% "
          f"{'scale' if np.std(d2)>10 else 'aniso':>10}")

# Verify quadratic lemma
e = np.array([.01,-.005,.003,-.002,-.006]); e -= e.mean()
M_ex = 6*(2*np.pi)**5*np.prod(R0*(1+e))
M_qu = M0*(1-0.5*np.sum(e**2))
print(f"\nQuadratic lemma check: |exact-quad|/M0 = {abs(M_ex-M_qu)/M0*1e6:.4f} ppm (O(eps^3))")
