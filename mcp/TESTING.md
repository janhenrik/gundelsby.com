# Testing the gundelsby.com MCP Server

## Quick Test

Run the automated test script:

```bash
cd /Users/jhg/src/gundelsby.com/mcp
/Users/jhg/src/gundelsby.com/.venv/bin/python test_server.py
```

This will verify:
- Server initialization
- Document loading (should find ~24 documents from your Jekyll site)
- Search tool functionality
- Resource reading
- Error handling

## Manual Testing with MCP Inspector

The [MCP Inspector](https://github.com/modelcontextprotocol/inspector) is a web-based tool for testing MCP servers interactively.

### Install MCP Inspector

```bash
npm install -g @modelcontextprotocol/inspector
```

### Run the Inspector

```bash
npx @modelcontextprotocol/inspector /Users/jhg/src/gundelsby.com/.venv/bin/python -m gundelsby_mcp
```

This will:
1. Start the MCP Inspector web interface
2. Connect it to your server
3. Open a browser where you can test tools and resources interactively

### What to Test in Inspector

1. **Resources Tab**: Should show a resource template `gundelsby://{path}`
   - Try reading: `gundelsby://index.md`
   - Try reading: `gundelsby://_posts/2024-01-01-example.md`

2. **Tools Tab**: Should show the `search` tool
   - Try searching for keywords that appear in your posts
   - Test with: "Jekyll", "blog", author names, etc.

## Testing with Claude Desktop

To use this server with Claude Desktop, add to your config:

### macOS
Edit: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "gundelsby": {
      "command": "/Users/jhg/src/gundelsby.com/.venv/bin/python",
      "args": ["-m", "gundelsby_mcp"],
      "env": {}
    }
  }
}
```

### Test in Claude Desktop

After restarting Claude Desktop:
1. Look for the hammer icon (🔨) - indicates tools are available
2. Try asking: "Search for posts about [topic]"
3. Try: "Read the content from index.md"

## Manual JSON-RPC Testing

You can also test with raw JSON-RPC messages:

```bash
cd /Users/jhg/src/gundelsby.com

# Start the server
/Users/jhg/src/gundelsby.com/.venv/bin/python -m gundelsby_mcp
```

Then send JSON-RPC messages via stdin:

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}}}
```

```json
{"jsonrpc":"2.0","id":2,"method":"tools/list"}
```

```json
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"search","arguments":{"query":"Jekyll"}}}
```

## Available Endpoints

### Resources
- **URI Template**: `gundelsby://{path}`
- **Example paths**:
  - `index.md`
  - `_posts/2025-01-01-post.md`
  - `_includes/header.html`

### Tools
- **search**: Search across all site documents
  - Parameter: `query` (string)
  - Returns: Text snippets with matches

## Troubleshooting

### "No documents found"
- Check that you're running from the repo root
- Verify markdown files exist in `_posts/`, root directory, etc.

### "Module not found"
```bash
cd /Users/jhg/src/gundelsby.com/mcp
pip install -e .
```

### "Permission denied"
Make sure the venv Python is executable:
```bash
chmod +x /Users/jhg/src/gundelsby.com/.venv/bin/python
```

## Development

### View server logs
The server uses stdio transport, so logs go to stderr:

```bash
/Users/jhg/src/gundelsby.com/.venv/bin/python -m gundelsby_mcp 2>server.log
```

### Check loaded documents
```python
from gundelsby_mcp.server import _load_documents
docs = _load_documents()
for uri, doc in docs.items():
    print(f"{uri}: {doc.metadata.get('title', 'No title')}")
```
