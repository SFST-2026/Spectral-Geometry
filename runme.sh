#!/bin/bash
# SFST v47 — Core Reproduction Script
# Run: bash runme.sh
# Expected: all 9 tests PASS in < 60 seconds

set -e

echo "=== SFST v47 Core Tests ==="
echo "Installing dependencies..."
pip install -q mpmath numpy scipy matplotlib 2>/dev/null || pip install -q mpmath numpy scipy matplotlib --break-system-packages 2>/dev/null

echo ""
echo "Running full test suite..."
python scripts/sfst_colab_notebook.py

echo ""
echo "Running unit tests..."
python scripts/unit_tests.py

echo ""
echo "=== All tests complete ==="
