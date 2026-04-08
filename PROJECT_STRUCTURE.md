# Project Structure

## Complete Directory Layout

```
AI Detector/
│
├── README.md                          # Main project documentation
├── QUICKSTART.md                      # Quick start guide (5 minutes)
├── PROJECT_STRUCTURE.md               # This file
├── setup.sh                           # Automated setup script
├── .gitignore                         # Git ignore rules
├── Dockerfile                         # Docker containerization
├── docker-compose.yml                 # Docker Compose configuration
│
├── backend/                           # Django Backend Application
│   │
│   ├── manage.py                      # Django management script
│   ├── requirements.txt               # Python dependencies
│   ├── .env.example                   # Environment variables template
│   │
│   ├── aidetector/                    # Django Project Configuration
│   │   ├── __init__.py
│   │   ├── settings.py               # Django settings & configuration
│   │   ├── urls.py                   # URL routing (main entry point)
│   │   └── wsgi.py                   # WSGI application
│   │
│   ├── detection/                     # AI Detection App
│   │   ├── __init__.py
│   │   ├── admin.py                  # Django admin configuration
│   │   ├── apps.py                   # App configuration
│   │   ├── models.py                 # Database models
│   │   ├── views.py                  # API views
│   │   ├── serializers.py            # DRF serializers
│   │   ├── urls.py                   # Detection URLs
│   │   └── detection_engine.py       # AI detection logic
│   │
│   ├── humanizer/                     # Text Humanization App
│   │   ├── __init__.py
│   │   ├── admin.py                  # Django admin configuration
│   │   ├── apps.py                   # App configuration
│   │   ├── models.py                 # Database models
│   │   ├── views.py                  # API views
│   │   ├── serializers.py            # DRF serializers
│   │   ├── urls.py                   # Humanizer URLs
│   │   └── humanization_engine.py    # Text humanization logic
│   │
│   ├── media/                         # Uploaded documents (generated)
│   ├── staticfiles/                   # Static files (generated)
│   └── db.sqlite3                     # SQLite database (generated)
│
└── frontend/                          # Frontend Application
    │
    ├── index.html                     # Main HTML page
    ├── css/
    │   └── style.css                 # Styling (responsive design)
    │
    ├── js/
    │   └── script.js                 # Frontend logic & API calls
    │
    └── assets/                        # Images, icons, etc.
        └── (placeholder for assets)
```

## File Descriptions

### Root Level
- **README.md**: Complete project documentation with all features, setup, and troubleshooting
- **QUICKSTART.md**: 5-minute quick start guide for immediate setup
- **setup.sh**: Bash script to automatically set up the entire project
- **Dockerfile**: Docker image for containerized deployment
- **docker-compose.yml**: Multi-container setup for easy orchestration

### Backend (`backend/`)

#### Project Configuration (`aidetector/`)
- **settings.py**: Django configuration including:
  - Database settings (SQLite)
  - Installed apps
  - Middleware configuration
  - CORS settings
  - REST Framework configuration
  - AI models settings

- **urls.py**: Main URL routing that:
  - Includes admin URLs
  - Routes to detection and humanizer APIs
  - Sets up REST framework routers

- **wsgi.py**: WSGI application for production deployment

#### Detection App (`detection/`)
- **models.py**: Two main models:
  - `Document`: Stores uploaded documents and their content
  - `DetectionResult`: Stores AI detection results

- **views.py**: API ViewSets:
  - `DocumentViewSet`: CRUD operations for documents
  - `DetectionResultViewSet`: Detection analysis endpoints

- **serializers.py**: DRF serializers for:
  - Converting models to JSON
  - Data validation

- **detection_engine.py**: Core detection logic:
  - `AIDetector` class using transformers
  - text preprocessing
  - Model inference

- **admin.py**: Django admin panel configuration for:
  - Document management
  - Results viewing

#### Humanizer App (`humanizer/`)
- **models.py**: Humanization model:
  - `Humanization`: Stores original and humanized text

- **views.py**: API ViewSets:
  - `HumanizationViewSet`: Humanization endpoints

- **serializers.py**: DRF serializers for humanization data

- **humanization_engine.py**: Humanization logic:
  - `TextHumanizer` class
  - Paraphrase generation
  - Text improvement scoring

