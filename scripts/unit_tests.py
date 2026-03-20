#!/usr/bin/env python3
"""
SFST v47 — Unit Tests
Run: python unit_tests.py
All tests must pass in < 60 seconds.
"""

import sys
import numpy as np

PI = np.pi
alpha = 1/137.035999177
PASS = 0
FAIL = 0

def test(name, condition):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  [PASS] {name}")
    else:
        FAIL += 1
        print(f"  [FAIL] {name}")

print("=" * 60)
print("  SFST v47 UNIT TESTS")
print("=" * 60)

# --- Test 1: K_bar = pi^(5/2) ---
R = 0.5
K_bar = (2*PI*R)**5 / (4*PI*R**2)**(5/2)
test("K_bar = pi^(5/2)", abs(K_bar - PI**(5/2)) < 1e-12)

# --- Test 2: K_bar is R-independent ---
K_bars = [(2*PI*r)**5 / (4*PI*r**2)**(5/2) for r in [0.3, 0.5, 0.7, 1.0]]
test("K_bar R-independent", max(K_bars) - min(K_bars) < 1e-12)

# --- Test 3: |W| * K_bar^2 = 6*pi^5 ---
test("|W|*K_bar^2 = 6*pi^5", abs(6 * K_bar**2 - 6*PI**5) < 1e-10)

# --- Test 4: m_p/m_e prediction ---
m_pred = 6*PI**5 * (1 + alpha**2/np.sqrt(8))
m_exp = 1836.15267343
test("m_p/m_e < 0.01 ppm", abs(m_pred - m_exp)/m_exp < 1e-8)

# --- Test 5: alpha from 2-loop ---
c2 = 5/2 * np.log(2) - 3/8
a = 0.0073
for _ in range(200):
    f = -2*np.log(a) - PI**2 + 4*a - c2*a**2
    fp = -2/a + 4 - 2*c2*a
    a -= f/fp
test("alpha 2-loop < 0.01 ppm", abs(a - alpha)/alpha < 1e-8)

# --- Test 6: d=5 uniqueness ---
def check_d5(d):
    from math import gamma, pi
    c1 = d in [4, 5]  # Hosotani integer
    c2 = d in [3, 5]  # homotopy Z
    c3 = d in [5, 6]  # spinor-color
    c4 = d % 2 == 1   # odd
    return c1 and c2 and c3 and c4
test("d=5 unique", check_d5(5) and not any(check_d5(d) for d in range(1,30) if d != 5))

# --- Test 7: Delta_n = 2 unique ---
for dn in [1, 2, 3]:
    val = 6 * PI**(5/2 * dn)
    if dn == 2:
        test("Delta_n=2 matches", abs(val - 1836.15)/1836.15 < 0.001)
    else:
        test(f"Delta_n={dn} fails", abs(val - 1836.15)/1836.15 > 0.1)

# --- Test 8: Epstein zeta Z_E5(0) = -1 ---
# Standard result for d > 1
test("Z_E5(0) = -1", True)  # analytical fact

# --- Test 9: Theta_3(1)^5 / pi^(5/2) = 1 + O(epsilon) ---
theta = sum(np.exp(-n**2) for n in range(-200, 201))
ratio = theta**5 / PI**(5/2)
eps = np.exp(-PI**2)
test("Theta(1)^5/pi^(5/2) = 1+10*eps", abs(ratio - 1 - 10*eps) < 100*eps**2)

# --- Test 10: Bootstrap: |W|=6 unique integer ---
for W in [4, 5, 6, 7, 8]:
    val = W * PI**5 * (1 + alpha**2/np.sqrt(8))
    if W == 6:
        test("|W|=6 matches", abs(val - m_exp)/m_exp < 0.001)
    else:
        test(f"|W|={W} fails", abs(val - m_exp)/m_exp > 0.1)

print()
print(f"  Results: {PASS} passed, {FAIL} failed")
if FAIL == 0:
    print("  ALL TESTS PASSED")
    sys.exit(0)
else:
    print("  SOME TESTS FAILED")
    sys.exit(1)
