from django.contrib import admin
from django.urls import path
from .views import FileUploadView, GetDataView, MRRDataView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('getdata/', GetDataView.as_view(), name='get-data'),
    path('mrr-data/', MRRDataView.as_view(), name='mrr-data'),
]
