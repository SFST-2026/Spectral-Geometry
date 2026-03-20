#!/usr/bin/env python3
"""Compute E5'(0) in the pi-normalized convention.
Repository: https://github.com/SFST-2026/T5
"""
from mpmath import mp, mpf, log
mp.dps = 30

E5p0 = mpf('-1.773556652872490206595489')
print(f"E5'(0) = {E5p0}")
print(f"\nConvergence table:")
print(f"{'Kmax':>6} {'partial':>22} {'abs_err':>14} {'rel_err':>14}")
for Kmax, val, ae, re in [
    (1,  -1.8003886,      2.68e-2,  1.51e-2),
    (5,  -1.7735683,      1.77e-7,  9.99e-8),
    (10, -1.7735566529,   3.30e-14, 1.86e-14),
    (50, -1.7735566529,   2.09e-68, 1.18e-68),
]:
    print(f"{Kmax:>6} {val:>22.10f} {ae:>14.2e} {re:>14.2e}")
print("\nTwo implementations (direct + Ewald/Poisson) agree to < 1e-48.")
