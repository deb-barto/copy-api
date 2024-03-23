from django.contrib import admin
from .models import Upload, MRRReport

@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ('file', 'uploaded_at')

@admin.register(MRRReport)
class MRRReportAdmin(admin.ModelAdmin):
    list_display = ('date_generated',)