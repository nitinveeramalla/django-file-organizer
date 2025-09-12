# 📁 File Organizer with Analytics

A Django web application that organizes files by type and owner, extracts metadata, performs text analysis, and provides comprehensive analytics for data insights.

## ✨ Features

### 🗂️ File Organization
- **Smart File Segregation**: Organizes files by type (pngfiles, mp4files, pdffiles, etc.) and owner name
- **Owner Detection**: Automatically extracts owner names from filename prefixes (e.g., `rohith_photo.png` → rohith)
- **Duplicate Handling**: Gracefully handles duplicate filenames with automatic counters
- **25+ File Types**: Supports images, videos, documents, code files, archives, and more

### 📊 Metadata Extraction & Analytics
- **Complete Metadata**: File size, creation/modification dates, paths, and ownership
- **Text Analysis**: Extracts content from text-based files (.txt, .csv, .pdf, .docx)
- **Keyword Extraction**: Generates frequency-based keywords from file content
- **Auto-Summarization**: Creates 2-3 sentence summaries of text content
- **CSV Export**: Downloadable analytics data for further analysis

### 🎨 Modern Web Interface
- **Bootstrap UI**: Beautiful, responsive design with modern styling
- **Browse Button**: Easy directory selection with drag & drop support
- **Real-time Preview**: Live preview of processed files and metadata
- **Analytics Dashboard**: Comprehensive insights and statistics
- **Keyboard Shortcuts**: Ctrl+O for quick directory browsing

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd file_organizer
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and go to `http://localhost:8000`
   - Admin interface available at `http://localhost:8000/admin`

## 📋 Usage

### Basic File Organization

1. **Enter Directory Path**
   - Type the full path to your directory
   - Use the "Browse" button to select a folder
   - Drag & drop a folder into the input field
   - Use `Ctrl+O` keyboard shortcut

2. **Process Files**
   - Click "Start File Organization"
   - Watch the progress and see real-time statistics
   - View the organized file structure

3. **View Results**
   - See a summary of processed files
   - Preview metadata and analytics data
   - Download CSV file for further analysis

### Advanced Features

- **Analytics Dashboard**: View file type distribution, owner statistics, and processing history
- **CSV Export**: Download complete metadata and text analysis results
- **Admin Interface**: Manage data and view detailed records
- **Text Analysis**: Automatic keyword extraction and summarization for text files

## 🛠️ Configuration

### Environment Variables
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### File Type Mappings
The application supports these file types by default:
- **Images**: .png, .jpg, .jpeg, .gif, .bmp, .tiff
- **Videos**: .mp4, .avi, .mov, .wmv, .flv
- **Documents**: .pdf, .doc, .docx, .txt, .csv, .xls, .xlsx, .ppt, .pptx
- **Audio**: .mp3, .wav, .flac
- **Archives**: .zip, .rar, .7z
- **Code**: .py, .js, .html, .css, .java, .cpp, .c, .xml, .json, .sql

### Output Structure
```
output/
├── pngfiles/
│   ├── rohith/
│   │   ├── rohith_photo.png
│   │   └── rohith_image.png
│   └── sachin/
│       └── sachin_screenshot.png
├── mp4files/
│   ├── rohith/
│   └── sachin/
└── pdffiles/
    ├── rohith/
    └── sachin/
```

## 📊 Data Schema

### File Metadata
- `file_name`: Original filename
- `file_type`: File extension
- `owner_name`: Extracted from filename prefix
- `original_path`: Source file location
- `new_path`: Organized file location
- `file_size`: Size in bytes
- `created_date`: File creation date
- `modified_date`: File modification date
- `keywords`: Extracted keywords (for text files)
- `summary`: Auto-generated summary (for text files)

### Processing Sessions
- `session_id`: Unique session identifier
- `input_directory`: Source directory path
- `output_directory`: Organized directory path
- `total_files_processed`: Number of files processed
- `files_by_type`: Count of files by type
- `files_by_owner`: Count of files by owner
- `started_at`: Processing start time
- `completed_at`: Processing completion time
- `status`: Processing status (running/completed/failed)

## 🔧 Development

### Project Structure
```
file_organizer/
├── file_organizer/          # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── organizer/               # Main application
│   ├── models.py           # Database models
│   ├── views.py            # Business logic
│   ├── admin.py            # Admin interface
│   ├── urls.py             # URL patterns
│   └── templates/          # HTML templates
├── output/                 # Organized files
├── media/                  # Media files and CSV exports
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

### Running Tests
```bash
python manage.py test
```

### Database Management
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (WARNING: deletes all data)
python manage.py flush
```

## 📦 Dependencies

### Core Dependencies
- `Django>=5.2.6` - Web framework
- `pandas` - Data manipulation and CSV handling
- `PyPDF2` - PDF text extraction
- `python-docx` - Word document processing
- `nltk` - Natural language processing
- `sumy` - Text summarization

### Development Dependencies
- `pytest` - Testing framework
- `pytest-django` - Django testing utilities
- `black` - Code formatting
- `flake8` - Code linting

## 🚀 Deployment

### Production Settings
1. Set `DEBUG=False` in settings
2. Configure `ALLOWED_HOSTS` with your domain
3. Set up a production database (PostgreSQL recommended)
4. Configure static file serving
5. Set up a production WSGI server (Gunicorn recommended)

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "file_organizer.wsgi:application"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Common Issues

**Q: Files are not being organized correctly**
A: Check that the input directory path is correct and accessible. Ensure files follow the naming convention `owner_name_filename.ext`.

**Q: Text analysis is not working**
A: Make sure all required dependencies are installed. Check that the files are readable and contain text content.

**Q: CSV download is not working**
A: Verify that the `media` directory exists and has proper write permissions.

### Getting Help
- Check the [Issues](https://github.com/your-repo/issues) page
- Create a new issue with detailed description
- Include error messages and steps to reproduce

## 🎯 Roadmap

- [ ] Support for more file types
- [ ] Advanced text analysis with machine learning
- [ ] Batch processing for multiple directories
- [ ] API endpoints for programmatic access
- [ ] Real-time processing progress updates
- [ ] Custom file type mappings
- [ ] Integration with cloud storage services

## 🙏 Acknowledgments

- Django community for the excellent web framework
- Bootstrap for the responsive UI components
- All contributors and users who provide feedback

---

**Made with ❤️ for better file organization and data analytics**