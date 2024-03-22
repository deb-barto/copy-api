from django.core.files.storage import default_storage
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .processing import get_processed_data
import pandas as pd

from .models import Upload
from .serializers import UploadSerializer

class FileUploadView(APIView):

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = UploadSerializer(data=request.data)
        if file_serializer.is_valid():
      
            uploaded_file = file_serializer.save()
            df = pd.read_excel(uploaded_file.file)
            json_data = df.to_dict(orient='records')

            for upload in Upload.objects.exclude(id=uploaded_file.id):
                if default_storage.exists(upload.file.name):
                    default_storage.delete(upload.file.name)
                upload.delete()

            return Response(json_data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class GetDataView(APIView):
    renderer_classes = [JSONRenderer]
    
    def get(self, request, *args, **kwargs):
        data = get_processed_data()
        return Response(data)