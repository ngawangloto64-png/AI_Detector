# Development Guide

Comprehensive guide for developers working on the AI Detector & Humanizer application.

## Table of Contents
1. [Setup for Development](#setup-for-development)
2. [Backend Development](#backend-development)
3. [Frontend Development](#frontend-development)
4. [Adding Features](#adding-features)
5. [Testing](#testing)
6. [Debugging](#debugging)
7. [Best Practices](#best-practices)

## Setup for Development

### 1. Prerequisites
```bash
# Check Python version (3.9+)
python3 --version

# Check Git (optional but recommended)
git --version
```

### 2. Clone/Navigate to Project
```bash
cd "AI Detector"
```

### 3. Create Development Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Verify activation (should show (venv) in prompt)
```

### 4. Install Dependencies
```bash
cd backend
pip install -r requirements.txt

# Optional: Install development tools
pip install ipython django-extensions black flake8 pytest pytest-django
```

### 5. Initialize Database
```bash
python manage.py migrate
python manage.py createsuperuser

# Create some test data
python manage.py shell
```

### 6. Start Development Servers

**Terminal 1 - Backend:**
```bash
cd backend
python manage.py runserver 0.0.0.0:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
python -m http.server 8080
```

## Backend Development

### Project Structure
```
backend/
├── aidetector/      # Project settings
├── detection/       # Detection app
├── humanizer/       # Humanization app
├── manage.py        # Django CLI
└── requirements.txt # Dependencies
```

### Adding a New Django App

```bash
cd backend
python manage.py startapp myapp

# Then add to settings.py INSTALLED_APPS
```

### Database Changes

```bash
# After modifying models.py
python manage.py makemigrations

# Review migrations
python manage.py showmigrations

# Apply migrations
python manage.py migrate

# Reverse migrations if needed
python manage.py migrate myapp 0001
```

### Django Shell for Testing

```bash
python manage.py shell

# Test detection
from detection.detection_engine import AIDetector
detector = AIDetector()
result = detector.detect("test text here")
print(result)

# Test database
from detection.models import Document
docs = Document.objects.all()
```

### Customizing Detection Model

Edit `backend/detection/detection_engine.py`:

```python
class AIDetector:
    def __init__(self):
        # Change model here
        self.detector = pipeline("text-classification", 
                               model="your-custom-model",
                               device=-1)  # -1 = CPU, 0+ = GPU
```

Available models:
- `roberta-base-openai-detector` (default, good for GPT-2)
- `distilbert-base-cased` (faster, less accurate)
- `xlnet-base-cased` (more powerful)
- Your own fine-tuned model

### Customizing Humanization Model

Edit `backend/humanizer/humanization_engine.py`:

```python
class TextHumanizer:
    def __init__(self):
        # Change model here
        self.paraphrase_pipeline = pipeline(
            "text2text-generation",
            model="google/flan-t5-large",  # Change to -large, -xl, etc.
            device=-1
        )
```

### API Response Customization

Edit `backend/detection/serializers.py`:

```python
class DetectionResultSerializer(serializers.ModelSerializer):
    # Add custom fields
    custom_field = serializers.SerializerMethodField()
    
    def get_custom_field(self, obj):
        return "custom value"
    
    class Meta:
        model = DetectionResult
        fields = [
            'id', 'document', 'ai_score', 'is_ai_generated',
            'confidence', 'custom_field'
        ]
```

## Frontend Development

### File Structure
```
frontend/
├── index.html       # Main HTML
├── css/
│   └── style.css    # All styling
└── js/
    └── script.js    # All logic
```

### Modifying UI

Edit `frontend/index.html`:
- Add new sections within appropriate tabs
- Update form inputs
- Add new results display areas

### Styling

Edit `frontend/css/style.css`:
- Uses CSS custom properties (`:root`)
- Responsive design with media queries
- Dark/light mode ready

```css
:root {
    --primary-color: #6366f1;
    --secondary-color: #8b5cf6;
    /* Add more variables */
}
```

### Frontend Logic

Edit `frontend/js/script.js`:
- API calls with fetch
- Event listeners
- State management
- Local storage

### Changing API Base URL

In `frontend/js/script.js`, line 1:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
// Change to your backend URL
```

### Adding New Tabs

```html
<!-- In index.html -->
<button class="tab-btn" data-tab="newtab">New Tab</button>
<div id="newtab" class="tab-content">
    <!-- Content here -->
</div>
```

```javascript
// In script.js - already handled by existing tab navigation
```

## Adding Features

### Feature: User Authentication

1. **Backend** - Create user model:
```python
# detection/models.py
from django.contrib.auth.models import User

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # ... rest of model
```

2. **Backend** - Create serializer:
```python
# detection/serializers.py
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
```

3. **Backend** - Add authentication view:
```python
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

# Add to detection/views.py
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    return Response({'error': 'Invalid credentials'})
```

### Feature: Batch Processing

1. **Backend** - Add task queue (Celery):
```python
# settings.py
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'

# tasks.py
from celery import shared_task
@shared_task
def detect_batch(document_ids):
    for doc_id in document_ids:
        # Process each document
        pass
```

2. **Frontend** - Add batch upload:
```html
<input type="file" multiple id="batchUpload">
```

### Feature: Advanced Analytics

1. **Backend** - Add analytics model:
```python
class Analytics(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    detection_time = models.FloatField()
    humanization_time = models.FloatField()
    # ... other metrics
```

2. **Backend** - Add analytics view:
```python
@action(detail=False)
def analytics(self, request):
    stats = Analytics.objects.aggregate(
        avg_detection_time=Avg('detection_time'),
        total_documents=Count('document')
    )
    return Response(stats)
```

## Testing

### Backend Testing

```bash
# Create tests file
touch backend/detection/tests.py
```

```python
# backend/detection/tests.py
from django.test import TestCase
from detection.models import Document
from detection.detection_engine import AIDetector

class DetectionTestCase(TestCase):
    def setUp(self):
        self.detector = AIDetector()
    
    def test_detection(self):
        result = self.detector.detect("test text")
        self.assertIn('ai_score', result)
    
    def test_document_creation(self):
        doc = Document.objects.create(
            title="Test",
            content="Test content",
            file_type="txt"
        )
        self.assertEqual(doc.title, "Test")
```

```bash
# Run tests
python manage.py test detection

# With coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Frontend Testing

```javascript
// In browser console, test API calls
fetch('http://localhost:8000/api/detect/results/detect_from_text/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({text: 'test'})
})
.then(r => r.json())
.then(data => console.log(data))
```

## Debugging

### Backend Debugging

```python
# Add print statements
def detect_content(self, text):
    print(f"Detecting: {text[:50]}...")
    result = self.detector(text)
    print(f"Result: {result}")
    return result

# Or use logging
import logging
logger = logging.getLogger(__name__)
logger.debug(f"Processing: {text}")
```

### Using Django Debug Toolbar

```bash
pip install django-debug-toolbar
```

```python
# settings.py
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
```

### Frontend Debugging

```javascript
// Browser DevTools (F12)
// Console
console.log('Debug info:', variable)

// Network tab - see API calls
// Inspect element - check DOM

// Add breakpoints in Sources tab
debugger;
```

### Logging Configuration

```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'DEBUG',
    },
}
```

## Best Practices

### Code Style

```bash
# Format code with black
pip install black
black backend/

# Check code quality
flake8 backend/
```

### Django Best Practices

1. **Keep models focused**: One responsibility per model
2. **Use QuerySets efficiently**: 
   ```python
   # Good
   documents = Document.objects.select_related('detection_result')
   
   # Bad - N+1 query problem
   for doc in Document.objects.all():
       detection = doc.detection_result  # Query for each doc
   ```

3. **Use serializers for validation**:
   ```python
   serializer = DocumentSerializer(data=request.data)
   if serializer.is_valid():
       serializer.save()
   ```

4. **Use permissions**:
   ```python
   from rest_framework.permissions import IsAuthenticated
   
   class DocumentViewSet(viewsets.ModelViewSet):
       permission_classes = [IsAuthenticated]
   ```

### Frontend Best Practices

1. **Use const for immutable values**:
   ```javascript
   const API_BASE_URL = 'http://localhost:8000/api';
   ```

2. **Handle errors**:
   ```javascript
   try {
       const response = await fetch(url);
       if (!response.ok) throw new Error('Failed');
       return await response.json();
   } catch (error) {
       console.error('Error:', error);
       showNotification('Error occurred', 'error');
   }
   ```

3. **Optimize network calls**:
   ```javascript
   // Good - debounce input
   let timeout;
   input.addEventListener('input', (e) => {
       clearTimeout(timeout);
       timeout = setTimeout(() => search(e.target.value), 300);
   });
   ```

4. **Manage state consistently**:
   ```javascript
   // Keep state in one place
   const state = {
       currentDocument: null,
       detectionResult: null,
       history: []
   };
   ```

## Performance Optimization

### Backend

```python
# Use select_related for ForeignKey
queryset = Document.objects.select_related('detection_result')

# Use prefetch_related for reverse relations
queryset = Document.objects.prefetch_related('humanization')

# Use defer to exclude fields
queryset = Document.objects.defer('large_text_field')

# Database indexing
class Document(models.Model):
    title = models.CharField(max_length=255, db_index=True)
```

### Frontend

```javascript
// Use debouncing for frequent events
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// Use lazy loading for images
<img loading="lazy" src="image.jpg">

// Minimize reflows
// Bad
for (let i = 0; i < items.length; i++) {
    element.style.width = element.offsetWidth + 1 + 'px';
}
// Good
let width = element.offsetWidth;
for (let i = 0; i < items.length; i++) {
    width += 1;
}
element.style.width = width + 'px';
```

## Deployment

### Docker Deployment

```bash
# Build image
docker build -t ai-detector .

# Run container
docker run -p 8000:8000 ai-detector

# Or use docker-compose
docker-compose up
```

### Production Checklist

- [ ] Set DEBUG = False
- [ ] Update SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up Gunicorn/Nginx
- [ ] Configure HTTPS/SSL
- [ ] Set up logging
- [ ] Configure email backend
- [ ] Run security checks
- [ ] Set up monitoring
- [ ] Create backup strategy

---

Happy coding! 🚀
