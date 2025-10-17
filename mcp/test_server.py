#!/usr/bin/env python3
"""Test script for the gundelsby.com MCP server."""

import asyncio
import json
import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from gundelsby_mcp.server import app, _load_documents


async def test_server():
    """Test the MCP server functionality."""
    print("=" * 60)
    print("Testing gundelsby.com MCP Server")
    print("=" * 60)

    # Test 1: Check server initialization
    print("\n1. Server Initialization")
    print(f"   ✓ Server name: {app.name}")
    print(f"   ✓ Server initialized successfully")

    # Test 2: Check document loading
    print("\n2. Document Loading")
    try:
        documents = _load_documents()
        print(f"   ✓ Loaded {len(documents)} documents")

        # Show first few documents
        print("\n   Sample documents:")
        for i, (uri, doc) in enumerate(list(documents.items())[:5]):
            title = doc.metadata.get("title", "No title") if doc.metadata else "No title"
            print(f"   - {uri}")
            print(f"     Title: {title}")
            if i >= 4:  # Show max 5
                break

        if len(documents) > 5:
            print(f"   ... and {len(documents) - 5} more")

    except Exception as e:
        print(f"   ✗ Error loading documents: {e}")
        return False

    # Test 3: Test the search tool
    print("\n3. Testing Search Tool")
    try:
        from gundelsby_mcp.server import search

        # Test search
        result = await search("Jan-Henrik")
        print(f"   ✓ Search completed")
        print(f"   Result preview: {result[:200]}...")

    except Exception as e:
        print(f"   ✗ Search failed: {e}")
        return False

    # Test 4: Test the resource endpoint
    print("\n4. Testing Resource Endpoint")
    try:
        from gundelsby_mcp.server import read_resource

        # Get the first document to test
        if documents:
            first_uri = list(documents.keys())[0]
            # Extract path from URI (remove gundelsby:// prefix)
            path = first_uri.replace("gundelsby://", "")

            content = await read_resource(path)
            print(f"   ✓ Read resource: {path}")
            print(f"   Content preview: {content[:200]}...")
        else:
            print("   ⚠ No documents to test")

    except Exception as e:
        print(f"   ✗ Resource read failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Test 5: Test with non-existent resource
    print("\n5. Testing Error Handling")
    try:
        await read_resource("nonexistent/file.md")
        print("   ✗ Should have raised FileNotFoundError")
        return False
    except FileNotFoundError:
        print("   ✓ Correctly raises FileNotFoundError for missing files")
    except Exception as e:
        print(f"   ✗ Unexpected error: {e}")
        return False

    print("\n" + "=" * 60)
    print("✓ All tests passed!")
    print("=" * 60)
    print("\nTo use the server with an MCP client:")
    print("  python -m gundelsby_mcp")
    print("\nOr from the venv:")
    print("  /Users/jhg/src/gundelsby.com/.venv/bin/python -m gundelsby_mcp")
    return True


if __name__ == "__main__":
    success = asyncio.run(test_server())
    sys.exit(0 if success else 1)
