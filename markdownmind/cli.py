#!/usr/bin/env python3
"""
MarkdownMind CLI
命令行接口模块
"""

import sys
import argparse
from pathlib import Path
from typing import Optional

from .core import MarkdownMind
from .utils import format_file_size, pluralize


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog="markdownmind",
        description="🧠 MarkdownMind - Lightweight Markdown Document Intelligence & Knowledge Graph CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s scan ~/my-notes              # Scan vault and build index
  %(prog)s search "python tutorial"     # Search documents
  %(prog)s tags                         # List all tags
  %(prog)s stats                        # Show vault statistics
  %(prog)s related note.md              # Find related documents
  %(prog)s export --format dot          # Export knowledge graph
        """,
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0",
    )
    
    parser.add_argument(
        "--vault",
        "-v",
        default=".",
        help="Path to Markdown vault (default: current directory)",
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Scan command
    scan_parser = subparsers.add_parser(
        "scan",
        help="Scan vault and build/update index",
    )
    scan_parser.add_argument(
        "path",
        nargs="?",
        help="Path to Markdown vault",
    )
    scan_parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Force full rebuild",
    )
    
    # Search command
    search_parser = subparsers.add_parser(
        "search",
        help="Search documents semantically",
    )
    search_parser.add_argument(
        "query",
        help="Search query",
    )
    search_parser.add_argument(
        "--limit",
        "-n",
        type=int,
        default=10,
        help="Maximum results (default: 10)",
    )
    
    # Tags command
    tags_parser = subparsers.add_parser(
        "tags",
        help="List all tags",
    )
    tags_parser.add_argument(
        "--limit",
        "-n",
        type=int,
        default=50,
        help="Maximum tags to show",
    )
    
    # Stats command
    subparsers.add_parser(
        "stats",
        help="Show vault statistics",
    )
    
    # Related command
    related_parser = subparsers.add_parser(
        "related",
        help="Find related documents",
    )
    related_parser.add_argument(
        "document",
        help="Document path (relative to vault)",
    )
    related_parser.add_argument(
        "--limit",
        "-n",
        type=int,
        default=5,
        help="Maximum results (default: 5)",
    )
    
    # Export command
    export_parser = subparsers.add_parser(
        "export",
        help="Export knowledge graph",
    )
    export_parser.add_argument(
        "--format",
        "-f",
        choices=["json", "dot", "gexf"],
        default="json",
        help="Export format (default: json)",
    )
    export_parser.add_argument(
        "--output",
        "-o",
        help="Output file (default: stdout)",
    )
    
    # Hub command
    subparsers.add_parser(
        "hub",
        help="Find hub documents (most connected)",
    )
    
    # Orphans command
    subparsers.add_parser(
        "orphans",
        help="Find orphaned documents (no links)",
    )
    
    return parser


def cmd_scan(args, mm: MarkdownMind):
    """Handle scan command."""
    vault_path = args.path or args.vault
    mm = MarkdownMind(vault_path)
    stats = mm.scan(force_rebuild=args.force)
    return 0


def cmd_search(args, mm: MarkdownMind):
    """Handle search command."""
    results = mm.search(args.query, limit=args.limit)
    
    if not results:
        print("🔍 No results found.")
        return 0
    
    print(f"🔍 Found {pluralize(len(results), 'result')} for '{args.query}':\n")
    
    for i, result in enumerate(results, 1):
        print(f"  {i}. \033[1m{result['title']}\033[0m")
        print(f"     📄 {result['path']}")
        if result['tags']:
            tags_str = ', '.join(f"#{tag}" for tag in result['tags'])
            print(f"     🏷️  {tags_str}")
        print(f"     📊 Score: {result['score']}")
        if result['summary']:
            summary = result['summary'][:100] + '...' if len(result['summary']) > 100 else result['summary']
            print(f"     💡 {summary}")
        print()
    
    return 0


def cmd_tags(args, mm: MarkdownMind):
    """Handle tags command."""
    tags = mm.get_tags()
    
    if not tags:
        print("🏷️  No tags found.")
        return 0
    
    # Sort by count
    sorted_tags = sorted(tags.items(), key=lambda x: x[1], reverse=True)[:args.limit]
    
    print(f"🏷️  {pluralize(len(tags), 'tag')} in vault:\n")
    
    max_count = max(tags.values())
    
    for tag, count in sorted_tags:
        # Visual bar
        bar_length = int(20 * count / max_count) if max_count > 0 else 0
        bar = "█" * bar_length
        print(f"  #{tag:<20} {bar} {count}")
    
    return 0


def cmd_stats(args, mm: MarkdownMind):
    """Handle stats command."""
    stats = mm.get_stats()
    
    print("📊 Vault Statistics\n")
    print(f"  📁 Vault Path:    {stats['vault_path']}")
    print(f"  📄 Documents:     {stats['total_documents']}")
    print(f"  📝 Total Words:   {stats['total_words']:,}")
    print(f"  💾 Total Size:    {stats['total_size']}")
    print(f"  🏷️  Tags:          {stats['total_tags']}")
    print(f"  🔗 Links:         {stats['total_links']}")
    
    return 0


def cmd_related(args, mm: MarkdownMind):
    """Handle related command."""
    results = mm.find_related(args.document, limit=args.limit)
    
    if not results:
        print(f"🔗 No related documents found for '{args.document}'.")
        return 0
    
    print(f"🔗 Documents related to '{args.document}':\n")
    
    for i, result in enumerate(results, 1):
        print(f"  {i}. \033[1m{result['title']}\033[0m")
        print(f"     📄 {result['path']}")
        print(f"     📊 Relevance: {result['score']:.2f}")
        if result['reasons']:
            print(f"     💡 {', '.join(result['reasons'])}")
        print()
    
    return 0


def cmd_export(args, mm: MarkdownMind):
    """Handle export command."""
    content = mm.export_graph(format=args.format)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Exported to {args.output}")
    else:
        print(content)
    
    return 0


def cmd_hub(args, mm: MarkdownMind):
    """Handle hub command."""
    hubs = mm.kg.find_hub_docs(limit=10)
    
    if not hubs:
        print("🕸️  No hub documents found.")
        return 0
    
    print("🕸️  Hub Documents (most connected):\n")
    
    for i, hub in enumerate(hubs, 1):
        print(f"  {i}. \033[1m{hub['title']}\033[0m")
        print(f"     📄 {hub['path']}")
        print(f"     🔗 {pluralize(hub['connections'], 'connection')}")
        print()
    
    return 0


def cmd_orphans(args, mm: MarkdownMind):
    """Handle orphans command."""
    orphans = mm.kg.find_orphaned_docs()
    
    if not orphans:
        print("✅ No orphaned documents found.")
        return 0
    
    print(f"🚨 {pluralize(len(orphans), 'orphaned document')}:\n")
    
    for orphan in orphans[:20]:  # Limit output
        doc = mm.get_document(orphan)
        title = doc.get("title", orphan) if doc else orphan
        print(f"  • {title}")
        print(f"    📄 {orphan}")
        print()
    
    if len(orphans) > 20:
        print(f"  ... and {len(orphans) - 20} more")
    
    return 0


def main(argv: Optional[list] = None) -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Initialize MarkdownMind
    vault_path = getattr(args, 'path', None) or args.vault
    mm = MarkdownMind(vault_path)
    
    # Load existing index for most commands
    if args.command != "scan":
        mm._load_index()
        mm.kg.build_from_documents(mm._documents)
        mm.search.build_index(mm._documents)
    
    # Dispatch command
    commands = {
        "scan": cmd_scan,
        "search": cmd_search,
        "tags": cmd_tags,
        "stats": cmd_stats,
        "related": cmd_related,
        "export": cmd_export,
        "hub": cmd_hub,
        "orphans": cmd_orphans,
    }
    
    handler = commands.get(args.command)
    if handler:
        return handler(args, mm)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
