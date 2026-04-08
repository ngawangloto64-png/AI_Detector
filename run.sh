#!/bin/bash
# AI Detector & Humanizer - Quick Start Script

set -e

echo "========================================="
echo "  AI Detector & Humanizer - Setup"
echo "========================================="

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

cd "$(dirname "$0")/backend"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "[1/4] Creating virtual environment..."
    python3 -m venv venv
else
    echo "[1/4] Virtual environment already exists."
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "[2/4] Installing dependencies..."
pip install -r requirements.txt --quiet

# Run migrations
echo "[3/4] Running database migrations..."
python manage.py makemigrations --noinput
python manage.py migrate --noinput

# Start server
echo "[4/4] Starting Django server..."
echo ""
echo "========================================="
echo "  Backend running at: http://127.0.0.1:8000"
echo "  Frontend: Open frontend/index.html in your browser"
echo "========================================="
echo ""

python manage.py runserver
