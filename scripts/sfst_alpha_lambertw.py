#!/usr/bin/env python3
"""Solve the SFST alpha-relation at 1-loop and 2-loop.
Repository: https://github.com/SFST-2026/T5
"""
from mpmath import mp, mpf, pi, log, exp, lambertw, sqrt
mp.dps = 50

alpha_CODATA = mpf('0.0072973525693')

# --- 1-loop ---
alpha_1L = -mpf(1)/2 * lambertw(-2*exp(-pi**2/2))
res_1L = float((alpha_1L - alpha_CODATA)/alpha_CODATA * 1e6)

# --- 2-loop ---
c2 = mpf(5)/2 * log(2) - mpf(3)/8
alpha = mpf('0.007298')
for _ in range(200):
    alpha = exp(-(pi**2 - 4*alpha + c2*alpha**2)/2)
res_2L = float((alpha - alpha_CODATA)/alpha_CODATA * 1e6)

# --- Mass ratio ---
mp_me_exp = mpf('1836.15267343')
LO  = 6*pi**5
NLO = LO * (1 + alpha_CODATA**2/sqrt(8))

print(f"alpha (1-loop) = {float(alpha_1L):.10f}  residual = {res_1L:.2f} ppm")
print(f"alpha (2-loop) = {float(alpha):.10f}  residual = {res_2L:.4f} ppm")
print(f"c2 = (5/2)ln2 - 3/8 = {float(c2):.10f}")
print(f"m_p/m_e  LO = {float(LO):.5f}   ({float((LO-mp_me_exp)/mp_me_exp*1e6):.2f} ppm)")
print(f"m_p/m_e NLO = {float(NLO):.5f}  ({float((NLO-mp_me_exp)/mp_me_exp*1e9):.2f} ppb)")
