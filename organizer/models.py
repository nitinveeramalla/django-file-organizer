from django.db import models
import uuid
from django.utils import timezone


class FileMetadata(models.Model):
    """Model to store metadata for processed files for analytics"""
    original_path = models.CharField(max_length=500, help_text='Original file path', default='')
    new_path = models.CharField(max_length=500, help_text='New organized file path', default='')
    filename = models.CharField(max_length=255, help_text='Original filename', default='')
    file_type = models.CharField(max_length=50, help_text='File extension/type', default='')
    file_size = models.BigIntegerField(help_text='File size in bytes', default=0)
    owner_name = models.CharField(max_length=100, help_text='Owner name extracted from filename', default='unknown')
    created_at = models.DateTimeField(default=timezone.now, help_text='When the record was created')
    moved_at = models.DateTimeField(default=timezone.now, help_text='When the file was moved')
    is_duplicate = models.BooleanField(default=False, help_text='Whether this was a duplicate filename')
    duplicate_counter = models.IntegerField(default=0, help_text='Counter for duplicate files')
    
    class Meta:
        verbose_name = 'File Metadata'
        verbose_name_plural = 'File Metadata'
        ordering = ['-moved_at']
    
    def __str__(self):
        return f"{self.filename} ({self.file_type}) - {self.owner_name}"


class ProcessingSession(models.Model):
    """Model to track processing sessions for analytics"""
    STATUS_CHOICES = [
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]
    
    session_id = models.CharField(max_length=100, unique=True, help_text='Unique session identifier', default='')
    input_directory = models.CharField(max_length=500, help_text='Input directory path', default='')
    output_directory = models.CharField(max_length=500, help_text='Output directory path', default='')
    total_files_processed = models.IntegerField(default=0, help_text='Total number of files processed')
    files_by_type = models.JSONField(default=dict, help_text='Count of files by type')
    files_by_owner = models.JSONField(default=dict, help_text='Count of files by owner')
    started_at = models.DateTimeField(default=timezone.now, help_text='When processing started')
    completed_at = models.DateTimeField(blank=True, null=True, help_text='When processing completed')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='running')
    error_message = models.TextField(blank=True, help_text='Error message if processing failed')
    
    class Meta:
        verbose_name = 'Processing Session'
        verbose_name_plural = 'Processing Sessions'
        ordering = ['-started_at']
    
    def __str__(self):
        return f"Session {self.session_id} - {self.status}"
    
    def save(self, *args, **kwargs):
        if not self.session_id:
            self.session_id = str(uuid.uuid4())
        super().save(*args, **kwargs)
