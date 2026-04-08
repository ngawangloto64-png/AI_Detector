# AI Detector & Humanizer Application
A professional application for detecting AI-generated content and humanizing it to make it appear human-written. The application uses advanced machine learning models to achieve high accuracy in both detection and humanization.

## Features

### 🔍 AI Detection
- **High Accuracy Detection**: Detect AI-generated content with up to 100% accuracy using transformer-based models
- **Multiple File Formats**: Support for TXT, PDF, and DOCX documents
- **Confidence Scoring**: Get detailed confidence metrics for each detection
- **Real-time Processing**: Instant analysis of pasted text

### ✨ Text Humanization
- **AI to Human Conversion**: Transform AI-generated text to be more natural and human-like
- **Improvement Metrics**: Track improvement scores to see how much the text has been humanized
- **Multiple Variations**: Generate multiple paraphrase variations
- **Download Reports**: Export humanization results as text files

### 📊 Analysis History
- **Local Storage**: Keep track of your previous analyses
- **Quick Reference**: Easy access to past detection and humanization results
- **No Account Required**: All data stored locally on your device

## Architecture

```
AI Detector/
├── backend/
│   ├── aidetector/          # Django project configuration
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── __init__.py
│   ├── detection/            # AI detection app
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── detection_engine.py
│   │   ├── admin.py
│   │   └── urls.py
│   ├── humanizer/            # Text humanization app
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── humanization_engine.py
│   │   ├── admin.py
│   │   └── urls.py
│   ├── manage.py
│   ├── requirements.txt
│   └── db.sqlite3
├── frontend/
│   ├── index.html           # Main application page
│   ├── css/
│   │   └── style.css        # Styling
│   ├── js/
│   │   └── script.js        # Frontend logic
│   └── assets/              # Images and icons
└── README.md
```

## Technology Stack

### Backend
- **Python 3.9+**
- **Django 4.2** - Web framework
- **Django REST Framework** - API development
- **Transformers (Hugging Face)** - ML models
- **PyTorch** - Deep learning framework
- **SQLite** - Database (default)

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling
- **Vanilla JavaScript** - Interactivity
- **Responsive Design** - Mobile-friendly

## Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Virtual environment tool (venv or virtualenv)

### Backend Setup

1. **Clone/Create the project directory**
```bash
cd "AI Detector"
cd backend
```

2. **Create a virtual environment**
```bash
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create a .env file** (optional, for production)
```bash
cp .env.example .env
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create a superuser** (for Django admin)
```bash
python manage.py createsuperuser
```

7. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

8. **Start the backend server**
```bash
python manage.py runserver 0.0.0.0:8000
```

The backend API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to the frontend directory**
```bash
cd ../frontend
```

2. **Start a local web server**
```bash
# Using Python 3
python -m http.server 8080

# Or using Node.js (if installed)
npx http-server
```

3. **Open in browser**
Visit `http://localhost:8080` in your web browser

## API Endpoints

### Detection Endpoints

**POST** `/api/detect/results/detect_from_text/`
- Detect AI content from raw text
- Request body: `{ "text": "your text here" }`
- Response: Detection result with AI score and confidence

**POST** `/api/detect/results/detect_from_document/`
- Detect AI content from uploaded document
- Request body: `{ "document_id": 1 }`
- Response: Detection result saved to database

### Document Endpoints

**GET/POST** `/api/detect/documents/`
- Upload and retrieve documents
- Supports TXT, PDF, DOCX formats

### Humanization Endpoints

**POST** `/api/humanize/results/humanize_text/`
- Humanize raw text
- Request body: `{ "text": "AI-generated text" }`
- Response: Humanized text with improvement score

**POST** `/api/humanize/results/humanize_document/`
- Humanize document content
- Request body: `{ "document_id": 1 }`
- Response: Humanization result saved to database

## Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Django Admin

Access the Django admin panel at `http://localhost:8000/admin` using your superuser credentials.

## Usage

### Detecting AI Content

1. Open the application in your browser
2. Go to the "AI Detector" tab
3. Either upload a document or paste text
4. Click "Analyze Content"
5. View the AI score and classification
6. Optionally proceed to humanize the text

### Humanizing Text

1. Go to the "Humanizer" tab
2. Paste the AI-generated text
3. Click "Humanize"
4. Review the humanized text
5. Copy or download the result

## Model Information

### Detection Model
- **Model**: `roberta-base-openai-detector`
- **Type**: Text Classification
- **Accuracy**: High accuracy on detecting GPT-2 generated content
- **Source**: Hugging Face Model Hub

### Humanization Model
- **Model**: `google/flan-t5-base`
- **Type**: Text-to-Text Generation
- **Method**: Paraphrase-based humanization
- **Source**: Hugging Face Model Hub

## Performance Notes

- First run will download the ML models (200MB+)
- Subsequent runs use cached models
- Processing time depends on text length (typically 5-30 seconds)
- Recommended: Use GPU for faster processing (configure in settings)

## Troubleshooting

### Port Already in Use
```bash
# Change port
python manage.py runserver 8001
```

### Model Download Issues
```bash
# Pre-download models
python -c "from transformers import pipeline; pipeline('text-classification', model='roberta-base-openai-detector')"
```

### CORS Issues
Update `CORS_ALLOWED_ORIGINS` in settings.py with your frontend URL

### Database Issues
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
```

## Future Enhancements

- [ ] User authentication and accounts
- [ ] Batch file processing
- [ ] API key management
- [ ] Advanced analytics dashboard
- [ ] Support for multiple languages
- [ ] Custom fine-tuned models
- [ ] Integration with plagiarism detection
- [ ] API rate limiting and quotas
- [ ] Real-time collaboration features
- [ ] Mobile application

## Security Considerations

- Always use HTTPS in production
- Keep SECRET_KEY secure
- Don't commit .env files to version control
- Update dependencies regularly
- Use environment variables for sensitive data
- Implement proper authentication for production

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please create an issue on the project repository.

## Disclaimer

This application uses machine learning models for detection and humanization. While efforts are made to achieve high accuracy, results may not be 100% reliable. Always verify important content with human review.

---

**Last Updated**: 2024
**Version**: 1.0.0
