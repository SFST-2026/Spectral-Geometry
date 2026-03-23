"""
Bestimme den EXAKTEN Faktor c₃_raw/c₃_CODATA bei steigendem M_cut.
Falls er gegen eine Konstante konvergiert: identifiziere sie.
"""
from mpmath import mp, mpf, pi as PI, log, sqrt, nstr, coth, exp, matrix, lu_solve
mp.dps = 50

c2 = mpf(5)/2*log(2) - mpf(3)/8
c3C = mpf('0.048690955374786034937')
d_S = 4
WEIGHTS = [mpf(0),mpf(0),mpf(1),mpf(-1),mpf(1)/2,mpf(-1)/2,mpf(1)/2,mpf(-1)/2]

def compute_p_coeffs(N_shell):
    """Berechne p₂, p₄, p₆ für gegebenes N_shell."""
    def P_coth(a):
        P_free = mpf(0); P_tw = mpf(0)
        for w in WEIGHTS:
            for label in ['tw','fr']:
                wa = w*a if label=='tw' else mpf(0)
                wa_sq = (2*wa)**2; s = mpf(0)
                if wa_sq > mpf('1e-20'):
                    arg = PI*sqrt(wa_sq)/2
                    s += d_S*(4*exp(-2*arg) if arg>50 else 2*log(coth(arg)))
                for r2 in range(1, N_shell+1):
                    cnt=0; mx=int(float(sqrt(mpf(r2))))+1
                    for n1 in range(-mx,mx+1):
                        if n1*n1>r2:continue
                        for n2 in range(-mx,mx+1):
                            s2=n1*n1+n2*n2
                            if s2>r2:continue
                            for n3 in range(-mx,mx+1):
                                s3=s2+n3*n3
                                if s3>r2:continue
                                n4sq=r2-s3;n4=int(round(float(sqrt(mpf(n4sq)))))
                                if n4*n4==n4sq:cnt+=2 if n4>0 else 1
                    if cnt>0:
                        M2=4*r2+wa_sq;arg=PI*sqrt(M2)/2
                        val=4*exp(-2*arg) if arg>50 else 2*log(coth(arg))
                        s+=d_S*cnt*val
                if label=='tw': P_tw+=s
                else: P_free+=s
        return P_tw - P_free
    
    # Symmetrisierte eps = da^2 Daten
    das = [mpf(k)/200 for k in range(1, 11)]  # da = 0.005 bis 0.05
    eps_P = []
    for da in das:
        Pp = P_coth(mpf(1)/2 + da)
        Pm = P_coth(mpf(1)/2 - da)
        eps_P.append((da**2, (Pp+Pm)/2))
    
    # Fit: P(eps) = P0 + p2*eps + p4*eps^2 + p6*eps^3
    n = len(eps_P); no = 4
    A = matrix(n, no); b = matrix(n, 1)
    for i, (e, P) in enumerate(eps_P):
        for j in range(no): A[i,j] = e**(j+1)  # eps, eps^2, eps^3, eps^4
        b[i] = P - eps_P[0][1]  # subtract P(eps_min) for stability... no
    # Actually fit P directly
    A2 = matrix(n, no+1); b2 = matrix(n, 1)
    for i, (e, P) in enumerate(eps_P):
        for j in range(no+1): A2[i,j] = e**j
        b2[i] = P
    pk = lu_solve(A2.T*A2, A2.T*b2)
    return pk[1], pk[2], pk[3]  # p2, p4, p6

print("="*70)
print("  KONVERGENZ DES RATIO c₃_raw/c₃_CODATA")
print("="*70)
print(f"  {'N':>4} {'p₂':>12} {'p₄':>12} {'p₆':>12} {'Ratio':>12} {'Ratio-5':>10} {'Ratio-π²/2':>10}")
print(f"  {'-'*75}")

import time
for N in [10, 12, 15, 18, 20, 25]:
    t0 = time.time()
    p2, p4, p6 = compute_p_coeffs(N)
    sigma4 = c2/p4
    sigma6 = sigma4 * sqrt(sigma4)
    c3_raw = p6 * sigma6
    ratio = c3_raw / c3C
    dt = time.time()-t0
    print(f"  {N:>4} {nstr(p2,8):>12} {nstr(p4,8):>12} {nstr(p6,8):>12} "
          f"{nstr(ratio,8):>12} {nstr(ratio-5,5):>10} {nstr(ratio-PI**2/2,5):>10} ({dt:.1f}s)")

print(f"\n  Kandidaten:")
print(f"    5     = {nstr(mpf(5), 10)}")
print(f"    π²/2  = {nstr(PI**2/2, 10)}")
print(f"    d_S+1 = 5")
print(f"    dim T⁵ = 5")

# Berechne c₃ für die besten Kandidaten
print(f"\n  c₃ = c₃_raw / N:")
for N_val, label in [(mpf(5), "5"), (PI**2/2, "pi^2/2"), 
                      (mpf('4.9515'), "4.9515 (fit)")]:
    c3_test = c3_raw / N_val
    err = abs(c3_test/c3C - 1)*100
    print(f"    N={label:>10}: c₃={nstr(c3_test,10)} err={float(err):.4f}%")
