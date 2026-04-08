from django.urls import path
from . import views

app_name = 'detection'

urlpatterns = [
    path('analyze/', views.detect_text, name='analyze_text'),
    path('upload/', views.detect_file, name='analyze_file'),
    path('history/', views.detection_history, name='history'),
]
