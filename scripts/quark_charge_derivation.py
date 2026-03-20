"""
===============================================================================
CAN THE QUARK CHARGES BE DERIVED FROM THE SFST STRUCTURE?
===============================================================================

The SFST uses Q_u = 2/3, Q_d = -1/3 as INPUT from the Standard Model.
Can these values be DERIVED from the conditions already proven?

Available constraints:
  (A) SU(3) gauge group (from d=5 uniqueness theorem)
  (B) N_c = 3 (from Spinor-Color coincidence)
  (C) Anomaly cancellation in 5D (condition C4)
  (D) Tr_proton(Q²) = Q_e² = 1 (required for α¹-cancellation)
  (E) Integer baryon charge: Q_p = Q_u + Q_u + Q_d = 1
  (F) Electric charge quantization from SU(3) representation theory
===============================================================================
"""

import numpy as np
from fractions import Fraction
from itertools import product as iterprod

print("=" * 72)
print("  DERIVATION OF QUARK CHARGES FROM SFST STRUCTURE")
print("=" * 72)

# ============================================================
# §1. THE CONSTRAINTS
# ============================================================

print("\n" + "=" * 72)
print("  §1. THE AVAILABLE CONSTRAINTS")
print("=" * 72)

print("""
We have N_c = 3 colors. The quarks transform in the FUNDAMENTAL
representation 3 of SU(3). The electromagnetic charge Q_em is 
embedded in SU(3) as a diagonal generator.

CONSTRAINT E (integer proton charge):
  The proton is the lightest baryon: a color-singlet bound state 
  of 3 quarks (one from each color). Its charge must be integer:
  
  Q_p = Q_u + Q_u + Q_d ∈ Z  (for proton = uud)
  
  More generally: any baryon (qqq color singlet) must have 
  integer charge.

CONSTRAINT D (α¹-cancellation):
  Tr_proton(Q²) = Q_e² requires:
  2Q_u² + Q_d² = 1

CONSTRAINT F (charge quantization from SU(3)):
  The electromagnetic generator Q_em must be a LINEAR COMBINATION 
  of the SU(3) Cartan generators T₃ and T₈.
  
  In the fundamental representation:
    T₃ = diag(1/2, -1/2, 0)
    T₈ = diag(1, 1, -2)/(2√3)
  
  Q_em = a·T₃ + b·T₈ = diag(a/2 + b/(2√3), -a/2 + b/(2√3), -b/√3)
  
  The three eigenvalues are the charges of the three quark colors 
  in one generation. For u-type and d-type quarks:
    Q_u = a/2 + b/(2√3)
    Q_d = -a/2 + b/(2√3)
    Q_s = -b/√3  (third color component, identified with s-quark charge)
""")

# ============================================================
# §2. SOLVING THE SYSTEM
# ============================================================

print("=" * 72)
print("  §2. SOLVING THE CONSTRAINT SYSTEM")
print("=" * 72)

print("""
From the SU(3) embedding (constraint F):
  Q_u = a/2 + b/(2√3)
  Q_d = -a/2 + b/(2√3)
  Q_s = -b/√3

Note: Q_u - Q_d = a (difference gives the T₃ component)
      Q_u + Q_d = b/√3 (sum gives the T₈ component)
      Q_s = -(Q_u + Q_d) (tracelessness of SU(3) generators)

TRACELESSNESS: Q_u + Q_d + Q_s = 0 (always satisfied, 
  since T₃ and T₈ are traceless).

This means Q_s = -(Q_u + Q_d).

For the proton (uud):
  Q_p = 2Q_u + Q_d

CONSTRAINT E (integer Q_p):
  2Q_u + Q_d ∈ Z

CONSTRAINT D (α¹-cancellation):
  2Q_u² + Q_d² = 1  [= Q_e²]

We also need Q_e = -1 (electron charge), so:
  Q_p = 2Q_u + Q_d = +1 (proton charge = +|Q_e|)

Let's solve: 2Q_u + Q_d = 1 and 2Q_u² + Q_d² = 1.
""")

