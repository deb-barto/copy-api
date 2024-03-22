import pandas as pd
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status

from .models import Upload
from .serializers import UploadSerializer  # Importe o UploadSerializer aqui

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = UploadSerializer(data=request.data)
        if file_serializer.is_valid():
            uploaded_file = file_serializer.save()
            file_obj = uploaded_file.file 
            df = pd.read_excel(file_obj)
            json_data = df.to_dict(orient='records')
            return Response(json_data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)