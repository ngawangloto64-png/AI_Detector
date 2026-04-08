from django.db import models


class HumanizationResult(models.Model):
    INTENSITY_CHOICES = [
        ('light', 'Light'),
        ('medium', 'Medium'),
        ('heavy', 'Heavy'),
    ]

    original_text = models.TextField()
    humanized_text = models.TextField()
    intensity = models.CharField(max_length=10, choices=INTENSITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Humanization {self.id} - {self.intensity}"
