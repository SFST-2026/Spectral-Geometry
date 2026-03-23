#!/usr/bin/env python3
"""
===============================================================================
SFST: THE 6.66 GAP INVESTIGATION — v2 (BUGFIX + GPU)
===============================================================================

BUGFIX: v1 applied exp(2πi·a·w) at EACH link → sin²(p+π) = sin²(p) → 
        trivially same as untwisted. CORRECT: exp(2πi·a·w/Ls) per link,
        so Polyakov loop = exp(2πi·a·w).

PLAN:
  Part A: Exact perturbative baseline (factorized ζ-regularized formula)
  Part B: Full Dirac operator on T⁵ lattice (naive + Wilson fermions)
          with Hosotani, instanton, and Monte Carlo backgrounds
  Part C: Monte Carlo SU(3) + fermionic determinant
  Part D: Faddeev-Popov / moduli space analysis
  Part E: Multi-GPU eigenvalue computation for Ls=5,6

HARDWARE TARGET: 4× A100 80GB or 8× V100 16GB
USAGE: python sfst_gap_v2.py [--part A|B|C|D|E|all] [--Ls 4,5] [--fermion naive|wilson]

===============================================================================
"""

import numpy as np
import os, sys, time, json, argparse
from itertools import product as iterprod

PI = np.pi

# Try importing cupy
try:
    import cupy as cp
    HAS_CUPY = True
except ImportError:
    HAS_CUPY = False
    cp = None


# =====================================================================
#  GPU UTILITIES
# =====================================================================

class GPUManager:
    """Manage multi-GPU resources."""
    
    def __init__(self):
        self.n_gpu = 0
        self.gpu_info = []
        self.backend = 'numpy'
        
        if HAS_CUPY:
            try:
                self.n_gpu = cp.cuda.runtime.getDeviceCount()
                self.backend = 'cupy'
                for i in range(self.n_gpu):
                    with cp.cuda.Device(i):
                        props = cp.cuda.runtime.getDeviceProperties(i)
                        name = props['name'].decode() if isinstance(props['name'], bytes) else str(props['name'])
                        mem = props['totalGlobalMem'] / 1e9
                        # Check FP64 performance
                        self.gpu_info.append({'name': name, 'mem_gb': mem, 'id': i})
            except Exception as e:
                print(f"  ⚠ GPU-Erkennung fehlgeschlagen: {e}")
                self.backend = 'numpy'
    
    def print_info(self):
        print(f"  Backend: {self.backend}")
        print(f"  GPUs: {self.n_gpu}")
        for g in self.gpu_info:
            print(f"    GPU {g['id']}: {g['name']} ({g['mem_gb']:.1f} GB)")
        if self.n_gpu > 0:
            print(f"  Gesamt-VRAM: {sum(g['mem_gb'] for g in self.gpu_info):.1f} GB")
    
    def best_gpu(self):
        """Return index of GPU with most memory."""
        if not self.gpu_info:
            return 0
        return max(self.gpu_info, key=lambda g: g['mem_gb'])['id']
    
    def use_gpu(self, idx=None):
        """Activate a specific GPU."""
        if self.backend != 'cupy':
            return np
        if idx is None:
            idx = self.best_gpu()
        cp.cuda.Device(idx).use()
        return cp
    
    def eigvalsh(self, M, gpu_idx=None):
        """Compute eigenvalues of Hermitian matrix, using GPU if available."""
        if self.backend == 'cupy':
            xp = self.use_gpu(gpu_idx)
            M_gpu = xp.asarray(M)
            eigs = xp.linalg.eigvalsh(M_gpu)
            result = eigs.get()
            del M_gpu, eigs
            xp.get_default_memory_pool().free_all_blocks()
            return result
        else:
            return np.linalg.eigvalsh(M)


# =====================================================================
#  SU(3) UTILITIES
# =====================================================================

def random_su3_near_identity(eps=0.2):
    """SU(3) matrix near identity via Cabibbo-Marinari."""
    M = np.eye(3, dtype=complex)
    for i, j in [(0, 1), (0, 2), (1, 2)]:
        a = np.array([1.0, 0, 0, 0]) + eps * np.random.randn(4)
        a /= np.linalg.norm(a)
        su2 = np.array([[a[0]+1j*a[3], a[2]+1j*a[1]], 
                         [-a[2]+1j*a[1], a[0]-1j*a[3]]])
        R = np.eye(3, dtype=complex)
        R[i,i] = su2[0,0]; R[i,j] = su2[0,1]
        R[j,i] = su2[1,0]; R[j,j] = su2[1,1]
        M = R @ M
    return M


def random_su3_uniform():
    """Uniform random SU(3) matrix (Haar measure, approximate)."""
    M = np.eye(3, dtype=complex)
    for _ in range(10):  # many hits for good Haar coverage
        M = random_su3_near_identity(eps=2.0) @ M
    return M


# =====================================================================
#  GAUGE LINK CONFIGURATIONS
# =====================================================================

