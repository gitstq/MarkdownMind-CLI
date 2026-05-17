"""
Markdown Parser Module
Markdown解析模块
"""

import re
from pathlib import Path
from typing import Dict, List, Set, Optional
from datetime import datetime


class MarkdownParser:
    """
    Parse Markdown files and extract metadata, content, and relationships.
    解析Markdown文件，提取元数据、内容和关系
    """
    
    # Regex patterns
    YAML_FRONT_MATTER = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)
    HEADER_PATTERN = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
    LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    WIKILINK_PATTERN = re.compile(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]')
    TAG_PATTERN = re.compile(r'#([a-zA-Z0-9_\-\u4e00-\u9fff]+)')
    CODE_BLOCK_PATTERN = re.compile(r'```[\w]*\n(.*?)```', re.DOTALL)
    INLINE_CODE_PATTERN = re.compile(r'`([^`]+)`')
    
    def __init__(self):
        self.stats = {
            "parsed": 0,
            "errors": 0,
        }
    
    def parse(self, file_path: Path, vault_path: Path) -> Dict:
        """
        Parse a Markdown file.
        
        Args:
            file_path: Path to the Markdown file
            vault_path: Root path of the vault
            
        Returns:
            Document information dictionary
        """
        rel_path = str(file_path.relative_to(vault_path))
        
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            raise ValueError(f"Cannot read file: {e}")
        
        # Extract front matter
        front_matter = self._extract_front_matter(content)
        body = self._remove_front_matter(content)
        
        # Extract components
        headers = self._extract_headers(body)
        links = self._extract_links(body, rel_path)
        wikilinks = self._extract_wikilinks(body)
        tags = self._extract_tags(body, front_matter)
        code_blocks = self._extract_code_blocks(body)
        
        # Calculate statistics
        word_count = len(re.findall(r'\b\w+\b', body))
        line_count = len(body.split('\n'))
        
        doc_info = {
            "path": rel_path,
            "title": self._extract_title(body, front_matter, file_path),
            "front_matter": front_matter,
            "headers": headers,
            "links": links,
            "wikilinks": wikilinks,
            "tags": list(tags),
            "code_blocks": code_blocks,
            "word_count": word_count,
            "line_count": line_count,
            "size": file_path.stat().st_size,
            "modified_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            "summary": self._generate_summary(body),
        }
        
        self.stats["parsed"] += 1
        return doc_info
    
    def _extract_front_matter(self, content: str) -> Dict:
        """Extract YAML front matter."""
        match = self.YAML_FRONT_MATTER.match(content)
        if match:
            yaml_content = match.group(1)
            return self._parse_yaml(yaml_content)
        return {}
    
    def _parse_yaml(self, yaml_content: str) -> Dict:
        """Simple YAML parser for front matter."""
        result = {}
        current_key = None
        current_list = []
        
        for line in yaml_content.split('\n'):
            line = line.rstrip()
            if not line or line.startswith('#'):
                continue
            
            # List item
            if line.strip().startswith('- '):
                value = line.strip()[2:].strip()
                if current_key:
                    current_list.append(value)
            else:
                # Save previous list
                if current_key and current_list:
                    result[current_key] = current_list
                    current_list = []
                
                # Parse key: value
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if value:
                        # Try to parse as number or boolean
                        if value.lower() == 'true':
                            result[key] = True
                        elif value.lower() == 'false':
                            result[key] = False
                        elif value.isdigit():
                            result[key] = int(value)
                        elif value.startswith('[') and value.endswith(']'):
                            # Array inline
                            result[key] = [v.strip().strip('"\'') for v in value[1:-1].split(',')]
                        else:
                            result[key] = value.strip('"\'')
                    else:
                        current_key = key
        
        # Save last list
        if current_key and current_list:
            result[current_key] = current_list
        
        return result
    
    def _remove_front_matter(self, content: str) -> str:
        """Remove YAML front matter from content."""
        match = self.YAML_FRONT_MATTER.match(content)
        if match:
            return content[match.end():]
        return content
    
    def _extract_headers(self, content: str) -> List[Dict]:
        """Extract headers with levels."""
        headers = []
        for match in self.HEADER_PATTERN.finditer(content):
            level = len(match.group(1))
            text = match.group(2).strip()
            headers.append({
                "level": level,
                "text": text,
            })
        return headers
    
    def _extract_links(self, content: str, doc_path: str) -> List[Dict]:
        """Extract markdown links."""
        links = []
        for match in self.LINK_PATTERN.finditer(content):
            text = match.group(1)
            url = match.group(2)
            
            # Determine link type
            link_type = "external"
            if url.startswith('#'):
                link_type = "anchor"
            elif not url.startswith(('http://', 'https://', 'mailto:')):
                link_type = "internal"
            
            links.append({
                "text": text,
                "url": url,
                "type": link_type,
            })
        return links
    
    def _extract_wikilinks(self, content: str) -> List[Dict]:
        """Extract wiki-style links [[target|alias]]."""
        links = []
        for match in self.WIKILINK_PATTERN.finditer(content):
            target = match.group(1).strip()
            alias = match.group(2).strip() if match.group(2) else target
            links.append({
                "target": target,
                "alias": alias,
            })
        return links
    
    def _extract_tags(self, content: str, front_matter: Dict) -> Set[str]:
        """Extract tags from content and front matter."""
        tags = set()
        
        # From front matter
        if 'tags' in front_matter:
            fm_tags = front_matter['tags']
            if isinstance(fm_tags, list):
                tags.update(fm_tags)
            else:
                tags.add(str(fm_tags))
        
        # From content (exclude code blocks)
        content_no_code = self.CODE_BLOCK_PATTERN.sub('', content)
        for match in self.TAG_PATTERN.finditer(content_no_code):
            tag = match.group(1)
            if not tag.isdigit():  # Exclude pure numbers
                tags.add(tag)
        
        return tags
    
    def _extract_code_blocks(self, content: str) -> List[Dict]:
        """Extract code blocks with language info."""
        blocks = []
        pattern = re.compile(r'```(\w*)\n(.*?)```', re.DOTALL)
        for match in pattern.finditer(content):
            language = match.group(1) or "text"
            code = match.group(2)
            blocks.append({
                "language": language,
                "lines": len(code.split('\n')),
            })
        return blocks
    
    def _extract_title(self, content: str, front_matter: Dict, file_path: Path) -> str:
        """Extract document title."""
        # From front matter
        if 'title' in front_matter:
            return front_matter['title']
        
        # From first H1
        match = self.HEADER_PATTERN.search(content)
        if match and len(match.group(1)) == 1:
            return match.group(2).strip()
        
        # From filename
        return file_path.stem.replace('-', ' ').replace('_', ' ').title()
    
    def _generate_summary(self, content: str, max_length: int = 200) -> str:
        """Generate document summary."""
        # Remove code blocks
        text = self.CODE_BLOCK_PATTERN.sub('', content)
        # Remove inline code
        text = self.INLINE_CODE_PATTERN.sub('', text)
        # Remove headers
        text = self.HEADER_PATTERN.sub('', text)
        # Remove links
        text = self.LINK_PATTERN.sub(r'\1', text)
        # Remove wikilinks
        text = self.WIKILINK_PATTERN.sub(r'\1', text)
        
        # Clean up
        text = re.sub(r'\s+', ' ', text).strip()
        
        if len(text) > max_length:
            text = text[:max_length].rsplit(' ', 1)[0] + '...'
        
        return text
