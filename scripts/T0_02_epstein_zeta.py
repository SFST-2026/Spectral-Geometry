"""
DEFINITIVE COMPUTATION: Z_{E_d}(-1/2) for d = 1..5
Using the theta function / Mellin transform with Jacobi inversion.

This proves that Z_{E_5}(-1/2) is a UNIQUE, well-defined number,
independent of any factorization scheme.

Method: 
Z_{E_d}(s) = pi^s / Gamma(s) * I(s,d)

where (after Jacobi inversion and splitting at t=1):

I(s,d) = integral_1^inf [t^{s-1} + t^{d/2-s-1}] * [theta_3(0,it)^d - 1] dt
         + 1/(s - d/2) - 1/s

This formula provides the meromorphic continuation to all s.
"""

import mpmath
from mpmath import mp, mpf, pi, gamma, log, exp, sqrt, power, quad, nstr

mp.dps = 50

def theta3(t, nmax=300):
    """theta_3(0, it) = 1 + 2 sum_{n=1}^inf exp(-pi n^2 t)"""
    s = mpf(1)
    for n in range(1, nmax+1):
        term = 2 * exp(-pi * n**2 * t)
        s += term
        if abs(term) < mpf(10)**(-mp.dps + 3):
            break
    return s

def Z_Epstein(d, s_val):
    """
    Z_{E_d}(s) via theta function with analytic continuation.
    """
    s = mpf(s_val)
    d_half = mpf(d) / 2
    
    def integrand(t):
        th = theta3(t)**d - 1
        return (power(t, s-1) + power(t, d_half - s - 1)) * th
    
    integral = quad(integrand, [1, 40], method='tanh-sinh')
    pole_terms = 1/(s - d_half) - 1/s
    I_total = integral + pole_terms
    
    prefactor = power(pi, s) / gamma(s)
    return prefactor * I_total

print("=" * 72)
print("  DIRECT COMPUTATION OF EPSTEIN ZETA Z_{E_d}(-1/2)")
print("  Method: Theta function + Jacobi inversion (no factorization)")
print("=" * 72)

results = {}
known = {
    1: ("2 * zeta_R(-1) = -1/6", mpf(-1)/6),
}

for d in range(1, 8):
    z = Z_Epstein(d, -0.5)
    results[d] = z
    line = f"  Z_{{E_{d}}}(-1/2) = {nstr(z, 30)}"
    if d in known:
        err = abs(z - known[d][1])
        line += f"   [known: {known[d][0]}, err={nstr(err, 3)}]"
    print(line)

print()
print("=" * 72)
print("  UNIQUENESS ARGUMENT")
print("=" * 72)
print("""
The value Z_{{E_5}}(-1/2) = {0}
is computed from the DEFINITION:

  Z_{{E_d}}(s) = pi^s / Gamma(s) * [integral_1^inf (t^{{s-1}} + t^{{d/2-s-1}})(theta^d - 1) dt
                                     + 1/(s-d/2) - 1/s]

This involves:
  (a) The Jacobi theta function: theta_3(0,it) = sum_n exp(-pi n^2 t)  [unique]
  (b) Its d-th power: theta^d  [unique, since d=5 is fixed]
  (c) The Mellin transform integral  [convergent for all s away from poles]
  (d) The analytic continuation via Jacobi identity  [canonical]

NO STEP involves a choice of factorization. The answer is unique.
""".format(nstr(results[5], 30)))

print("=" * 72)
print("  WHAT DOES THIS MEAN FOR c_2?")
print("=" * 72)

c2_claimed = mpf(5)/2 * log(2) - mpf(3)/8
print(f"""
Claimed: c_2 = (5/2) ln 2 - 3/8 = {nstr(c2_claimed, 30)}

The question is: how does c_2 relate to Z_{{E_5}}(-1/2)?

If c_2 is determined SOLELY by Z_{{E_5}}(-1/2) through a formula like
  c_2 = f(Z_{{E_5}}(-1/2))
where f is some known function from the physical derivation,
then c_2 is UNIQUE because Z_{{E_5}}(-1/2) is unique.

The Elizalde factorization enters only as a COMPUTATIONAL METHOD
to evaluate Z_{{E_5}}(-1/2). If the method is correctly applied,
it must give the same answer as the direct computation.

If different factorizations give DIFFERENT answers for c_2, then
either:
  (1) The factorization formula is being applied incorrectly, or
  (2) c_2 does NOT depend solely on Z_{{E_5}}(-1/2) but on additional
      regularization-scheme-dependent quantities.

Our direct computation settles case (1): Z_{{E_5}}(-1/2) is unique.
The question of case (2) — whether the PHYSICAL derivation introduces
additional scheme dependence — is a physics question, not a math one.
""")

