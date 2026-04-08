from django.contrib import admin
from .models import HumanizationResult


@admin.register(HumanizationResult)
class HumanizationResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'intensity', 'created_at']
    list_filter = ['intensity']
    readonly_fields = ['created_at']