def make_links_hosotani(Ls, a_twist, mu_twist=4):
    """
    CORRECT Hosotani twist: phase distributed over Ls links.
    U_mu(x) = exp(2πi·a·H/Ls) for mu = mu_twist, else identity.
    Polyakov loop = U^Ls = exp(2πi·a·H).
    """
    N = Ls**5
    shape = (Ls, Ls, Ls, Ls, Ls, 3, 3)
    
    # Phase PER LINK: θ_c = 2π·a·w_c / Ls
    weights = np.array([1.0, 0.0, -1.0])
    U_twist = np.diag(np.exp(2j * PI * a_twist * weights / Ls))
    eye3 = np.eye(3, dtype=complex)
    
    links = []
    for mu in range(5):
        link = np.zeros(shape, dtype=complex)
        for idx in np.ndindex(Ls, Ls, Ls, Ls, Ls):
            link[idx] = U_twist if mu == mu_twist else eye3
        links.append(link)
    
    # Verify Polyakov loop
    P = np.eye(3, dtype=complex)
    for step in range(Ls):
        P = P @ U_twist
    P_expected = np.diag(np.exp(2j * PI * a_twist * weights))
    assert np.allclose(P, P_expected, atol=1e-12), \
        f"Polyakov loop check failed: {np.diag(P)} vs {np.diag(P_expected)}"
    
    print(f"    Polyakov-Phasen: {np.angle(np.diag(P))/PI}π")
    
    return links


def make_links_free(Ls):
    """Trivial (unit) gauge links."""
    shape = (Ls, Ls, Ls, Ls, Ls, 3, 3)
    eye3 = np.eye(3, dtype=complex)
    links = []
    for mu in range(5):
        link = np.zeros(shape, dtype=complex)
        for idx in np.ndindex(Ls, Ls, Ls, Ls, Ls):
            link[idx] = eye3
        links.append(link)
    return links


def make_links_instanton(Ls, k_inst, a_twist=0.5, rho_frac=0.3):
    """
    Instanton (k=k_inst) + Hosotani twist.
    SU(2) ⊂ SU(3) BPST instanton in directions 0-3,
    Hosotani twist in direction 4.
    """
    shape = (Ls, Ls, Ls, Ls, Ls, 3, 3)
    a_lat = PI / Ls  # lattice spacing
    rho = rho_frac * PI  # instanton radius
    
    # 't Hooft symbols
    eta = np.zeros((3, 4, 4))
    eta[0,0,1] =  1; eta[0,1,0] = -1; eta[0,2,3] =  1; eta[0,3,2] = -1
    eta[1,0,2] =  1; eta[1,2,0] = -1; eta[1,3,1] =  1; eta[1,1,3] = -1
    eta[2,0,3] =  1; eta[2,3,0] = -1; eta[2,1,2] =  1; eta[2,2,1] = -1
    
    sigma = np.zeros((3, 2, 2), dtype=complex)
    sigma[0] = [[0,1],[1,0]]
    sigma[1] = [[0,-1j],[1j,0]]
    sigma[2] = [[1,0],[0,-1]]
    
    L_phys = PI
    centers = [np.array([L_phys*(i+0.5)/k_inst]*4) for i in range(k_inst)]
    
    weights = np.array([1.0, 0.0, -1.0])
    U_twist_5 = np.diag(np.exp(2j * PI * a_twist * weights / Ls))
    
    links = []
    for mu in range(5):
        link = np.zeros(shape, dtype=complex)
        
        for idx in np.ndindex(Ls, Ls, Ls, Ls, Ls):
            if mu == 4:
                link[idx] = U_twist_5
            else:
                x = np.array(idx[:4], dtype=float) * a_lat
                mid = x.copy(); mid[mu] += 0.5 * a_lat
                
                A_sum = np.zeros((2, 2), dtype=complex)
                for c in centers:
                    for shifts in iterprod([-1, 0, 1], repeat=4):
                        c_s = c + np.array(shifts) * L_phys
                        dx = mid - c_s
                        r2 = np.sum(dx**2)
                        if r2 < 1e-20:
                            continue
                        fac = rho**2 / (r2 * (r2 + rho**2))
                        for a_idx in range(3):
                            coeff = sum(eta[a_idx, mu, nu] * dx[nu] for nu in range(4))
                            A_sum += coeff * fac * sigma[a_idx]
                
                # Cayley transform for unitarity
                M = 1j * a_lat * A_sum
                I2 = np.eye(2, dtype=complex)
                U_2x2 = np.linalg.solve(I2 - 0.5*M, I2 + 0.5*M)
                
                U_3x3 = np.eye(3, dtype=complex)
                U_3x3[:2, :2] = U_2x2
                link[idx] = U_3x3
        
        links.append(link)
    
    return links


