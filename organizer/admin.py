from django.contrib import admin
from .models import FileMetadata, ProcessingSession


@admin.register(FileMetadata)
class FileMetadataAdmin(admin.ModelAdmin):
    list_display = ['filename', 'file_type', 'owner_name', 'file_size_mb', 'moved_at', 'is_duplicate']
    list_filter = ['file_type', 'owner_name', 'is_duplicate', 'moved_at']
    search_fields = ['filename', 'owner_name', 'original_path', 'new_path']
    readonly_fields = ['created_at', 'moved_at']
    ordering = ['-moved_at']
    
    fieldsets = (
        ('File Information', {
            'fields': ('filename', 'file_type', 'file_size', 'owner_name')
        }),
        ('Paths', {
            'fields': ('original_path', 'new_path')
        }),
        ('Metadata', {
            'fields': ('is_duplicate', 'duplicate_counter', 'created_at', 'moved_at')
        }),
    )


@admin.register(ProcessingSession)
class ProcessingSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'status', 'total_files_processed', 'started_at', 'duration']
    list_filter = ['status', 'started_at']
    search_fields = ['session_id', 'input_directory', 'output_directory']
    readonly_fields = ['session_id', 'started_at', 'completed_at', 'duration']
    ordering = ['-started_at']
    
    fieldsets = (
        ('Session Information', {
            'fields': ('session_id', 'status', 'started_at', 'completed_at', 'duration')
        }),
        ('Directories', {
            'fields': ('input_directory', 'output_directory')
        }),
        ('Statistics', {
            'fields': ('total_files_processed', 'files_by_type', 'files_by_owner')
        }),
        ('Error Information', {
            'fields': ('error_message',),
            'classes': ('collapse',)
        }),
    )
    
    def duration(self, obj):
        return obj.duration
    duration.short_description = 'Duration'
