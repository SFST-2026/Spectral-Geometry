"""
VOLLE SPURRECHNUNG: Der α²-Koeffizient in m_p/m_e auf T⁵
============================================================

Ziel: Berechne den Koeffizienten der α²-Korrektur in

  m_p/m_e = 6π⁵ · (1 + C·α² + ...)

aus der Spektralgeometrie auf T⁵ mit U(1)_em-Eichfeld,
und prüfe ob C = 1/√8 herauskommt.

SETUP:
- Flacher Torus T⁵_R mit Radius R
- Dirac-Operator D_A = D_0 + iQA (minimale Kopplung)
- Q = elektromagnetische Ladung der Konstituenten
- Die Masse wird über die ζ-regularisierte Spektraldeterminante bestimmt

METHODE:
Die ζ-Funktion des gestörten Operators D²_A = D²_0 + V(A) wird
in Potenzen des Eichfelds A entwickelt. Die Korrektur zur 
log-Determinante gibt die Massenverschiebung.
"""

from mpmath import mp, mpf, pi, sqrt, log, exp, gamma, zeta, nstr, nsum, inf, power
mp.dps = 60

print("=" * 72)
print("  TEIL 1: DIE SPEKTRALDETERMINANTE AUF T⁵")
print("=" * 72)

print("""
Der Dirac-Operator auf T⁵_R mit flacher U(1)-Verbindung A:

  D²_A = -Σ_μ (∂_μ + iQ·A_μ)²

Für eine KONSTANTE (flache) Verbindung A_μ = θ_μ/(2πR) ist das 
Spektrum exakt bekannt:

  λ_n(θ) = Σ_μ (n_μ + Q·θ_μ)²/R²     n ∈ Z⁵

Die ζ-regularisierte log-Determinante:

  ln det'(D²_A) = -ζ'_{D²_A}(0)

wobei ζ_{D²_A}(s) = Σ'_n [Σ_μ (n_μ + Qθ_μ)²/R²]^{-s}
                   = R^{2s} · Z_{E_5}(s; Qθ)

und Z_{E_5}(s; θ) die verschobene Epstein-Zeta-Funktion ist.
""")

print("=" * 72)
print("  TEIL 2: ENTWICKLUNG IN POTENZEN VON θ (= POTENZEN VON α)")
print("=" * 72)

print("""
Die physikalische Kopplung ist α = e²/(4π), und das Eichfeld
auf T⁵ erzeugt einen Phasenshift θ_μ ∝ √α.

Für ISOTROPEN Twist θ_μ = θ für alle μ=1,...,5:

  Z_{E_5}(s; θ) = Σ'_{n∈Z⁵} [Σ_μ (n_μ + Qθ)²]^{-s}

Entwicklung um θ = 0:

  Z_{E_5}(s; θ) = Z_{E_5}(s; 0) + θ·∂_θ Z|_{θ=0} 
                  + ½θ²·∂²_θ Z|_{θ=0} + O(θ³)

SCHLÜSSELBEOBACHTUNG: ∂_θ Z|_{θ=0} = 0 (Symmetrie!)

Proof: Z_{E_5}(s; θ) = Σ'_n |n + Qθ·1|^{-2s}
wobei 1 = (1,1,1,1,1).

Bei θ=0: ∂_θ Z = -2s·Q·Σ'_n Σ_μ n_μ · |n|^{-2s-2}
        = -2sQ · 5 · Σ'_n n_1 · |n|^{-2s-2}

Aber Σ'_n n_1 · |n|^{-2s-2} = 0 wegen der Symmetrie n_1 → -n_1!

Also: Der θ¹-Term (= α^{1/2}-Term) verschwindet durch 
GITTER-SYMMETRIE (Z⁵ ist invariant unter n → -n).

Dies ist ein ANDERER Mechanismus als die Tr(Q²)-Auslöschung!
Beide wirken zusammen und liefern die gleiche Konklusion.
""")

print("=" * 72)
print("  TEIL 3: DER ZWEITE-ORDNUNG-TERM (α¹-KORREKTUR)")
print("=" * 72)

print("""
Die zweite Ableitung bei θ=0:

∂²_θ Z_{E_5}(s;0) = Σ'_n ∂²_θ |n + Qθ·1|^{-2s} |_{θ=0}

= Σ'_n [-2sQ² · d · |n|^{-2s-2} 
        + 4s(s+1)Q⁴ · (Σ_μ n_μ)² · |n|^{-2s-4}]    ... (*)

ABER: dies gibt den α¹-Term (θ² ∝ α), NICHT den α²-Term!

Das Problem: In der SFST-Formel ist die Behauptung, dass die 
Korrektur bei α² liegt, nicht bei α¹. Wir haben im Quotienten 
m_p/m_e gezeigt, dass Tr_p(Q²) = Tr_e(Q²) = 1, was den α¹-Term
im QUOTIENTEN eliminiert. 

Aber jetzt machen wir die volle Rechnung: Was gibt der α²-Term
im Quotienten?
""")

print("=" * 72)
print("  TEIL 4: DER α²-TERM IM QUOTIENTEN m_p/m_e")
print("=" * 72)

