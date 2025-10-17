"""Model Context Protocol server for gundelsby.com content."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import frontmatter
from mcp.server.fastmcp import FastMCP
from mcp.types import Resource, TextContent

_URI_PREFIX = "gundelsby://"
_REPO_ROOT = Path(__file__).resolve().parents[3]
_MD_EXTENSIONS = {".md", ".markdown"}
_CONTENT_PATTERNS = (
    "*.md",
    "_posts/**/*.md",
    "_includes/**/*.html",
    "_layouts/**/*.html",
)
_EXCLUDED_TOP_LEVEL = {".git", ".venv", "_site", "node_modules"}


@dataclass
class Document:
    """Represents a site document exposed over MCP."""

    rel_path: Path
    raw_text: str
    metadata: dict[str, Any]
    content: str
    mime_type: str


def _is_excluded(path: Path) -> bool:
    return any(part in _EXCLUDED_TOP_LEVEL for part in path.parts)


def _source_files() -> list[Path]:
    files: set[Path] = set()
    for pattern in _CONTENT_PATTERNS:
        for match in _REPO_ROOT.glob(pattern):
            if match.is_file() and not _is_excluded(match):
                files.add(match)
    return sorted(files)


def _to_document(path: Path) -> Document:
    raw_text = path.read_text(encoding="utf-8")
    metadata: dict[str, Any] = {}
    content = raw_text
    suffix = path.suffix.lower()
    if suffix in _MD_EXTENSIONS:
        parsed = frontmatter.loads(raw_text)
        metadata = dict(parsed.metadata or {})
        content = parsed.content
        mime_type = "text/markdown"
    elif suffix == ".html":
        mime_type = "text/html"
    else:
        mime_type = "text/plain"
    return Document(
        rel_path=path.relative_to(_REPO_ROOT),
        raw_text=raw_text,
        metadata=metadata,
        content=content,
        mime_type=mime_type,
    )


def _load_documents() -> dict[str, Document]:
    docs: dict[str, Document] = {}
    for path in _source_files():
        doc = _to_document(path)
        uri = f"{_URI_PREFIX}{doc.rel_path.as_posix()}"
        docs[uri] = doc
    return docs


# Cache documents at module load time to avoid re-scanning on every request
_DOCUMENTS_CACHE: dict[str, Document] = _load_documents()

app = FastMCP("gundelsby.com")


@app.resource("gundelsby://{path}")
async def read_resource(path: str) -> str:
    """Read a document from the gundelsby.com site."""
    uri = f"{_URI_PREFIX}{path}"
    document = _DOCUMENTS_CACHE.get(uri)
    if not document:
        raise FileNotFoundError(f"Resource not found: {uri}")
    return document.raw_text


@app.tool(name="list_papers", description="Get the complete list of published academic papers")
async def list_papers() -> str:
    """Return the full list of published papers from papers.md."""
    uri = f"{_URI_PREFIX}papers.md"
    document = _DOCUMENTS_CACHE.get(uri)
    if not document:
        return "Papers page not found."
    return document.content


@app.tool(name="get_cv", description="Get Jan Henrik's curriculum vitae / resume")
async def get_cv() -> str:
    """Return the CV/resume content from cv.md."""
    uri = f"{_URI_PREFIX}cv.md"
    document = _DOCUMENTS_CACHE.get(uri)
    if not document:
        return "CV page not found."
    return document.content


@app.tool(name="list_talks", description="Get the list of public talks/presentations (in Norwegian: foredrag)")
async def list_talks() -> str:
    """Return the list of talks/presentations from foredrag.md."""
    uri = f"{_URI_PREFIX}foredrag.md"
    document = _DOCUMENTS_CACHE.get(uri)
    if not document:
        return "Talks page not found."
    return document.content


@app.tool(name="search", description="Case-insensitive search across site documents")
async def search(query: str) -> str:
    """Search for content across all site documents.

    Returns a concise list of matching documents with context snippets.
    """
    needle = query.strip().lower()
    if not needle:
        return "Empty query supplied."

    matches: list[dict[str, Any]] = []
    for document in _DOCUMENTS_CACHE.values():
        source_text = document.content if document.content else document.raw_text
        haystack = source_text.lower()
        idx = haystack.find(needle)
        if idx == -1:
            continue

        # Extract a shorter, more focused snippet
        start = max(idx - 60, 0)
        end = min(idx + 80, len(source_text))
        snippet = source_text[start:end].strip()
        # Clean up snippet - collapse multiple spaces/newlines
        snippet = " ".join(snippet.split())

        # Get document title if available
        title = document.metadata.get("title", "") if document.metadata else ""

        matches.append({
            "path": document.rel_path.as_posix(),
            "title": title,
            "snippet": snippet,
            "uri": f"{_URI_PREFIX}{document.rel_path.as_posix()}"
        })

    if not matches:
        return f"No matches found for '{query}'."

    # Format results concisely
    result_lines = [f"Found {len(matches)} match{'es' if len(matches) != 1 else ''} for '{query}':\n"]

    for i, match in enumerate(matches[:15], 1):  # Limit to 15 matches
        title_part = f" - {match['title']}" if match['title'] else ""
        result_lines.append(f"{i}. {match['path']}{title_part}")
        result_lines.append(f"   ...{match['snippet']}...")
        result_lines.append("")  # Empty line between matches

    if len(matches) > 15:
        result_lines.append(f"... and {len(matches) - 15} more matches")

    return "\n".join(result_lines)


def main() -> None:
    """Run the MCP server."""
    app.run()


if __name__ == "__main__":
    main()
