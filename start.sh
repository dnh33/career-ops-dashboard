#!/bin/bash
# Career Ops Dashboard — start script
# Usage: ./start.sh

set -e

BACKEND_LOG="/opt/career-ops-dashboard/backend.log"
FRONTEND_LOG="/opt/career-ops-dashboard/serve.log"
export CAREER_OPS_API_KEY="Ojy29OB8AJwvBAXZuF-244Su_L9RswRzpKSM5u8I2xE"

# Kill any existing instances
pkill -f "uvicorn app.main:app" 2>/dev/null || true
pkill -f "python3 serve.py" 2>/dev/null || true
sleep 1

# Start backend
cd /opt/career-ops-dashboard/backend
source venv/bin/activate
nohup uvicorn app.main:app --host 127.0.0.1 --port 18000 > "$BACKEND_LOG" 2>&1 &
echo "Backend PID: $!"

# Start frontend proxy (serves static + proxies /api to backend)
cd /opt/career-ops-dashboard
nohup python3 serve.py 18080 > "$FRONTEND_LOG" 2>&1 &
echo "Frontend PID: $!"

sleep 2

# Verify
echo ""
echo "── Verification ──"
curl -s http://127.0.08000/api/stats && echo " ← backend"
curl -s -o /dev/null -w ": %{http_code}\n" http://127.0.0.1:18080/
echo ""
echo "Dashboard: https://rune-runtime.tail022030.ts.net/"