- **admin.py**: Django admin configuration for humanization results

### Frontend (`frontend/`)

#### HTML (`index.html`)
- Responsive single-page application with:
  - Tab-based navigation (Detector, Humanizer, History)
  - File upload interface
  - Text input areas
  - Results display sections
  - Loading indicators
  - Notification system

#### Styling (`css/style.css`)
- Modern, responsive design with:
  - CSS custom properties (variables)
  - Flexbox and grid layouts
  - Smooth animations
  - Mobile-first approach
  - Dark/light mode ready

#### JavaScript (`js/script.js`)
- Frontend logic including:
  - API communication
  - Event handling
  - File drag-and-drop
  - Local storage for history
  - UI state management
  - Notification system

## API Endpoints

### Detection Endpoints
```
POST /api/detect/results/detect_from_text/
POST /api/detect/results/detect_from_document/
GET  /api/detect/documents/
POST /api/detect/documents/
```

### Humanizer Endpoints
```
POST /api/humanize/results/humanize_text/
POST /api/humanize/results/humanize_document/
GET  /api/humanize/results/
```

## Data Models

### Document Model
```
- id (PK)
- user (FK to User)
- title
- file
- content
- file_type (choices: txt, pdf, docx)
- uploaded_at
- updated_at
```

### DetectionResult Model
```
- id (PK)
- document (OneToOne FK)
- ai_score (0-100)
- is_ai_generated (Boolean)
- confidence (0-1)
- detected_at
- model_used
- details (JSON)
```

### Humanization Model
```
- id (PK)
- document (OneToOne FK)
- original_text
- humanized_text
- improvement_score (0-100)
- model_used
- humanized_at
- details (JSON)
```

## Environment Variables

Configure in `.env` file:
```
SECRET_KEY              # Django secret key
DEBUG                   # Debug mode (True/False)
ALLOWED_HOSTS          # Comma-separated allowed hosts
DATABASE_URL           # Database connection string (default: SQLite)
```

## Dependencies Overview

### Backend Dependencies
- **Django 4.2.0**: Web framework
- **djangorestframework 3.14.0**: REST API framework
- **django-cors-headers**: CORS support
- **transformers 4.35.2**: Hugging Face models
- **torch 2.1.0**: PyTorch (ML library)
- **scipy, scikit-learn**: Scientific computing
- **Pillow**: Image processing
- **others**: Utilities and helpers

### Frontend Dependencies
- No external frameworks (vanilla JavaScript)
- Uses modern browser APIs
- Local storage for persistence
- Fetch API for HTTP requests

## Static Files & Media

### Static Files (`staticfiles/`)
- Generated by `python manage.py collectstatic`
- CSS, JavaScript, and assets for admin panel

### Media Files (`media/`)
- Uploaded documents
- Generated during runtime

### Database
- **db.sqlite3**: Default SQLite database
- Auto-generated during migrations
- Contains all stored data

## Development Workflow

1. **Local Development**:
   - Virtual environment activation
   - Dependencies installation
   - Database migrations
   - Server startup

2. **Code Changes**:
   - Edit models → Run migrations
   - Edit views/serializers → No migration needed
   - Edit frontend → Refresh browser (no build needed)

3. **Testing**:
   - API testing with curl or Postman
   - Frontend testing in browser
   - Check admin panel at `/admin`

## Production Deployment

Key changes for production:
1. Set `DEBUG = False`
2. Update `SECRET_KEY`
3. Configure `ALLOWED_HOSTS`
4. Use production WSGI server (Gunicorn)
5. Configure proper database (PostgreSQL recommended)
6. Set up SSL/HTTPS
7. Implement proper authentication
8. Configure logging and monitoring

## File Statistics

- **Backend**: ~1000 lines of Python code
- **Frontend**: ~800 lines of HTML/CSS/JS
- **Total**: ~1800 lines of code
- **Configuration**: 5 main files

## Growth Potential

The architecture supports:
- User authentication and accounts
- Multiple detection/humanization models
- Batch processing
- Advanced analytics
- Database optimization
- Caching mechanisms
- API versioning
- Webhooks and async tasks

---

For more details, see README.md and QUICKSTART.md