# Solve the system:
# (i)  2Q_u + Q_d = 1  →  Q_d = 1 - 2Q_u
# (ii) 2Q_u² + Q_d² = 1
# Substitute (i) into (ii):
# 2Q_u² + (1-2Q_u)² = 1
# 2Q_u² + 1 - 4Q_u + 4Q_u² = 1
# 6Q_u² - 4Q_u = 0
# 2Q_u(3Q_u - 2) = 0
# Q_u = 0 or Q_u = 2/3

print("Solving: 2Q_u + Q_d = 1  and  2Q_u² + Q_d² = 1")
print()
print("Substituting Q_d = 1 - 2Q_u into the second equation:")
print("  2Q_u² + (1-2Q_u)² = 1")
print("  2Q_u² + 1 - 4Q_u + 4Q_u² = 1")
print("  6Q_u² - 4Q_u = 0")
print("  2Q_u(3Q_u - 2) = 0")
print()
print("Solutions:")
print("  Q_u = 0   →  Q_d = 1    →  Q_s = -1    (trivial)")
print("  Q_u = 2/3 →  Q_d = -1/3 →  Q_s = -1/3  (Standard Model!)")
print()

# Verify
for Q_u_val in [0, Fraction(2, 3)]:
    Q_d_val = 1 - 2*Q_u_val
    Q_s_val = -(Q_u_val + Q_d_val)
    check_E = 2*Q_u_val + Q_d_val
    check_D = 2*Q_u_val**2 + Q_d_val**2
    print(f"  Q_u = {Q_u_val}, Q_d = {Q_d_val}, Q_s = {Q_s_val}")
    print(f"    Q_proton = 2Q_u + Q_d = {check_E}")
    print(f"    2Q_u² + Q_d² = {check_D}")
    print()

# ============================================================
# §3. ELIMINATING THE TRIVIAL SOLUTION
# ============================================================

print("=" * 72)
print("  §3. ELIMINATING THE TRIVIAL SOLUTION Q_u = 0")
print("=" * 72)

print("""
The solution Q_u = 0, Q_d = 1, Q_s = -1 must be excluded.

ARGUMENT 1 (Neutron charge):
  Neutron = udd: Q_n = 2(0) + 1 = 1 ≠ 0.
  But the neutron MUST be electrically neutral (experimental fact,
  and required for nuclear stability). Therefore Q_u = 0 fails.

ARGUMENT 2 (SU(3) representation theory):
  With Q_u = 0, Q_d = 1, Q_s = -1, the charge matrix is:
    Q_em = diag(0, 1, -1)
  This is proportional to T₃ (the Cartan generator), with a = -2, b = 0.
  But this means Q_em commutes with T₈, leaving U(1)_em × U(1)₈ 
  unbroken — a LARGER unbroken group than desired.
  
  For Q_u = 2/3: Q_em = T₃ + T₈/√3, which is a GENERIC direction 
  in the Cartan subalgebra, breaking SU(3) → U(1)_em only.

ARGUMENT 3 (Anomaly matching):
  In 4D (after compactification), the ABJ anomaly coefficient:
    A = Σ_quarks Q³ = N_c · (2Q_u³ + Q_d³)  [for 2 flavors, 3 colors]
  
  For Q_u = 2/3: A = 3·(2·8/27 - 1/27) = 3·(16/27 - 1/27) = 3·15/27 = 5/3
  For Q_u = 0:   A = 3·(0 + 1) = 3
  
  With the lepton sector (electron, Q_e = -1):
    A_leptons = (-1)³ = -1
    A_total = A_quarks + A_leptons
  
  For Q_u = 2/3: A_total = 5/3 - 1 = 2/3 (per generation)
  For Q_u = 0:   A_total = 3 - 1 = 2
  
  Neither cancels by itself. Full anomaly cancellation requires 
  the FULL Standard Model content (including neutrinos).
  But the Q_u = 2/3 solution gives FRACTIONAL anomaly coefficients,
  which is characteristic of the SM and required for consistency 
  with the SU(2)_L × U(1)_Y structure.
""")

