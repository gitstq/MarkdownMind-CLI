"""
MarkdownMind Core Engine
核心引擎模块
"""

import os
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple
from datetime import datetime

from .parser import MarkdownParser
from .knowledge_graph import KnowledgeGraph
from .search_engine import SemanticSearch
from .utils import get_file_hash, format_file_size


class MarkdownMind:
    """
    Main entry point for MarkdownMind functionality.
    主入口类，整合所有功能模块
    """
    
    def __init__(self, vault_path: str, index_path: Optional[str] = None):
        """
        Initialize MarkdownMind instance.
        
        Args:
            vault_path: Path to Markdown vault/directory
            index_path: Path to store index files (default: .markdownmind in vault)
        """
        self.vault_path = Path(vault_path).expanduser().resolve()
        self.index_path = Path(index_path) if index_path else self.vault_path / ".markdownmind"
        self.index_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize components
        self.parser = MarkdownParser()
        self.kg = KnowledgeGraph()
        self.search = SemanticSearch()
        
        # Cache
        self._documents: Dict[str, Dict] = {}
        self._index_file = self.index_path / "index.json"
        self._graph_file = self.index_path / "knowledge_graph.json"
        
    def scan(self, force_rebuild: bool = False) -> Dict:
        """
        Scan vault and build/update index.
        扫描文档库并构建/更新索引
        
        Args:
            force_rebuild: Force full rebuild even if index exists
            
        Returns:
            Scan statistics
        """
        print(f"🔍 Scanning vault: {self.vault_path}")
        
        # Load existing index
        existing_index = self._load_index() if not force_rebuild else {}
        
        # Find all markdown files
        md_files = list(self.vault_path.rglob("*.md"))
        md_files = [f for f in md_files if not f.name.startswith(".")]
        
        print(f"📄 Found {len(md_files)} Markdown files")
        
        new_docs = 0
        updated_docs = 0
        unchanged_docs = 0
        
        for file_path in md_files:
            rel_path = str(file_path.relative_to(self.vault_path))
            file_hash = get_file_hash(file_path)
            
            # Check if file needs updating
            if rel_path in existing_index:
                if existing_index[rel_path].get("hash") == file_hash:
                    self._documents[rel_path] = existing_index[rel_path]
                    unchanged_docs += 1
                    continue
                else:
                    updated_docs += 1
            else:
                new_docs += 1
            
            # Parse document
            try:
                doc_info = self.parser.parse(file_path, self.vault_path)
                doc_info["hash"] = file_hash
                doc_info["indexed_at"] = datetime.now().isoformat()
                self._documents[rel_path] = doc_info
            except Exception as e:
                print(f"  ⚠️  Error parsing {rel_path}: {e}")
        
        # Build knowledge graph
        print("🕸️  Building knowledge graph...")
        self.kg.build_from_documents(self._documents)
        
        # Build search index
        print("🔎 Building search index...")
        self.search.build_index(self._documents)
        
        # Save index
        self._save_index()
        self._save_graph()
        
        stats = {
            "total_files": len(md_files),
            "new_files": new_docs,
            "updated_files": updated_docs,
            "unchanged_files": unchanged_docs,
            "total_tags": len(self.kg.get_all_tags()),
            "total_links": len(self.kg.get_all_links()),
        }
        
        print(f"\n✅ Scan complete!")
        print(f"   📊 Total: {stats['total_files']} files")
        print(f"   🆕 New: {stats['new_files']}")
        print(f"   🔄 Updated: {stats['updated_files']}")
        print(f"   ⏭️  Unchanged: {stats['unchanged_files']}")
        print(f"   🏷️  Tags: {stats['total_tags']}")
        print(f"   🔗 Links: {stats['total_links']}")
        
        return stats
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search documents semantically.
        语义搜索文档
        
        Args:
            query: Search query
            limit: Maximum results
            
        Returns:
            List of matching documents with scores
        """
        return self.search.search(query, self._documents, limit)
    
    def find_related(self, doc_path: str, limit: int = 5) -> List[Dict]:
        """
        Find related documents.
        查找相关文档
        
        Args:
            doc_path: Document path (relative to vault)
            limit: Maximum results
            
        Returns:
            List of related documents
        """
        return self.kg.find_related(doc_path, limit)
    
    def get_document(self, doc_path: str) -> Optional[Dict]:
        """
        Get document info by path.
        获取文档信息
        """
        return self._documents.get(doc_path)
    
    def get_tags(self) -> Dict[str, int]:
        """
        Get all tags with counts.
        获取所有标签及计数
        """
        return self.kg.get_all_tags()
    
    def get_stats(self) -> Dict:
        """
        Get vault statistics.
        获取文档库统计信息
        """
        if not self._documents:
            self._load_index()
        
        total_words = sum(d.get("word_count", 0) for d in self._documents.values())
        total_size = sum(d.get("size", 0) for d in self._documents.values())
        
        return {
            "total_documents": len(self._documents),
            "total_words": total_words,
            "total_size": format_file_size(total_size),
            "total_tags": len(self.kg.get_all_tags()),
            "total_links": len(self.kg.get_all_links()),
            "vault_path": str(self.vault_path),
        }
    
    def export_graph(self, format: str = "json") -> str:
        """
        Export knowledge graph.
        导出知识图谱
        
        Args:
            format: Export format (json, dot, gexf)
            
        Returns:
            Exported content
        """
        return self.kg.export(format)
    
    def _load_index(self) -> Dict:
        """Load index from disk."""
        if self._index_file.exists():
            try:
                with open(self._index_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self._documents = data.get("documents", {})
                    return self._documents
            except Exception as e:
                print(f"⚠️  Error loading index: {e}")
        return {}
    
    def _save_index(self):
        """Save index to disk."""
        data = {
            "version": "1.0.0",
            "updated_at": datetime.now().isoformat(),
            "vault_path": str(self.vault_path),
            "documents": self._documents,
        }
        with open(self._index_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _save_graph(self):
        """Save knowledge graph to disk."""
        graph_data = self.kg.to_dict()
        with open(self._graph_file, "w", encoding="utf-8") as f:
            json.dump(graph_data, f, ensure_ascii=False, indent=2)
