import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .rewriter import humanize_text
from .models import HumanizationResult


@csrf_exempt
@require_http_methods(["POST"])
def humanize(request):
    """Humanize AI-generated text."""
    try:
        body = json.loads(request.body)
        text = body.get('text', '').strip()
        intensity = body.get('intensity', 'medium')
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'error': 'Invalid JSON payload.'}, status=400)

    if not text:
        return JsonResponse({'error': 'No text provided.'}, status=400)

    if intensity not in ('light', 'medium', 'heavy'):
        intensity = 'medium'

    result = humanize_text(text, intensity=intensity)

    HumanizationResult.objects.create(
        original_text=text[:5000],
        humanized_text=result['humanized_text'][:5000],
        intensity=intensity,
    )

    return JsonResponse(result)


@csrf_exempt
@require_http_methods(["GET"])
def humanization_history(request):
    """Get recent humanization results."""
    results = HumanizationResult.objects.all()[:20]
    data = [
        {
            'id': r.id,
            'intensity': r.intensity,
            'original_preview': r.original_text[:100] + '...',
            'humanized_preview': r.humanized_text[:100] + '...',
            'created_at': r.created_at.isoformat(),
        }
        for r in results
    ]
    return JsonResponse({'results': data})