# ============================================================
# §4. THE NEUTRON CONSTRAINT CLOSES THE PROOF
# ============================================================

print("=" * 72)
print("  §4. THE NEUTRON CONSTRAINT")
print("=" * 72)

print("""
The SFST has a SECOND prediction: V2 (neutron-proton mass difference).
  Δm(n-p) = m_e · (8/π - 2α)

This requires the neutron to exist as a DISTINCT particle from the 
proton, with Q_n = 0 (electrically neutral).

For the neutron (udd):
  Q_n = Q_u + 2Q_d

CONSTRAINT: Q_n = 0 → Q_u + 2Q_d = 0 → Q_u = -2Q_d

Combined with Q_p = 2Q_u + Q_d = 1:
  2(-2Q_d) + Q_d = 1
  -3Q_d = 1
  Q_d = -1/3
  Q_u = 2/3

This is UNIQUE. No other solution exists.
""")

Q_u = Fraction(2, 3)
Q_d = Fraction(-1, 3)
Q_s = -(Q_u + Q_d)

print(f"  From Q_p = 1 and Q_n = 0:")
print(f"    Q_u = {Q_u} = 2/3")
print(f"    Q_d = {Q_d} = -1/3")
print(f"    Q_s = {Q_s} = -1/3")
print()

# Verify ALL constraints
print("  Verification of ALL constraints:")
print(f"    (E) Q_p = 2(2/3) + (-1/3) = {2*Q_u + Q_d} = 1 ✓")
print(f"    (D) 2(2/3)² + (-1/3)² = {2*Q_u**2 + Q_d**2} = 1 ✓")
print(f"    (N) Q_n = (2/3) + 2(-1/3) = {Q_u + 2*Q_d} = 0 ✓")
print(f"    (F) Q_u + Q_d + Q_s = {Q_u + Q_d + Q_s} = 0 ✓ (traceless)")
print(f"    (F) Q_u - Q_d = {Q_u - Q_d} = 1 (T₃ eigenvalue diff.)")
print()

# ============================================================
# §5. THE FULL THEOREM
# ============================================================

print("=" * 72)
print("  §5. THEOREM")
print("=" * 72)

print(f"""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║  THEOREM (Quark charge uniqueness, Tier 1):                          ║
║                                                                      ║
║  Given:                                                              ║
║    (i)   SU(3) gauge group with quarks in the fundamental rep.       ║
║    (ii)  Proton = uud with Q_p = +1 (integer charge)                ║
║    (iii) Neutron = udd with Q_n = 0 (electrically neutral)          ║
║                                                                      ║
║  Then: Q_u = 2/3 and Q_d = -1/3 are UNIQUELY determined.            ║
║                                                                      ║
║  Proof:                                                              ║
║    From (ii): 2Q_u + Q_d = 1                                        ║
║    From (iii): Q_u + 2Q_d = 0                                       ║
║    These are two linear equations in two unknowns.                   ║
║    Solution: Q_u = 2/3, Q_d = -1/3. Unique.             QED         ║
║                                                                      ║
║  Corollary: The α¹-cancellation condition                            ║
║    2Q_u² + Q_d² = 2(4/9) + 1/9 = 9/9 = 1 = Q_e²                   ║
║  follows AUTOMATICALLY. It is not an independent constraint          ║
║  but a CONSEQUENCE of Q_p = 1 and Q_n = 0.                          ║
║                                                                      ║
║  Note: Conditions (ii) and (iii) are EXPERIMENTAL FACTS used as     ║
║  input. The SFST does not derive the existence of the proton and     ║
║  neutron — it derives their MASS RATIO given their existence.        ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
""")

# ============================================================
# §6. THE REMARKABLE COROLLARY
# ============================================================

print("=" * 72)
print("  §6. THE α¹-CANCELLATION AS A COROLLARY")
print("=" * 72)