def make_links_random_thermalized(Ls, beta, n_therm=100, n_hits=3):
    """Generate thermalized SU(3) config via Metropolis on T⁵."""
    shape = (Ls, Ls, Ls, Ls, Ls, 3, 3)
    strides = np.array([Ls**4, Ls**3, Ls**2, Ls, 1])
    N = Ls**5
    
    # Cold start: all links = identity
    links = [np.zeros(shape, dtype=complex) for _ in range(5)]
    for mu in range(5):
        for idx in np.ndindex(Ls, Ls, Ls, Ls, Ls):
            links[mu][idx] = np.eye(3, dtype=complex)
    
    def flat(coords):
        return int(np.dot(np.array(coords), strides))
    
    def staple(site_coords, mu):
        S = np.zeros((3, 3), dtype=complex)
        for nu in range(5):
            if nu == mu: continue
            
            xpmu = list(site_coords)
            xpmu[mu] = (xpmu[mu] + 1) % Ls
            
            xpnu = list(site_coords)
            xpnu[nu] = (xpnu[nu] + 1) % Ls
            
            xmnu = list(site_coords)
            xmnu[nu] = (xmnu[nu] - 1) % Ls
            
            xpmumnu = list(xpmu)
            xpmumnu[nu] = (xpmumnu[nu] - 1) % Ls
            
            # Forward
            S += (links[nu][tuple(xpmu)] 
                  @ links[mu][tuple(xpnu)].conj().T 
                  @ links[nu][tuple(site_coords)].conj().T)
            # Backward
            S += (links[nu][tuple(xpmumnu)].conj().T 
                  @ links[mu][tuple(xmnu)].conj().T 
                  @ links[nu][tuple(xmnu)])
        return S
    
    # Metropolis sweeps
    print(f"    Thermalisierung: {n_therm} Sweeps, β={beta}")
    for sweep in range(n_therm):
        acc = 0; tot = 0
        for idx in np.ndindex(Ls, Ls, Ls, Ls, Ls):
            for mu in range(5):
                S = staple(idx, mu)
                U_old = links[mu][idx].copy()
                for hit in range(n_hits):
                    R = random_su3_near_identity(eps=0.3)
                    U_new = R @ U_old
                    dS = -beta/3.0 * np.real(np.trace((U_new - U_old) @ S.conj().T))
                    if dS < 0 or np.random.random() < np.exp(-dS):
                        U_old = U_new
                        links[mu][idx] = U_new
                        acc += 1
                    tot += 1
        
        if sweep % 20 == 0 or sweep == n_therm - 1:
            print(f"      Sweep {sweep:4d}: Akzeptanz = {acc/tot:.3f}", flush=True)
    
    return links


# =====================================================================
#  DIRAC OPERATOR CONSTRUCTION
# =====================================================================