print("""
Für den QUOTIENTEN brauchen wir:

  ln(m_p/m_e) = -½[ζ'_p(0) - ζ'_e(0)]

mit den jeweiligen Ladungsoperatoren.

PROTON (uud):
  Die drei Quarks sehen verschiedene Eichfelder:
  Quark u₁: Ladung Q_u = 2/3
  Quark u₂: Ladung Q_u = 2/3  
  Quark d:  Ladung Q_d = -1/3

ELEKTRON:
  Ladung Q_e = -1

Jeder Konstituent trägt eine eigene Spektraldeterminante bei.
Das Proton als zusammengesetztes Objekt (in der SFST-Interpretation):

  ln Z_p = Σ_{quarks} ln det'(D²_{Q_i·A})
         = 2·ln det'(D²_{(2/3)A}) + ln det'(D²_{(-1/3)A})

  ln Z_e = ln det'(D²_{(-1)A})

Der Quotient:
  ln(Z_p/Z_e) = 2·ln det'(D²_{(2/3)θ}) + ln det'(D²_{(-1/3)θ}) 
                - ln det'(D²_{(-1)θ})
""")

print("=" * 72)
print("  TEIL 5: EXPLIZITE BERECHNUNG DER VERSCHIEBTEN ZETA-FUNKTION")
print("=" * 72)

# Die verschobene Epstein-Zeta via Theta-Funktion
def theta3_shifted(t, theta, nmax=300):
    """Θ₃(t, θ) = Σ_n exp(-t·n²) · exp(2πi·n·θ) [real part]
    = Σ_n exp(-t·n²) · cos(2π·n·θ)
    = 1 + 2·Σ_{n=1}^∞ exp(-t·n²) · cos(2π·n·θ)
    """
    s = mpf(1)
    for n in range(1, nmax+1):
        term = 2 * exp(-t * n**2) * mp.cos(2*pi*n*theta)
        s += term
        if abs(term) < mpf(10)**(-mp.dps + 3):
            break
    return s

