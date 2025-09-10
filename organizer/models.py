from django.db import models
from django.utils import timezone
import os


class FileMetadata(models.Model):
    """Model to store metadata about processed files for analytics"""
    
    # File information
    original_path = models.CharField(max_length=500, help_text="Original file path")
    new_path = models.CharField(max_length=500, help_text="New organized file path")
    filename = models.CharField(max_length=255, help_text="Original filename")
    file_type = models.CharField(max_length=50, help_text="File extension/type")
    file_size = models.BigIntegerField(help_text="File size in bytes")
    
    # Owner information (extracted from filename prefix)
    owner_name = models.CharField(max_length=100, help_text="Owner name extracted from filename")
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now, help_text="When the record was created")
    moved_at = models.DateTimeField(default=timezone.now, help_text="When the file was moved")
    
    # Additional metadata
    is_duplicate = models.BooleanField(default=False, help_text="Whether this was a duplicate filename")
    duplicate_counter = models.IntegerField(default=0, help_text="Counter for duplicate files")
    
    class Meta:
        ordering = ['-moved_at']
        verbose_name = "File Metadata"
        verbose_name_plural = "File Metadata"
    
    def __str__(self):
        return f"{self.filename} ({self.file_type}) - {self.owner_name}"
    
    @property
    def file_size_mb(self):
        """Return file size in MB"""
        return round(self.file_size / (1024 * 1024), 2)
    
    @property
    def file_size_kb(self):
        """Return file size in KB"""
        return round(self.file_size / 1024, 2)


class ProcessingSession(models.Model):
    """Model to track processing sessions for analytics"""
    
    session_id = models.CharField(max_length=100, unique=True, help_text="Unique session identifier")
    input_directory = models.CharField(max_length=500, help_text="Input directory path")
    output_directory = models.CharField(max_length=500, help_text="Output directory path")
    total_files_processed = models.IntegerField(default=0, help_text="Total number of files processed")
    files_by_type = models.JSONField(default=dict, help_text="Count of files by type")
    files_by_owner = models.JSONField(default=dict, help_text="Count of files by owner")
    started_at = models.DateTimeField(default=timezone.now, help_text="When processing started")
    completed_at = models.DateTimeField(null=True, blank=True, help_text="When processing completed")
    status = models.CharField(max_length=20, default='running', choices=[
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ])
    error_message = models.TextField(blank=True, help_text="Error message if processing failed")
    
    class Meta:
        ordering = ['-started_at']
        verbose_name = "Processing Session"
        verbose_name_plural = "Processing Sessions"
    
    def __str__(self):
        return f"Session {self.session_id} - {self.status}"
    
    @property
    def duration(self):
        """Return processing duration"""
        if self.completed_at:
            return self.completed_at - self.started_at
        return timezone.now() - self.started_at
