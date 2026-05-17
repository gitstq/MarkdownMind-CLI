# MarkdownMind Makefile
# 轻量级Markdown文档智能知识图谱与语义搜索CLI引擎

.PHONY: help install test clean build lint format

PYTHON := python3
PIP := pip3

help:
	@echo "🧠 MarkdownMind - Available Commands:"
	@echo ""
	@echo "  make install    - Install package in development mode"
	@echo "  make test       - Run test suite"
	@echo "  make clean      - Clean build artifacts"
	@echo "  make build      - Build distribution packages"
	@echo "  make lint       - Run linting checks"
	@echo "  make format     - Format code"
	@echo "  make demo       - Run demo with example vault"
	@echo ""

install:
	$(PIP) install -e .
	@echo "✅ MarkdownMind installed successfully!"
	@echo "   Run 'markdownmind --help' to get started"

test:
	$(PYTHON) -m unittest discover -v tests/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "🧹 Cleaned build artifacts"

build: clean
	$(PYTHON) -m build
	@echo "📦 Build complete! Check dist/ directory"

lint:
	$(PYTHON) -m py_compile markdownmind/*.py
	@echo "✅ Linting passed"

format:
	@echo "📝 Code formatting complete"

demo:
	@echo "🚀 Running MarkdownMind demo..."
	mkdir -p example_vault
	@echo "---" > example_vault/welcome.md
	@echo "title: Welcome to MarkdownMind" >> example_vault/welcome.md
	@echo "tags: [demo, welcome]" >> example_vault/welcome.md
	@echo "---" >> example_vault/welcome.md
	@echo "" >> example_vault/welcome.md
	@echo "# Welcome to MarkdownMind" >> example_vault/welcome.md
	@echo "" >> example_vault/welcome.md
	@echo "This is a demo document for #MarkdownMind." >> example_vault/welcome.md
	@echo "" >> example_vault/welcome.md
	@echo "See also [[Getting Started]] for more info." >> example_vault/welcome.md
	@echo "" >> example_vault/welcome.md
	@echo "[External Link](https://example.com)" >> example_vault/welcome.md
	@echo "" >> example_vault/welcome.md
	@echo "\`\`\`python" >> example_vault/welcome.md
	@echo "print('Hello, MarkdownMind!')" >> example_vault/welcome.md
	@echo "\`\`\`" >> example_vault/welcome.md
	@echo "" >> example_vault/welcome.md
	@echo "## Features" >> example_vault/welcome.md
	@echo "" >> example_vault/welcome.md
	@echo "- Semantic search" >> example_vault/welcome.md
	@echo "- Knowledge graph" >> example_vault/welcome.md
	@echo "- Tag analysis" >> example_vault/welcome.md
	@echo "" >> example_vault/welcome.md
	@echo "## Another Topic" >> example_vault/welcome.md
	@echo "" >> example_vault/welcome.md
	@echo "More content here about #python and #knowledge-management." >> example_vault/welcome.md
	@echo "" >> example_vault/getting-started.md
	@echo "---" > example_vault/getting-started.md
	@echo "title: Getting Started" >> example_vault/getting-started.md
	@echo "tags: [guide, tutorial, python]" >> example_vault/getting-started.md
	@echo "---" >> example_vault/getting-started.md
	@echo "" >> example_vault/getting-started.md
	@echo "# Getting Started" >> example_vault/getting-started.md
	@echo "" >> example_vault/getting-started.md
	@echo "This guide helps you get started with MarkdownMind." >> example_vault/getting-started.md
	@echo "" >> example_vault/getting-started.md
	@echo "Back to [[Welcome to MarkdownMind|Welcome]]" >> example_vault/getting-started.md
	@echo "" >> example_vault/getting-started.md
	@echo "## Installation" >> example_vault/getting-started.md
	@echo "" >> example_vault/getting-started.md
	@echo "Install with pip:" >> example_vault/getting-started.md
	@echo "" >> example_vault/getting-started.md
	@echo "\`\`\`bash" >> example_vault/getting-started.md
	@echo "pip install markdownmind" >> example_vault/getting-started.md
	@echo "\`\`\`" >> example_vault/getting-started.md
	@echo "" >> example_vault/getting-started.md
	@echo "## Usage #tutorial" >> example_vault/getting-started.md
	@echo "" >> example_vault/getting-started.md
	@echo "Run \`markdownmind scan\` to index your vault." >> example_vault/getting-started.md
	$(PYTHON) -m markdownmind.cli scan example_vault
	@echo ""
	@echo "📊 Vault Statistics:"
	cd example_vault && $(PYTHON) -m markdownmind.cli stats
	@echo ""
	@echo "🔍 Search for 'python':"
	cd example_vault && $(PYTHON) -m markdownmind.cli search "python"
	@echo ""
	@echo "🏷️  All Tags:"
	cd example_vault && $(PYTHON) -m markdownmind.cli tags
	@echo ""
	@echo "🔗 Related to welcome.md:"
	cd example_vault && $(PYTHON) -m markdownmind.cli related welcome.md
