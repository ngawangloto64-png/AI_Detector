# Getting Started Checklist

Complete this checklist to get your AI Detector application running.

## ✅ Pre-Installation

- [ ] Python 3.9 or higher installed (`python3 --version`)
- [ ] Terminal/Command Prompt available
- [ ] Git installed (optional but recommended)
- [ ] At least 4GB of free disk space
- [ ] Internet connection (for downloading dependencies and ML models)

## ✅ Installation Steps

### 1. Navigate to Backend Directory
```bash
cd "AI Detector"
cd backend
```

### 2. Create Virtual Environment
- [ ] Linux/macOS: `python3 -m venv venv && source venv/bin/activate`
- [ ] Windows: `python -m venv venv && venv\Scripts\activate`
- [ ] Should see `(venv)` in your prompt

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
- [ ] Wait for all packages to install (2-5 minutes)
- [ ] No errors reported

### 4. Initialize Database
```bash
python manage.py migrate
```
- [ ] Success message shown

### 5. Create Admin User (Optional)
```bash
python manage.py createsuperuser
```
- [ ] Enter username, email, and password
- [ ] Remember credentials for `/admin` access

### 6. Start Backend Server
```bash
python manage.py runserver 0.0.0.0:8000
```
- [ ] Shows "Starting development server at http://127.0.0.1:8000/"

### 7. Start Frontend Server (New Terminal)
```bash
cd frontend
python -m http.server 8080
```
- [ ] Shows "Serving HTTP on 0.0.0.0 port 8080"

### 8. Open Application
- [ ] Open browser and visit: `http://localhost:8080`
- [ ] Should see AI Detector & Humanizer interface
- [ ] All tabs visible (AI Detector, Humanizer, History)

## ✅ Verification Steps

### Test Detection
- [ ] Paste sample text in AI Detector tab
- [ ] Click "Analyze Content"
- [ ] See AI score displayed
- [ ] See classification result

### Test Humanization
- [ ] Go to Humanizer tab
- [ ] Paste some text
- [ ] Click "Humanize"
- [ ] See humanized version
- [ ] Improvement score displayed

### Test History
- [ ] Switch to History tab
- [ ] Previous analyses visible
- [ ] Data persists on page reload

## ✅ Admin Access

- [ ] Visit `http://localhost:8000/admin`
- [ ] Login with superuser credentials
- [ ] See Documents and Detection Results
- [ ] Create/edit documents through admin

## ✅ API Testing

Test with curl or Postman:

### Test Detection Endpoint
```bash
curl -X POST http://localhost:8000/api/detect/results/detect_from_text/ \
  -H "Content-Type: application/json" \
  -d '{"text":"write a test text here"}'
```
- [ ] Returns JSON with ai_score, confidence, etc.

### Test Humanization Endpoint
```bash
curl -X POST http://localhost:8000/api/humanize/results/humanize_text/ \
  -H "Content-Type: application/json" \
  -d '{"text":"test text"}'
```
- [ ] Returns JSON with humanized_text and improvement_score

## ✅ Troubleshooting Common Issues

### Port Already in Use
```bash
# Change port for backend
python manage.py runserver 8001

# Change port for frontend
python -m http.server 8081

# Update frontend API URL in js/script.js line 1
```
- [ ] Both servers running on different ports

### Import Errors
```bash
# Verify virtual environment
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows

# Reinstall packages
pip install -r requirements.txt
```
- [ ] No import errors

### Slow Model Download
- [ ] First run downloads ML models (200MB+)
- [ ] This is normal and only happens once
- [ ] Be patient (5-10 minutes depending on connection)

### Database Errors
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
```
- [ ] Database recreated successfully

## ✅ Configuration

### Change API URL (Production)
Edit `frontend/js/script.js` line 1:
```javascript
const API_BASE_URL = 'http://your-backend-url:8000/api';
```

### Environment Variables
Create `backend/.env`:
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,example.com
```

## ✅ Next Steps

### For Development
- [ ] Read DEVELOPMENT.md for detailed guide
- [ ] Explore PROJECT_STRUCTURE.md
- [ ] Run `python backend/verify_setup.py` to verify setup
- [ ] Try modifying detection/humanization models

### For Production
- [ ] Read production section in README.md
- [ ] Set DEBUG=False
- [ ] Update ALLOWED_HOSTS
- [ ] Use production WSGI server (Gunicorn)
- [ ] Configure HTTPS/SSL

### For Learning
- [ ] Explore Django admin panel
- [ ] Check API responses with curl
- [ ] Customize frontend styling
- [ ] Experiment with different ML models

## ✅ Additional Resources

- **README.md** - Complete documentation
- **QUICKSTART.md** - 5-minute quick start
- **DEVELOPMENT.md** - For developers
- **PROJECT_STRUCTURE.md** - Architecture overview
- **API Endpoints** - See README.md API section

## ✅ Support & Help

If you encounter issues:

1. Check error messages carefully
2. Review relevant documentation section
3. Run `python backend/verify_setup.py`
4. Check browser console (F12 in DevTools)
5. Check server console/terminal for error logs

## 🎉 Success Indicators

You're successful when you see:
- ✓ Backend server running on port 8000
- ✓ Frontend accessible on port 8080
- ✓ Can detect AI content with a score
- ✓ Can humanize text with improvement score
- ✓ Analysis history persists
- ✓ Admin panel accessible

---

**Estimated Setup Time**: 10-15 minutes (first run includes model download)

**Happy detecting and humanizing!** 🚀
