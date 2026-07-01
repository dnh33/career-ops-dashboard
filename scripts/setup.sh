#!/usr/bin/env bash
set -euo pipefail

echo "==> Setting up Career Ops Dashboard..."

# Frontend deps
echo "==> Installing frontend dependencies..."
cd "$(dirname "$0")/../frontend"
npm install

# Backend deps
echo "==> Installing backend dependencies..."
cd "$(dirname "$0")/../backend"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "==> Setup complete. Run ./scripts/start.sh to launch."
