"""
Utility Functions
工具函数模块
"""

import hashlib
from pathlib import Path
from typing import Union


def get_file_hash(file_path: Union[str, Path], algorithm: str = "md5") -> str:
    """
    Calculate file hash.
    计算文件哈希值
    
    Args:
        file_path: Path to file
        algorithm: Hash algorithm (md5, sha256)
        
    Returns:
        Hash string
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        return ""
    
    hasher = hashlib.md5() if algorithm == "md5" else hashlib.sha256()
    
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    
    return hasher.hexdigest()[:16]


def format_file_size(size_bytes: int) -> str:
    """
    Format file size to human readable.
    格式化文件大小为人类可读格式
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string
    """
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    Truncate text to maximum length.
    截断文本到最大长度
    
    Args:
        text: Input text
        max_length: Maximum length
        suffix: Suffix for truncated text
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)].rsplit(' ', 1)[0] + suffix


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters.
    清理文件名中的非法字符
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    import re
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip(' .')
    # Ensure not empty
    if not sanitized:
        sanitized = "untitled"
    return sanitized


def count_words(text: str) -> int:
    """
    Count words in text (supports English and Chinese).
    统计文本字数（支持中英文）
    
    Args:
        text: Input text
        
    Returns:
        Word count
    """
    import re
    
    # Count English words
    english_words = len(re.findall(r'\b[a-zA-Z]+\b', text))
    
    # Count Chinese characters
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', text))
    
    return english_words + chinese_chars


def highlight_text(text: str, query: str) -> str:
    """
    Highlight query terms in text.
    高亮文本中的查询词
    
    Args:
        text: Original text
        query: Query terms to highlight
        
    Returns:
        Highlighted text
    """
    import re
    
    if not query:
        return text
    
    terms = query.lower().split()
    highlighted = text
    
    for term in terms:
        if len(term) < 2:
            continue
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        highlighted = pattern.sub(f"\033[1;33m{term}\033[0m", highlighted)
    
    return highlighted


def pluralize(count: int, singular: str, plural: str = None) -> str:
    """
    Return singular or plural form based on count.
    根据数量返回单数或复数形式
    
    Args:
        count: Number
        singular: Singular form
        plural: Plural form (default: singular + 's')
        
    Returns:
        Appropriate form
    """
    if plural is None:
        plural = singular + 's'
    
    return f"{count} {singular if count == 1 else plural}"
