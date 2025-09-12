import os
import shutil
from pathlib import Path
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
from .models import FileMetadata, ProcessingSession
from .text_analysis import analyze_text_file, get_file_dates
from .csv_export import generate_csv_export, get_csv_preview, get_analytics_summary
import json


def home(request):
    """Main page with form to input directory path"""
    if request.method == 'POST':
        input_path = request.POST.get('input_path', '').strip()
        
        if not input_path:
            messages.error(request, 'Please provide a valid directory path.')
            return render(request, 'organizer/home.html')
        
        if not os.path.exists(input_path) or not os.path.isdir(input_path):
            messages.error(request, 'The provided path does not exist or is not a directory.')
            return render(request, 'organizer/home.html')
        
        # Start processing
        return process_files(request, input_path)
    
    return render(request, 'organizer/home.html')


def process_files(request, input_path):
    """Process files in the given directory"""
    try:
        # Create processing session
        session = ProcessingSession.objects.create(
            input_directory=input_path,
            output_directory=os.path.join(os.path.dirname(input_path), 'output')
        )
        
        # File type mappings
        file_type_mappings = {
            '.png': 'pngfiles',
            '.jpg': 'jpgfiles', 
            '.jpeg': 'jpgfiles',
            '.gif': 'giffiles',
            '.bmp': 'bmpfiles',
            '.tiff': 'tifffiles',
            '.mp4': 'mp4files',
            '.avi': 'avifiles',
            '.mov': 'movfiles',
            '.wmv': 'wmvfiles',
            '.flv': 'flvfiles',
            '.pdf': 'pdffiles',
            '.doc': 'docfiles',
            '.docx': 'docxfiles',
            '.txt': 'txtfiles',
            '.csv': 'csvfiles',
            '.xls': 'xlsfiles',
            '.xlsx': 'xlsxfiles',
            '.ppt': 'pptfiles',
            '.pptx': 'pptxfiles',
            '.mp3': 'mp3files',
            '.wav': 'wavfiles',
            '.flac': 'flacfiles',
            '.zip': 'zipfiles',
            '.rar': 'rarfiles',
            '.7z': '7zfiles',
            '.html': 'htmlfiles',
            '.htm': 'htmlfiles',
            '.css': 'cssfiles',
            '.js': 'jsfiles',
            '.py': 'pyfiles',
            '.java': 'javafiles',
            '.cpp': 'cppfiles',
            '.c': 'cfiles',
            '.xml': 'xmlfiles',
            '.json': 'jsonfiles',
            '.sql': 'sqlfiles',
        }
        
        # Statistics tracking
        files_by_type = {}
        files_by_owner = {}
        total_files = 0
        
        # Process each file
        for root, dirs, files in os.walk(input_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = Path(file).suffix.lower()
                
                if file_ext in file_type_mappings:
                    # Extract owner name from filename (assume format: owner_name_*)
                    owner_name = extract_owner_name(file)
                    
                    # Create organized directory structure
                    output_base = session.output_directory
                    type_folder = file_type_mappings[file_ext]
                    owner_folder = os.path.join(output_base, type_folder, owner_name)
                    
                    # Create directories if they don't exist
                    os.makedirs(owner_folder, exist_ok=True)
                    
                    # Handle duplicate filenames
                    new_file_path = handle_duplicate_filename(owner_folder, file)
                    
                    # Move file
                    shutil.move(file_path, new_file_path)
                    
                    # Get file size
                    file_size = os.path.getsize(new_file_path)
                    
                    # Get file dates
                    created_date, modified_date = get_file_dates(new_file_path)
                    
                    # Analyze text content for text-based files
                    keywords = ""
                    summary = ""
                    if file_ext in ['.txt', '.csv', '.pdf', '.docx']:
                        keywords, summary = analyze_text_file(new_file_path)
                    
                    # Create metadata record
                    FileMetadata.objects.create(
                        original_path=file_path,
                        new_path=new_file_path,
                        filename=file,
                        file_type=file_ext,
                        file_size=file_size,
                        owner_name=owner_name,
                        created_date=created_date,
                        modified_date=modified_date,
                        keywords=keywords,
                        summary=summary,
                        moved_at=timezone.now()
                    )
                    
                    # Update statistics
                    total_files += 1
                    files_by_type[file_ext] = files_by_type.get(file_ext, 0) + 1
                    files_by_owner[owner_name] = files_by_owner.get(owner_name, 0) + 1
        
        # Update session with results
        session.total_files_processed = total_files
        session.files_by_type = files_by_type
        session.files_by_owner = files_by_owner
        session.status = 'completed'
        session.completed_at = timezone.now()
        session.save()
        
        # Generate CSV export
        try:
            csv_path, csv_filename = generate_csv_export(session.session_id)
            session.csv_file = csv_filename
            session.save()
        except Exception as e:
            print(f"Error generating CSV: {e}")
        
        # Prepare summary message
        summary_parts = [f"{total_files} files processed"]
        for file_type, count in sorted(files_by_type.items()):
            summary_parts.append(f"{count} {file_type.upper()}")
        
        messages.success(request, ', '.join(summary_parts))
        return redirect('organizer:results', session_id=session.session_id)
        
    except Exception as e:
        if 'session' in locals():
            session.status = 'failed'
            session.error_message = str(e)
            session.completed_at = timezone.now()
            session.save()
        
        messages.error(request, f'Error processing files: {str(e)}')
        return render(request, 'organizer/home.html')


def extract_owner_name(filename):
    """Extract owner name from filename (assume format: owner_name_*)"""
    # Remove extension
    name_without_ext = Path(filename).stem
    
    # Split by underscore and take first part
    parts = name_without_ext.split('_')
    if parts:
        return parts[0].lower()
    else:
        return 'unknown'


def handle_duplicate_filename(directory, filename):
    """Handle duplicate filenames by appending counter"""
    base_path = os.path.join(directory, filename)
    
    if not os.path.exists(base_path):
        return base_path
    
    # Split filename and extension
    name, ext = os.path.splitext(filename)
    counter = 1
    
    while True:
        new_filename = f"{name}_{counter}{ext}"
        new_path = os.path.join(directory, new_filename)
        
        if not os.path.exists(new_path):
            return new_path
        
        counter += 1


def results(request, session_id):
    """Display processing results"""
    try:
        session = ProcessingSession.objects.get(session_id=session_id)
        recent_files = FileMetadata.objects.filter(
            moved_at__gte=session.started_at
        ).order_by('-moved_at')[:20]
        
        # Get CSV preview data
        csv_preview = get_csv_preview(20)
        
        context = {
            'session': session,
            'recent_files': recent_files,
            'csv_preview': csv_preview,
        }
        return render(request, 'organizer/results.html', context)
    except ProcessingSession.DoesNotExist:
        messages.error(request, 'Processing session not found.')
        return redirect('organizer:home')


def analytics(request):
    """Display analytics dashboard"""
    # Get recent sessions
    recent_sessions = ProcessingSession.objects.filter(
        status='completed'
    ).order_by('-completed_at')[:10]
    
    # Get analytics summary
    analytics_data = get_analytics_summary()
    
    context = {
        'recent_sessions': recent_sessions,
        'file_types': list(analytics_data['file_types'].items()),
        'owners': list(analytics_data['owners'].items()),
        'total_files': analytics_data['total_files'],
        'total_size_mb': analytics_data['total_size_mb'],
        'text_analyzed': analytics_data['text_analyzed'],
    }
    
    return render(request, 'organizer/analytics.html', context)


def download_csv(request, session_id=None):
    """Download CSV file"""
    try:
        if session_id:
            session = ProcessingSession.objects.get(session_id=session_id)
            if session.csv_file:
                file_path = os.path.join(settings.BASE_DIR, 'media', session.csv_file)
            else:
                # Generate CSV if not exists
                file_path, filename = generate_csv_export(session_id)
        else:
            # Generate general CSV
            file_path, filename = generate_csv_export()
        
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                return response
        else:
            raise Http404("CSV file not found")
    
    except Exception as e:
        messages.error(request, f'Error downloading CSV: {str(e)}')
        return redirect('organizer:home')