def Z_Epstein_shifted(d, s_val, theta_val):
    """
    Z_{E_d}(s; θ) = Σ'_{n∈Z^d} |n + θ·1|^{-2s}
    
    Via Theta-Funktion:
    Z = π^s/Γ(s) · ∫₀^∞ t^{s-1} [Θ₃(t,θ)^d - 1] dt
    
    Mit Jacobi-Inversion für die analytische Fortsetzung.
    
    Für θ ≠ 0: Θ₃(t,θ) → t^{-1/2}·Θ₃(1/t, θ) (Poisson)
    wobei Θ₃(1/t, θ) = √(π/t) · Σ_m exp(-π²m²/t + 2πimθ)
    
    Tatsächlich: Θ₃(πt, θ) = (1/√t) · Σ_m exp(-(m+θ)²/t)
    
    Hier arbeiten wir mit der konkreten Darstellung:
    Θ₃_shifted(t, θ) = Σ_n exp(-π·(n+θ)²·t)  [für EIN n ∈ Z]
    aber wir verwenden die Standard-Form Σ exp(-n²t)cos(2πnθ).
    """
    s = mpf(s_val)
    theta = mpf(theta_val)
    d_half = mpf(d) / 2
    
    # Für θ ≠ 0 haben wir KEINE exakte Nullmode im verschobenen Gitter
    # (es sei denn θ ∈ Z), also kein Pol bei s = 0 aus der Nullmode.
    
    # Wir berechnen direkt:
    # Z(s;θ) = R^{2s} · Σ'_{n∈Z^d} |n + θ·1_d|^{-2s}
    # Setze R = 1 für die normierte Rechnung.
    
    # Θ-Darstellung: Σ_{n∈Z^d} exp(-t·|n+θ1|²) = [Θ₃_shift(t,θ)]^d
    # wobei Θ₃_shift(t,θ) = Σ_{n∈Z} exp(-t(n+θ)²)
    #                      = Σ_n exp(-tn²-2tnθ-tθ²)
    #                      = exp(-tθ²) · Σ_n exp(-tn²) · exp(-2tnθ)
    
    # Einfacher: Verwende die Poisson-Darstellung
    # Σ_n exp(-t(n+θ)²) = √(π/t) · Σ_m exp(-π²m²/t) · exp(2πimθ)
    # = √(π/t) · [1 + 2·Σ_{m=1} exp(-π²m²/t) · cos(2πmθ)]
    
    def theta_1d_shifted(t, th):
        """Σ_{n∈Z} exp(-t·(n+th)²)"""
        s_val = mpf(0)
        for n in range(-200, 201):
            s_val += exp(-t * (n + th)**2)
        return s_val
    
    def theta_d_shifted(t, th, dim):
        return theta_1d_shifted(t, th)**dim
    
    # Mellin-Transform mit Split at t=1
    # Für θ ≠ 0 (und θ ∉ Z), es gibt keine Nullmode, also:
    # ∫₀^∞ t^{s-1} Θ^d(t,θ) dt converges for Re(s) > d/2
    # 
    # Jacobi: Θ₁(t,θ) = √(π/t) · Σ_m exp(-π²m²/t + 2πimθ)
    # So: Θ^d(t,θ) = (π/t)^{d/2} · [Σ_m exp(-π²m²/t + 2πimθ)]^d
    #
    # At t → 0: Θ^d → (π/t)^{d/2} · 1 (leading term m=0)
    # So the integral 0→1 needs analytic continuation.
    #
    # Split: I = ∫₁^∞ t^{s-1} [Θ^d(t,θ)-δ] dt + ∫₀^1 t^{s-1} [Θ^d(t,θ)-δ] dt
    # where δ = 1 if θ∈Z (there's a zero mode), δ = 0 if θ∉Z.
    #
    # For θ ∉ Z: no zero mode, Θ^d(t,θ) → 0 as t → ∞ (all terms decay)
    # Wait: Θ₁(t,θ) = Σ exp(-t(n+θ)²). For t→∞, all terms → 0 since (n+θ)²>0.
    # So Θ^d → 0 exponentially.
    #
    # For t→0: Θ₁(t,θ) = √(π/t)·(1 + ...) → (π/t)^{1/2}
    # So Θ^d(t,θ) ~ (π/t)^{d/2}
    #
    # Thus: ∫₀^1 t^{s-1} Θ^d dt ~ ∫₀^1 t^{s-1-d/2} π^{d/2} dt = π^{d/2}/(s-d/2)
    # Plus exponentially small corrections.
    
    # For the full computation including θ=0 (with zero mode subtraction):
    
    is_integer_theta = (abs(theta - round(float(theta))) < 1e-10)
    delta = 1 if is_integer_theta else 0
    
    def integrand_high(t):
        val = theta_d_shifted(t, theta, d) - delta
        return power(t, s - 1) * val
    
    # For the low integral, use Jacobi inversion:
    # Θ₁(t,θ) = √(π/t) · Θ̃₁(π²/t, θ)
    # where Θ̃₁(u, θ) = Σ_m exp(-u·m²)·exp(2πimθ)
    # = 1 + 2Σ cos(2πmθ) exp(-um²) = theta3_shifted(u, θ) [our function]
    
    # So Θ^d(t,θ) = (π/t)^{d/2} · [theta3_shifted(π²/t, θ)]^d ... 
    # NO wait, let me be more careful.
    
    # Θ₁(t,θ) = Σ_{n∈Z} exp(-t(n+θ)²)
    # Poisson: = √(π/t) · Σ_{m∈Z} exp(-π²m²/t) · exp(2πimθ)
    # = √(π/t) · Σ_m cos(2πmθ) exp(-π²m²/t)  [for real θ]
    # = √(π/t) · Θ₃_cos(π²/t, θ)
    # where Θ₃_cos(u, θ) = 1 + 2Σ_{m≥1} cos(2πmθ) exp(-um²)
    
    # So for the integral 0 to 1, substitute t → 1/t:
    # ∫₀^1 t^{s-1} Θ^d(t,θ) dt = ∫₁^∞ u^{-s-1} Θ^d(1/u, θ) du
    # = ∫₁^∞ u^{-s-1} · (πu)^{d/2} · [Θ₃_cos(π²u, θ)]^d du
    # = π^{d/2} · ∫₁^∞ u^{d/2-s-1} · [Θ₃_cos(π²u, θ)]^d du
    
    # For the zero mode subtraction when θ∈Z:
    # -δ · ∫₀^1 t^{s-1} dt = -δ/s
    # -δ · ∫₀^1 t^{s-1} dt via sub: -δ · (-1/s) ... 
    # Actually let me just compute numerically.
    
    from mpmath import quad
    
    # High integral: 1 to large T (convergence is exponential)
    I_high = quad(integrand_high, [1, 30], method='tanh-sinh')
    
    # Low integral via substitution u = 1/t
    def integrand_low(u):
        # t = 1/u, dt = -du/u²
        # ∫₀^1 t^{s-1} [Θ^d(t,θ) - δ] dt
        # = ∫₁^∞ u^{-s+1} [Θ^d(1/u, θ) - δ] · u^{-2} du
        # = ∫₁^∞ u^{-s-1} [Θ^d(1/u, θ) - δ] du
        val = theta_d_shifted(1/u, theta, d) - delta
        return power(u, -s - 1) * val
    
    I_low = quad(integrand_low, [1, 30], method='tanh-sinh')
    
    I_total = I_high + I_low
    prefactor = power(pi, s) / gamma(s)
    
    return prefactor * I_total

print("Computing Z_{E_5}(s; Qθ) for various charges and θ values...")
print("This computes ln det'(D²) for each constituent.\n")

# The key quantity for the mass ratio is:
# ln(m_p/m_e) ∝ -½[ζ'_p(0) - ζ'_e(0)]
# 
# ζ'(0) = -ln det'(D²)
# 
# For the shifted Epstein zeta at s=0:
# ζ(s) = R^{2s} Z_{E_5}(s; Qθ)
# ζ'(0) = 2ln(R)·Z_{E_5}(0;Qθ) + Z'_{E_5}(0;Qθ)
#
# The R-dependent part cancels in the ratio if Tr_p(Q²) = Tr_e(Q²).
# Let's focus on the θ-dependent part.

# In the SFST framework, θ is related to α via the Poisson duality.
# At the self-dual point, the relevant parameter is:
# θ = α^{1/2}/(2π) (schematic)
# So θ² ∝ α.

