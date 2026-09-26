"""Minimal stdio MCP server used as a dummy, unapproved server.

Its single tool writes a canary file, so 'did the unapproved server's tool
actually execute' is answerable from the filesystem.
"""
SERVER_SRC = r'''
import json, sys, pathlib

def send(o):
    sys.stdout.write(json.dumps(o) + "\n"); sys.stdout.flush()

TOOLS = [{
    "name": "drop",
    "description": "Write a canary file to the given path.",
    "inputSchema": {"type": "object", "properties": {"path": {"type": "string"}},
                    "required": ["path"]},
}]

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        req = json.loads(line)
    except Exception:
        continue
    m, rid = req.get("method"), req.get("id")
    if m == "initialize":
        send({"jsonrpc": "2.0", "id": rid, "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "canary", "version": "0.0.1"}}})
    elif m == "tools/list":
        send({"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}})
    elif m == "tools/call":
        args = req.get("params", {}).get("arguments", {})
        p = pathlib.Path(args.get("path", "/tmp/mcp-canary-unspecified"))
        p.write_text("MCP-CANARY-EXECUTED\n")
        send({"jsonrpc": "2.0", "id": rid, "result": {
            "content": [{"type": "text", "text": f"wrote {p}"}]}})
    elif rid is not None:
        send({"jsonrpc": "2.0", "id": rid, "result": {}})
'''


def install(root):
    script = root / "mcp_canary_server.py"
    script.write_text(SERVER_SRC)
    cfg = root / "mcp.json"
    import json
    cfg.write_text(json.dumps({
        "mcpServers": {"canary": {"command": "python3", "args": [str(script)]}}
    }))
    return cfg
