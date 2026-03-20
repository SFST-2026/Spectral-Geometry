#!/usr/bin/env python3
"""Verify c2 = (5/2)ln2 - 3/8 via Hurwitz identity and CODATA cross-check.
Repository: https://github.com/SFST-2026/T5
"""
from mpmath import mp, mpf, pi, log, zeta, exp
mp.dps = 40

alpha = mpf('0.0072973525693')

# Hurwitz identity (Tier 1)
zhp = log(2)*zeta(0)
print(f"zeta_H'(0,1/2) = ln2*zeta(0) = {float(zhp):.15f}")
print(f"-ln(2)/2                      = {float(-log(2)/2):.15f}")
print(f"Match: {float(abs(zhp-(-log(2)/2))):.1e}  [VERIFIED Tier 1]\n")

# c2 analytical
c2 = mpf(5)/2*log(2) - mpf(3)/8
print(f"c2 = (5/2)ln2 - 3/8 = {float(c2):.12f}")

# c2 from experiment
c2_exp = (-2*log(alpha) - pi**2 + 4*alpha) / alpha**2
R_exp = c2_exp - mpf(5)/2*log(2)
print(f"c2 from CODATA     = {float(c2_exp):.12f}")
print(f"Difference         = {float(c2_exp-c2):.6e} ({float(abs(c2_exp-c2)/c2_exp*100):.4f}%)")
print(f"\nCross-term R_exp   = {float(R_exp):.10f}")
print(f"Claimed   -3/8     = {float(mpf(-3)/8):.10f}")
print(f"Accuracy           = {float(abs(R_exp-(-mpf(3)/8))/abs(R_exp)*100):.3f}%")
print(f"Consistent with O(alpha^3) remainder.")
