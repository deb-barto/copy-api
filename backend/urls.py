from django.contrib import admin
from django.urls import path
from .views import FileUploadView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', FileUploadView.as_view(), name='file-upload')
]
