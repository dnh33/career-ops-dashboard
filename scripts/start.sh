#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$SCRIPT_DIR.."

LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"

echo "==> Starting backend (port 8000)..."
cd "$ROOT/backend"
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > "$LOG_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

echo "==> Starting frontend (port 4321)..."
cd "$ROOT/frontend"
npm run dev > "$LOG_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

echo ""
echo "==> Servers started."
echo "  Frontend:  http://localhost:4321"
echo "  Backend:   http://localhost:8000"
echo "  Logs:      $LOG_DIR/"
echo ""
echo "  Stop with: kill $BACKEND_PID $FRONTEND_PID"

# Save PIDs for later
echo "$BACKEND_PID" > "$ROOT/.backend.pid"
echo "$FRONTEND_PID" > "$ROOT/.frontend.pid"