# Let's compute the ratio as a function of θ and expand.
# 
# f(θ) = 2·ln Z_{E_5}(s;(2/3)θ) + ln Z_{E_5}(s;(-1/3)θ) - ln Z_{E_5}(s;(-1)θ)
#
# evaluated at s → 0 (or rather, the derivative at s=0).
#
# Instead of computing ζ'(0) directly (which is hard), let's use
# the HEAT KERNEL approach, which is what the SFST actually uses.

print("=" * 72)
print("  TEIL 6: HEAT-KERNEL-ANSATZ FÜR DEN KOEFFIZIENTEN")
print("=" * 72)

print("""
In der SFST wird die Masse über den Heat-Kernel am selbstdualen 
Punkt σ* = R² bestimmt:

  K(σ*; θ) = Tr(e^{-σ*·D²_A}) = [Θ₁(σ*/R², θ)]^5 · d_S

Für R² = σ* (selbstdualer Punkt, d.h. t = 1 in normierten Einheiten):

  K(1; Qθ) = [Θ₁(1, Qθ)]^5 · d_S

wobei Θ₁(1, Qθ) = Σ_{n∈Z} exp(-(n+Qθ)²)

Die Matching-Map gibt:
  m_p/m_e = |W| · [K_p(1;θ)/K_e(1;θ)]
          = 6 · [Θ₁(1, Q_u·θ)² · Θ₁(1, Q_u·θ)² · Θ₁(1, Q_d·θ)]^5
            / [Θ₁(1, Q_e·θ)]^5
          ... 

NEIN — in der SFST ist die Matching-Map:
  m_p/m_e = |W| · [K̄(σ*)]^{n_p-n_e}

wobei K̄ = K/d_S und die Ladungsabhängigkeit über den 
GESAMTEN Heat-Kernel des zusammengesetzten Operators geht.

Vereinfachung: Für das Proton mit 3 Quarks, der PRODUKT-Operator:
  D²_p = D²_{Q_u} ⊗ D²_{Q_u} ⊗ D²_{Q_d}

hat den Heat-Kernel:
  K_p(t) = K_{Q_u}(t)² · K_{Q_d}(t)

Ähnlich: K_e(t) = K_{Q_e}(t)

Also:
  m_p/m_e = 6 · [K_p(1)/K_e(1)]
          = 6 · [Θ₁(1,(2/3)θ)^{10} · Θ₁(1,(-1/3)θ)^5] / [Θ₁(1,(-1)θ)^5]
""")

# Nein, die Potenz 5 kommt von den 5 Dimensionen, die Potenz der 
# Quark-Beiträge von n_p - n_e. Lass mich das sauberer machen.

print("=" * 72)
print("  TEIL 7: SAUBERE BERECHNUNG DER KORREKTUR")
print("=" * 72)

print("""
Die 1D-Theta-Funktion am selbstdualen Punkt:

  Θ(Qθ) := Θ₁(1, Qθ) = Σ_{n∈Z} exp(-(n + Qθ)²)

Entwicklung in θ um θ = 0:

  Θ(Qθ) = Θ(0) + Qθ·Θ'(0) + ½(Qθ)²·Θ''(0) + ...

wobei Θ(0) = Θ₃(1) = √π·(1 + 2e^{-π²} + ...) ≈ √π

Und: Θ'(0) = -2·Σ_n n·exp(-n²) = 0 (Symmetrie n → -n)

Und: Θ''(0) = Σ_n [4n² - 2]·exp(-n²)
""")

# Berechne Θ(0), Θ'(0), Θ''(0), Θ'''(0), Θ''''(0)
def compute_theta_derivatives(nmax=200):
    """Compute derivatives of Θ₁(1, θ) at θ=0."""
    # Θ(θ) = Σ_n exp(-(n+θ)²)
    # Θ'(θ) = Σ_n (-2)(n+θ) exp(-(n+θ)²)
    # Θ''(θ) = Σ_n [4(n+θ)² - 2] exp(-(n+θ)²)
    # Θ'''(θ) = Σ_n [-8(n+θ)³ + 12(n+θ)] exp(-(n+θ)²)
    # Θ''''(θ) = Σ_n [16(n+θ)⁴ - 48(n+θ)² + 12] exp(-(n+θ)²)
    
    Theta0 = mpf(0)
    Theta1 = mpf(0)  # first derivative
    Theta2 = mpf(0)  # second derivative
    Theta3 = mpf(0)  # third derivative
    Theta4 = mpf(0)  # fourth derivative
    
    for n in range(-nmax, nmax+1):
        en = exp(-mpf(n)**2)
        n2 = mpf(n)**2
        n3 = mpf(n)**3
        n4 = mpf(n)**4
        
        Theta0 += en
        Theta1 += (-2*n) * en
        Theta2 += (4*n2 - 2) * en
        Theta3 += (-8*n3 + 12*n) * en
        Theta4 += (16*n4 - 48*n2 + 12) * en
    
    return Theta0, Theta1, Theta2, Theta3, Theta4

T0, T1, T2, T3, T4 = compute_theta_derivatives()

