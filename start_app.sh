#!/bin/bash

# Kill running ports if any (cleanup)
lsof -t -i :8000 | xargs kill -9 2>/dev/null
lsof -t -i :5173 | xargs kill -9 2>/dev/null

echo "Starting Backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

echo "Starting Frontend..."
cd ../frontend
npm run dev -- --host &
FRONTEND_PID=$!

echo "------------------------------------------------"
echo "CRM Tool is running!"
echo "------------------------------------------------"
echo "Backend API: http://localhost:8000/docs"
echo "Frontend App: http://localhost:5173"
echo "------------------------------------------------"
echo "Press CTRL+C to stop all services."

trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
