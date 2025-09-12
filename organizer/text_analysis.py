"""
Text analysis utilities for extracting keywords and generating summaries
Enhanced with comprehensive CSV analysis and detailed data insights
"""
import os
import re
import csv
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.stem import WordNetLemmatizer
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

try:
    from sumy.parsers.plaintext import PlaintextParser
    from sumy.nlp.tokenizers import Tokenizer
    from sumy.summarizers.lsa import LsaSummarizer
    from sumy.summarizers.text_rank import TextRankSummarizer
    SUMY_AVAILABLE = True
except ImportError:
    SUMY_AVAILABLE = False


def extract_text_from_file(file_path):
    """
    Extract text content from various file types
    """
    file_ext = Path(file_path).suffix.lower()
    
    try:
        if file_ext == '.txt':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        
        elif file_ext == '.csv':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        
        elif file_ext == '.pdf' and PDF_AVAILABLE:
            text = ""
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        
        elif file_ext == '.docx' and DOCX_AVAILABLE:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        
        else:
            return ""
    
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return ""


def extract_keywords(text, max_keywords=10):
    """
    Extract keywords from text using frequency analysis
    """
    if not text or not text.strip():
        return ""
    
    # Clean and tokenize text
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    words = text.split()
    
    # Remove common stopwords if NLTK is available
    if NLTK_AVAILABLE:
        try:
            stop_words = set(stopwords.words('english'))
            words = [word for word in words if word not in stop_words and len(word) > 2]
        except:
            # Fallback to basic stopwords
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
            words = [word for word in words if word not in stop_words and len(word) > 2]
    else:
        # Basic stopwords
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        words = [word for word in words if word not in stop_words and len(word) > 2]
    
    # Count word frequencies
    word_counts = Counter(words)
    
    # Get top keywords
    keywords = [word for word, count in word_counts.most_common(max_keywords)]
    
    return ', '.join(keywords)


def generate_summary(text, max_sentences=3):
    """
    Generate a summary of the text
    """
    if not text or not text.strip():
        return ""
    
    # Clean text
    text = re.sub(r'\s+', ' ', text.strip())
    
    # If text is too short, return as is
    if len(text.split()) < 20:
        return text[:200] + "..." if len(text) > 200 else text
    
    # Try using Sumy for better summarization
    if SUMY_AVAILABLE:
        try:
            parser = PlaintextParser.from_string(text, Tokenizer("english"))
            summarizer = LsaSummarizer()
            summary_sentences = summarizer(parser.document, max_sentences)
            summary = ' '.join([str(sentence) for sentence in summary_sentences])
            return summary if summary else text[:300] + "..."
        except:
            pass
    
    # Fallback to simple sentence extraction
    try:
        if NLTK_AVAILABLE:
            sentences = sent_tokenize(text)
        else:
            # Basic sentence splitting
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= max_sentences:
            return text
        
        # Take first and last sentences
        if len(sentences) >= 2:
            summary = sentences[0] + " " + sentences[-1]
        else:
            summary = sentences[0]
        
        return summary[:300] + "..." if len(summary) > 300 else summary
    
    except:
        # Final fallback
        return text[:200] + "..." if len(text) > 200 else text


def get_file_dates(file_path):
    """
    Get file creation and modification dates
    """
    try:
        stat = os.stat(file_path)
        created_date = datetime.fromtimestamp(stat.st_ctime)
        modified_date = datetime.fromtimestamp(stat.st_mtime)
        return created_date, modified_date
    except:
        return None, None


def analyze_csv_file(file_path):
    """
    Comprehensive CSV analysis including table description, attributes, and private data detection
    """
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            # Read first few lines to understand structure
            sample_lines = []
            for i, line in enumerate(f):
                if i >= 10:  # Read first 10 lines for analysis
                    break
                sample_lines.append(line.strip())
        
        if not sample_lines:
            return "", ""
        
        # Parse CSV structure
        csv_reader = csv.reader(sample_lines)
        headers = next(csv_reader) if sample_lines else []
        
        # Analyze data types and patterns
        data_analysis = analyze_csv_data_structure(file_path, headers)
        
        # Generate comprehensive summary
        summary = generate_csv_summary(file_path, headers, data_analysis)
        
        # Extract keywords from content
        keywords = extract_keywords_from_csv(file_path, headers)
        
        return keywords, summary
        
    except Exception as e:
        print(f"Error analyzing CSV file {file_path}: {e}")
        return "", f"Error analyzing CSV file: {str(e)}"


