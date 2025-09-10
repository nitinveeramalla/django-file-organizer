from django import forms
from django.core.exceptions import ValidationError
import os


class DirectoryPathForm(forms.Form):
    """Form for inputting directory path for file organization"""
    
    directory_path = forms.CharField(
        max_length=500,
        label="Directory Path",
        help_text="Enter the full path to the directory containing files to organize",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'C:\\Users\\username\\Documents\\files_to_organize',
            'style': 'width: 100%;'
        })
    )
    
    output_directory = forms.CharField(
        max_length=500,
        required=False,
        label="Output Directory (Optional)",
        help_text="Leave empty to use default 'output' folder in the same directory",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'C:\\Users\\username\\Documents\\organized_files',
            'style': 'width: 100%;'
        })
    )
    
    def clean_directory_path(self):
        """Validate that the directory path exists and is accessible"""
        directory_path = self.cleaned_data.get('directory_path')
        
        if not directory_path:
            raise ValidationError("Directory path is required.")
        
        # Normalize the path
        directory_path = os.path.normpath(directory_path)
        
        if not os.path.exists(directory_path):
            raise ValidationError(f"Directory does not exist: {directory_path}")
        
        if not os.path.isdir(directory_path):
            raise ValidationError(f"Path is not a directory: {directory_path}")
        
        if not os.access(directory_path, os.R_OK):
            raise ValidationError(f"Directory is not readable: {directory_path}")
        
        return directory_path
    
    def clean_output_directory(self):
        """Validate output directory if provided"""
        output_directory = self.cleaned_data.get('output_directory')
        
        if output_directory:
            # Normalize the path
            output_directory = os.path.normpath(output_directory)
            
            # Check if parent directory exists
            parent_dir = os.path.dirname(output_directory)
            if not os.path.exists(parent_dir):
                raise ValidationError(f"Parent directory does not exist: {parent_dir}")
            
            if not os.access(parent_dir, os.W_OK):
                raise ValidationError(f"Parent directory is not writable: {parent_dir}")
        
        return output_directory
    
    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        directory_path = cleaned_data.get('directory_path')
        output_directory = cleaned_data.get('output_directory')
        
        if directory_path and output_directory:
            # Normalize paths for comparison
            directory_path = os.path.normpath(directory_path)
            output_directory = os.path.normpath(output_directory)
            
            # Check if output directory is the same as or inside input directory
            if output_directory == directory_path:
                raise ValidationError("Output directory cannot be the same as input directory.")
            
            try:
                # Check if output directory is inside input directory
                common_path = os.path.commonpath([directory_path, output_directory])
                if common_path == directory_path:
                    raise ValidationError("Output directory cannot be inside the input directory.")
            except ValueError:
                # Paths are on different drives, which is fine
                pass
        
        return cleaned_data


class AnalyticsFilterForm(forms.Form):
    """Form for filtering analytics data"""
    
    file_type = forms.ChoiceField(
        choices=[('', 'All Types')] + [
            ('png', 'PNG Images'),
            ('jpg', 'JPG Images'),
            ('jpeg', 'JPEG Images'),
            ('mp4', 'MP4 Videos'),
            ('avi', 'AVI Videos'),
            ('pdf', 'PDF Documents'),
            ('csv', 'CSV Files'),
            ('doc', 'DOC Documents'),
            ('docx', 'DOCX Documents'),
            ('txt', 'Text Files'),
        ],
        required=False,
        label="File Type",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    owner_name = forms.CharField(
        max_length=100,
        required=False,
        label="Owner Name",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter owner name to filter'
        })
    )
    
    date_from = forms.DateField(
        required=False,
        label="From Date",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        label="To Date",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
