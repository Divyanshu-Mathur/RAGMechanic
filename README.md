# RAGMechanic

**A modular Python framework for building, evaluating, and diagnosing Retrieval-Augmented Generation (RAG) systems.**

RAGMechanic is designed to help developers experiment with RAG pipelines through reusable components for document ingestion, text splitting, embeddings, vector storage, retrieval, contextual compression, LLM integration, evaluation, and reporting.

The goal is to make it easier to build RAG applications, compare configurations, identify retrieval and generation issues, and inspect evaluation results without implementing every component from scratch.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Install](#install)
- [Installation](#install)
- [Quick Start](#quick-start)
- [Core Components](#core-components)
- [Vector Stores](#vector-stores)
- [LLM Providers](#llm-providers)
- [Evaluation and Reporting](#evaluation-and-reporting)
- [Examples](#Example-Notebook)

## Overview

Building a RAG application involves more than connecting a language model to a vector database. Document parsing, chunking, embedding quality, retrieval relevance, context selection, and generation all affect the final result.

RAGMechanic organizes these stages into modular components so that developers can build and experiment with different RAG configurations.

The framework is intended for:

- Developers building document question-answering applications.
- AI engineers experimenting with retrieval strategies and vector databases.
- Researchers comparing RAG configurations and evaluation results.
- Students learning how RAG systems work internally.
- Contributors building reusable components for retrieval-augmented applications.

## Features

### Document ingestion

Load supported document formats and prepare their contents for downstream processing.

Potentially supported formats, depending on the installed loaders and current implementation:

- PDF
- DOCX
- PPTX
- TXT

### Text splitting

Split documents into smaller chunks for embedding and retrieval.

Configurable parameters include:

- Chunk size
- Chunk overlap

### Embeddings

Generate vector representations of document chunks and queries using supported embedding integrations.

The project includes an embeddings module and can be extended to support additional embedding providers.

### Vector storage

Modular vector-store implementations are organized under `vector_store/`.

The repository currently contains integrations for:

- Chroma
- FAISS
- Pinecone
- Qdrant

Actual availability depends on the implementation, installed dependencies, provider credentials, and configuration.

### Retrieval

Retrieve relevant document chunks based on a user's query.

The retrieval component provides the foundation for supplying context to a language model.

### Contextual compression

Reduce or refine retrieved context before passing it to the language model.

This can help focus generation on relevant information and reduce unnecessary context, depending on the compression strategy and its configuration.

### LLM integration

A dedicated LLM manager provides a place to configure language-model integrations.

The dependency configuration includes integrations for Google Gemini, xAI, Mistral, and Anthropic.

### Evaluation

The evaluation module is designed to assess RAG outputs and store evaluation results.

Evaluation metrics and their prerequisites depend on the configured evaluator and supported implementation.

### Persistent result storage

The storage module uses a database to persist supported pipeline or evaluation information.

### HTML reports

The reporting module generates HTML reports intended to make evaluation results easier to inspect.

Report fields and available visualizations depend on the current reporting implementation.

## Architecture

A typical RAG workflow follows these stages:

1. **Ingestion:** Load source documents.
2. **Splitting:** Divide documents into smaller chunks.
3. **Embedding:** Convert chunks into vector representations.
4. **Indexing:** Store vectors and associated document information.
5. **Retrieval:** Find relevant chunks for a query.
6. **Compression:** Refine retrieved context when enabled.
7. **Generation:** Send the query and selected context to the language model.
8. **Evaluation:** Assess the generated answer using supported metrics.
9. **Storage and reporting:** Persist results and generate reports.

The exact execution flow depends on the selected components and pipeline configuration.

## Project Structure

```text
ragmechanic/
├── documents/
├── output/
│   ├── database/
│   └── report/
├── src/
│   └── ragmechanic/
│       ├── compression/
│       ├── embeddings/
│       ├── evaluation/
│       ├── ingestion/
│       ├── llm/
│       ├── report/
│       ├── retriever/
│       ├── storage/
│       ├── vector_store/
│       └── pipeline.py
├── examples.ipynb
├── docs/
├── pyproject.toml
├── README.md
└── .gitignore
```

The `documents/` and `output/` directories shown above are useful for local development and examples. They do not necessarily need to be distributed as part of the installed package.


## Install

### Option 1: Install from PyPI (Recommended)

Install the latest published release of RAGMechanic:

```bash
python -m pip install ragmechanic
```

### Option 2: Install from GitHub (Development)

To use the latest repository version or contribute to development, clone the repository:

```bash
git clone https://github.com/Divyanshu-Mathur/RAGMechanic.git
cd ragmechanic
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment.

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux or macOS:**

```bash
source .venv/bin/activate
```

Upgrade pip and install the package in editable mode:

```bash
python -m pip install --upgrade pip
python -m pip install -e .
```

## Quick Start

```python
from ragmechanic import RAGPipeline

# Configure the pipeline using supported arguments.
pipeline = RAGPipeline(
    docs="path/to/documents",
    embedding_model="YOUR_EMBEDDING_MODEL",
    llm_provider="YOUR_PROVIDER",
    llm_model="YOUR_MODEL",
    vector_store="chroma",
    chunk_size=800,
    chunk_overlap=150,
)

```

## Core Components

### Document loading

**Module:** `ragmechanic.ingestion`

Responsible for loading supported source documents and preparing their content for subsequent processing.

### Text splitting

**Module:** `ragmechanic.ingestion`

Responsible for creating chunks from document content, using configurable splitting parameters where supported.

### Embeddings

**Module:** `ragmechanic.embeddings`

Responsible for creating vector representations used in similarity-based retrieval.

### Vector stores

**Module:** `ragmechanic.vector_store`

Provides the abstraction and implementations for supported vector databases and similarity-search backends.

### Retrieval

**Module:** `ragmechanic.retriever`

Responsible for finding candidate document chunks relevant to a query.

### Contextual compression

**Module:** `ragmechanic.compression`

Provides functionality for refining retrieved context before generation.

### Language-model management

**Module:** `ragmechanic.llm`

Centralizes supported LLM configuration and integration logic.

### Evaluation

**Module:** `ragmechanic.evaluation`

Provides evaluation-related functionality for assessing supported RAG outputs.

### Storage

**Module:** `ragmechanic.storage`

Handles persistence of supported data and results.

### Reporting

**Module:** `ragmechanic.report`

Provides HTML report generation functionality.

## Vector Stores

RAGMechanic contains modules for the following vector-store backends:

| Backend | Python package |
|---|---|
| Chroma | `chromadb`, `langchain-chroma` |
| FAISS | `faiss-cpu` |
| Pinecone | `langchain-pinecone` |
| Qdrant | `langchain-qdrant` |

Each backend may have different requirements for persistence, authentication, indexing, and configuration.


## LLM Providers

The project's dependency configuration includes the following LangChain integrations:

| Provider | Integration package |
|---|---|
| Google Gemini | `langchain-google-genai` |
| xAI | `langchain-xai` |
| Mistral | `langchain-mistralai` |
| Anthropic | `langchain-anthropic` |

Provider availability depends on the LLM manager implementation and the installed integration package.

Follow each provider's documentation for API-key setup, model availability, rate limits, and pricing.

## Evaluation and Reporting

RAGMechanic separates evaluation and reporting into dedicated modules.

A typical evaluation workflow may include:

1. Run a query against the configured RAG pipeline.
2. Collect the answer and retrieved context.
3. Supply the required evaluation inputs.
4. Compute the metrics supported by the evaluator.
5. Store the results.
6. Generate an HTML report.

### Output files

For local development, generated artifacts can be organized as follows:

```text
output/
├── database/
│   └── ragmechanic.db
└── report/
    └── rag_report.html
```

These paths are examples of the repository's current local output organization. Actual output paths should be configurable and documented according to the implementation.

## Example Notebook

Explore the end-to-end RAG workflow in
[`examples.ipynb`](./examples.ipynb).

The notebook demonstrates pipeline configuration, document querying,
evaluation, and HTML report generation.