def analyze_csv_data_structure(file_path, headers):
    """
    Analyze CSV data structure, types, and patterns
    """
    analysis = {
        'total_rows': 0,
        'columns': {},
        'data_types': {},
        'sample_values': {},
        'private_data_indicators': [],
        'numeric_columns': [],
        'text_columns': [],
        'date_columns': [],
        'email_columns': [],
        'phone_columns': [],
        'id_columns': []
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            csv_reader = csv.DictReader(f)
            
            # Analyze each column
            for col in headers:
                analysis['columns'][col] = {
                    'sample_values': [],
                    'data_type': 'text',
                    'unique_count': 0,
                    'null_count': 0,
                    'private_indicators': []
                }
            
            row_count = 0
            for row in csv_reader:
                row_count += 1
                if row_count > 1000:  # Limit analysis to first 1000 rows
                    break
                
                for col in headers:
                    value = row.get(col, '').strip()
                    
                    # Collect sample values
                    if len(analysis['columns'][col]['sample_values']) < 5 and value:
                        analysis['columns'][col]['sample_values'].append(value)
                    
                    # Count nulls
                    if not value:
                        analysis['columns'][col]['null_count'] += 1
                    
                    # Detect data types
                    detect_data_type(col, value, analysis)
                    
                    # Detect private data
                    detect_private_data(col, value, analysis)
            
            analysis['total_rows'] = row_count
            
    except Exception as e:
        print(f"Error analyzing CSV structure: {e}")
    
    return analysis


def detect_data_type(column_name, value, analysis):
    """
    Detect data type for a column based on sample values
    """
    if not value:
        return
    
    col_lower = column_name.lower()
    
    # Check for numeric data
    if re.match(r'^-?\d+\.?\d*$', value):
        if col_lower in ['price', 'amount', 'cost', 'total', 'sum', 'value', 'salary', 'income']:
            analysis['numeric_columns'].append(column_name)
            analysis['columns'][column_name]['data_type'] = 'currency'
        else:
            analysis['numeric_columns'].append(column_name)
            analysis['columns'][column_name]['data_type'] = 'numeric'
    
    # Check for dates
    elif re.match(r'\d{4}-\d{2}-\d{2}|\d{2}/\d{2}/\d{4}|\d{2}-\d{2}-\d{4}', value):
        analysis['date_columns'].append(column_name)
        analysis['columns'][column_name]['data_type'] = 'date'
    
    # Check for emails
    elif re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
        analysis['email_columns'].append(column_name)
        analysis['columns'][column_name]['data_type'] = 'email'
    
    # Check for phone numbers
    elif re.match(r'[\+]?[1-9]?[0-9]{7,15}$', re.sub(r'[^\d+]', '', value)):
        analysis['phone_columns'].append(column_name)
        analysis['columns'][column_name]['data_type'] = 'phone'
    
    # Check for IDs
    elif col_lower in ['id', 'customer_id', 'user_id', 'order_id', 'product_id']:
        analysis['id_columns'].append(column_name)
        analysis['columns'][column_name]['data_type'] = 'id'
    
    else:
        analysis['text_columns'].append(column_name)
        analysis['columns'][column_name]['data_type'] = 'text'


def detect_private_data(column_name, value, analysis):
    """
    Detect potentially private or sensitive data
    """
    if not value:
        return
    
    col_lower = column_name.lower()
    value_lower = value.lower()
    
    # Common private data indicators
    private_indicators = {
        'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'phone': r'[\+]?[1-9]?[0-9]{7,15}',
        'ssn': r'\d{3}-\d{2}-\d{4}',
        'credit_card': r'\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}',
        'address': r'\d+\s+[a-zA-Z\s]+(?:street|st|avenue|ave|road|rd|boulevard|blvd|drive|dr|lane|ln)',
        'zip_code': r'\d{5}(?:-\d{4})?',
        'name': r'^[A-Z][a-z]+\s+[A-Z][a-z]+$'
    }
    
    # Check column name patterns
    sensitive_columns = ['name', 'email', 'phone', 'address', 'ssn', 'social', 'credit', 'card', 'password', 'pin', 'dob', 'birth', 'age', 'salary', 'income', 'ssn', 'tax', 'id']
    
    for indicator in sensitive_columns:
        if indicator in col_lower:
            analysis['private_data_indicators'].append(f"Column '{column_name}' may contain {indicator} data")
            analysis['columns'][column_name]['private_indicators'].append(indicator)
    
    # Check value patterns
    for pattern_name, pattern in private_indicators.items():
        if re.search(pattern, value):
            analysis['private_data_indicators'].append(f"Value in column '{column_name}' matches {pattern_name} pattern")
            analysis['columns'][column_name]['private_indicators'].append(pattern_name)


def extract_keywords_from_csv(file_path, headers):
    """
    Extract keywords from CSV content
    """
    keywords = []
    
    # Add column names as keywords
    keywords.extend([col.lower().replace('_', ' ') for col in headers])
    
    # Add common data analysis terms
    keywords.extend(['data', 'table', 'dataset', 'records', 'information'])
    
    # Analyze content for additional keywords
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            content_keywords = extract_keywords(content, max_keywords=5)
            if content_keywords:
                keywords.extend(content_keywords.split(', '))
    except:
        pass
    
    return ', '.join(list(set(keywords))[:10])


def generate_csv_summary(file_path, headers, analysis):
    """
    Generate concise summary with PII detection for CSV file
    """
    filename = Path(file_path).stem
    owner = extract_owner_from_filename(filename)
    
    summary_parts = []
    
    # High-level one-line summary
    table_purpose = infer_table_purpose(headers, analysis)
    pii_columns = get_pii_columns(headers, analysis)
    pii_status = f" (Contains PII: {', '.join(pii_columns)})" if pii_columns else " (No PII detected)"
    
    summary_parts.append(f"📊 **{Path(file_path).name}** - {table_purpose} dataset with {analysis['total_rows']:,} records{pii_status}")
    
    # Basic information
    summary_parts.append(f"\n**File Details:**")
    summary_parts.append(f"• **Owner:** {owner}")
    summary_parts.append(f"• **Total Records:** {analysis['total_rows']:,}")
    summary_parts.append(f"• **Total Fields:** {len(headers)}")
    
    # PII Analysis
    summary_parts.append(f"\n**🔒 PII (Personal Identifiable Information) Analysis:**")
    if pii_columns:
        summary_parts.append(f"⚠️ **PII COLUMNS DETECTED:** {', '.join(pii_columns)}")
        summary_parts.append("These columns contain personal information that requires special handling and privacy protection.")
    else:
        summary_parts.append("✅ **No PII columns detected** - Safe for general business use")
    
    # Column analysis with PII indicators
    summary_parts.append(f"\n**📈 Column Analysis:**")
    for col in headers:
        col_info = analysis['columns'][col]
        data_type = col_info['data_type']
        sample_values = col_info['sample_values'][:3]
        is_pii = col in pii_columns
        pii_indicator = " 🔒 PII" if is_pii else ""
        
        summary_parts.append(f"• **{col}** ({data_type}){pii_indicator}: {', '.join(sample_values) if sample_values else 'No data'}")
    
    # Data type summary
    if analysis['numeric_columns']:
        summary_parts.append(f"\n**🔢 Numeric Columns:** {', '.join(set(analysis['numeric_columns']))}")
    if analysis['date_columns']:
        summary_parts.append(f"**📅 Date Columns:** {', '.join(set(analysis['date_columns']))}")
    if analysis['email_columns']:
        summary_parts.append(f"**📧 Email Columns:** {', '.join(set(analysis['email_columns']))}")
    if analysis['phone_columns']:
        summary_parts.append(f"**📞 Phone Columns:** {', '.join(set(analysis['phone_columns']))}")
    
    # Data quality insights
    summary_parts.append(f"\n**📊 Data Quality:**")
    quality_issues = []
    for col in headers:
        col_info = analysis['columns'][col]
        null_percentage = (col_info['null_count'] / analysis['total_rows']) * 100 if analysis['total_rows'] > 0 else 0
        if null_percentage > 10:
            quality_issues.append(f"• **{col}**: {null_percentage:.1f}% missing values")
    
    if quality_issues:
        summary_parts.append("⚠️ **Data Quality Issues:**")
        for issue in quality_issues:
            summary_parts.append(issue)
    else:
        summary_parts.append("✅ **Data Quality: Excellent** - All fields have complete data")
    
    return '\n'.join(summary_parts)


def infer_table_purpose(headers, analysis):
    """
    Infer the purpose of the table based on column names and data
    """
    col_lower = [col.lower() for col in headers]
    
    # Common table types
    if any(word in ' '.join(col_lower) for word in ['customer', 'client', 'user', 'person']):
        if any(word in ' '.join(col_lower) for word in ['order', 'purchase', 'transaction']):
            return "customer transaction/order"
        else:
            return "customer/user information"
    
    elif any(word in ' '.join(col_lower) for word in ['product', 'item', 'inventory']):
        return "product/inventory"
    
    elif any(word in ' '.join(col_lower) for word in ['sale', 'revenue', 'income', 'financial']):
        return "sales/financial"
    
    elif any(word in ' '.join(col_lower) for word in ['employee', 'staff', 'worker', 'hr']):
        return "employee/human resources"
    
    elif any(word in ' '.join(col_lower) for word in ['feedback', 'review', 'rating', 'survey']):
        return "feedback/survey"
    
    elif any(word in ' '.join(col_lower) for word in ['log', 'event', 'activity', 'tracking']):
        return "activity/log"
    
    else:
        return "general data"


def extract_owner_from_filename(filename):
    """
    Extract owner name from filename
    """
    parts = filename.split('_')
    if len(parts) > 1:
        return parts[0].title()
    return "Unknown"


def analyze_text_file(file_path):
    """
    Complete text analysis for a file with enhanced summaries
    """
    file_ext = Path(file_path).suffix.lower()
    
    # Special handling for CSV files
    if file_ext == '.csv':
        return analyze_csv_file(file_path)
    
    # Extract text
    text = extract_text_from_file(file_path)
    
    if not text:
        return "", ""
    
    # Extract keywords
    keywords = extract_keywords(text)
    
    # Generate enhanced summary
    summary = generate_enhanced_summary(file_path, text)
    
    return keywords, summary


def generate_enhanced_summary(file_path, text):
    """
    Generate enhanced summary with file-specific insights
    """
    filename = Path(file_path).name
    file_ext = Path(file_path).suffix.lower()
    owner = extract_owner_from_filename(Path(file_path).stem)
    
    summary_parts = []
    
    # File information
    summary_parts.append(f"📄 **File Analysis Report**")
    summary_parts.append(f"**File:** {filename}")
    summary_parts.append(f"**Owner:** {owner}")
    summary_parts.append(f"**Type:** {get_file_type_description(file_ext)}")
    summary_parts.append(f"**Size:** {len(text)} characters")
    
    # Content analysis
    word_count = len(text.split())
    line_count = len(text.splitlines())
    
    summary_parts.append(f"\n**📊 Content Statistics:**")
    summary_parts.append(f"• Words: {word_count}")
    summary_parts.append(f"• Lines: {line_count}")
    summary_parts.append(f"• Characters: {len(text)}")
    
    # Content description
    summary_parts.append(f"\n**📝 Content Description:**")
    if file_ext == '.py':
        summary_parts.append("This is a Python script file containing code and programming logic.")
    elif file_ext == '.js':
        summary_parts.append("This is a JavaScript file containing web application code.")
    elif file_ext == '.html':
        summary_parts.append("This is an HTML file containing web page structure and content.")
    elif file_ext == '.css':
        summary_parts.append("This is a CSS file containing styling and design rules.")
    elif file_ext == '.sql':
        summary_parts.append("This is an SQL file containing database schema and queries.")
    elif file_ext == '.cpp':
        summary_parts.append("This is a C++ source code file containing programming logic.")
    elif file_ext == '.txt':
        summary_parts.append("This is a text file containing written content and information.")
    else:
        summary_parts.append("This is a text-based file containing structured or unstructured data.")
    
    # Generate content summary
    content_summary = generate_summary(text)
    if content_summary:
        summary_parts.append(f"\n**📖 Content Summary:**")
        summary_parts.append(content_summary)
    
    return '\n'.join(summary_parts)


def get_file_type_description(file_ext):
    """
    Get human-readable description of file type
    """
    descriptions = {
        '.txt': 'Text Document',
        '.py': 'Python Script',
        '.js': 'JavaScript File',
        '.html': 'HTML Document',
        '.css': 'CSS Stylesheet',
        '.sql': 'SQL Database File',
        '.cpp': 'C++ Source Code',
        '.csv': 'CSV Data File',
        '.json': 'JSON Data File',
        '.xml': 'XML Document',
        '.md': 'Markdown Document'
    }
    return descriptions.get(file_ext, 'Unknown File Type')


def get_detailed_table_context(headers, analysis):
    """
    Get detailed context about what the table contains
    """
    col_lower = [col.lower() for col in headers]
    context_parts = []
    
    if any(word in ' '.join(col_lower) for word in ['customer', 'client', 'user']):
        context_parts.append("customer information and interactions")
    
    if any(word in ' '.join(col_lower) for word in ['product', 'item', 'inventory']):
        context_parts.append("product details and inventory management")
    
    if any(word in ' '.join(col_lower) for word in ['sale', 'purchase', 'order', 'transaction']):
        context_parts.append("sales transactions and financial records")
    
    if any(word in ' '.join(col_lower) for word in ['feedback', 'review', 'rating', 'survey']):
        context_parts.append("customer feedback and satisfaction metrics")
    
    if any(word in ' '.join(col_lower) for word in ['date', 'time', 'created', 'updated']):
        context_parts.append("temporal tracking and historical data")
    
    if any(word in ' '.join(col_lower) for word in ['region', 'location', 'address', 'city']):
        context_parts.append("geographical and location-based information")
    
    return " and ".join(context_parts) if context_parts else "business operations and data management"


def generate_business_context(headers, analysis):
    """
    Generate business context for the dataset
    """
    col_lower = [col.lower() for col in headers]
    context_parts = []
    
    # Determine business domain
    if any(word in ' '.join(col_lower) for word in ['customer', 'client', 'user', 'person']):
        if any(word in ' '.join(col_lower) for word in ['order', 'purchase', 'transaction', 'sale']):
            context_parts.append("This dataset appears to be from an e-commerce or retail business, tracking customer purchases and transactions.")
        else:
            context_parts.append("This dataset appears to be a customer relationship management (CRM) system, storing customer information and profiles.")
    
    elif any(word in ' '.join(col_lower) for word in ['product', 'item', 'inventory', 'stock']):
        context_parts.append("This dataset appears to be an inventory management system, tracking product information and stock levels.")
    
    elif any(word in ' '.join(col_lower) for word in ['feedback', 'review', 'rating', 'survey']):
        context_parts.append("This dataset appears to be a customer feedback system, collecting and analyzing customer opinions and satisfaction ratings.")
    
    elif any(word in ' '.join(col_lower) for word in ['employee', 'staff', 'worker', 'hr']):
        context_parts.append("This dataset appears to be a human resources system, managing employee information and records.")
    
    else:
        context_parts.append("This dataset appears to be a general business data collection, storing various types of operational information.")
    
    # Add data volume context
    if analysis['total_rows'] < 100:
        context_parts.append("The dataset is relatively small, suggesting it may be a sample, test data, or a specific subset of a larger system.")
    elif analysis['total_rows'] < 1000:
        context_parts.append("The dataset is of moderate size, likely representing a specific time period or business segment.")
    else:
        context_parts.append("The dataset contains a substantial amount of data, suggesting it represents a significant portion of business operations.")
    
    return " ".join(context_parts)


def get_detailed_data_type_description(data_type):
    """
    Get detailed description of data type
    """
    descriptions = {
        'text': 'Text/String - Contains written information and descriptions',
        'numeric': 'Numeric - Contains numbers that can be used for calculations',
        'currency': 'Currency - Contains monetary values and financial amounts',
        'date': 'Date/Time - Contains temporal information and timestamps',
        'email': 'Email Address - Contains electronic mail contact information',
        'phone': 'Phone Number - Contains telephone contact information',
        'id': 'Identifier - Contains unique reference numbers or codes',
        'boolean': 'True/False - Contains binary yes/no or true/false values'
    }
    return descriptions.get(data_type, f'{data_type.title()} - Contains {data_type} data')


def get_field_purpose(column_name, data_type, sample_values):
    """
    Generate human-readable purpose description for a field
    """
    col_lower = column_name.lower()
    
    # Common field purposes based on column names
    if 'id' in col_lower:
        return "This field serves as a unique identifier to distinguish each record from others in the dataset."
    
    elif 'name' in col_lower:
        if 'customer' in col_lower or 'client' in col_lower:
            return "This field stores the full name of customers or clients in the system."
        elif 'product' in col_lower:
            return "This field contains the name or title of products or items."
        else:
            return "This field stores names or titles of entities referenced in the data."
    
    elif 'email' in col_lower:
        return "This field contains email addresses for communication and contact purposes."
    
    elif 'phone' in col_lower:
        return "This field stores phone numbers for direct communication with customers or contacts."
    
    elif 'date' in col_lower or 'time' in col_lower:
        return "This field tracks when events occurred or when records were created/modified."
    
    elif 'price' in col_lower or 'amount' in col_lower or 'cost' in col_lower:
        return "This field contains monetary values representing prices, costs, or financial amounts."
    
    elif 'quantity' in col_lower or 'count' in col_lower:
        return "This field stores numerical counts or quantities of items or occurrences."
    
    elif 'category' in col_lower or 'type' in col_lower:
        return "This field categorizes or classifies records into different groups or types."
    
    elif 'rating' in col_lower or 'score' in col_lower:
        return "This field contains numerical ratings or scores used for evaluation purposes."
    
    elif 'region' in col_lower or 'location' in col_lower:
        return "This field specifies geographical or organizational locations or regions."
    
    elif 'status' in col_lower or 'state' in col_lower:
        return "This field indicates the current status or condition of records or processes."
    
    else:
        # Generic purpose based on data type
        if data_type == 'currency':
            return "This field contains financial or monetary values for business calculations."
        elif data_type == 'date':
            return "This field tracks temporal information and can be used for time-based analysis."
        elif data_type == 'email':
            return "This field contains contact information for communication purposes."
        elif data_type == 'phone':
            return "This field stores contact information for direct communication."
        elif data_type == 'id':
            return "This field serves as a unique reference identifier for the record."
        else:
            return "This field contains descriptive or categorical information relevant to the business process."


def generate_relationship_analysis(headers, analysis):
    """
    Generate analysis of relationships between fields
    """
    relationships = []
    
    # Look for common relationship patterns
    id_fields = [col for col in headers if 'id' in col.lower()]
    name_fields = [col for col in headers if 'name' in col.lower()]
    date_fields = [col for col in headers if 'date' in col.lower() or 'time' in col.lower()]
    price_fields = [col for col in headers if any(word in col.lower() for word in ['price', 'amount', 'cost', 'total'])]
    
    if len(id_fields) > 1:
        relationships.append(f"• **Multiple Identifiers:** Found {len(id_fields)} ID fields ({', '.join(id_fields)}) - these likely represent different types of references or hierarchical relationships.")
    
    if name_fields and id_fields:
        relationships.append(f"• **Name-ID Pairs:** The dataset contains both identifier fields ({', '.join(id_fields)}) and name fields ({', '.join(name_fields)}) - this suggests a normalized data structure where IDs reference detailed information.")
    
    if price_fields and 'quantity' in [col.lower() for col in headers]:
        relationships.append(f"• **Financial Calculations:** The dataset contains both price fields ({', '.join(price_fields)}) and quantity information - this enables calculation of totals, revenue, and financial metrics.")
    
    if date_fields:
        relationships.append(f"• **Temporal Tracking:** Found {len(date_fields)} date/time fields ({', '.join(date_fields)}) - this enables time-series analysis and chronological tracking of events.")
    
    # Look for foreign key relationships
    if 'customer_id' in [col.lower() for col in headers] and 'customer' in [col.lower() for col in headers]:
        relationships.append(f"• **Customer Relationships:** The dataset links to customer information through customer ID references, enabling customer-specific analysis and reporting.")
    
    if 'product_id' in [col.lower() for col in headers] and 'product' in [col.lower() for col in headers]:
        relationships.append(f"• **Product Relationships:** The dataset references product information through product ID fields, enabling product-specific analysis and inventory tracking.")
    
    if not relationships:
        relationships.append("• **Data Structure:** The fields appear to be independent attributes without obvious hierarchical relationships.")
        relationships.append("• **Analysis Potential:** Each field can be analyzed individually or in combination with others for business insights.")
    
    return "\n".join(relationships)


def get_pii_columns(headers, analysis):
    """
    Identify columns that contain Personal Identifiable Information (PII)
    """
    pii_columns = []
    
    # PII column name patterns - very specific to avoid false positives
    pii_patterns = [
        'customer_name', 'client_name', 'user_name', 'first_name', 'last_name', 'full_name',
        'email', 'email_address', 'e_mail',
        'phone', 'phone_number', 'telephone', 'mobile', 'cell',
        'address', 'street_address', 'home_address', 'billing_address', 'shipping_address',
        'ssn', 'social_security', 'tax_id', 'national_id',
        'credit_card', 'card_number', 'account_number',
        'dob', 'date_of_birth', 'birth_date', 'age',
        'passport', 'license', 'drivers_license',
        'ip_address', 'mac_address',
        'username', 'login', 'user_id'
    ]
    
    # Additional PII patterns that should be detected
    additional_pii_patterns = [
        'name'  # Generic name pattern
    ]
    
    # Non-PII patterns that should be excluded even if they contain names
    non_pii_patterns = [
        'product_name', 'item_name', 'service_name', 'category_name', 'product',
        'purchase_date', 'order_date', 'created_date', 'updated_date', 'date',
        'region', 'location', 'city', 'state', 'country',
        'status', 'type', 'category', 'description', 'rep', 'sales_rep'
    ]
    
    for col in headers:
        col_lower = col.lower()
        
        # Skip if it's clearly not PII
        if any(pattern in col_lower for pattern in non_pii_patterns):
            continue
            
        # Check if column name matches PII patterns
        if any(pattern in col_lower for pattern in pii_patterns):
            pii_columns.append(col)
            continue
            
        # Check additional PII patterns but exclude non-PII patterns
        if any(pattern in col_lower for pattern in additional_pii_patterns) and not any(pattern in col_lower for pattern in non_pii_patterns):
            pii_columns.append(col)
            continue
        
        # Check if column contains PII data based on sample values
        col_info = analysis['columns'].get(col, {})
        sample_values = col_info.get('sample_values', [])
        
        for value in sample_values:
            if not value:
                continue
                
            # Check for email pattern
            if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
                pii_columns.append(col)
                break
            
            # Check for phone pattern
            if re.match(r'[\+]?[1-9]?[0-9]{7,15}$', re.sub(r'[^\d+]', '', value)):
                pii_columns.append(col)
                break
            
            # Check for SSN pattern
            if re.match(r'\d{3}-\d{2}-\d{4}', value):
                pii_columns.append(col)
                break
            
            # Check for credit card pattern
            if re.match(r'\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}', value):
                pii_columns.append(col)
                break
            
            # Check for name pattern (First Last) - but only for specific column types that are clearly PII
            if re.match(r'^[A-Z][a-z]+\s+[A-Z][a-z]+$', value) and any(word in col_lower for word in ['customer_name', 'client_name', 'user_name', 'first_name', 'last_name', 'full_name', 'sales_rep', 'contact_person']):
                pii_columns.append(col)
                break
    
    return list(set(pii_columns))  # Remove duplicates


def generate_business_insights(headers, analysis):
    """
    Generate business insights and recommendations
    """
    insights = []
    
    # Data volume insights
    if analysis['total_rows'] < 100:
        insights.append("• **Data Volume:** This is a small dataset, ideal for testing, prototyping, or analyzing specific business scenarios.")
    elif analysis['total_rows'] < 10000:
        insights.append("• **Data Volume:** This is a medium-sized dataset, suitable for detailed analysis and business intelligence reporting.")
    else:
        insights.append("• **Data Volume:** This is a large dataset, requiring robust analytics tools and potentially big data processing capabilities.")
    
    # Field composition insights
    if len(analysis['numeric_columns']) > len(headers) * 0.5:
        insights.append("• **Analytical Potential:** The dataset is rich in numerical data, making it excellent for statistical analysis, trend identification, and predictive modeling.")
    
    if analysis['date_columns']:
        insights.append("• **Time Series Analysis:** With date fields present, this dataset is perfect for analyzing trends over time, seasonal patterns, and temporal business cycles.")
    
    if analysis['private_data_indicators']:
        insights.append("• **Privacy Considerations:** The dataset contains sensitive information that requires careful handling, compliance with data protection regulations, and appropriate security measures.")
    else:
        insights.append("• **Data Safety:** The dataset appears to contain non-sensitive information, making it suitable for broader sharing and analysis without privacy concerns.")
    
    # Business use case recommendations
    col_lower = [col.lower() for col in headers]
    
    if any(word in ' '.join(col_lower) for word in ['customer', 'client', 'user']):
        insights.append("• **Customer Analytics:** This dataset is ideal for customer segmentation, behavior analysis, lifetime value calculations, and personalized marketing strategies.")
    
    if any(word in ' '.join(col_lower) for word in ['product', 'item', 'inventory']):
        insights.append("• **Product Analytics:** Use this data for inventory optimization, product performance analysis, demand forecasting, and supply chain management.")
    
    if any(word in ' '.join(col_lower) for word in ['sale', 'purchase', 'transaction', 'revenue']):
        insights.append("• **Financial Analytics:** This dataset enables revenue analysis, sales forecasting, profitability calculations, and financial performance tracking.")
    
    if any(word in ' '.join(col_lower) for word in ['feedback', 'review', 'rating', 'satisfaction']):
        insights.append("• **Customer Experience:** Use this data to measure customer satisfaction, identify improvement areas, track sentiment trends, and enhance service quality.")
    
    # Data quality recommendations
    quality_score = 100
    for col in headers:
        col_info = analysis['columns'][col]
        null_percentage = (col_info['null_count'] / analysis['total_rows']) * 100 if analysis['total_rows'] > 0 else 0
        if null_percentage > 10:
            quality_score -= 20
    
    if quality_score >= 90:
        insights.append("• **Data Quality:** The dataset has excellent data quality with minimal missing values, making it highly reliable for business analysis and decision-making.")
    elif quality_score >= 70:
        insights.append("• **Data Quality:** The dataset has good data quality with some minor gaps that should be addressed before comprehensive analysis.")
    else:
        insights.append("• **Data Quality:** The dataset has significant data quality issues that need to be resolved before reliable business analysis can be performed.")
    
    return "\n".join(insights)
