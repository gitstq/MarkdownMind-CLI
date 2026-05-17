"""
Tests for Knowledge Graph
"""

import unittest
from markdownmind.knowledge_graph import KnowledgeGraph


class TestKnowledgeGraph(unittest.TestCase):
    """Test cases for KnowledgeGraph."""
    
    def setUp(self):
        self.kg = KnowledgeGraph()
    
    def test_build_from_documents(self):
        """Test building graph from documents."""
        documents = {
            "doc1.md": {
                "title": "Document 1",
                "tags": ["python", "tutorial"],
                "links": [{"url": "doc2.md", "type": "internal", "text": "Doc 2"}],
                "wikilinks": [],
                "word_count": 100,
            },
            "doc2.md": {
                "title": "Document 2",
                "tags": ["python", "advanced"],
                "links": [],
                "wikilinks": [],
                "word_count": 200,
            },
        }
        
        self.kg.build_from_documents(documents)
        
        self.assertEqual(len(self.kg.nodes), 2)
        self.assertEqual(len(self.kg.get_all_tags()), 3)
    
    def test_find_related(self):
        """Test finding related documents."""
        documents = {
            "doc1.md": {
                "title": "Document 1",
                "tags": ["python"],
                "links": [{"url": "doc2.md", "type": "internal", "text": "Doc 2"}],
                "wikilinks": [],
                "word_count": 100,
            },
            "doc2.md": {
                "title": "Document 2",
                "tags": ["python"],
                "links": [],
                "wikilinks": [],
                "word_count": 200,
            },
            "doc3.md": {
                "title": "Document 3",
                "tags": ["javascript"],
                "links": [],
                "wikilinks": [],
                "word_count": 150,
            },
        }
        
        self.kg.build_from_documents(documents)
        related = self.kg.find_related("doc1.md")
        
        # Should find doc2 (linked + shared tag)
        self.assertTrue(any(r['path'] == 'doc2.md' for r in related))
    
    def test_find_orphaned_docs(self):
        """Test finding orphaned documents."""
        documents = {
            "doc1.md": {
                "title": "Document 1",
                "tags": [],
                "links": [{"url": "doc2.md", "type": "internal", "text": "Doc 2"}],
                "wikilinks": [],
                "word_count": 100,
            },
            "doc2.md": {
                "title": "Document 2",
                "tags": [],
                "links": [],
                "wikilinks": [],
                "word_count": 200,
            },
            "orphan.md": {
                "title": "Orphan",
                "tags": [],
                "links": [],
                "wikilinks": [],
                "word_count": 50,
            },
        }
        
        self.kg.build_from_documents(documents)
        orphans = self.kg.find_orphaned_docs()
        
        self.assertIn("orphan.md", orphans)


if __name__ == '__main__':
    unittest.main()
