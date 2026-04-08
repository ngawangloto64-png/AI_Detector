from django.db import models


class DetectionResult(models.Model):
    text_input = models.TextField()
    ai_probability = models.FloatField()
    verdict = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Detection {self.id} - {self.verdict} ({self.ai_probability}%)"
