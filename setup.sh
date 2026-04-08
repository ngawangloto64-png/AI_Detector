#!/bin/bash
# Quick Start Script for AI Detector

echo "🚀 AI Detector & Humanizer - Quick Start"
echo "========================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "backend/venv" ]; then
    echo "📦 Creating virtual environment..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    cd ..
else
    echo "✓ Virtual environment already exists"
    source backend/venv/bin/activate
fi

# Install dependencies
echo "📚 Installing dependencies..."
cd backend
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Run migrations
echo "🔄 Running migrations..."
python manage.py migrate
echo "✓ Migrations complete"

# Create superuser if needed
echo ""
echo "👤 Create superuser (optional)?"
echo "   Run: python manage.py createsuperuser"
echo ""

# Provide startup instructions
echo "🎯 Ready to start!"
echo ""
echo "Backend server:"
echo "  cd backend"
echo "  python manage.py runserver 0.0.0.0:8000"
echo ""
echo "Frontend server (open another terminal):"
echo "  cd frontend"
echo "  python -m http.server 8080"
echo ""
echo "Then visit: http://localhost:8080"
echo ""