# Now let's try to see if c_2 can be related to Z values
print("=" * 72)
print("  EXPLORING THE RELATIONSHIP c_2 <-> Z_{E_d}(-1/2)")
print("=" * 72)

z5 = results[5]
c2 = c2_claimed

# Let's check some simple relationships
print(f"\n  c_2 = {nstr(c2, 20)}")
print(f"  Z_5 = {nstr(z5, 20)}")
print(f"  c_2 / Z_5 = {nstr(c2/z5, 20)}")
print(f"  c_2 + Z_5 = {nstr(c2 + z5, 20)}")
print(f"  c_2 * Z_5 = {nstr(c2 * z5, 20)}")

# Check: is c_2 related to differences of Z values?
for d1 in range(1, 6):
    for d2 in range(d1+1, 6):
        diff = results[d2] - results[d1]
        ratio = c2 / diff if diff != 0 else None
        if ratio and abs(abs(ratio) - round(abs(ratio))) < 0.01:
            print(f"  c_2 / (Z_{d2} - Z_{d1}) ≈ {nstr(ratio, 15)}")

# Check ratios with simple numbers
print(f"\n  Z_5 / ln(2) = {nstr(z5 / log(2), 20)}")
print(f"  Z_5 * pi = {nstr(z5 * pi, 20)}")
print(f"  Z_5 * 2*pi = {nstr(z5 * 2 * pi, 20)}")

# Some known Epstein zeta closed forms
# Z_{E_2}(-1/2) should relate to Dirichlet beta function
# Z_{E_2}(s) = 4 * zeta(s) * L_{-4}(s) for the form m^2 + n^2
# Wait, actually Z_{E_2}(s) = sum'_{m,n} (m^2+n^2)^{-s}
# = 4 sum_{n=1}^inf r_2(n) n^{-s} where r_2(n) = #{(a,b): a^2+b^2=n}/4 ... 
# Actually the representation number formula is more complex.

print("\n" + "=" * 72)
print("  CLOSED FORMS FOR LOW-DIMENSIONAL EPSTEIN ZETA")
print("=" * 72)

# Z_{E_1}(-1/2) = -1/6  ✓
# Z_{E_2}(s) = 4 * L_{-4}(s) * zeta(s) where L_{-4}(s) = sum (-1)^n (2n+1)^{-s} = beta(s)
# So Z_{E_2}(-1/2) = 4 * beta(-1/2) * zeta(-1/2)

from mpmath import zeta as mpzeta

# Dirichlet beta function: beta(s) = sum_{n=0}^inf (-1)^n (2n+1)^{-s}
# = L(s, chi_{-4})
# beta(-1/2) can be computed via: beta(s) = 4^{-s} [zeta(s, 1/4) - zeta(s, 3/4)]
def dirichlet_beta(s):
    from mpmath import hurwitz as hz
    return mpf(4)**(-s) * (mpmath.hurwitz(s, mpf(1)/4) - mpmath.hurwitz(s, mpf(3)/4))

# Actually Z_{E_2}(s) = 4 zeta(s) beta(s) is for the FULL sum including negative indices
# This should be: sum_{(m,n) != (0,0)} (m^2+n^2)^{-s}
# The representation: r_2(n) = 4 sum_{d|n} chi_{-4}(d)
# So Z_{E_2}(s) = 4 zeta(s) L_{-4}(s)

beta_neg_half = dirichlet_beta(mpf(-1)/2)
zeta_neg_half = mpzeta(mpf(-1)/2)
z2_from_formula = 4 * zeta_neg_half * beta_neg_half
print(f"\n  Z_{{E_2}} via r_2 representation:")
print(f"    4 * zeta(-1/2) * beta(-1/2) = {nstr(z2_from_formula, 30)}")
print(f"    Direct computation:            {nstr(results[2], 30)}")
print(f"    Match: {abs(z2_from_formula - results[2]) < mpf(10)**(-30)}")