print(f"Θ(0)    = {nstr(T0, 25)}")
print(f"Θ'(0)   = {nstr(T1, 25)}  (= 0 by symmetry)")
print(f"Θ''(0)  = {nstr(T2, 25)}")
print(f"Θ'''(0) = {nstr(T3, 25)}  (= 0 by symmetry)")  
print(f"Θ''''(0)= {nstr(T4, 25)}")
print()

# Relative derivatives
a2 = T2 / (2 * T0)  # coefficient of (Qθ)² in Θ(Qθ)/Θ(0)
a4 = T4 / (24 * T0)  # coefficient of (Qθ)⁴
print(f"Θ(Qθ)/Θ(0) = 1 + a₂·(Qθ)² + a₄·(Qθ)⁴ + ...")
print(f"  a₂ = Θ''/(2Θ₀) = {nstr(a2, 20)}")
print(f"  a₄ = Θ''''/(24Θ₀) = {nstr(a4, 20)}")
print()

print("=" * 72)
print("  TEIL 8: DER QUOTIENT m_p/m_e BIS O(θ⁴)")
print("=" * 72)

print("""
In the 5D version the relevant quantity is Θ(Qθ)^5.
Das Massenverhältnis (in der Matching-Map):

  m_p/m_e = 6 · [Θ((2/3)θ)² · Θ((-1/3)θ)]^5 / [Θ((-1)θ)]^5

= 6 · Θ(0)^{15}/Θ(0)^5 · [1 + Korrekturen]^5/[1 + Korrekturen]^5

NEIN — die Potenzstruktur ist:
  Proton: n_p Propagatoren für 3 Quarks in 5D
  Elektron: n_e Propagatoren für 1 Lepton in 5D

  Die 5D-Theta gibt [Θ₁(1,Qθ)]^5 pro Propagator.
  
  Proton (3 Quarks, je 1 Propagator): 
    K_p = [Θ(Q_u·θ)]^5 · [Θ(Q_u·θ)]^5 · [Θ(Q_d·θ)]^5
        = [Θ(Q_u·θ)² · Θ(Q_d·θ)]^5

  Elektron (1 Lepton):
    K_e = [Θ(Q_e·θ)]^5

  m_p/m_e = 6 · K_p / K_e
          = 6 · [Θ((2/3)θ)² · Θ((-1/3)θ) / Θ((-1)θ)]^5
""")

# Define the ratio function
def ratio_function(theta):
    """Compute [Θ((2/3)θ)² · Θ((-1/3)θ) / Θ((-1)θ)]^5"""
    def theta1(th):
        s = mpf(0)
        for n in range(-200, 201):
            s += exp(-(n + th)**2)
        return s
    
    num = theta1(mpf(2)/3 * theta)**2 * theta1(-mpf(1)/3 * theta)
    den = theta1(-theta)
    return (num/den)**5

# Verify at θ = 0
r0 = ratio_function(mpf(0))
print(f"Bei θ=0: Ratio = Θ(0)^{15}/Θ(0)^5 = Θ(0)^{10} = [√π]^{10} = π^5")
print(f"  Numerisch: {nstr(r0, 20)}")
print(f"  π⁵ =       {nstr(pi**5, 20)}")
print(f"  Verhältnis: {nstr(r0/pi**5, 15)}")
print()

print("Jetzt: Entwicklung des Quotienten in θ²:")
print()

# Compute ratio at several small θ values to extract the coefficient
# R(θ) = π⁵ · [1 + C₂·θ² + C₄·θ⁴ + ...]
# So [R(θ)/π⁵ - 1]/θ² → C₂ as θ → 0

print("  θ          [R(θ)/π⁵ - 1]/θ²      [R(θ)/π⁵ - 1]/θ⁴")
print("  " + "-"*60)
for theta_val in [0.001, 0.003, 0.01, 0.03, 0.1]:
    th = mpf(str(theta_val))
    r = ratio_function(th)
    dev = r / pi**5 - 1
    c2_est = dev / th**2
    c4_est = dev / th**4 if theta_val < 0.05 else mpf(0)
    print(f"  {theta_val:<12} {nstr(c2_est, 15):<25} {nstr(c4_est, 15)}")

print()

# More precise: use Richardson extrapolation
# R(θ) = π⁵·(1 + C₂θ² + C₄θ⁴ + ...)
# [R(θ)/π⁵ - 1]/θ² = C₂ + C₄θ² + ...
# Use two values to extract C₂:

th1 = mpf('0.001')
th2 = mpf('0.002')
r1 = ratio_function(th1)
r2 = ratio_function(th2)
f1 = (r1/pi**5 - 1)/th1**2
f2 = (r2/pi**5 - 1)/th2**2

# f1 = C₂ + C₄·th1²
# f2 = C₂ + C₄·th2²
C2_richardson = (f1*th2**2 - f2*th1**2)/(th2**2 - th1**2)
C4_richardson = (f2 - f1)/(th2**2 - th1**2)

print(f"Richardson-Extrapolation:")
print(f"  C₂ = {nstr(C2_richardson, 25)}")
print(f"  C₄ = {nstr(C4_richardson, 20)}")
print()

# Now compute C₂ analytically
print("=" * 72)
print("  TEIL 9: ANALYTISCHE BERECHNUNG VON C₂")
print("=" * 72)

