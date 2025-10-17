# Gundelsby MCP Server

This package exposes the Markdown and HTML sources from the gundelsby.com Jekyll repository over the Model Context Protocol (MCP).

## Prerequisites

- Python 3.10+
- An MCP-compatible client (OpenAI Desktop, Claude Desktop, etc.)

## Setup

```
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Running the server

```
python -m gundelsby_mcp
```

The server uses STDIO transport and automatically scans the repository's Markdown and include files. Connect your MCP client to the started process to browse resources or call the `search` tool.
