# File Organizer Django Application

A Django web application that automatically organizes files by type and owner name, with built-in data analytics capabilities.

## Features

- **Automatic File Organization**: Scans directories and organizes files by type (PNG, MP4, PDF, CSV, etc.) and owner name
- **Smart Owner Detection**: Extracts owner names from filename prefixes (rohith, sachin, nitin, himani, etc.)
- **Duplicate Handling**: Gracefully handles duplicate filenames with automatic renaming
- **Data Analytics**: Comprehensive analytics dashboard with charts and statistics
- **Session Tracking**: Tracks processing sessions with detailed metadata
- **Admin Interface**: Full Django admin interface for data management

## Supported File Types

### Images
- PNG, JPG, JPEG, GIF, BMP, TIFF, WebP

### Videos
- MP4, AVI, MOV, WMV, FLV, WebM, MKV

### Documents
- PDF, DOC, DOCX, TXT, RTF

### Spreadsheets
- CSV, XLS, XLSX

### Presentations
- PPT, PPTX

### Archives
- ZIP, RAR, 7Z, TAR, GZ

### Audio
- MP3, WAV, FLAC, AAC

### Code Files
- PY, JS, HTML, CSS, Java, CPP, C

### Other
- JSON, XML, SQL

## Installation

1. **Clone or download the project**
   ```bash
   cd file_organizer
   ```

2. **Install Django** (if not already installed)
   ```bash
   pip install django
   ```

3. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser** (optional, for admin access)
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**
   - Main application: http:<IP Address>:8000/
   - Admin interface: http:<IP Address>:8000/admin/

## Usage

### 1. Organize Files

1. Navigate to the main page (http://<IP Address>:8000/)
2. Enter the path to a directory containing files to organize
3. Optionally specify an output directory (defaults to 'output' folder)
4. Click "Organize Files" to start the process
5. View the results and statistics

### 2. View Analytics

1. Go to the Analytics page (http://<IP Address>:8000/analytics/)
2. Use filters to analyze specific file types, owners, or date ranges
3. View charts showing file distribution by type and owner
4. Browse processed files with pagination
5. View recent processing sessions

### 3. Admin Interface

1. Go to http://<IP Address>/admin/
2. Login with your superuser credentials
3. Manage FileMetadata and ProcessingSession records
4. View detailed information about processed files

## Folder Structure

The application creates the following organized structure:

```
output/
├── pngfiles/
│   ├── rohith/
│   │   ├── rohith_file1.png
│   │   └── rohith_file2.png
│   ├── sachin/
│   ├── nitin/
│   └── himani/
├── mp4files/
│   ├── rohith/
│   ├── sachin/
│   ├── nitin/
│   └── himani/
├── pdffiles/
│   ├── rohith/
│   ├── sachin/
│   ├── nitin/
│   └── himani/
└── csvfiles/
    ├── rohith/
    ├── sachin/
    ├── nitin/
    └── himani/
```

## Data Analytics

The application logs comprehensive metadata for analytics:

### File Metadata
- Original and new file paths
- File type and size
- Owner name (extracted from filename)
- Processing timestamps
- Duplicate information

### Processing Sessions
- Session ID and status
- Input/output directories
- File counts by type and owner
- Processing duration
- Error messages (if any)

### Analytics Features
- File distribution charts (pie and bar charts)
- Owner statistics
- File type analysis
- Processing session history
- Filterable data views
- Export capabilities

## API Endpoints

- `GET /api/analytics/` - Returns analytics data in JSON format for charts

## Configuration

### Adding New File Types

Edit `organizer/file_organizer.py` and add new extensions to the `FILE_TYPE_MAPPINGS` dictionary:

```python
FILE_TYPE_MAPPINGS = {
    # ... existing mappings ...
    '.new_extension': 'newtypefiles',
}
```

### Adding New Owner Names

Edit `organizer/file_organizer.py` and add new names to the `KNOWN_OWNERS` list:

```python
KNOWN_OWNERS = ['rohith', 'sachin', 'nitin', 'himani', 'new_owner']
```

## Testing

A test directory with sample files is included:
- `test_files/` - Contains sample files with different owners and types

## Security Notes

- The application validates directory paths to prevent security issues
- File operations are performed safely with proper error handling
- Admin interface is protected by Django's authentication system

## Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure the application has read/write permissions to the specified directories
2. **Path Not Found**: Verify that the input directory path exists and is accessible
3. **Database Errors**: Run `python manage.py migrate` to ensure database is up to date

### Logs

Check the Django console output for detailed error messages and processing logs.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
