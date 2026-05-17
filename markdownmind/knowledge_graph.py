"""
Knowledge Graph Module
知识图谱模块
"""

import json
from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict


class KnowledgeGraph:
    """
    Build and manage knowledge graph from Markdown documents.
    从Markdown文档构建和管理知识图谱
    """
    
    def __init__(self):
        self.nodes: Dict[str, Dict] = {}  # Document nodes
        self.edges: List[Dict] = []       # Relationships
        self.tags: Dict[str, Set[str]] = defaultdict(set)  # Tag -> documents
        self.links: Dict[str, List[Dict]] = defaultdict(list)  # Document -> links
        
    def build_from_documents(self, documents: Dict[str, Dict]):
        """
        Build knowledge graph from parsed documents.
        
        Args:
            documents: Dictionary of document path -> document info
        """
        self.nodes = {}
        self.edges = []
        self.tags = defaultdict(set)
        self.links = defaultdict(list)
        
        # Create nodes
        for path, doc in documents.items():
            self.nodes[path] = {
                "id": path,
                "title": doc.get("title", path),
                "tags": doc.get("tags", []),
                "word_count": doc.get("word_count", 0),
            }
            
            # Index tags
            for tag in doc.get("tags", []):
                self.tags[tag].add(path)
            
            # Index links
            for link in doc.get("links", []):
                self.links[path].append(link)
            
            for wikilink in doc.get("wikilinks", []):
                self.links[path].append({
                    "text": wikilink.get("alias", wikilink["target"]),
                    "url": wikilink["target"],
                    "type": "wikilink",
                })
        
        # Create edges based on links
        self._build_edges()
        
        # Create edges based on tag similarity
        self._build_tag_edges()
    
    def _build_edges(self):
        """Build edges from document links."""
        for source_path, links in self.links.items():
            for link in links:
                if link["type"] in ("internal", "wikilink"):
                    target = link["url"]
                    
                    # Resolve target path
                    if not target.endswith('.md'):
                        target += '.md'
                    
                    # Check if target exists in our graph
                    if target in self.nodes:
                        self.edges.append({
                            "source": source_path,
                            "target": target,
                            "type": "links_to",
                            "weight": 1.0,
                        })
    
    def _build_tag_edges(self):
        """Build edges based on shared tags."""
        tag_docs = defaultdict(set)
        
        for path, node in self.nodes.items():
            for tag in node.get("tags", []):
                tag_docs[tag].add(path)
        
        # Create edges for documents sharing tags
        edges_added = set()
        for tag, docs in tag_docs.items():
            docs_list = list(docs)
            for i in range(len(docs_list)):
                for j in range(i + 1, len(docs_list)):
                    source, target = docs_list[i], docs_list[j]
                    edge_key = tuple(sorted([source, target]))
                    
                    if edge_key not in edges_added:
                        self.edges.append({
                            "source": source,
                            "target": target,
                            "type": "shared_tag",
                            "weight": 0.5,
                            "tag": tag,
                        })
                        edges_added.add(edge_key)
    
    def find_related(self, doc_path: str, limit: int = 5) -> List[Dict]:
        """
        Find related documents.
        
        Args:
            doc_path: Document path
            limit: Maximum number of results
            
        Returns:
            List of related documents with relationship info
        """
        if doc_path not in self.nodes:
            return []
        
        related = defaultdict(lambda: {"score": 0, "reasons": []})
        
        # Find directly linked documents
        for edge in self.edges:
            if edge["source"] == doc_path:
                target = edge["target"]
                related[target]["score"] += edge["weight"]
                related[target]["reasons"].append(f"linked from this doc")
            elif edge["target"] == doc_path:
                source = edge["source"]
                related[source]["score"] += edge["weight"]
                related[source]["reasons"].append(f"links to this doc")
        
        # Find documents with shared tags
        doc_tags = set(self.nodes[doc_path].get("tags", []))
        for other_path, other_node in self.nodes.items():
            if other_path == doc_path:
                continue
            
            other_tags = set(other_node.get("tags", []))
            shared = doc_tags & other_tags
            
            if shared:
                score = len(shared) * 0.3
                related[other_path]["score"] += score
                related[other_path]["reasons"].append(f"shared tags: {', '.join(shared)}")
        
        # Sort by score
        sorted_related = sorted(
            related.items(),
            key=lambda x: x[1]["score"],
            reverse=True
        )[:limit]
        
        result = []
        for path, info in sorted_related:
            if path in self.nodes:
                result.append({
                    "path": path,
                    "title": self.nodes[path]["title"],
                    "score": info["score"],
                    "reasons": info["reasons"],
                })
        
        return result
    
    def get_all_tags(self) -> Dict[str, int]:
        """Get all tags with document counts."""
        return {tag: len(docs) for tag, docs in self.tags.items()}
    
    def get_all_links(self) -> List[Dict]:
        """Get all links in the graph."""
        return self.edges
    
    def get_tag_cloud(self, limit: int = 50) -> List[Dict]:
        """
        Get tag cloud data.
        
        Returns:
            List of tags with size info for visualization
        """
        tag_counts = self.get_all_tags()
        if not tag_counts:
            return []
        
        max_count = max(tag_counts.values())
        min_count = min(tag_counts.values())
        
        tags = []
        for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:limit]:
            # Normalize size between 1 and 5
            if max_count == min_count:
                size = 3
            else:
                size = 1 + 4 * (count - min_count) / (max_count - min_count)
            
            tags.append({
                "text": tag,
                "count": count,
                "size": round(size, 1),
            })
        
        return tags
    
    def find_orphaned_docs(self) -> List[str]:
        """Find documents with no incoming or outgoing links."""
        connected = set()
        for edge in self.edges:
            connected.add(edge["source"])
            connected.add(edge["target"])
        
        return [path for path in self.nodes if path not in connected]
    
    def find_hub_docs(self, limit: int = 10) -> List[Dict]:
        """Find documents with most connections."""
        connection_counts = defaultdict(int)
        for edge in self.edges:
            connection_counts[edge["source"]] += 1
            connection_counts[edge["target"]] += 1
        
        sorted_docs = sorted(
            connection_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit]
        
        return [
            {
                "path": path,
                "title": self.nodes[path]["title"],
                "connections": count,
            }
            for path, count in sorted_docs
            if path in self.nodes
        ]
    
    def export(self, format: str = "json") -> str:
        """
        Export graph in various formats.
        
        Args:
            format: Export format (json, dot, gexf)
            
        Returns:
            Exported content
        """
        if format == "json":
            return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
        
        elif format == "dot":
            return self._export_dot()
        
        elif format == "gexf":
            return self._export_gexf()
        
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def to_dict(self) -> Dict:
        """Convert graph to dictionary."""
        return {
            "nodes": list(self.nodes.values()),
            "edges": self.edges,
            "stats": {
                "node_count": len(self.nodes),
                "edge_count": len(self.edges),
                "tag_count": len(self.tags),
            },
        }
    
    def _export_dot(self) -> str:
        """Export as GraphViz DOT format."""
        lines = ["digraph KnowledgeGraph {"]
        lines.append("  rankdir=LR;")
        lines.append('  node [shape=box, style=rounded];')
        
        # Add nodes
        for path, node in self.nodes.items():
            label = node["title"].replace('"', '\\"')
            lines.append(f'  "{path}" [label="{label}"];')
        
        # Add edges
        for edge in self.edges:
            source = edge["source"]
            target = edge["target"]
            lines.append(f'  "{source}" -> "{target}";')
        
        lines.append("}")
        return '\n'.join(lines)
    
    def _export_gexf(self) -> str:
        """Export as GEXF format for Gephi."""
        lines = ['<?xml version="1.0" encoding="UTF-8"?>']
        lines.append('<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">')
        lines.append('  <graph mode="static" defaultedgetype="directed">')
        
        # Nodes
        lines.append('    <nodes>')
        for path, node in self.nodes.items():
            lines.append(f'      <node id="{path}" label="{node["title"]}" />')
        lines.append('    </nodes>')
        
        # Edges
        lines.append('    <edges>')
        for i, edge in enumerate(self.edges):
            lines.append(f'      <edge id="{i}" source="{edge["source"]}" target="{edge["target"]}" />')
        lines.append('    </edges>')
        
        lines.append('  </graph>')
        lines.append('</gexf>')
        
        return '\n'.join(lines)