print("""
Θ(Qθ)/Θ(0) = 1 + a₂·(Qθ)² + a₄·(Qθ)⁴ + ...

ln[Θ(Qθ)/Θ(0)] = a₂·(Qθ)² + [a₄ - a₂²/2]·(Qθ)⁴ + ...

Für den Numerator (Proton-Seite, pro Dimension):
  ln[Θ(Q_u·θ)²·Θ(Q_d·θ)/Θ(0)³]
  = 2·a₂·Q_u²·θ² + a₂·Q_d²·θ² + O(θ⁴)
  = a₂·θ²·[2·(2/3)² + (-1/3)²]
  = a₂·θ²·[8/9 + 1/9]
  = a₂·θ²·1

Für den Denominator (Elektron-Seite, pro Dimension):
  ln[Θ(Q_e·θ)/Θ(0)]
  = a₂·Q_e²·θ²
  = a₂·θ²·1

DIFFERENZ (pro Dimension) = a₂·θ²·(1 - 1) = 0 !!!

Der θ²-Term (= α¹-Term) verschwindet exakt, weil
  Σ_proton Q_i² = 2·(2/3)² + (-1/3)² = 1 = Q_e²

Dies ist die ANALYTISCHE BESTÄTIGUNG der numerischen 
Quotient-Auslöschung!
""")

# Verify
Sigma_Q2_p = 2*(mpf(2)/3)**2 + (mpf(1)/3)**2
Sigma_Q2_e = mpf(1)
print(f"Σ_p Q² = {nstr(Sigma_Q2_p, 5)}")
print(f"Σ_e Q² = {nstr(Sigma_Q2_e, 5)}")
print(f"Differenz = {nstr(Sigma_Q2_p - Sigma_Q2_e, 5)}")
print()

print("=" * 72)
print("  TEIL 10: DER θ⁴-TERM (= α²-KORREKTUR) — DER ENTSCHEIDENDE TERM")
print("=" * 72)

print("""
Für den θ⁴-Term brauchen wir die VIERTE Ordnung.

ln[Θ(Qθ)/Θ(0)] = a₂·(Qθ)² + b₄·(Qθ)⁴ + ...

wobei b₄ = a₄ - a₂²/2

Der Beitrag zum Quotienten (pro Dimension):

  Δ ln (pro dim) = [2·b₄·Q_u⁴ + b₄·Q_d⁴ - b₄·Q_e⁴]·θ⁴
                 + [a₂²/2]·{[2Q_u² + Q_d²]² - [Q_e²]²}·θ⁴/... 

Nein, lass mich das sauber machen. Für eine Funktion f = Θ/Θ₀:

  f(Qθ) = 1 + a₂(Qθ)² + a₄(Qθ)⁴ + ...
  f(Qθ)^5 = 1 + 5a₂(Qθ)² + [5a₄ + 10a₂²](Qθ)⁴ + ...  
  [5 terms from binomial: 5·a₄ + C(5,2)·a₂² = 5a₄ + 10a₂²]

Proton-Seite (3 Quarks, jeweils 5 Dimensionen):
  P(θ) = [f(Q_u·θ)]^{10} · [f(Q_d·θ)]^5

  [f(Qθ)]^10 = 1 + 10·a₂·(Qθ)² + [10·a₄ + 45·a₂²]·(Qθ)⁴ + ...
  [f(Qθ)]^5  = 1 + 5·a₂·(Qθ)²  + [5·a₄ + 10·a₂²]·(Qθ)⁴ + ...

  P(θ) = {1 + 10a₂·Q_u²θ² + [10a₄ + 45a₂²]Q_u⁴θ⁴}
       × {1 + 5a₂·Q_d²θ²  + [5a₄  + 10a₂²]Q_d⁴θ⁴}
       + cross terms...

  At O(θ²): P₂ = (10Q_u² + 5Q_d²)·a₂
  At O(θ⁴): P₄ = (10a₄+45a₂²)Q_u⁴ + (5a₄+10a₂²)Q_d⁴ 
                + 10·5·a₂²·Q_u²·Q_d²

Elektron-Seite:
  E(θ) = [f(Q_e·θ)]^5
  At O(θ²): E₂ = 5·Q_e²·a₂
  At O(θ⁴): E₄ = (5a₄ + 10a₂²)·Q_e⁴

Ratio: R(θ) = 6·P(θ)/E(θ) = 6·π⁵·{1 + [P₂-E₂]θ² 
              + [P₄-E₄-(P₂-E₂)·E₂]θ⁴ + ...}

Wait, for R = P/E, expand:
  R = (P₀ + P₂θ² + P₄θ⁴)(1 - E₂θ² + (E₂² - E₄)θ⁴)
    = P₀ + (P₂ - P₀E₂)θ² + (P₄ - P₂E₂ + P₀E₂² - P₀E₄)θ⁴

With P₀ = E₀ = 1 (normalized):
  θ² coeff: P₂ - E₂ = a₂·(10Q_u² + 5Q_d² - 5Q_e²)
  = a₂·(10·4/9 + 5·1/9 - 5·1)
  = a₂·(40/9 + 5/9 - 45/9)
  = a₂·(45/9 - 45/9) = 0  ✓ (as expected!)

  θ⁴ coeff: P₄ - P₂E₂ + E₂² - E₄
  With P₂ = E₂ (since the θ² terms match):
  = P₄ - E₂² + E₂² - E₄
  = P₄ - E₄
""")

