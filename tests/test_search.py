"""
Tests for Search Engine
"""

import unittest
from markdownmind.search_engine import SemanticSearch


class TestSemanticSearch(unittest.TestCase):
    """Test cases for SemanticSearch."""
    
    def setUp(self):
        self.search = SemanticSearch()
    
    def test_build_index(self):
        """Test building search index."""
        documents = {
            "doc1.md": {
                "title": "Python Tutorial",
                "tags": ["python", "beginner"],
                "summary": "Learn Python basics",
                "headers": [{"text": "Introduction", "level": 1}],
            },
            "doc2.md": {
                "title": "JavaScript Guide",
                "tags": ["javascript", "web"],
                "summary": "JavaScript for web development",
                "headers": [{"text": "Getting Started", "level": 1}],
            },
        }
        
        self.search.build_index(documents)
        self.assertGreater(self.search.total_docs, 0)
    
    def test_search(self):
        """Test searching documents."""
        documents = {
            "doc1.md": {
                "title": "Python Tutorial",
                "tags": ["python", "programming"],
                "summary": "Learn Python programming basics",
                "headers": [{"text": "Introduction", "level": 1}],
            },
            "doc2.md": {
                "title": "JavaScript Guide",
                "tags": ["javascript", "web"],
                "summary": "JavaScript for web development",
                "headers": [{"text": "Getting Started", "level": 1}],
            },
        }
        
        self.search.build_index(documents)
        results = self.search.search("python", documents)
        
        self.assertGreater(len(results), 0)
        # Python doc should rank higher
        self.assertEqual(results[0]['path'], 'doc1.md')
    
    def test_tokenize(self):
        """Test text tokenization."""
        text = "Hello World! This is a test."
        tokens = self.search._tokenize(text)
        
        self.assertIn("hello", tokens)
        self.assertIn("world", tokens)
        self.assertIn("test", tokens)


if __name__ == '__main__':
    unittest.main()
