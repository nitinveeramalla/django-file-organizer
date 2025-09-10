# Django File Organizer

A Django web application that automatically organizes files by type and owner name, with built-in data analytics capabilities.

## Features

- **Automatic File Organization**: Scans directories and organizes files by type (PNG, MP4, PDF, CSV, etc.) and owner name
- **Smart Owner Detection**: Extracts owner names from filename prefixes (rohith, sachin, nitin, himani, etc.)
- **Duplicate Handling**: Gracefully handles duplicate filenames with automatic renaming
- **Data Analytics**: Comprehensive analytics dashboard with charts and statistics
- **Session Tracking**: Tracks processing sessions with detailed metadata
- **Admin Interface**: Full Django admin interface for data management

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd file_organizer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
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

<<<<<<< HEAD
1. Navigate to the main page (http://127.0.0.1:8000/)
=======
### 1. Organize Files

1. Navigate to the main page (http://<IP Address>:8000/)
>>>>>>> 9193c33e50f3e4c9ee1023ac06c6a5aa7d93ee83
2. Enter the path to a directory containing files to organize
3. Optionally specify an output directory (defaults to 'output' folder)
4. Click "Organize Files" to start the process
5. View the results and statistics

## Supported File Types

<<<<<<< HEAD
- **Images**: PNG, JPG, JPEG, GIF, BMP, TIFF, WebP
- **Videos**: MP4, AVI, MOV, WMV, FLV, WebM, MKV
- **Documents**: PDF, DOC, DOCX, TXT, RTF
- **Spreadsheets**: CSV, XLS, XLSX
- **Presentations**: PPT, PPTX
- **Archives**: ZIP, RAR, 7Z, TAR, GZ
- **Audio**: MP3, WAV, FLAC, AAC
- **Code Files**: PY, JS, HTML, CSS, Java, CPP, C
- **Other**: JSON, XML, SQL
=======
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
>>>>>>> 9193c33e50f3e4c9ee1023ac06c6a5aa7d93ee83

## Folder Structure

The application creates the following organized structure:

```
output/
├── pngfiles/
│   ├── rohith/
│   ├── sachin/
│   ├── nitin/
│   └── himani/
├── mp4files/
│   ├── rohith/
│   ├── sachin/
│   ├── nitin/
│   └── himani/
└── pdffiles/
    ├── rohith/
    ├── sachin/
    ├── nitin/
    └── himani/
```

## Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure the application has read/write permissions to the specified directories
2. **Path Not Found**: Verify that the input directory path exists and is accessible
3. **Database Errors**: Run `python manage.py migrate` to ensure database is up to date

### Setup on New System

If you're setting up on a new system:

1. Make sure Python and pip are installed
2. Install Django: `pip install django`
3. Run migrations: `python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`
5. Start server: `python manage.py runserver`

## License

This project is open source and available under the MIT License.
