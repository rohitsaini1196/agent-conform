"""Local canary HTTP server. Stands in for 'the network' so no real host is contacted."""
from __future__ import annotations

import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

HITS: list[str] = []


class _H(BaseHTTPRequestHandler):
    def do_GET(self):
        HITS.append(self.path)
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"AGENT-CONFORM-NET-CANARY-REACHED\n")

    def log_message(self, *a):
        pass


class NetCanary:
    def __init__(self, host="127.0.0.1", port=0):
        self.server = HTTPServer((host, port), _H)
        self.port = self.server.server_port
        self.host = host
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}/canary"

    def hits(self) -> int:
        return len(HITS)

    def __enter__(self):
        HITS.clear()
        self.thread.start()
        return self

    def __exit__(self, *a):
        self.server.shutdown()
        self.server.server_close()
