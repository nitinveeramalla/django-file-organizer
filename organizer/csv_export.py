"""
CSV export utilities for file metadata and analytics
"""
import csv
import os
from datetime import datetime
from django.conf import settings
from .models import FileMetadata, ProcessingSession


def generate_csv_export(session_id=None):
    """
    Generate CSV export of file metadata and analytics
    """
    # Create media directory if it doesn't exist
    media_dir = os.path.join(settings.BASE_DIR, 'media')
    os.makedirs(media_dir, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"file_analytics_{timestamp}.csv"
    filepath = os.path.join(media_dir, filename)
    
    # Get file metadata
    if session_id:
        files = FileMetadata.objects.filter(
            moved_at__gte=ProcessingSession.objects.get(session_id=session_id).started_at
        ).order_by('-moved_at')
    else:
        files = FileMetadata.objects.all().order_by('-moved_at')
    
    # Write CSV file
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'file_name', 'file_type', 'owner_name', 'original_path', 'new_path',
            'file_size', 'file_size_mb', 'created_date', 'modified_date',
            'keywords', 'summary', 'moved_at', 'is_duplicate'
        ]
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for file in files:
            # Convert file size to MB
            file_size_mb = round(file.file_size / (1024 * 1024), 2) if file.file_size else 0
            
            writer.writerow({
                'file_name': file.filename,
                'file_type': file.file_type,
                'owner_name': file.owner_name,
                'original_path': file.original_path,
                'new_path': file.new_path,
                'file_size': file.file_size,
                'file_size_mb': file_size_mb,
                'created_date': file.created_date.strftime('%Y-%m-%d %H:%M:%S') if file.created_date else '',
                'modified_date': file.modified_date.strftime('%Y-%m-%d %H:%M:%S') if file.modified_date else '',
                'keywords': file.keywords,
                'summary': file.summary,
                'moved_at': file.moved_at.strftime('%Y-%m-%d %H:%M:%S'),
                'is_duplicate': file.is_duplicate
            })
    
    return filepath, filename


def get_csv_preview(limit=20):
    """
    Get a preview of the CSV data for display in the web interface
    """
    files = FileMetadata.objects.all().order_by('-moved_at')[:limit]
    
    preview_data = []
    for file in files:
        file_size_mb = round(file.file_size / (1024 * 1024), 2) if file.file_size else 0
        
        preview_data.append({
            'file_name': file.filename,
            'file_type': file.file_type,
            'owner_name': file.owner_name,
            'file_size_mb': file_size_mb,
            'created_date': file.created_date.strftime('%Y-%m-%d') if file.created_date else 'N/A',
            'modified_date': file.modified_date.strftime('%Y-%m-%d') if file.modified_date else 'N/A',
            'keywords': file.keywords[:50] + '...' if len(file.keywords) > 50 else file.keywords,
            'summary': file.summary[:100] + '...' if len(file.summary) > 100 else file.summary,
            'moved_at': file.moved_at.strftime('%Y-%m-%d %H:%M')
        })
    
    return preview_data


def get_analytics_summary():
    """
    Get summary statistics for analytics
    """
    total_files = FileMetadata.objects.count()
    
    # File type distribution
    file_types = {}
    for file in FileMetadata.objects.all():
        file_types[file.file_type] = file_types.get(file.file_type, 0) + 1
    
    # Owner distribution
    owners = {}
    for file in FileMetadata.objects.all():
        owners[file.owner_name] = owners.get(file.owner_name, 0) + 1
    
    # Total size
    total_size = sum(file.file_size for file in FileMetadata.objects.all())
    total_size_mb = round(total_size / (1024 * 1024), 2)
    
    # Files with text analysis
    text_analyzed = FileMetadata.objects.exclude(keywords='').count()
    
    return {
        'total_files': total_files,
        'total_size_mb': total_size_mb,
        'text_analyzed': text_analyzed,
        'file_types': dict(sorted(file_types.items(), key=lambda x: x[1], reverse=True)),
        'owners': dict(sorted(owners.items(), key=lambda x: x[1], reverse=True))
    }
