# Spectral Geometry on T⁵ with SU(3) — Repository v47

**GitHub:** https://github.com/SFST-2026/Spectral-Geometry

**Full title:** *Spectral Geometry on T⁵ with SU(3): Algebraic Identities and Their Physical Consequences*

**Author:** Martin Wolfgang Le Borgne  
**Version:** v47 (March 2026)  
**Status:** Prepared for submission

## Contents

| Directory | Description |
|-----------|-------------|
| `paper/` | Main paper LaTeX source |
| `supplement/` | Supplementary material with Appendices Z–Z16 |
| `appendices/` | Individual appendix LaTeX files |
| `scripts/` | Python scripts for computational reproduction |
| `figures/` | Generated figures |
| `data/` | Numerical output data |

## Quick Reproduction

```bash
pip install -r requirements.txt
bash runme.sh
```

Runs the full test suite (Colab notebook + unit tests) in under 60 seconds.

## Key Scripts

| Script | What it verifies | Runtime |
|--------|-----------------|---------|
| `sfst_colab_notebook.py` | All 9 core claims | ~2 s |
| `unit_tests.py` | 16 unit tests | ~5 s |
| `triple_verification.py` | K̄ = π^(5/2) via 3 methods, 30 digits | ~30 s |
| `d5_uniqueness.py` | d=5 uniqueness theorem | ~1 s |
| `bootstrap_closure.py` | WH M as unique fixed point | ~1 s |
| `toy_model_axiom_m.py` | Matching identity in d=1–5 | ~5 s |

## Dependencies

See `requirements.txt`. Core: Python ≥ 3.8, mpmath, numpy, scipy, matplotlib.

## Citation

M. W. Le Borgne, "Spectral Geometry on T⁵ with SU(3): Algebraic Identities and Their Physical Consequences," v47 (2026).
