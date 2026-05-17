"""
Tests for Markdown Parser
"""

import unittest
from pathlib import Path
import tempfile
import os

from markdownmind.parser import MarkdownParser


class TestMarkdownParser(unittest.TestCase):
    """Test cases for MarkdownParser."""
    
    def setUp(self):
        self.parser = MarkdownParser()
    
    def test_parse_simple_document(self):
        """Test parsing a simple markdown document."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write("# Test Document\n\nThis is a test.\n")
            temp_path = f.name
        
        try:
            result = self.parser.parse(Path(temp_path), Path(temp_path).parent)
            self.assertEqual(result['title'], 'Test Document')
            self.assertGreater(result['word_count'], 0)
        finally:
            os.unlink(temp_path)
    
    def test_extract_front_matter(self):
        """Test YAML front matter extraction."""
        content = """---
title: My Title
tags: [test, markdown]
---

# Content
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            temp_path = f.name
        
        try:
            result = self.parser.parse(Path(temp_path), Path(temp_path).parent)
            self.assertEqual(result['front_matter']['title'], 'My Title')
            self.assertEqual(result['title'], 'My Title')
        finally:
            os.unlink(temp_path)
    
    def test_extract_tags(self):
        """Test tag extraction."""
        content = "# Title\n\nThis is #important and #urgent."
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            temp_path = f.name
        
        try:
            result = self.parser.parse(Path(temp_path), Path(temp_path).parent)
            self.assertIn('important', result['tags'])
            self.assertIn('urgent', result['tags'])
        finally:
            os.unlink(temp_path)
    
    def test_extract_links(self):
        """Test link extraction."""
        content = "# Title\n\n[Link](https://example.com) and [Internal](./other.md)"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            temp_path = f.name
        
        try:
            result = self.parser.parse(Path(temp_path), Path(temp_path).parent)
            self.assertEqual(len(result['links']), 2)
        finally:
            os.unlink(temp_path)
    
    def test_extract_wikilinks(self):
        """Test wiki-style link extraction."""
        content = "# Title\n\nSee [[Other Page]] and [[Target|Display Text]]"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            temp_path = f.name
        
        try:
            result = self.parser.parse(Path(temp_path), Path(temp_path).parent)
            self.assertEqual(len(result['wikilinks']), 2)
        finally:
            os.unlink(temp_path)


if __name__ == '__main__':
    unittest.main()
