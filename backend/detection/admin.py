from django.contrib import admin
from .models import DetectionResult


@admin.register(DetectionResult)
class DetectionResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'verdict', 'ai_probability', 'created_at']
    list_filter = ['verdict']
    readonly_fields = ['created_at']
