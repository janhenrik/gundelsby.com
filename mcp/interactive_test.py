#!/usr/bin/env python3
"""Interactive test client for the MCP server."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from gundelsby_mcp.server import search, read_resource, _load_documents


async def main():
    """Run interactive tests."""
    print("🧪 MCP Server Interactive Test")
    print("=" * 60)

    # Load documents first
    docs = _load_documents()
    print(f"\n✓ Loaded {len(docs)} documents\n")

    while True:
        print("\nChoose a test:")
        print("  1. Search for content")
        print("  2. Read a resource")
        print("  3. List all resources")
        print("  4. Exit")
        print()

        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            query = input("\nEnter search query: ").strip()
            if query:
                print("\nSearching...")
                result = await search(query)
                print("\n" + "─" * 60)
                print(result)
                print("─" * 60)

        elif choice == "2":
            print("\nAvailable resources (showing first 10):")
            for i, uri in enumerate(list(docs.keys())[:10]):
                path = uri.replace("gundelsby://", "")
                print(f"  {i+1}. {path}")

            path = input("\nEnter resource path (or number): ").strip()

            # Handle numeric selection
            if path.isdigit():
                idx = int(path) - 1
                if 0 <= idx < min(10, len(docs)):
                    uri = list(docs.keys())[idx]
                    path = uri.replace("gundelsby://", "")

            try:
                print(f"\nReading: {path}")
                content = await read_resource(path)
                print("\n" + "─" * 60)
                # Show first 500 chars
                if len(content) > 500:
                    print(content[:500])
                    print(f"\n... ({len(content) - 500} more characters)")
                else:
                    print(content)
                print("─" * 60)
                print(f"\nTotal length: {len(content)} characters")
            except FileNotFoundError:
                print(f"\n✗ Resource not found: {path}")

        elif choice == "3":
            print(f"\nAll {len(docs)} resources:")
            print("─" * 60)
            for uri, doc in sorted(docs.items()):
                path = uri.replace("gundelsby://", "")
                title = doc.metadata.get("title", "") if doc.metadata else ""
                if title:
                    print(f"  {path} - {title}")
                else:
                    print(f"  {path}")
            print("─" * 60)

        elif choice == "4":
            print("\nGoodbye! 👋")
            break

        else:
            print("\n✗ Invalid choice")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye! 👋")
        sys.exit(0)
