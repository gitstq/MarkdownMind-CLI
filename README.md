<div align="center">

# 🧠 MarkdownMind

**Lightweight Markdown Document Intelligence & Knowledge Graph CLI**

**轻量级Markdown文档智能知识图谱与语义搜索CLI引擎**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-orange.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)]()

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

<a name="english"></a>
## 🇺🇸 English

### 🎉 Project Introduction

**MarkdownMind** is a powerful CLI tool that transforms your Markdown vault into an intelligent knowledge base. It automatically builds knowledge graphs, enables semantic search, and helps you discover connections between your notes.

**Key Differentiators:**
- 🚀 **Zero Dependencies** - Pure Python standard library, no external packages required
- 🧠 **Semantic Search** - TF-IDF based intelligent document retrieval
- 🕸️ **Knowledge Graph** - Automatic relationship mapping between documents
- 🏷️ **Tag Intelligence** - Smart tag analysis and cloud generation
- 🔗 **Link Analysis** - Support for both Markdown and Wiki-style links
- 📊 **Vault Statistics** - Comprehensive analytics for your knowledge base

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🔍 **Semantic Search** | Find documents by meaning, not just keywords |
| 🕸️ **Knowledge Graph** | Visualize connections between your notes |
| 🏷️ **Tag Management** | Analyze and explore your tagging patterns |
| 🔗 **Link Analysis** | Track internal and external links |
| 📈 **Statistics** | Word count, document metrics, and more |
| 🚀 **Fast Indexing** | Incremental scanning for large vaults |
| 📝 **Multi-format Export** | JSON, DOT (GraphViz), GEXF (Gephi) |

### 🚀 Quick Start

#### Installation

```bash
# Install from PyPI (coming soon)
pip install markdownmind

# Or install from source
git clone https://github.com/gitstq/MarkdownMind-CLI.git
cd MarkdownMind-CLI
pip install -e .
```

#### Basic Usage

```bash
# Scan your vault and build index
markdownmind scan ~/my-notes

# Search documents
markdownmind search "python tutorial"

# List all tags
markdownmind tags

# Show statistics
markdownmind stats

# Find related documents
markdownmind related note.md

# Export knowledge graph
markdownmind export --format dot --output graph.dot
```

### 📖 Detailed Usage Guide

#### Scanning Your Vault

```bash
# First-time scan
markdownmind scan ~/Documents/Obsidian

# Force rebuild
markdownmind scan ~/Documents/Obsidian --force
```

#### Semantic Search

```bash
# Basic search
markdownmind search "machine learning"

# Limit results
markdownmind search "python" --limit 5
```

#### Knowledge Graph Operations

```bash
# Find hub documents (most connected)
markdownmind hub

# Find orphaned documents
markdownmind orphans

# Export for visualization
markdownmind export --format gexf --output graph.gexf
```

### 💡 Design Philosophy

MarkdownMind is designed with the following principles:

1. **Privacy First** - All processing happens locally, no data leaves your machine
2. **Zero Dependencies** - Uses only Python standard library for maximum portability
3. **Speed** - Incremental indexing and efficient algorithms
4. **Compatibility** - Works with Obsidian, Logseq, and any Markdown-based system

### 📦 Packaging & Deployment

```bash
# Build distribution
make build

# Run tests
make test

# Clean build artifacts
make clean
```

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<a name="简体中文"></a>
## 🇨🇳 简体中文

### 🎉 项目介绍

**MarkdownMind** 是一个强大的CLI工具，可以将您的Markdown文档库转换为智能知识库。它自动构建知识图谱，实现语义搜索，并帮助您发现笔记之间的关联。

**核心差异化亮点：**
- 🚀 **零依赖** - 纯Python标准库实现，无需外部包
- 🧠 **语义搜索** - 基于TF-IDF的智能文档检索
- 🕸️ **知识图谱** - 自动映射文档间的关系
- 🏷️ **标签智能** - 智能标签分析和词云生成
- 🔗 **链接分析** - 支持Markdown和Wiki风格链接
- 📊 **文档库统计** - 知识库的综合分析

### ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🔍 **语义搜索** | 通过含义而不仅是关键词查找文档 |
| 🕸️ **知识图谱** | 可视化笔记之间的连接 |
| 🏷️ **标签管理** | 分析和探索您的标签模式 |
| 🔗 **链接分析** | 跟踪内部和外部链接 |
| 📈 **统计分析** | 字数统计、文档指标等 |
| 🚀 **快速索引** | 大型文档库的增量扫描 |
| 📝 **多格式导出** | JSON、DOT (GraphViz)、GEXF (Gephi) |

### 🚀 快速开始

#### 安装

```bash
# 从PyPI安装（即将推出）
pip install markdownmind

# 或从源码安装
git clone https://github.com/gitstq/MarkdownMind-CLI.git
cd MarkdownMind-CLI
pip install -e .
```

#### 基本用法

```bash
# 扫描文档库并构建索引
markdownmind scan ~/my-notes

# 搜索文档
markdownmind search "python教程"

# 列出所有标签
markdownmind tags

# 显示统计信息
markdownmind stats

# 查找相关文档
markdownmind related note.md

# 导出知识图谱
markdownmind export --format dot --output graph.dot
```

### 📖 详细使用指南

#### 扫描文档库

```bash
# 首次扫描
markdownmind scan ~/Documents/Obsidian

# 强制重建
markdownmind scan ~/Documents/Obsidian --force
```

#### 语义搜索

```bash
# 基础搜索
markdownmind search "机器学习"

# 限制结果数量
markdownmind search "python" --limit 5
```

#### 知识图谱操作

```bash
# 查找枢纽文档（连接最多的）
markdownmind hub

# 查找孤立文档
markdownmind orphans

# 导出用于可视化
markdownmind export --format gexf --output graph.gexf
```

### 💡 设计理念

MarkdownMind 遵循以下设计原则：

1. **隐私优先** - 所有处理都在本地进行，数据不会离开您的机器
2. **零依赖** - 仅使用Python标准库，确保最大可移植性
3. **速度** - 增量索引和高效算法
4. **兼容性** - 与Obsidian、Logseq和任何基于Markdown的系统兼容

### 📦 打包与部署

```bash
# 构建分发包
make build

# 运行测试
make test

# 清理构建产物
make clean
```

### 🤝 贡献指南

欢迎贡献！请随时提交Pull Request。

1. Fork本仓库
2. 创建您的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'feat: 添加某个 AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

### 📄 开源协议

基于MIT协议分发。更多信息请查看 `LICENSE` 文件。

---

<a name="繁體中文"></a>
## 🇹
<a name="繁體中文"></a>
## 🇹
