#!/usr/bin/env bash
# Anti-slop audit — Hermes Terminal design system compliance
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== Anti-Slop Audit ==="
echo ""

FAIL=0

echo "1. Hardcoded hex colors in components (expect zero outside token defs)..."
HEX_MATCHES=$(rg -n '#[0-9a-fA-F]{3,8}\b' src/components/ --glob '!**/globals.css' | rg -v '&#[0-9a-fA-F]+;' || true)
if [ -n "$HEX_MATCHES" ]; then
  echo "FAIL: Hardcoded hex found:"
  echo "$HEX_MATCHES"
  FAIL=1
else
  echo "PASS: No hardcoded hex in src/components/"
fi
echo ""

echo "2. font-family in components (expect var(--font-*) or inherit)..."
FONT_MATCHES=$(rg -n 'font-family:' src/components/ | rg -v 'var\(--font-|inherit' || true)
if [ -n "$FONT_MATCHES" ]; then
  echo "FAIL: Non-token font-family:"
  echo "$FONT_MATCHES"
  FAIL=1
else
  echo "PASS: All font-family uses CSS tokens"
fi
echo ""

echo "3. client:load directives (expect zero)..."
CLIENT_LOAD=$(rg -n 'client:load' src/ || true)
if [ -n "$CLIENT_LOAD" ]; then
  echo "FAIL: client:load found:"
  echo "$CLIENT_LOAD"
  FAIL=1
else
  echo "PASS: No client:load directives"
fi
echo ""

echo "4. Forbidden display fonts..."
FORBIDDEN_FONTS=$(rg -in '\bInter\b|\bPlayfair\b|\bGaramond\b|\bLora\b|\bMerriweather\b' src/components/primitives/ src/pages/settings.astro src/pages/index.astro || true)
if [ -n "$FORBIDDEN_FONTS" ]; then
  echo "FAIL: Forbidden fonts:"
  echo "$FORBIDDEN_FONTS"
  FAIL=1
else
  echo "PASS: No forbidden display fonts"
fi
echo ""

echo "5. Bounce/elastic easing..."
BOUNCE=$(rg -in 'bounce|elastic|overshoot' src/ || true)
if [ -n "$BOUNCE" ]; then
  echo "FAIL: Bounce/elastic easing:"
  echo "$BOUNCE"
  FAIL=1
else
  echo "PASS: No bounce/elastic easing"
fi
echo ""

if [ "$FAIL" -eq 0 ]; then
  echo "=== All anti-slop checks passed ==="
  exit 0
else
  echo "=== Anti-slop audit FAILED ==="
  exit 1
fi
