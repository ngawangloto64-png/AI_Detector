from django.urls import path
from . import views

app_name = 'humanizer'

urlpatterns = [
    path('humanize/', views.humanize, name='humanize'),
    path('history/', views.humanization_history, name='history'),
]
