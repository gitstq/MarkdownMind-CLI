"""
MarkdownMind Setup Script
MarkdownMind安装脚本
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="markdownmind",
    version="1.0.0",
    author="MarkdownMind Team",
    author_email="hello@markdownmind.dev",
    description="🧠 Lightweight Markdown Document Intelligence & Knowledge Graph CLI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/MarkdownMind",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Text Processing :: Markup",
        "Topic :: Utilities",
        "Topic :: Software Development :: Documentation",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "markdownmind=markdownmind.cli:main",
            "mdmind=markdownmind.cli:main",
        ],
    },
    keywords=[
        "markdown",
        "knowledge-graph",
        "semantic-search",
        "cli",
        "documentation",
        "notes",
        "knowledge-base",
        "obsidian",
        "zettelkasten",
    ],
    project_urls={
        "Bug Reports": "https://github.com/gitstq/MarkdownMind/issues",
        "Source": "https://github.com/gitstq/MarkdownMind",
        "Documentation": "https://github.com/gitstq/MarkdownMind#readme",
    },
)
