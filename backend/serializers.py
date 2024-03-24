from rest_framework import serializers
from .models import Upload

class UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Upload
        fields = ['file', 'uploaded_at']

from rest_framework import serializers

class DynamicFieldsSerializer(serializers.Serializer):
    def __init__(self, *args, **kwargs):
        data = kwargs.get('data')
        
        if isinstance(data, dict):
            for field_name, field_value in data.items():
                field_class = serializers.CharField if isinstance(field_value, str) else serializers.IntegerField
                self.fields[field_name] = field_class()
        
      
        elif isinstance(data, list) and data:
            first_item = data[0]
            for field_name, field_value in first_item.items():
                field_class = serializers.CharField if isinstance(field_value, str) else serializers.IntegerField
                self.fields[field_name] = field_class()
        
        super(serializers.Serializer, self).__init__(*args, **kwargs)