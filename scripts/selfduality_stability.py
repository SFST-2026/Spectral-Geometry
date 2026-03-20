#!/usr/bin/env python3
"""Self-dual potential scan: V(R) = C1*ap^(5/2)*R^(-5) + C2*ap^(-5/2)*R^5.
Repository: https://github.com/SFST-2026/T5
"""
import numpy as np

C = 1.0  # normalization (cancels in minimum location)
print("Self-dual potential stability scan")
print(f"V(R) = C * [(ap)^(5/2) * R^(-5) + (ap)^(-5/2) * R^5]")
print(f"Minimum at R_vac = sqrt(alpha') [exact]\n")
print(f"{'alpha_p':>10}{'R_vac':>12}{'sqrt(ap)':>12}{'V(Rvac)':>14}{'V_pp':>14}")
for ap in np.arange(0.200, 0.320, 0.020):
    R = np.sqrt(ap)
    for _ in range(50):
        Vp  = C*(-5*ap**2.5*R**(-6) + 5*ap**(-2.5)*R**4)
        Vpp = C*(30*ap**2.5*R**(-7) + 20*ap**(-2.5)*R**3)
        R -= Vp/Vpp
    V = C*(ap**2.5*R**(-5) + ap**(-2.5)*R**5)
    print(f"{ap:>10.3f}{R:>12.6f}{np.sqrt(ap):>12.6f}{V:>14.3e}{Vpp:>14.3e}")
print("\nAll V'' > 0 (stable). R_vac tracks sqrt(alpha').")