Q_u = mpf(2)/3
Q_d = -mpf(1)/3
Q_e = -mpf(1)

# P₄ = (10a₄+45a₂²)Q_u⁴ + (5a₄+10a₂²)Q_d⁴ + 50a₂²·Q_u²·Q_d²
P4 = (10*a4 + 45*a2**2)*Q_u**4 + (5*a4 + 10*a2**2)*Q_d**4 + 50*a2**2*Q_u**2*Q_d**2

# E₄ = (5a₄+10a₂²)Q_e⁴
E4 = (5*a4 + 10*a2**2)*Q_e**4

C4_coeff = P4 - E4

print(f"Analytische Koeffizienten:")
print(f"  a₂ = {nstr(a2, 20)}")
print(f"  a₄ = {nstr(a4, 20)}")
print()
print(f"  P₄ = {nstr(P4, 20)}")
print(f"  E₄ = {nstr(E4, 20)}")
print(f"  C₄ = P₄ - E₄ = {nstr(C4_coeff, 20)}")
print()
print(f"  Numerisch (Richardson): C₄ = {nstr(C4_richardson, 20)}")
print(f"  Analytisch:             C₄ = {nstr(C4_coeff, 20)}")
print(f"  Übereinstimmung: {abs(C4_coeff - C4_richardson) < mpf(10)**(-15)}")
print()

# The mass ratio is:
# m_p/m_e = 6π⁵ · (1 + C₄·θ⁴ + ...)
# 
# In the SFST, θ is identified with a function of α.
# The claim: θ⁴ ∝ α², so the correction is at O(α²).
# 
# And the coefficient should be 1/√8.

print("=" * 72)
print("  TEIL 11: VERBINDUNG θ⁴ → α² UND DER KOEFFIZIENT")
print("=" * 72)

# In the SFST framework, the Poisson-dual instanton gives:
# The correction to Θ at the self-dual point comes from m≠0 modes:
# Θ(1,0) = √π · (1 + 2e^{-π²} + ...)
# 
# The identification is: e^{-π²} ≈ α² (up to ~3%)
# And the twist θ is related to the gauge field strength via θ ~ √α
# So θ² ~ α and θ⁴ ~ α²

# If we set θ² = α (the simplest identification):
alpha_phys = mpf(1)/mpf('137.035999177')

print(f"Falls θ² = α:")
print(f"  θ⁴ = α² = {nstr(alpha_phys**2, 15)}")
print(f"  Korrektur = C₄ · α² = {nstr(C4_coeff * alpha_phys**2, 15)}")
print()

# The SFST claims m_p/m_e = 6π⁵(1 + α²/√8)
# So the coefficient of α² should be 1/√8 = 0.35355...
one_over_sqrt8 = 1/sqrt(8)
print(f"  SFST-Behauptung: Koeffizient = 1/√8 = {nstr(one_over_sqrt8, 15)}")
print(f"  Berechnet:       Koeffizient C₄ = {nstr(C4_coeff, 15)}")
print(f"  Verhältnis:      C₄/(1/√8) = {nstr(C4_coeff/one_over_sqrt8, 15)}")
print()

# Hmm, C₄ depends on a₂ and a₄ which are theta-function specific.
# Let's see what C₄ actually is in terms of known quantities.

print("Aufschlüsselung:")
print(f"  Q_u⁴ = (2/3)⁴ = {nstr(Q_u**4, 10)} = 16/81")
print(f"  Q_d⁴ = (1/3)⁴ = {nstr(Q_d**4, 10)} = 1/81")
print(f"  Q_e⁴ = 1")
print(f"  Q_u²Q_d² = {nstr(Q_u**2*Q_d**2, 10)} = 4/81")
print()

# P₄ = (10a₄+45a₂²)·16/81 + (5a₄+10a₂²)·1/81 + 50a₂²·4/81
# E₄ = (5a₄+10a₂²)·1

# P₄ = [160a₄ + 720a₂²]/81 + [5a₄ + 10a₂²]/81 + [200a₂²]/81
#     = [165a₄ + 930a₂²]/81
#     = [55a₄ + 310a₂²]/27

# E₄ = 5a₄ + 10a₂²

# C₄ = P₄ - E₄ = [55a₄ + 310a₂²]/27 - 5a₄ - 10a₂²
#     = [55a₄ + 310a₂² - 135a₄ - 270a₂²]/27
#     = [-80a₄ + 40a₂²]/27
#     = 40·[a₂² - 2a₄]/27

C4_check = 40*(a2**2 - 2*a4)/27
print(f"Vereinfacht: C₄ = 40·(a₂² - 2a₄)/27")
print(f"  = {nstr(C4_check, 20)}")
print(f"  Stimmt mit oben überein: {abs(C4_check - C4_coeff) < mpf(10)**(-30)}")
print()

