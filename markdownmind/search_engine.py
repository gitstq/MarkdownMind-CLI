"""
Semantic Search Engine Module
语义搜索引擎模块
"""

import re
import math
from typing import Dict, List, Tuple, Set
from collections import defaultdict, Counter


class SemanticSearch:
    """
    TF-IDF based semantic search for Markdown documents.
    基于TF-IDF的语义搜索引擎
    """
    
    def __init__(self):
        self.doc_freq: Dict[str, int] = {}  # Document frequency
        self.total_docs: int = 0
        self.stopwords: Set[str] = self._load_stopwords()
    
    def _load_stopwords(self) -> Set[str]:
        """Load common stopwords."""
        return {
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'shall',
            'can', 'need', 'dare', 'ought', 'used', 'to', 'of', 'in',
            'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
            'through', 'during', 'before', 'after', 'above', 'below',
            'between', 'under', 'and', 'but', 'or', 'yet', 'so', 'if',
            'because', 'although', 'though', 'while', 'where', 'when',
            'that', 'which', 'who', 'whom', 'whose', 'what', 'this',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'its',
            'our', 'their', '的', '了', '在', '是', '我', '有', '和',
            '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到',
            '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己',
        }
    
    def build_index(self, documents: Dict[str, Dict]):
        """
        Build search index from documents.
        
        Args:
            documents: Dictionary of document path -> document info
        """
        self.total_docs = len(documents)
        self.doc_freq = defaultdict(int)
        
        # Calculate document frequency for each term
        for path, doc in documents.items():
            # Combine title, headers, tags, and summary for indexing
            content_parts = [
                doc.get("title", ""),
                " ".join(h["text"] for h in doc.get("headers", [])),
                " ".join(doc.get("tags", [])),
                doc.get("summary", ""),
            ]
            content = " ".join(content_parts)
            
            # Get unique terms in this document
            terms = set(self._tokenize(content))
            for term in terms:
                self.doc_freq[term] += 1
    
    def search(self, query: str, documents: Dict[str, Dict], limit: int = 10) -> List[Dict]:
        """
        Search documents by query.
        
        Args:
            query: Search query
            documents: Documents to search
            limit: Maximum results
            
        Returns:
            List of matching documents with scores
        """
        if not documents or not query.strip():
            return []
        
        query_terms = self._tokenize(query)
        if not query_terms:
            return []
        
        # Calculate TF-IDF scores
        scores = {}
        for path, doc in documents.items():
            score = self._calculate_score(query_terms, doc)
            if score > 0:
                scores[path] = score
        
        # Sort by score
        sorted_results = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        
        # Format results
        results = []
        for path, score in sorted_results:
            doc = documents[path]
            results.append({
                "path": path,
                "title": doc.get("title", path),
                "summary": doc.get("summary", "")[:200],
                "score": round(score, 4),
                "tags": doc.get("tags", [])[:5],
            })
        
        return results
    
    def _tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into terms.
        
        Args:
            text: Input text
            
        Returns:
            List of tokens
        """
        # Convert to lowercase
        text = text.lower()
        
        # Extract words (including Chinese characters)
        # English words
        words = re.findall(r'[a-z]+', text)
        # Chinese characters
        chinese = re.findall(r'[\u4e00-\u9fff]', text)
        
        tokens = words + chinese
        
        # Filter stopwords and short tokens
        tokens = [t for t in tokens if t not in self.stopwords and len(t) > 1]
        
        return tokens
    
    def _calculate_score(self, query_terms: List[str], doc: Dict) -> float:
        """
        Calculate TF-IDF score for document.
        
        Args:
            query_terms: Tokenized query
            doc: Document info
            
        Returns:
            Relevance score
        """
        # Prepare document content
        content_parts = [
            doc.get("title", ""),
            " ".join(h["text"] for h in doc.get("headers", [])),
            " ".join(doc.get("tags", [])),
            doc.get("summary", ""),
        ]
        content = " ".join(content_parts).lower()
        
        doc_terms = self._tokenize(content)
        doc_counter = Counter(doc_terms)
        
        score = 0.0
        for term in query_terms:
            # Term frequency
            tf = doc_counter.get(term, 0)
            if tf == 0:
                continue
            
            # Inverse document frequency
            df = self.doc_freq.get(term, 1)
            idf = math.log(self.total_docs / df) if df > 0 else 0
            
            # TF-IDF with normalization
            tf_normalized = 1 + math.log(tf) if tf > 0 else 0
            score += tf_normalized * idf
            
            # Boost for exact title match
            if term in doc.get("title", "").lower():
                score *= 2.0
            
            # Boost for tag match
            if term in [t.lower() for t in doc.get("tags", [])]:
                score *= 1.5
        
        return score
    
    def suggest(self, partial: str, documents: Dict[str, Dict], limit: int = 5) -> List[str]:
        """
        Provide search suggestions based on partial input.
        
        Args:
            partial: Partial search term
            documents: Documents to search
            limit: Maximum suggestions
            
        Returns:
            List of suggestions
        """
        if not partial or len(partial) < 2:
            return []
        
        partial_lower = partial.lower()
        suggestions = set()
        
        # Collect from titles
        for doc in documents.values():
            title = doc.get("title", "")
            if partial_lower in title.lower():
                suggestions.add(title)
            
            # Collect from tags
            for tag in doc.get("tags", []):
                if partial_lower in tag.lower():
                    suggestions.add(tag)
        
        return list(suggestions)[:limit]
    
    def find_similar(self, doc_path: str, documents: Dict[str, Dict], limit: int = 5) -> List[Dict]:
        """
        Find documents similar to a given document.
        
        Args:
            doc_path: Path of reference document
            documents: All documents
            limit: Maximum results
            
        Returns:
            List of similar documents
        """
        if doc_path not in documents:
            return []
        
        doc = documents[doc_path]
        
        # Build query from document
        query_parts = [
            doc.get("title", ""),
            " ".join(doc.get("tags", [])),
        ]
        query = " ".join(query_parts)
        
        results = self.search(query, documents, limit + 1)
        
        # Remove the reference document itself
        return [r for r in results if r["path"] != doc_path][:limit]
