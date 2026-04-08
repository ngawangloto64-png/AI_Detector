# AI Detector Application - Copilot Instructions

## Project Overview
A professional AI detection and humanization application with:
- **Backend**: Django REST API with AI detection and text humanization
- **Frontend**: HTML/CSS/JavaScript for document upload and results
- **Features**: AI detection (aim for 100%), text humanization (make AI 0%)

## Architecture
```
backend/
  - aidetector/ (Django project)
  - detection/ (Django app for detection logic)
  - humanizer/ (Django app for humanization logic)
  - manage.py
  - requirements.txt

frontend/
  - index.html
  - css/ (styling)
  - js/ (frontend logic)
  - assets/ (images, icons)
```

## Development Workflow
1. Backend: Django REST API with endpoints for detection and humanization
2. Frontend: Upload documents, display detection results, humanize text
3. Integration: Frontend calls backend API endpoints

## Configuration Notes
- Python 3.9+
- Django 4.2+
- Django REST Framework
- AI detection library: use transformer-based models (Hugging Face)
- Text humanization: use paraphrasing/rewriting models
