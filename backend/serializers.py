from rest_framework import serializers
from .models import Upload

class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ['file', 'uploaded_at']

class XLSXDataSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nome = serializers.CharField(max_length=255)