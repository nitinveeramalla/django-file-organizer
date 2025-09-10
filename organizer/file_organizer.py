import os
import shutil
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import mimetypes

from django.utils import timezone
from .models import FileMetadata, ProcessingSession


class FileOrganizer:
    """Main class for organizing files by type and owner"""
    
    # File type mappings
    FILE_TYPE_MAPPINGS = {
        # Images
        '.png': 'pngfiles',
        '.jpg': 'jpgfiles', 
        '.jpeg': 'jpgfiles',
        '.gif': 'giffiles',
        '.bmp': 'bmpfiles',
        '.tiff': 'tifffiles',
        '.webp': 'webpfiles',
        
        # Videos
        '.mp4': 'mp4files',
        '.avi': 'avifiles',
        '.mov': 'movfiles',
        '.wmv': 'wmvfiles',
        '.flv': 'flvfiles',
        '.webm': 'webmfiles',
        '.mkv': 'mkvfiles',
        
        # Documents
        '.pdf': 'pdffiles',
        '.doc': 'docfiles',
        '.docx': 'docxfiles',
        '.txt': 'txtfiles',
        '.rtf': 'rtffiles',
        
        # Spreadsheets
        '.csv': 'csvfiles',
        '.xls': 'xlsfiles',
        '.xlsx': 'xlsxfiles',
        
        # Presentations
        '.ppt': 'pptfiles',
        '.pptx': 'pptxfiles',
        
        # Archives
        '.zip': 'zipfiles',
        '.rar': 'rarfiles',
        '.7z': '7zfiles',
        '.tar': 'tarfiles',
        '.gz': 'gzfiles',
        
        # Audio
        '.mp3': 'mp3files',
        '.wav': 'wavfiles',
        '.flac': 'flacfiles',
        '.aac': 'aacfiles',
        
        # Code files
        '.py': 'pyfiles',
        '.js': 'jsfiles',
        '.html': 'htmlfiles',
        '.css': 'cssfiles',
        '.java': 'javafiles',
        '.cpp': 'cppfiles',
        '.c': 'cfiles',
        
        # Other
        '.json': 'jsonfiles',
        '.xml': 'xmlfiles',
        '.sql': 'sqlfiles',
    }
    
    # Known owner prefixes (can be extended)
    KNOWN_OWNERS = ['rohith', 'sachin', 'nitin', 'himani']
    
    def __init__(self, input_directory: str, output_directory: Optional[str] = None):
        """
        Initialize the file organizer
        
        Args:
            input_directory: Path to the directory containing files to organize
            output_directory: Path to the output directory (optional)
        """
        self.input_directory = Path(input_directory).resolve()
        
        if output_directory:
            self.output_directory = Path(output_directory).resolve()
        else:
            # Default output directory in the same parent as input
            self.output_directory = self.input_directory.parent / 'output'
        
        self.session_id = str(uuid.uuid4())[:8]
        self.session = None
        self.stats = {
            'total_files': 0,
            'files_by_type': {},
            'files_by_owner': {},
            'duplicates': 0,
            'errors': []
        }
    
    def start_session(self) -> ProcessingSession:
        """Start a new processing session"""
        self.session = ProcessingSession.objects.create(
            session_id=self.session_id,
            input_directory=str(self.input_directory),
            output_directory=str(self.output_directory),
            status='running'
        )
        return self.session
    
    def get_file_type_category(self, file_path: Path) -> str:
        """
        Get the category folder name for a file based on its extension
        
        Args:
            file_path: Path to the file
            
        Returns:
            Category folder name (e.g., 'pngfiles', 'mp4files')
        """
        extension = file_path.suffix.lower()
        return self.FILE_TYPE_MAPPINGS.get(extension, 'otherfiles')
    
    def extract_owner_name(self, filename: str) -> str:
        """
        Extract owner name from filename prefix
        
        Args:
            filename: The filename to analyze
            
        Returns:
            Owner name (defaults to 'unknown' if not found)
        """
        filename_lower = filename.lower()
        
        for owner in self.KNOWN_OWNERS:
            if filename_lower.startswith(owner):
                return owner
        
        # If no known owner found, try to extract first word before underscore or dash
        import re
        match = re.match(r'^([a-zA-Z]+)[_-]', filename)
        if match:
            return match.group(1).lower()
        
        return 'unknown'
    
    def generate_unique_filename(self, target_path: Path, original_filename: str) -> Path:
        """
        Generate a unique filename if the target file already exists
        
        Args:
            target_path: The target directory path
            original_filename: The original filename
            
        Returns:
            Unique file path
        """
        file_path = target_path / original_filename
        
        if not file_path.exists():
            return file_path
        
        # File exists, generate unique name
        name, ext = os.path.splitext(original_filename)
        counter = 1
        
        while True:
            new_filename = f"{name}_{counter}{ext}"
            new_path = target_path / new_filename
            if not new_path.exists():
                return new_path
            counter += 1
    
    def scan_files(self) -> List[Path]:
        """
        Scan the input directory for files to organize
        
        Returns:
            List of file paths to organize
        """
        files = []
        
        try:
            for root, dirs, filenames in os.walk(self.input_directory):
                for filename in filenames:
                    file_path = Path(root) / filename
                    files.append(file_path)
        except Exception as e:
            self.stats['errors'].append(f"Error scanning directory: {str(e)}")
        
        return files
    
    def organize_file(self, file_path: Path) -> Optional[FileMetadata]:
        """
        Organize a single file by moving it to the appropriate location
        
        Args:
            file_path: Path to the file to organize
            
        Returns:
            FileMetadata object if successful, None if failed
        """
        try:
            # Get file information
            file_type_category = self.get_file_type_category(file_path)
            owner_name = self.extract_owner_name(file_path.name)
            file_size = file_path.stat().st_size
            
            # Create directory structure
            type_dir = self.output_directory / file_type_category
            owner_dir = type_dir / owner_name
            
            # Create directories if they don't exist
            owner_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate unique filename
            target_path = self.generate_unique_filename(owner_dir, file_path.name)
            
            # Check if this is a duplicate
            is_duplicate = target_path.name != file_path.name
            duplicate_counter = 0
            
            if is_duplicate:
                # Extract counter from filename
                import re
                match = re.search(r'_(\d+)$', target_path.stem)
                if match:
                    duplicate_counter = int(match.group(1))
                self.stats['duplicates'] += 1
            
            # Move the file
            shutil.move(str(file_path), str(target_path))
            
            # Create metadata record
            metadata = FileMetadata.objects.create(
                original_path=str(file_path),
                new_path=str(target_path),
                filename=file_path.name,
                file_type=file_path.suffix.lower(),
                file_size=file_size,
                owner_name=owner_name,
                moved_at=timezone.now(),
                is_duplicate=is_duplicate,
                duplicate_counter=duplicate_counter
            )
            
            # Update statistics
            self.stats['total_files'] += 1
            self.stats['files_by_type'][file_type_category] = self.stats['files_by_type'].get(file_type_category, 0) + 1
            self.stats['files_by_owner'][owner_name] = self.stats['files_by_owner'].get(owner_name, 0) + 1
            
            return metadata
            
        except Exception as e:
            error_msg = f"Error organizing file {file_path}: {str(e)}"
            self.stats['errors'].append(error_msg)
            return None
    
    def organize_all_files(self) -> Dict:
        """
        Organize all files in the input directory
        
        Returns:
            Dictionary with processing results and statistics
        """
        # Start processing session
        self.start_session()
        
        try:
            # Scan for files
            files_to_organize = self.scan_files()
            
            if not files_to_organize:
                self.stats['errors'].append("No files found in the input directory")
                return self.get_results()
            
            # Process each file
            processed_files = []
            for file_path in files_to_organize:
                metadata = self.organize_file(file_path)
                if metadata:
                    processed_files.append(metadata)
            
            # Update session with results
            if self.session:
                self.session.total_files_processed = self.stats['total_files']
                self.session.files_by_type = self.stats['files_by_type']
                self.session.files_by_owner = self.stats['files_by_owner']
                self.session.status = 'completed'
                self.session.completed_at = timezone.now()
                self.session.save()
            
            return self.get_results()
            
        except Exception as e:
            # Mark session as failed
            if self.session:
                self.session.status = 'failed'
                self.session.error_message = str(e)
                self.session.completed_at = timezone.now()
                self.session.save()
            
            self.stats['errors'].append(f"Processing failed: {str(e)}")
            return self.get_results()
    
    def get_results(self) -> Dict:
        """
        Get processing results and statistics
        
        Returns:
            Dictionary with results
        """
        return {
            'session_id': self.session_id,
            'total_files': self.stats['total_files'],
            'files_by_type': self.stats['files_by_type'],
            'files_by_owner': self.stats['files_by_owner'],
            'duplicates': self.stats['duplicates'],
            'errors': self.stats['errors'],
            'output_directory': str(self.output_directory),
            'success': len(self.stats['errors']) == 0
        }
