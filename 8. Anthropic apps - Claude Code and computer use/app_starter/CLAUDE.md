# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Commands

```bash
# Start the MCP server (stdio transport)
uv run main.py

# Run all tests
uv run pytest

# Run a single test file / test
uv run pytest tests/test_document.py
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_pdf
```

## Architecture

This is an MCP (Model Context Protocol) server exposing document-processing tools to AI assistants, built on `mcp[cli]` (FastMCP).

- `main.py` is the server entrypoint: it instantiates `FastMCP`, registers tools via `mcp.tool()(function)`, and runs the server. New tools must be registered here to be exposed.
- `tools/` holds plain Python functions, one concern per module (e.g. `tools/math.py`, `tools/document.py`). These functions are the actual tool implementations and are registered with the MCP server in `main.py` — they are not decorated in place.
- `tools/document.py` wraps `markitdown` (`MarkItDown`) to convert binary document data (PDF, DOCX, etc.) into markdown text, driven off a `StreamInfo(extension=...)` hint rather than a file path.
- `tests/fixtures/` contains real sample documents (`.docx`, `.pdf`) used by tests instead of mocks, so tests exercise the actual `markitdown` conversion pipeline.

## Defining MCP tools

Tools are plain Python functions registered with the MCP server by calling:

```python
mcp.tool()(my_function)
```

Tool docstrings become the tool description the AI assistant sees, so precision directly affects tool-selection behavior. Docstrings should:

- Begin with a one-line summary
- Provide a detailed explanation of functionality
- Explain when to use (and not use) the tool
- Include usage examples with expected input/output

Parameters should be typed with pydantic `Field` for per-parameter descriptions:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does")
) -> ReturnType:
    """Comprehensive docstring here"""
    # Implementation
```

`tools/math.py`'s `add` function is the reference example of this convention (one-line summary, explanation, "When to use", doctest-style `>>>` examples).

Always give function arguments explicit types (pydantic `Field`-typed parameters for tools, standard type hints elsewhere).
