# backend/equipment/models.py
from django.db import models
from django.utils import timezone

class Upload(models.Model):
    csv_file = models.FileField(upload_to="uploads/")
    original_filename = models.CharField(max_length=256)
    uploaded_at = models.DateTimeField(default=timezone.now)
    summary_json = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Upload {self.id} - {self.original_filename}"