def build_dirac_op(Ls, links, fermion_type='naive', mass=0.0, r_wilson=1.0):
    """
    Build the 5D Dirac operator D on T⁵.
    
    fermion_type:
      'naive': D = iΣ γ_μ ∇_μ (has doublers, but no Wilson-r ambiguity)
      'wilson': D = iΣ γ_μ ∇_μ - r/(2a) Σ Δ_μ (Wilson term removes doublers)
    
    Returns D†D (Hermitian positive semi-definite) for eigenvalue computation.
    """
    N = Ls**5
    Nc, dS = 3, 4
    dim = N * Nc * dS
    
    mem_gb = dim**2 * 16 / 1e9
    print(f"    dim = {dim}, Matrix = {mem_gb:.2f} GB", flush=True)
    
    if mem_gb > 100:
        print(f"    ⚠ Zu groß für dichte Matrix — brauche iterativen Solver")
        return None, dim
    
    # Gamma matrices (Euclidean, Hermitian, {γ_μ, γ_ν} = 2δ_μν)
    gamma = np.zeros((5, 4, 4), dtype=complex)
    gamma[0] = np.array([[0,0,0,1j],[0,0,1j,0],[0,-1j,0,0],[-1j,0,0,0]])
    gamma[1] = np.array([[0,0,0,-1],[0,0,1,0],[0,1,0,0],[-1,0,0,0]])
    gamma[2] = np.array([[0,0,1j,0],[0,0,0,-1j],[-1j,0,0,0],[0,1j,0,0]])
    gamma[3] = np.array([[0,0,1,0],[0,0,0,1],[1,0,0,0],[0,1,0,0]])
    gamma[4] = np.array([[1,0,0,0],[0,1,0,0],[0,0,-1,0],[0,0,0,-1]])
    
    strides = np.array([Ls**4, Ls**3, Ls**2, Ls, 1])
    
    # Neighbor tables
    nbr_fwd = np.zeros((N, 5), dtype=int)
    nbr_bwd = np.zeros((N, 5), dtype=int)
    for x in np.ndindex(Ls, Ls, Ls, Ls, Ls):
        i = int(np.dot(x, strides))
        for mu in range(5):
            f = list(x); f[mu] = (f[mu]+1) % Ls
            b = list(x); b[mu] = (b[mu]-1) % Ls
            nbr_fwd[i, mu] = int(np.dot(f, strides))
            nbr_bwd[i, mu] = int(np.dot(b, strides))
    
    # Flatten links
    lnk = [links[mu].reshape(N, Nc, Nc) for mu in range(5)]
    
    # Build D
    D = np.zeros((dim, dim), dtype=complex)
    I_s = np.eye(dS, dtype=complex)
    
    print(f"    Operator ({fermion_type}) konstruieren...", flush=True)
    t0 = time.time()
    
    for site in range(N):
        for mu in range(5):
            fwd = nbr_fwd[site, mu]
            bwd = nbr_bwd[site, mu]
            U_f = lnk[mu][site]         # U_μ(x)
            U_b = lnk[mu][bwd].conj().T  # U_μ†(x-μ)
            
            # Naive part: (i γ_μ / 2) [U_μ(x) δ_{y,x+μ} - U_μ†(x-μ) δ_{y,x-μ}]
            ig = 0.5j * gamma[mu]
            
            for c in range(Nc):
                for cp in range(Nc):
                    for s in range(dS):
                        row = site*Nc*dS + c*dS + s
                        for sp in range(dS):
                            D[row, fwd*Nc*dS + cp*dS + sp] += ig[s,sp] * U_f[c,cp]
                            D[row, bwd*Nc*dS + cp*dS + sp] -= ig[s,sp] * U_b[c,cp]
            
            if fermion_type == 'wilson':
                # Wilson term: -r/(2) [U_μ(x) δ_{y,x+μ} + U_μ†(x-μ) δ_{y,x-μ} - 2 δ_{xy}]
                for c in range(Nc):
                    for cp in range(Nc):
                        for s in range(dS):
                            row = site*Nc*dS + c*dS + s
                            sp = s  # Wilson term is diagonal in spinor
                            
                            D[row, fwd*Nc*dS+cp*dS+sp] -= 0.5*r_wilson * I_s[s,sp] * U_f[c,cp]
                            D[row, bwd*Nc*dS+cp*dS+sp] -= 0.5*r_wilson * I_s[s,sp] * U_b[c,cp]
                            D[row, site*Nc*dS+c*dS+sp] += r_wilson * I_s[s,sp] * (1.0 if c==cp else 0.0)
    
    dt = time.time() - t0
    print(f"    Konstruktion: {dt:.1f}s")
    
    # D†D (Hermitian, positive semi-definite)
    DdD = D.conj().T @ D
    herm_err = np.linalg.norm(DdD - DdD.conj().T) / np.linalg.norm(DdD)
    print(f"    ||D†D - (D†D)†|| / ||D†D|| = {herm_err:.2e}")
    
    return DdD, dim


# =====================================================================
#  PART A: EXACT PERTURBATIVE (ζ-REGULARIZED)
# =====================================================================

def part_A():
    """Factorized det ratio — NO lattice artifacts."""
    print("\n" + "=" * 72)
    print("  PART A: EXAKTE PERTURBATIVE BASELINE")
    print("=" * 72)
    
    R, a = 0.5, 0.5
    weights = [-1, 0, 1]
    NfxdS = 8
    target = 4 * np.log(6 * PI**5)
    
    def F_mode(m2, a_val, ws):
        beta = np.sqrt(m2) if m2 > 0 else 0
        if beta < 1e-12:
            return sum(2*np.log(abs(2*np.sin(PI*a_val*w))) for w in ws if w != 0)
        result = 0.0
        for w in ws:
            alpha = a_val * w
            num = np.cosh(2*PI*beta) - np.cos(2*PI*alpha)
            den = 2*np.sinh(PI*beta)**2
            if den > 0 and num > 0:
                result += np.log(num/den)
        return result
    
    # Already converged at L_perp=5 (exponential decay)
    L_perp = 10
    total = 0.0
    for n1, n2, n3, n4 in iterprod(range(-L_perp, L_perp+1), repeat=4):
        total += F_mode(n1**2 + n2**2 + n3**2 + n4**2, a, weights)
    
    full = total * NfxdS
    gap = target - full
    
    print(f"\n  Skalarer Sektor:    {total:.8f}")
    print(f"  × N_f·d_S = 8:     {full:.8f}")
    print(f"  WH M Zielwert:      {target:.8f}")
    print(f"  LÜCKE:             {gap:.8f}")
    print(f"  exp(Lücke):        {np.exp(gap):.4f}")
    
    # Decomposition
    print(f"\n  Zerlegung:")
    print(f"    4·ln(6π⁵) = 4·ln(6) + 20·ln(π)")
    print(f"              = {4*np.log(6):.6f} + {20*np.log(PI):.6f}")
    print(f"    Perturbativ = {full:.6f}")
    print(f"    Lücke       = {gap:.6f} ≈ 4·ln(π) + 3·ln(2) = {4*np.log(PI)+3*np.log(2):.6f}")
    print(f"                 (Abw. {abs(gap - 4*np.log(PI)-3*np.log(2)):.6f})")
    
    return {'scalar': total, 'full': full, 'target': target, 'gap': gap}


