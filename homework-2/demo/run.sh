#!/bin/bash
# Run Customer Support Ticket System API Server (Linux/Mac)

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Starting server on http://localhost:8000"
echo "API docs available at http://localhost:8000/docs"
echo ""

uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
