from django.contrib import admin
from .models import FileMetadata, ProcessingSession


@admin.register(FileMetadata)
class FileMetadataAdmin(admin.ModelAdmin):
    list_display = ['filename', 'file_type', 'owner_name', 'file_size', 'moved_at']
    list_filter = ['file_type', 'owner_name', 'moved_at', 'is_duplicate']
    search_fields = ['filename', 'owner_name', 'original_path', 'new_path']
    readonly_fields = ['created_at', 'moved_at']
    ordering = ['-moved_at']


@admin.register(ProcessingSession)
class ProcessingSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'status', 'total_files_processed', 'started_at', 'completed_at']
    list_filter = ['status', 'started_at', 'completed_at']
    search_fields = ['session_id', 'input_directory', 'output_directory']
    readonly_fields = ['session_id', 'started_at', 'completed_at']
    ordering = ['-started_at']
