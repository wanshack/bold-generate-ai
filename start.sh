#!/bin/bash

echo "Starting Stock Prediction Platform..."
echo "====================================="
echo ""

cd "$(dirname "$0")"

echo "Starting Backend Server (Port 8000)..."
cd backend
python3 main.py &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

cd ..

echo ""
echo "Starting Frontend Server (Port 5173)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

echo ""
echo "====================================="
echo "Stock Prediction Platform is running!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo "API Docs: http://localhost:8000/docs"
echo "====================================="
echo ""
echo "Press Ctrl+C to stop both servers"

trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT

wait
