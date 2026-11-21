#!/bin/bash
# One-command launcher: installs dependencies on first run, then starts API (8000) and UI (5173).
set -e
cd "$(dirname "$0")"

# Free the ports if a previous run is still going
lsof -t -i :8000 | xargs kill -9 2>/dev/null || true
lsof -t -i :5173 | xargs kill -9 2>/dev/null || true

echo "Preparing backend..."
cd backend
[ -d venv ] || python3 -m venv venv
venv/bin/pip install -q -r requirements.txt
venv/bin/uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

echo "Preparing frontend..."
cd ../frontend
[ -d node_modules ] || npm install
npm run dev -- --host &
FRONTEND_PID=$!

echo "------------------------------------------------"
echo "CRM Tool is running!"
echo "Backend API docs: http://localhost:8000/docs"
echo "Frontend app:     http://localhost:5173"
echo "Press CTRL+C to stop."
echo "------------------------------------------------"

trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait
