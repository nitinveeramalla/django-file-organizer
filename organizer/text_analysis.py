"""
Text analysis utilities for extracting keywords and generating summaries
"""
import os
import re
from collections import Counter
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


def analyze_text_file(file_path):
    """
    Complete text analysis for a file
    """
    # Extract text
    text = extract_text_from_file(file_path)
    
    if not text:
        return "", ""
    
    # Extract keywords
    keywords = extract_keywords(text)
    
    # Generate summary
    summary = generate_summary(text)
    
    return keywords, summary