# =====================================================================
#  PART B: LATTICE DIRAC SPECTRUM
# =====================================================================

def part_B(gpu, Ls_list=[4], fermion='naive', r_wilson=1.0):
    """
    Full Dirac spectrum on T⁵ lattice with various backgrounds.
    Tests both naive and Wilson fermions.
    """
    print("\n" + "=" * 72)
    print(f"  PART B: GITTER-DIRAC-SPEKTRUM ({fermion.upper()} Fermionen)")
    if fermion == 'wilson':
        print(f"  Wilson-Parameter r = {r_wilson}")
    print("=" * 72)
    
    target = 4 * np.log(6 * PI**5)
    results = {}
    
    for Ls in Ls_list:
        print(f"\n  {'─'*60}")
        print(f"  Ls = {Ls}  (N = {Ls**5}, dim = {Ls**5*12})")
        print(f"  {'─'*60}")
        
        dim = Ls**5 * 12
        mem = dim**2 * 16 / 1e9
        max_mem = max([g['mem_gb'] for g in gpu.gpu_info], default=4)
        
        if mem > max_mem * 0.8:
            print(f"    ⚠ {mem:.1f} GB > verfügbarer Speicher — überspringe")
            continue
        
        configs = [
            ('free',     'Frei (a=0)',        lambda: make_links_free(Ls)),
            ('hoso',     'Hosotani (a=1/2)',   lambda: make_links_hosotani(Ls, 0.5)),
            ('inst_k1',  'Instanton k=1',      lambda: make_links_instanton(Ls, 1)),
            ('inst_k2',  'Instanton k=2',      lambda: make_links_instanton(Ls, 2)),
        ]
        
        data = {}
        for key, label, make_fn in configs:
            print(f"\n  [{key}] {label}")
            links = make_fn()
            
            DdD, d = build_dirac_op(Ls, links, fermion, r_wilson=r_wilson)
            if DdD is None:
                continue
            
            t0 = time.time()
            eigs = gpu.eigvalsh(DdD)
            dt = time.time() - t0
            print(f"    Eigenwerte: {dt:.1f}s")
            
            tol = max(1e-10 * np.max(eigs), 1e-14)
            nz = int(np.sum(eigs < tol))
            nzero = eigs[eigs >= tol]
            ld = float(np.sum(np.log(nzero)))
            
            print(f"    n_zero = {nz}, ln(det') = {ld:.4f}")
            print(f"    eig_range: [{np.min(eigs):.2e}, {np.max(eigs):.2e}]")
            
            data[key] = {'ln_det': ld, 'n_zero': nz, 'n_eig': len(eigs)}
            del DdD
        
        # Ratios
        print(f"\n  ── VERHÄLTNISSE (Ls={Ls}, {fermion}) ──")
        if 'free' in data and 'hoso' in data:
            r = data['hoso']['ln_det'] - data['free']['ln_det']
            print(f"    ln(det'_hoso/det'_free)    = {r:.6f}")
            print(f"    (Zielwert perturbativ:      23.397)")
        if 'free' in data and 'inst_k2' in data:
            r = data['inst_k2']['ln_det'] - data['free']['ln_det']
            print(f"    ln(det'_k2/det'_free)      = {r:.6f}")
            print(f"    (WH M Zielwert:             {target:.6f})")
        if 'hoso' in data and 'inst_k2' in data:
            r = data['inst_k2']['ln_det'] - data['hoso']['ln_det']
            print(f"    ln(det'_k2/det'_hoso)      = {r:.6f}")
            print(f"    (Instanton-Beitrag zur Lücke, Soll ≈ 6.66)")
        
        results[Ls] = data
    
    return results


# =====================================================================
#  PART C: MONTE CARLO + FERMIONIC DETERMINANT
# =====================================================================

