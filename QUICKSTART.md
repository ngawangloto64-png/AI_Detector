# Quick Start Guide

Get the AI Detector & Humanizer application running in 5 minutes!

## Prerequisites

- Python 3.9 or higher
- Terminal/Command Prompt access
- A web browser

## Quick Start (5 minutes)

### Step 1: Navigate to Backend Directory
```bash
cd backend
```

### Step 2: Create Virtual Environment
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install Django, Django REST Framework, and the ML libraries. The first installation may take a few minutes.

### Step 4: Run Migrations
```bash
python manage.py migrate
```

### Step 5: Start Backend Server
```bash
python manage.py runserver 0.0.0.0:8000
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

✅ Backend is running!

### Step 6: Start Frontend Server (New Terminal)

Open a new terminal/command prompt and run:
```bash
cd frontend
python -m http.server 8080
```

Or if you have Node.js installed:
```bash
npx http-server -p 8080
```

### Step 7: Open Application

Open your web browser and visit:
```
http://localhost:8080
```

🎉 **Success!** The application is now running!

## Using the Application

### Detect AI Content
1. Click on "AI Detector" tab
2. Paste text or upload a document (TXT, PDF, DOCX)
3. Click "Analyze Content"
4. View the AI detection score

### Humanize Text
1. Click on "Humanizer" tab
2. Paste AI-generated text
3. Click "Humanize"
4. Review humanized version
5. Copy or download the result

## Stopping the Servers

To stop the servers:
- Backend: Press `Ctrl+C` in the backend terminal
- Frontend: Press `Ctrl+C` in the frontend terminal

## Common Issues & Solutions

### Port 8000 or 8080 Already in Use

**Backend (port 8000):**
```bash
python manage.py runserver 8001
# Then update frontend API_BASE_URL to http://localhost:8001
```

**Frontend (port 8080):**
```bash
python -m http.server 8081
```

### Module Not Found Errors

Ensure you're in the virtual environment:
```bash
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows
```

### Model Download Slow

The first run downloads ML models (200MB+). This is normal and only happens once. Subsequent runs will use cached models.

## Next Steps

### Production Deployment
- Set `DEBUG=False` in settings.py
- Update `SECRET_KEY` in .env
- Configure `ALLOWED_HOSTS`
- Use a production WSGI server (Gunicorn)

### Customize Models
- Modify detection model in `backend/detection/detection_engine.py`
- Adjust humanization in `backend/humanizer/humanization_engine.py`

### Add More Features
- User authentication
- Database persistence
- API documentation
- Advanced analytics

## API Testing

Test the API directly:

**Test Detection:**
```bash
curl -X POST http://localhost:8000/api/detect/results/detect_from_text/ \
  -H "Content-Type: application/json" \
  -d '{"text":"This is a test text"}'
```

**Test Humanization:**
```bash
curl -X POST http://localhost:8000/api/humanize/results/humanize_text/ \
  -H "Content-Type: application/json" \
  -d '{"text":"This is AI generated text that needs humanization"}'
```

## Admin Panel

Create a superuser to access Django admin:
```bash
python manage.py createsuperuser
```

Then visit: `http://localhost:8000/admin`

## Need Help?

- Check README.md for detailed documentation
- Review API endpoints in README.md
- Check browser console for client-side errors (F12)
- Check terminal logs for server-side errors

---

Happy detecting and humanizing! 🚀