# For Z_{E_4}: r_4(n) = 8 sum_{d|n, 4 nmid d} d (for n >= 1)
# Z_{E_4}(s) = 8 zeta(s) zeta(s-1) (1 - 4^{1-s}) + ... it's complicated
# Actually: Z_{E_4}(s) = 8(1-4^{1-s}) zeta(s) zeta(s-1) for the Jacobi representation
# Let me check: 
z4_jacobi = 8 * (1 - mpf(4)**(1 - mpf(-1)/2)) * mpzeta(mpf(-1)/2) * mpzeta(mpf(-1)/2 - 1)
print(f"\n  Z_{{E_4}} via Jacobi r_4 formula (rough):")
print(f"    8(1-4^{{3/2}}) zeta(-1/2) zeta(-3/2) = {nstr(z4_jacobi, 30)}")
print(f"    Direct computation:                     {nstr(results[4], 30)}")
# This won't match exactly because the formula is more involved

print("\n" + "=" * 72)
print("  FINAL CONCLUSION")
print("=" * 72)
print(f"""
THEOREM: Z_{{E_5}}(-1/2) is a unique, well-defined real number.

PROOF: The Epstein zeta function Z_{{E_d}}(s) is defined as the analytic 
continuation of sum'_{{n in Z^d}} |n|^{{-2s}} to all s in C.

The analytic continuation is achieved via the theta function integral 
representation with Jacobi inversion, which provides a CANONICAL 
meromorphic continuation with poles only at s = 0 and s = d/2.

At s = -1/2, d = 5, we are away from both poles (s=0 and s=5/2),
so the value is unique and well-defined:

  Z_{{E_5}}(-1/2) = {nstr(results[5], 40)}

NUMERICAL VALUE (50-digit precision):
  Z_{{E_5}}(-1/2) = {results[5]}

IMPLICATION FOR c_2:
If the derivation of c_2 reduces to computing Z_{{E_5}}(-1/2) 
(possibly with additional UNIQUELY DETERMINED operations), 
then c_2 is unique regardless of which factorization one uses 
as a computational intermediate step.

The Elizalde factorization T^2 x T^3 is merely a computational 
technique. If applied correctly, it MUST yield the same value of 
Z_{{E_5}}(-1/2). The fact that different factorizations seem to give 
different results would indicate an ERROR in the application of 
the factorization formula, not an ambiguity in the final answer.

HOWEVER: if the physical derivation of c_2 involves additional 
regularization steps beyond computing Z_{{E_5}}(-1/2) — for instance, 
if different subtraction schemes for UV divergences are needed for 
different factorizations — then the scheme dependence is a PHYSICAL 
issue, not a mathematical one about the Epstein zeta function itself.
""")

# Verify Z_{E_5}(-1/2) against the sum representation numerically
print("=" * 72)
print("  BRUTE-FORCE PARTIAL SUM VERIFICATION")
print("=" * 72)

# Compute partial sums of sum'_{n in Z^5} |n|^1 (since 2s = -1 => sum |n|^{2*(-(-1/2))} = |n|^1)
# Wait: Z_{E_5}(s) = sum' |n|^{-2s}, so at s = -1/2, we get sum' |n|^{+1}
# This DIVERGES! The analytic continuation gives a finite value to this divergent sum.
# Let's verify with the regulated partial sums.

print("\nNote: Z_{E_5}(-1/2) = sum'_{n in Z^5} |n|^{+1} (DIVERGENT)")
print("The theta function method assigns a FINITE value via analytic continuation.")
print("We cannot verify directly by summation, but we CAN verify the method itself.")
print()

# Instead, verify at a point where the sum converges, e.g. s = 3
print("Verification at s = 3 (where sum converges):")
z5_s3 = Z_Epstein(5, 3)
print(f"  Z_{{E_5}}(3) via theta = {nstr(z5_s3, 20)}")

# Brute force
total = mpf(0)
N = 8
count = 0
for n1 in range(-N, N+1):
    for n2 in range(-N, N+1):
        for n3 in range(-N, N+1):
            for n4 in range(-N, N+1):
                for n5 in range(-N, N+1):
                    r2 = n1**2 + n2**2 + n3**2 + n4**2 + n5**2
                    if r2 > 0:
                        total += mpf(r2)**(-3)
                        count += 1

print(f"  Brute force (|n_i| <= {N}, {count} terms) = {nstr(total, 20)}")
print(f"  Difference = {nstr(abs(z5_s3 - total), 8)}")
print(f"  (Difference from truncation of infinite sum)")