def part_C(gpu, Ls=4, betas=[5.0, 8.0, 12.0], n_therm=60, n_meas=10):
    """MC SU(3) on T⁵ + measure fermionic determinant."""
    print("\n" + "=" * 72)
    print(f"  PART C: MONTE CARLO SU(3) AUF T⁵ (Ls={Ls})")
    print("=" * 72)
    
    results = {}
    for beta in betas:
        print(f"\n  ── β = {beta:.1f} ──")
        
        links = make_links_random_thermalized(Ls, beta, n_therm=n_therm)
        
        # Measure Polyakov loop in direction 5
        strides = np.array([Ls**4, Ls**3, Ls**2, Ls, 1])
        poly_sum = 0j
        n_loops = 0
        for x0,x1,x2,x3 in iterprod(range(Ls), repeat=4):
            P = np.eye(3, dtype=complex)
            for x4 in range(Ls):
                P = P @ links[4][x0,x1,x2,x3,x4]
            poly_sum += np.trace(P) / 3
            n_loops += 1
        poly_avg = poly_sum / n_loops
        
        print(f"    ⟨P₅⟩ = {poly_avg:.4f}, |⟨P₅⟩| = {abs(poly_avg):.4f}")
        print(f"    arg(⟨P₅⟩)/π = {np.angle(poly_avg)/PI:.4f}")
        
        # Fermionic det for this config
        dim = Ls**5 * 12
        mem = dim**2 * 16 / 1e9
        max_mem = max([g['mem_gb'] for g in gpu.gpu_info], default=4)
        
        if mem < max_mem * 0.8:
            DdD, d = build_dirac_op(Ls, links, 'naive')
            if DdD is not None:
                eigs = gpu.eigvalsh(DdD)
                tol = max(1e-10*np.max(eigs), 1e-14)
                nz = int(np.sum(eigs < tol))
                ld = float(np.sum(np.log(eigs[eigs >= tol])))
                print(f"    ln(det') = {ld:.4f}, n_zero = {nz}")
                results[beta] = {'poly': complex(poly_avg), 'ln_det': ld, 'n_zero': nz}
                del DdD
        else:
            print(f"    ⚠ Matrix zu groß ({mem:.1f} GB)")
            results[beta] = {'poly': complex(poly_avg)}
    
    return results


# =====================================================================
#  PART D: FADDEEV-POPOV / MODULI SPACE
# =====================================================================

def part_D(perturbative_val=23.397):
    """Analytical decomposition of the 6.66 gap."""
    print("\n" + "=" * 72)
    print("  PART D: FADDEEV-POPOV / MODULI-RAUM-ANALYSE")
    print("=" * 72)
    
    target = 4 * np.log(6 * PI**5)
    gap = target - perturbative_val
    
    print(f"\n  Perturbativ:   {perturbative_val:.6f}")
    print(f"  Zielwert:      {target:.6f}")
    print(f"  Lücke:         {gap:.6f}")
    print(f"  exp(Lücke):    {np.exp(gap):.4f}")
    
    # === Key decomposition ===
    print(f"\n  ── STRUKTURELLE ZERLEGUNG ──")
    print(f"  4·ln(6π⁵) = 4·ln(6) + 4·5·ln(π)")
    
    # What does the perturbative part contain?
    # Perturbative = N_f·d_S × Σ_{n_perp} F(|n_perp|²)
    # The dominant contribution is the n_perp=0 sector:
    F0 = 2 * np.log(4)  # = ln(16) = 2·ln(4)
    F_rest = 2.924651 - F0  # higher modes
    print(f"\n  Perturbativ (Skalar-Sektor = {2.924651:.6f}):")
    print(f"    n_perp=0:  F(0) = 2·ln(4) = {F0:.6f}")
    print(f"    n_perp≠0:  ΔF   = {F_rest:.6f}")
    print(f"    Gesamt × 8 = {2.924651*8:.6f}")
    
    # === Integer decomposition of gap ===
    print(f"\n  ── GANZZAHLIGE ZERLEGUNG DER LÜCKE ──")
    print(f"  Lücke = {gap:.6f}")
    
    best = []
    for a in range(-5, 15):
        for b in range(-5, 10):
            for c in range(-3, 5):
                val = a*np.log(PI) + b*np.log(2) + c*np.log(3)
                err = abs(val - gap)
                if err < 0.02:
                    best.append((err, a, b, c, val))
    
    best.sort()
    print(f"  Top-Kandidaten (a·ln(π) + b·ln(2) + c·ln(3)):")
    for err, a, b, c, val in best[:8]:
        expr = f"ln(π^{a}·2^{b}·3^{c})" if c != 0 else f"ln(π^{a}·2^{b})"
        num_val = PI**a * 2**b * 3**c
        print(f"    {a:+d}·lnπ {b:+d}·ln2 {c:+d}·ln3 = {val:.6f} "
              f"(Δ={err:.5f}) = {expr} = ln({num_val:.2f})")
    
    # === Physical interpretation ===
    print(f"\n  ── PHYSIKALISCHE INTERPRETATION ──")
    print(f"""
  Die Lücke von {gap:.4f} ≈ ln(8π⁴) = {np.log(8*PI**4):.4f} (Δ={abs(gap-np.log(8*PI**4)):.4f})
  
  Mögliche Quellen:
  
  1. INSTANTON-MODULI-MAß:
     24 Nullmoden bei k=2, SU(3) auf T⁵
     Jede Gaußsche Integration gibt √π
     24 × ½·ln(π) = {24*0.5*np.log(PI):.4f} → zu groß (×2)
     
     Benötigter Faktor pro Mode: {np.exp(gap/24):.6f}
     √π = {np.sqrt(PI):.6f} (zu groß)
     π^(1/4) = {PI**0.25:.6f} (näher!)
     
  2. GHOST-DETERMINANTE:
     Det(FP-Operator) auf dem Instanton-Hintergrund
     Beitrag: ln det'(−D²_ghost) im Instanton-Feld
     
  3. BOSONIC FLUCTUATION DETERMINANT:
     1-Loop-Fluktuation um die Instanton-Sattelpunktlösung:
     [det'(−D²_gauge)]^{{-1/2}} / [det'(−D²_ghost)]
     
  4. 8π⁴-INTERPRETATION:
     8π⁴ = 2³ × π⁴
     = 2 × (2π)² × π²
     = 2 × Vol(S¹)² × π²
     Könnte die Normierung des 2-Instanton-Maßes sein:
     ∫ d⁴x₁ d⁴x₂ / Vol(S¹)² × ...
""")
    
    # === Alternative: total decomposition ===
    print(f"  ── ALTERNATIVE ZERLEGUNG ──")
    print(f"  Was wenn die Aufteilung perturbativ/nicht-perturbativ")
    print(f"  ANDERS sein sollte?\n")
    
    # Maybe the correct split is:
    # 4·ln(6π⁵) = 4·ln(6) + 20·ln(π)
    # Perturbative should give 20·ln(π) (from the spectrum)
    # Non-perturbative gives 4·ln(6) = 4·ln(|W(SU(3))|)
    
    twenty_ln_pi = 20 * np.log(PI)
    four_ln_6 = 4 * np.log(6)
    print(f"  20·ln(π) = {twenty_ln_pi:.6f}")
    print(f"  4·ln(6)  = {four_ln_6:.6f}")
    print(f"  Summe    = {twenty_ln_pi + four_ln_6:.6f}")
    print(f"  Perturbativ: {perturbative_val:.6f}")
    print(f"  Diff (20·ln(π) - pert): {twenty_ln_pi - perturbative_val:.6f}")
    
    # Hmm, if perturbative = 20·ln(π) - correction, what's the correction?
    corr = twenty_ln_pi - perturbative_val
    print(f"\n  Korrektur: 20·ln(π) - 23.397 = {corr:.6f} ≈ -{abs(corr):.4f}")
    print(f"  Also: Perturbativ = 20·ln(π) - {abs(corr):.4f}")
    print(f"  Und: Lücke = 4·ln(6) + {abs(corr):.4f} = {four_ln_6 + abs(corr):.4f}")
    
    # Is the correction a known number?
    print(f"\n  Ist {abs(corr):.6f} eine bekannte Zahl?")
    for label, val in [
        ("½·ln(π)", 0.5*np.log(PI)),
        ("ln(2)", np.log(2)),
        ("ln(3)/2", np.log(3)/2),
        ("2·ln(2)-ln(π)", 2*np.log(2)-np.log(PI)),
        ("ln(π)-ln(2)", np.log(PI)-np.log(2)),
    ]:
        print(f"    {label} = {val:.6f} (Δ={abs(val-abs(corr)):.6f})")
    
    return {'gap': gap, 'target': target, 'perturbative': perturbative_val}