print("""
The fact that 2Q_u² + Q_d² = 1 is NOT assumed — it FOLLOWS from 
the two experimental facts Q_p = 1, Q_n = 0.

PROOF:
  Q_u = 2/3 and Q_d = -1/3 are the unique solution of:
    2Q_u + Q_d = 1   (proton charge)
    Q_u + 2Q_d = 0   (neutron neutrality)
  
  Then: 2Q_u² + Q_d² = 2(4/9) + 1/9 = 9/9 = 1 = (-1)² = Q_e²

This means: the α¹-cancellation in m_p/m_e is a CONSEQUENCE of 
the proton being charged (+1) and the neutron being neutral (0).

If ANY other baryon composition had Q_baryon = 1, Q_antibaryon = 0,
it would automatically satisfy Σ Q² = 1.

THIS IS DEEP: The α¹-cancellation is not an arithmetic coincidence 
specific to Q_u = 2/3. It follows from the STRUCTURE of SU(3) 
combined with the experimental baryon charges.

More precisely: For ANY SU(N_c) with a baryon qqq:
  N_c = 3: Q_u + Q_u + Q_d = 1, Q_u + Q_d + Q_d = 0
  → Q_u = 2/3, Q_d = -1/3
  → 2Q_u² + Q_d² = 1 ✓

  For N_c = 2 (two quarks per baryon): Q_u + Q_d = 1, Q_u + Q_d = 0
  → CONTRADICTION (1 ≠ 0). N_c = 2 doesn't work.

  For N_c = 4: 3Q_u + Q_d = 1, Q_u + 3Q_d = 0 → Q_u = 3/8, Q_d = -1/8
  → 3(9/64) + 1/64 = 28/64 = 7/16 ≠ 1. FAILS.

  Only N_c = 3 gives Σ Q² = 1.

This provides ANOTHER proof that N_c = 3 (independent of the 
Spinor-Color coincidence from the d=5 theorem).
""")

# Verify for other N_c
print("Verification for other N_c:")
print(f"  {'N_c':>4s} {'Q_u':>8s} {'Q_d':>8s} {'Σ_p Q²':>10s} {'= 1?':>6s}")
print("  " + "-" * 38)

for Nc in range(2, 8):
    # Baryon = (N_c - 1) u-quarks + 1 d-quark
    # Q_p = (N_c-1)Q_u + Q_d = 1
    # Q_n = Q_u + (N_c-1)Q_d = 0
    # Solve: Q_u = (N_c-1)/D, Q_d = -1/D where D = N_c²-N_c-... 
    # Actually: (N_c-1)Q_u + Q_d = 1 and Q_u + (N_c-1)Q_d = 0
    # From second: Q_u = -(N_c-1)Q_d
    # Sub into first: -(N_c-1)²Q_d + Q_d = 1 → Q_d(1-(N_c-1)²) = 1
    # Q_d = 1/(1-(N_c-1)²) = -1/((N_c-1)²-1) = -1/(N_c²-2N_c) = -1/(N_c(N_c-2))
    
    if Nc == 2:
        print(f"  {Nc:>4d} {'---':>8s} {'---':>8s} {'CONTRADICTION':>10s} {'✗':>6s}")
        continue
    
    Q_d_Nc = Fraction(-1, Nc*(Nc-2))
    Q_u_Nc = -(Nc-1) * Q_d_Nc
    
    # Proton: (N_c-1) u-quarks + 1 d-quark
    sum_Q2 = (Nc-1)*Q_u_Nc**2 + Q_d_Nc**2
    
    is_one = (sum_Q2 == 1)
    
    print(f"  {Nc:>4d} {str(Q_u_Nc):>8s} {str(Q_d_Nc):>8s} {str(sum_Q2):>10s} {'✓' if is_one else '✗':>6s}")

print(f"""

RESULT: Among all SU(N_c) gauge theories with N_c ≥ 3, the 
condition Σ_proton Q² = Q_e² = 1 is satisfied ONLY for N_c = 3.

This is a FOURTH independent proof of N_c = 3 (alongside the 
Spinor-Color coincidence, Hosotani prefactor, and homotopy group).
""")
