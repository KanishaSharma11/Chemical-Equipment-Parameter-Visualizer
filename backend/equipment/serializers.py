# backend/equipment/serializers.py
from rest_framework import serializers
from .models import Upload

class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ["id", "original_filename", "uploaded_at", "summary_json"]
