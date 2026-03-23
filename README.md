# Parameter-Free Derivation of m_p/m_e and α from Spectral Geometry on T⁵ with SU(3)

**Author:** Martin Wolfgang Le Borgne  
**Version:** v55 (March 2026)

## Main Result

```
m_p/m_e = 6π⁵(1 + α²/√8) = 1836.15268  (0.002 ppm)
-2 ln α = π² - 4α + c₂α²               (0.009 ppm)
```

**No free parameters.** 33 parameter-free consequences from spectral geometry on the five-torus T⁵ with SU(3) gauge field, including Maxwell and Einstein equations as Kaluza-Klein limits.

## Key Predictions (Testable)

| # | Prediction | Test | Timeline |
|---|---|---|---|
| V31 | Neutrinos are Dirac (0νββ forbidden) | LEGEND/nEXO/CUPID | 2027-28 |
| V22 | θ_QCD = 0 (no axion needed) | nEDM experiments | 2028 |
| V23 | Proton stable (τ > 10^1000 yr) | Hyper-K | 2027+ |
| V32 | Σm_ν ≈ 0.08 eV | KATRIN/Planck | ongoing |

## Repository Structure

```
paper/                    # LaTeX sources and PDFs
  sfst_paper_v55.pdf      # Main paper (34 pages)
  sfst_paper_v55.tex
  sfst_supplement_v55.pdf  # Supplement (55 pages)
  sfst_supplement_v55.tex
  reviewer_roadmap_v55.pdf # Reviewer roadmap (8 pages)
  reviewer_roadmap_v55.tex

scripts/                  # Numbered by tier
  T0_*.py                 # Tier 0: Known results (verification)
  T01_*.py                # Tier 0+1: Known methods, our application
  T1_*.py                 # Tier 1: New results (proved here)
  UTIL_*.py               # Utilities (notebook, solvers, tests)

data/                     # Numerical data files
results/                  # Computation outputs
```

## Tier System

| Tier | Count | Meaning |
|---|---|---|
| **0** | 9 | Known results (cited, not proved here) |
| **0+1** | 5 | Known methods, our specific application |
| **1** | 12 | New results (proved here) |
| **2/3** | 0 | None remaining |

## Quick Verification

```bash
pip install mpmath numpy
python scripts/UTIL_01_colab_notebook.py  # 9 tests, <60s
```

## Citation

```bibtex
@article{LeBorgne2026,
  author  = {Le Borgne, Martin Wolfgang},
  title   = {Parameter-Free Derivation of $m_p/m_e$ and $\alpha$ 
             from Spectral Geometry on $T^5$ with SU(3)},
  year    = {2026},
  note    = {v55, 33 parameter-free consequences, 
             0.002 ppm accuracy for $m_p/m_e$}
}
```

## License

MIT License. See [LICENSE](LICENSE).
