import json
import chardet
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .analyzer import analyze_text
from .models import DetectionResult


@csrf_exempt
@require_http_methods(["POST"])
def detect_text(request):
    """Analyze pasted text for AI content."""
    try:
        body = json.loads(request.body)
        text = body.get('text', '').strip()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)

    if not text:
        return JsonResponse({'error': 'No text provided.'}, status=400)

    result = analyze_text(text)

    DetectionResult.objects.create(
        text_input=text[:5000],
        ai_probability=result['ai_probability'],
        verdict=result['verdict'],
    )

    return JsonResponse(result)


@csrf_exempt
@require_http_methods(["POST"])
def detect_file(request):
    """Analyze an uploaded document for AI content."""
    uploaded_file = request.FILES.get('file')
    if not uploaded_file:
        return JsonResponse({'error': 'No file uploaded.'}, status=400)

    allowed_types = ['.txt', '.md', '.doc', '.docx', '.pdf', '.rtf']
    file_ext = '.' + uploaded_file.name.rsplit('.', 1)[-1].lower() if '.' in uploaded_file.name else ''
    if file_ext not in allowed_types:
        return JsonResponse({
            'error': f'Unsupported file type. Allowed: {", ".join(allowed_types)}'
        }, status=400)

    try:
        raw_content = uploaded_file.read()

        # Try to detect encoding
        detected = chardet.detect(raw_content)
        encoding = detected.get('encoding', 'utf-8') or 'utf-8'

        try:
            text = raw_content.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            text = raw_content.decode('utf-8', errors='ignore')

        text = text.strip()
        if not text:
            return JsonResponse({'error': 'The uploaded file appears to be empty.'}, status=400)

        result = analyze_text(text)
        result['filename'] = uploaded_file.name

        DetectionResult.objects.create(
            text_input=text[:5000],
            ai_probability=result['ai_probability'],
            verdict=result['verdict'],
        )

        return JsonResponse(result)

    except Exception as e:
        return JsonResponse({'error': f'Error processing file: {str(e)}'}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def detection_history(request):
    """Get recent detection results."""
    results = DetectionResult.objects.all()[:20]
    data = [
        {
            'id': r.id,
            'ai_probability': r.ai_probability,
            'verdict': r.verdict,
            'preview': r.text_input[:100] + '...' if len(r.text_input) > 100 else r.text_input,
            'created_at': r.created_at.isoformat(),
        }
        for r in results
    ]
    return JsonResponse({'results': data})