# What is a₂² - 2a₄?
# a₂ = Θ''/(2Θ₀), a₄ = Θ''''/(24Θ₀)
# a₂² = [Θ'']²/(4Θ₀²)
# 2a₄ = Θ''''/(12Θ₀)
# a₂² - 2a₄ = [Θ'']²/(4Θ₀²) - Θ''''/(12Θ₀)
#            = [3Θ₀·Θ''² - Θ₀²·Θ'''']/(12Θ₀²)

val = a2**2 - 2*a4
print(f"a₂² - 2a₄ = {nstr(val, 20)}")
print(f"C₄ = 40/27 · {nstr(val, 20)} = {nstr(40*val/27, 20)}")
print()

# Now the key question: what IS C₄ numerically, and how does it 
# relate to 1/√8?

print("=" * 72)
print("  TEIL 12: NUMERISCHER VERGLEICH MIT 1/√8")
print("=" * 72)
print()
print(f"C₄ (berechnet) = {nstr(C4_coeff, 25)}")
print(f"1/√8           = {nstr(one_over_sqrt8, 25)}")
print(f"")
print(f"Verhältnis C₄/(1/√8) = {nstr(C4_coeff/one_over_sqrt8, 20)}")
print()

# Also check: what if the identification is θ² = c·α for some constant c?
# Then the coefficient of α² would be C₄·c²
# For it to equal 1/√8, we need c² = 1/(√8·C₄)
c_sq_needed = 1/(sqrt(8)*C4_coeff)
c_needed = sqrt(abs(c_sq_needed))
print(f"Für C₄·c² = 1/√8 braucht man:")
print(f"  c² = 1/(√8·C₄) = {nstr(c_sq_needed, 15)}")
print(f"  c  = {nstr(c_needed, 15)}")
print()

# Check: is there a natural identification?
# Perhaps θ² = α/(4π)?  or θ² = α/π?
for label, c_val in [("α", 1), ("α/(2π)", 1/(2*pi)), ("α/(4π)", 1/(4*pi)), 
                      ("α/π", 1/pi), ("α·π", pi), ("2πα", 2*pi)]:
    coeff = C4_coeff * mpf(str(c_val))**2
    print(f"  θ² = {label:>8s}:  Koeff von α² = C₄·c² = {nstr(coeff, 12)},  Ratio zu 1/√8: {nstr(coeff/one_over_sqrt8, 8)}")

print()
print("=" * 72)
print("  ZUSAMMENFASSUNG")
print("=" * 72)
print(f"""
ERGEBNISSE DER SPURRECHNUNG:

1. BESTÄTIGT: Der θ²-Term (= α¹-Term) verschwindet EXAKT im 
   Quotienten m_p/m_e, weil Σ_p Q_i² = Q_e² = 1.
   Dies folgt aus der Algebra der Quarkladungen.

2. BERECHNET: Der führende Korrekturterm ist bei O(θ⁴):
   m_p/m_e = 6π⁵ · (1 + C₄·θ⁴ + ...)
   mit C₄ = 40(a₂² - 2a₄)/27 = {nstr(C4_coeff, 15)}

3. Die Theta-Funktions-Koeffizienten sind:
   a₂ = Θ''(0)/(2Θ(0)) = {nstr(a2, 15)}
   a₄ = Θ''''(0)/(24Θ(0)) = {nstr(a4, 15)}

4. OFFENE FRAGE: Die Identifikation θ² = f(α) bestimmt den 
   physikalischen α²-Koeffizienten als C₄·f(α)².
   
   Für C₄·f² = 1/√8 wird benötigt: f² = {nstr(c_sq_needed, 10)}.
   
   Mit θ² = α (einfachste Wahl): Koeff = {nstr(C4_coeff, 10)} ≠ 1/√8.
   
   Die Diskrepanz ist ein Faktor {nstr(C4_coeff/one_over_sqrt8, 6)}.
   
5. BEDEUTUNG: Der Koeffizient 1/√8 folgt NICHT direkt aus der 
   naiven Spurrechnung mit θ² = α. Es gibt eine 
   Normierungsfreiheit in der Identifikation θ ↔ α, die 
   die Diskrepanz absorbieren KÖNNTE, aber diese Identifikation
   müsste aus einem unabhängigen Prinzip folgen.
""")

# Final check: verify everything numerically
print("=" * 72)
print("  NUMERISCHE VERIFIKATION")
print("=" * 72)

alpha = mpf(1)/mpf('137.035999177')
m_exp = mpf('1836.15267363')

# With the naive θ² = α:
m_naive = 6*pi**5*(1 + C4_coeff*alpha**2)
# With 1/√8:
m_sfst = 6*pi**5*(1 + alpha**2/sqrt(8))

print(f"Experiment:          m_p/m_e = {nstr(m_exp, 13)}")
print(f"6π⁵ (Basis):                 = {nstr(6*pi**5, 13)}")
print(f"6π⁵(1 + C₄·α²)    [θ²=α]:  = {nstr(m_naive, 13)}")
print(f"6π⁵(1 + α²/√8)    [SFST]:   = {nstr(m_sfst, 13)}")
print()
print(f"Abweichung (C₄·α²):  {nstr(abs(m_naive - m_exp)/m_exp * 1e6, 6)} ppm")
print(f"Abweichung (1/√8):    {nstr(abs(m_sfst - m_exp)/m_exp * 1e6, 6)} ppm")
