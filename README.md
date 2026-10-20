# RAGMechanic

**A modular Python framework for building, evaluating, and diagnosing
Retrieval-Augmented Generation (RAG) systems.**

RAGMechanic provides reusable components for document ingestion, text
splitting, embeddings, vector storage, retrieval, contextual
compression, LLM integration, evaluation, persistent result storage, and
HTML reporting.

It is designed to help developers experiment with RAG configurations,
inspect retrieved context, track pipeline latency, and review evaluation
results without implementing every component from scratch.

## Table of Contents

-   [Overview](#overview)
-   [Features](#features)
-   [Architecture](#architecture)
-   [Project Structure](#project-structure)
-   [Installation](#installation)
-   [Quick Start](#quick-start)
-   [Working with Query Results](#working-with-query-results)
-   [Evaluation and Reporting](#evaluation-and-reporting)
-   [Database and Persistence](#database-and-persistence)
-   [Output Files](#output-files)
-   [Core Components](#core-components)
-   [Vector Stores](#vector-stores)
-   [LLM Providers](#llm-providers)

## Overview

A RAG application involves more than connecting a language model to a
vector database. Document parsing, chunking, embedding quality,
retrieval relevance, context selection, and answer generation all affect
the final result.

RAGMechanic organizes these stages into modular components so developers
can build and experiment with different RAG configurations.

It may be useful for: - Developers building document question-answering
applications. - AI engineers experimenting with retrieval strategies and
vector stores. - Researchers comparing RAG configurations and evaluation
results. - Students learning how RAG systems work internally. -
Contributors building reusable components for retrieval-augmented
applications.

## Features

### Document ingestion and text splitting

Load supported documents and split their content into chunks for
embedding and retrieval. Supported formats and loader requirements
depend on the installed dependencies and configured implementation;
common formats in the project include PDF, DOCX, PPTX, and TXT.

Chunk size and overlap can be configured when supported by the selected
pipeline configuration.

### Embeddings and vector storage

Generate vector representations for document chunks and queries, then
use a configured vector-store backend for similarity search. The
repository includes modules for Chroma, FAISS, Pinecone, and Qdrant.
Each backend may require its own package, credentials, and
configuration.

### Retrieval and contextual compression

Retrieve candidate chunks relevant to a question and, when enabled,
refine the retrieved context before sending it to the language model.

### LLM integrations

RAGMechanic provides an LLM management module. The repository's
dependency configuration includes integrations for Google Gemini, xAI,
Mistral, and Anthropic. Actual availability depends on the installed
integration and the implementation/configuration used.

### Evaluation

The evaluation workflow supports the metrics represented in the current
result/database model: - Faithfulness - Answer relevancy - Hallucination

Metric availability and prerequisites depend on the evaluator
configuration and installed evaluation dependencies.

### Persistent storage and HTML reports

RAGMechanic stores query information, retrieved and compressed chunks,
latency/count metadata, and evaluation results in a SQLite database. An
HTML report can be generated to inspect available evaluation results.
The exact report contents depend on the report implementation and
available records.

## Architecture

A typical workflow follows these stages:

1.  **Ingestion:** Load source documents.
2.  **Splitting:** Divide document content into chunks.
3.  **Embedding:** Convert chunks into vector representations.
4.  **Indexing:** Store vectors and associated document information.
5.  **Retrieval:** Find candidate chunks for a query.
6.  **Compression:** Refine retrieved context when enabled.
7.  **Generation:** Generate an answer using the query and selected
    context.
8.  **Persistence:** Store the query, answer, retrieved/compressed
    chunks, and pipeline metadata.
9.  **Evaluation:** Evaluate queries that do not yet have stored
    evaluation results.
10. **Reporting:** Generate an HTML report from available stored
    results.

The exact execution flow depends on the selected components and pipeline
configuration.

## Project Structure

The repository is organized around the following modules:

``` text
ragmechanic/
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
├── docs/
├── examples.ipynb
├── pyproject.toml
├── README.md
└── .gitignore
```

Your local working directory may also contain `documents/` and `output/`
folders. These are runtime/development folders, not necessarily part of
the installed package.

## Installation

### Option 1: Install from PyPI

Install the latest published release:

``` bash
python -m pip install ragmechanic
```

### Option 2: Install from GitHub for development

Clone the repository:

``` bash
git clone https://github.com/Divyanshu-Mathur/RAGMechanic.git
cd RAGMechanic
```

Create and activate a virtual environment.

**Windows PowerShell:**

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux or macOS:**

``` bash
python -m venv .venv
source .venv/bin/activate
```

Install the project in editable mode:

``` bash
python -m pip install --upgrade pip
python -m pip install -e .
```

Install any additional provider, vector-store, or evaluation
dependencies required by your configuration. If optional extras are
defined in `pyproject.toml`, install the extra that matches the feature
you intend to use.

## Quick Start

The following example illustrates the pipeline API. Replace the
placeholder model/provider values with values supported by your
installed configuration, and make sure `docs` points to your documents.

``` python
from ragmechanic import RAGPipeline

rag = RAGPipeline(
    docs="path/to/documents",
    embedding_model="YOUR_EMBEDDING_MODEL",
    llm_provider="YOUR_PROVIDER",
    llm_model="YOUR_MODEL",
    vector_store="chroma",
    chunk_size=800,
    chunk_overlap=150,
    db_path = "YOUR_DATABASE_PATH"

)

# Ask a question
result = rag.ask("What is machine learning?")

# Print the generated answer
print(result.answer)

# Inspect the retrieved source chunks
for document in result.retrieved_documents:
    print(document.page_content)

# Evaluate pending queries stored in the database
rag.evaluate()

# Generate the HTML report
rag.save_html()
```

The constructor arguments and supported values depend on the installed
package version and configured integrations.

## Working with Query Results

Each call to `rag.ask()` returns a `RAGResult` object. The result
includes the question, generated answer, retrieved documents, compressed
documents, available latency information, and evaluation data when
present.

``` python
result = rag.ask(
    "What is the syllabus of Module 1 of Computer Networks?"
)

print("Query ID:", result.id)
print("Question:", result.question)
print("Answer:", result.answer)
print("Retrieved document count:", len(result.retrieved_documents))
print("Compressed document count:", len(result.compressed_documents))
print("Retrieval latency:", result.retrieval_latency)
print("Compression latency:", result.compression_latency)
print("Generation latency:", result.generation_latency)

for document in result.retrieved_documents:
    print("Source:", document.metadata.get("source"))
    print("Page:", document.metadata.get("page"))
    print("Content:", document.page_content)
```

The `id` may be populated when the result is read back from persistent
storage; whether it is available immediately from `ask()` depends on the
pipeline implementation. Latency values are measured by the pipeline and
may be zero or unavailable for fields that were not recorded.

## Evaluation and Reporting

RAGMechanic separates query execution, evaluation, persistence, and
report generation.

### Single-query workflow

``` python
result = rag.ask("What is machine learning?")

# Check the database and evaluate queries with no stored evaluation
rag.evaluate()

# Create/update the HTML report from available stored results
rag.save_html()
```

### Batch workflow

You can run several questions before triggering evaluation:

``` python
questions = [
    "What is machine learning?",
    "What is deep learning?",
    "What is retrieval-augmented generation?",
]

for question in questions:
    rag.ask(question)

# Evaluate all stored queries that are missing evaluation records
rag.evaluate()

# Generate the report
rag.save_html()
```

### Incremental evaluation

The database tracks evaluations separately from query records. When
`evaluate()` uses the database's pending-query workflow, it can identify
query IDs that have no corresponding evaluation record. This supports
incremental processing: previously stored unevaluated queries can be
evaluated along with newly added queries.

Completed evaluations are stored by query ID. Calling evaluation again
should not require reevaluating records that already have an evaluation
row, unless the implementation or configuration explicitly
updates/re-runs them.

### Evaluation metrics

The current database result model has fields for:

  -----------------------------------------------------------------------
  Metric                              Description
  ----------------------------------- -----------------------------------
  Faithfulness                        Assesses whether the answer is
                                      supported by the supplied context.

  Answer relevancy                    Assesses how relevant the answer is
                                      to the question.

  Hallucination                       Represents the evaluator's
                                      hallucination metric/result.
  -----------------------------------------------------------------------

Interpretation, score ranges, and metric prerequisites depend on the
configured evaluator. 

### What the HTML report is for

The report is intended to make stored evaluation results easier to
inspect. Use it after evaluation:

``` python
rag.evaluate()
rag.save_html()
```


## Database and Persistence

RAGMechanic uses SQLite for persistent query and evaluation records.
SQLite stores data in a local database file and does not require a
separate database server.

The database layer defines four tables.

### 1. `queries`

Stores one record per saved query, including: - `id`: unique query
identifier. - `question` and `answer`. - Retrieval, compression,
generation, and total latency fields. - Retrieved and compressed chunk
counts. - Compression ratio. - Creation timestamp.

### 2. `retrieved_chunks`

Stores retrieved document chunks associated with a query: - `query_id`:
links the chunk to its query. - Content and source. - Page and chunk
ID. - Rank and similarity score.

A query may have multiple retrieved chunks.

### 3. `compressed_chunks`

Stores compressed/refined chunks associated with a query. It includes
the query relationship, content, source, page, chunk ID, rank, and
similarity score where available.

### 4. `evaluations`

Stores evaluation results linked to a query: - `query_id`: unique
relationship to the query record. - Faithfulness. - Answer relevancy. -
Hallucination. - Evaluation timestamp.

The database schema allows at most one evaluation row per query ID;
saving an evaluation for the same query ID updates that row.

### How the tables relate

``` text
queries
  ├── retrieved_chunks       (one query can have many chunks)
  ├── compressed_chunks      (one query can have many chunks)
  └── evaluations            (zero or one evaluation record per query)
```

### Example lifecycle

1.  `rag.ask("What is machine learning?")` runs the query. The
    pipeline's storage integration saves the query and associated chunk
    information when persistence is enabled by the implementation.
2.  The query receives a database ID.
3.  `rag.evaluate()` checks for query IDs that do not yet have
    evaluation records and evaluates pending queries.
4.  Evaluation scores and the evaluation timestamp are saved.
5.  `rag.save_html()` generates the report using the reporting
    implementation and available stored data.

For example, if the database contains query IDs `1`, `2`, and `3`, and
only query `1` has an evaluation row, the pending-query lookup
identifies `2` and `3` for evaluation. A subsequent query can be added
and evaluated on a later call.

### Database location

The database class defaults to a file named `ragmechanic.db` relative to
the process's current working directory when no other path is supplied.

For predictable output locations, run your application from the intended
working directory or configure an explicit database/output path if the
installed pipeline version exposes that option. Avoid storing generated
data inside a virtual environment, because virtual environments are
disposable and may be recreated.

## Output Files

A typical output layout may look like this:

``` text
output/
├── database/
│   └── ragmechanic.db
└── report/
    └── rag_report.html
```

This is an example layout, not a guarantee of the default paths. The
actual database and report paths depend on the configuration used by the
installed package and the current working directory.

-   **Database:** persists query, chunk, and evaluation records.
-   **HTML report:** presents available report data for review.
-   **Source documents:** remain at the location you provide unless your
    own application moves or copies them.

Back up the SQLite database if you need to preserve evaluation history.
Do not commit databases containing private documents or sensitive query
content to a public repository.

## Core Components

  -----------------------------------------------------------------------
  Module                              Responsibility
  ----------------------------------- -----------------------------------
  `ragmechanic.ingestion`             Loading documents and preparing
                                      content for processing.

  `ragmechanic.embeddings`            Creating vector representations.

  `ragmechanic.vector_store`          Vector-store implementations and
                                      related logic.

  `ragmechanic.retriever`             Retrieving candidate chunks for a
                                      query.

  `ragmechanic.compression`           Refining retrieved context when
                                      enabled.

  `ragmechanic.llm`                   LLM configuration and integration
                                      logic.

  `ragmechanic.evaluation`            Evaluating supported RAG outputs.

  `ragmechanic.storage`               Persisting query, chunk, and
                                      evaluation data.

  `ragmechanic.report`                Result models and HTML report
                                      generation.

  `ragmechanic.pipeline`              Orchestrating the RAG workflow.
  -----------------------------------------------------------------------

## Vector Stores

The repository includes modules for these vector-store backends:

  Backend    Integration package
  ---------- --------------------------------
  Chroma     `chromadb`, `langchain-chroma`
  FAISS      `faiss-cpu`
  Pinecone   `langchain-pinecone`
  Qdrant     `langchain-qdrant`

Install and configure the integration required for your selected
backend. Credentials, persistence behavior, and supported configuration
values differ by provider.

## LLM Providers

The project's dependency configuration includes these LangChain
integrations:

  Provider        Integration package
  --------------- --------------------------
  Google Gemini   `langchain-google-genai`
  xAI             `langchain-xai`
  Mistral         `langchain-mistralai`
  Anthropic       `langchain-anthropic`

Provider availability depends on the implementation and installed
integration. Configure API keys securely using the method supported by
the selected provider and your application.
