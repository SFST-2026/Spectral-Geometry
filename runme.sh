#!/bin/bash
# SFST v55 — Quick Verification Suite
# Runs all core checks in under 60 seconds.
# Requires: Python 3.8+, mpmath, numpy

set -e
echo "================================================"
echo "  SFST v55 — Quick Verification"
echo "================================================"
echo ""

echo "[1/3] Core claims (9 tests)..."
python3 scripts/UTIL_01_colab_notebook.py
echo ""

echo "[2/3] Unit tests..."
python3 scripts/UTIL_05_unit_tests.py
echo ""

echo "[3/3] Alpha solver..."
python3 scripts/UTIL_04_alpha_solver.py
echo ""

echo "================================================"
echo "  All checks passed."
echo "================================================"