# =====================================================================
#  PART E: MULTI-GPU EIGENVALUE FOR Ls=5,6
# =====================================================================

def part_E(gpu, Ls=5, fermion='naive'):
    """
    Large-scale eigenvalue computation for Ls=5,6.
    Requires A100 80GB or larger.
    Ls=5: dim=37500, matrix=22.5 GB → fits in A100 80GB
    Ls=6: dim=93312, matrix=139 GB → needs 2×A100 80GB or CPU offload
    """
    print("\n" + "=" * 72)
    print(f"  PART E: GROẞSKALA-EIGENWERTE (Ls={Ls})")
    print("=" * 72)
    
    dim = Ls**5 * 12
    mem = dim**2 * 16 / 1e9
    print(f"  dim = {dim}, Matrix = {mem:.1f} GB")
    
    max_gpu = max([g['mem_gb'] for g in gpu.gpu_info], default=0)
    
    if mem > max_gpu * 0.8:
        print(f"  ⚠ Brauche {mem:.0f} GB, größte GPU hat {max_gpu:.0f} GB")
        if mem < 200:  # CPU fallback for moderate sizes
            print(f"  → Verwende CPU (langsam aber möglich)")
        else:
            print(f"  → Nicht möglich. Brauche iterativen Solver (Lanczos).")
            print(f"     TODO: Implementiere Lanczos für die k kleinsten Eigenwerte")
            return None
    
    configs = [
        ('free', 'Frei', lambda: make_links_free(Ls)),
        ('hoso', 'Hosotani a=1/2', lambda: make_links_hosotani(Ls, 0.5)),
    ]
    
    target = 4 * np.log(6 * PI**5)
    data = {}
    
    for key, label, make_fn in configs:
        print(f"\n  [{key}] {label}")
        links = make_fn()
        DdD, d = build_dirac_op(Ls, links, fermion)
        if DdD is None:
            continue
        
        t0 = time.time()
        eigs = gpu.eigvalsh(DdD)
        dt = time.time() - t0
        
        tol = max(1e-10*np.max(eigs), 1e-14)
        nz = int(np.sum(eigs < tol))
        ld = float(np.sum(np.log(eigs[eigs >= tol])))
        
        print(f"    {len(eigs)} Eigenwerte in {dt:.1f}s")
        print(f"    n_zero = {nz}, ln(det') = {ld:.4f}")
        
        data[key] = {'ln_det': ld, 'n_zero': nz, 'time': dt}
        del DdD
    
    if 'free' in data and 'hoso' in data:
        ratio = data['hoso']['ln_det'] - data['free']['ln_det']
        print(f"\n  ln(det'_hoso/det'_free) = {ratio:.6f}")
        print(f"  Perturbatives Ziel:       23.397")
        print(f"  WH M Ziel:                {target:.6f}")
    
    return data


# =====================================================================
#  MAIN
# =====================================================================

def main():
    parser = argparse.ArgumentParser(description='SFST Gap Investigation v2')
    parser.add_argument('--part', type=str, default='all')
    parser.add_argument('--Ls', type=str, default='4')
    parser.add_argument('--fermion', type=str, default='naive', 
                        choices=['naive', 'wilson', 'both'])
    parser.add_argument('--r-wilson', type=float, default=1.0)
    parser.add_argument('--beta', type=str, default='5.0,8.0')
    parser.add_argument('--mc-therm', type=int, default=60)
    parser.add_argument('--mc-meas', type=int, default=10)
    args = parser.parse_args()
    
    Ls_list = [int(x) for x in args.Ls.split(',')]
    betas = [float(x) for x in args.beta.split(',')]
    parts = args.part.upper().split(',') if args.part != 'all' else ['A','B','C','D']
    
    print("=" * 72)
    print("  SFST: THE 6.66 GAP INVESTIGATION v2")
    print("=" * 72)
    
    gpu = GPUManager()
    gpu.print_info()
    
    results = {}
    
    if 'A' in parts:
        results['A'] = part_A()
    
    if 'B' in parts:
        if args.fermion == 'both':
            for ft in ['naive', 'wilson']:
                print(f"\n  ════ FERMION-TYP: {ft.upper()} ════")
                results[f'B_{ft}'] = part_B(gpu, Ls_list, ft, args.r_wilson)
        else:
            results['B'] = part_B(gpu, Ls_list, args.fermion, args.r_wilson)
    
    if 'C' in parts:
        results['C'] = part_C(gpu, Ls_list[0], betas, args.mc_therm, args.mc_meas)
    
    if 'D' in parts:
        pert = results.get('A', {}).get('full', 23.397)
        results['D'] = part_D(pert)
    
    if 'E' in parts:
        for Ls in Ls_list:
            results[f'E_Ls{Ls}'] = part_E(gpu, Ls, args.fermion)
    
    # Save
    outdir = '/mnt/user-data/outputs'
    os.makedirs(outdir, exist_ok=True)
    
    def serialize(obj):
        if isinstance(obj, dict):
            return {str(k): serialize(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [serialize(v) for v in obj]
        elif isinstance(obj, complex):
            return {'re': obj.real, 'im': obj.imag}
        elif isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj
    
    with open(f'{outdir}/sfst_gap_v2_results.json', 'w') as f:
        json.dump(serialize(results), f, indent=2, default=str)
    
    print(f"\n  Ergebnisse: {outdir}/sfst_gap_v2_results.json")
    
    # === USAGE EXAMPLES FOR GPU CLUSTER ===
    print(f"\n" + "=" * 72)
    print("  NUTZUNG AUF GPU-CLUSTER")
    print("=" * 72)
    print(f"""
  # Part A + D (analytisch, kein GPU nötig):
  python sfst_gap_v2.py --part A,D

  # Part B mit naiven Fermionen, Ls=4 (braucht ~2.4 GB VRAM):
  python sfst_gap_v2.py --part B --Ls 4 --fermion naive

  # Part B mit Wilson-Fermionen, verschiedene r:
  python sfst_gap_v2.py --part B --Ls 4 --fermion wilson --r-wilson 1.0
  python sfst_gap_v2.py --part B --Ls 4 --fermion wilson --r-wilson 0.5
  python sfst_gap_v2.py --part B --Ls 4 --fermion wilson --r-wilson 0.1

  # Part B: beide Fermiontypen vergleichen:
  python sfst_gap_v2.py --part B --Ls 3,4 --fermion both

  # Part C: Monte Carlo (Ls=4, braucht ~5 min):
  python sfst_gap_v2.py --part C --Ls 4 --beta 5.0,8.0,12.0

  # Part E: Großskalig auf A100 (Ls=5, braucht 22 GB):
  python sfst_gap_v2.py --part E --Ls 5

  # Alles auf A100 80GB:
  python sfst_gap_v2.py --part A,B,C,D,E --Ls 4,5 --fermion both
""")


if __name__ == '__main__':
    main()
