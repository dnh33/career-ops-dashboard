#!/usr/bin/env python3
"""Serve Career Ops Dashboard static files + proxy /api to backend.

Fixes: CLOSE-WAIT deadlock from urllib leaving connections half-closed.
Uses ThreadingMixin for concurrent requests and proper connection cleanup.

SSE Support: Special handling for /api/evaluate/*/stream endpoints
to forward Server-Sent Events without buffering.
"""

import http.server
import socketserver
import urllib.request
import urllib.error
import os
import sys
import socket
import threading
import time

BACKEND = "http://localhost:18000"
DIST_DIR = "/opt/career-ops-dashboard/frontend/dist/client"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8083
API_KEY = os.environ.get("CAREER_OPS_API_KEY", "")

# SSE endpoints that need streaming proxy (no buffering)
SSE_PATHS = ("/api/evaluate/", "/stream")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIST_DIR, **kwargs)

    def is_sse_endpoint(self, path: str) -> bool:
        """Check if path is an SSE stream endpoint."""
        return any(sse_path in path for sse_path in SSE_PATHS) and path.endswith("/stream")

    def do_GET(self):
        if self.path.startswith("/api/"):
            if self.is_sse_endpoint(self.path):
                self.proxy_sse_stream("GET")
            else:
                self.proxy_request("GET")
        else:
            super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/"):
            self.proxy_request("POST")
        else:
            self.send_error(405)

    def do_PUT(self):
        if self.path.startswith("/api/"):
            self.proxy_request("PUT")
        else:
            self.send_error(405)

    def do_DELETE(self):
        if self.path.startswith("/api/"):
            self.proxy_request("DELETE")
        else:
            self.send_error(405)

    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-API-Key")
        self.end_headers()

    def proxy_request(self, method):
        """Proxy a regular (non-streaming) request to backend."""
        target = BACKEND + self.path
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        req = urllib.request.Request(target, data=body, method=method)
        if body:
            req.add_header("Content-Type", self.headers.get("Content-Type", "application/json"))
        # Always inject API key from server env (frontend doesn't know it)
        if API_KEY:
            req.add_header("X-API-Key", API_KEY)

        try:
            # Use urlopen with explicit response closing via context manager
            resp = urllib.request.urlopen(req, timeout=30)
            try:
                self.send_response(resp.status)
                for key, val in resp.getheaders():
                    if key.lower() not in ("transfer-encoding", "connection"):
                        self.send_header(key, val)
                # Ensure CORS headers
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                # Read all data then write — ensures we consume the full response
                data = resp.read()
                self.wfile.write(data)
                self.wfile.flush()
            finally:
                resp.close()
        except urllib.error.HTTPError as e:
            try:
                self.send_response(e.code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(e.read())
                self.wfile.flush()
            finally:
                e.close()
        except Exception as e:
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(f'{{"error": "{str(e)}"}}'.encode())
            self.wfile.flush()

    def proxy_sse_stream(self, method):
        """Proxy SSE stream from backend WITHOUT buffering.
        Streams chunk-by-chunk to maintain real-time delivery.
        """
        target = BACKEND + self.path
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        req = urllib.request.Request(target, data=body, method=method)
        if body:
            req.add_header("Content-Type", self.headers.get("Content-Type", "application/json"))
        if API_KEY:
            req.add_header("X-API-Key", API_KEY)

        try:
            # Open connection to backend
            resp = urllib.request.urlopen(req, timeout=300)  # Long timeout for SSE
            try:
                # Send response headers immediately - no buffering!
                self.send_response(resp.status)
                for key, val in resp.getheaders():
                    if key.lower() not in ("transfer-encoding", "connection"):
                        self.send_header(key, val)
                # Critical SSE headers - must not be buffered by nginx/proxy
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Connection", "keep-alive")
                self.send_header("X-Accel-Buffering", "no")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.flush()

                # Stream response body chunk by chunk
                # Read in small chunks to maintain streaming
                while True:
                    chunk = resp.read(4096)  # Read 4KB at a time
                    if not chunk:
                        break
                    try:
                        self.wfile.write(chunk)
                        self.wfile.flush()
                    except (BrokenPipeError, ConnectionResetError):
                        # Client disconnected - stop streaming
                        break
            finally:
                resp.close()
        except urllib.error.HTTPError as e:
            try:
                self.send_response(e.code)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(e.read())
                self.wfile.flush()
            finally:
                e.close()
        except Exception as e:
            # Client may have disconnected
            pass

    def log_message(self, format, *args):
        pass


class ReuseTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True  # Threads die with main process

    def process_request(self, request, client_address):
        """Ensure socket is properly closed after handling."""
        try:
            self.finish_request(request, client_address)
        except Exception:
            self.handle_error(request, client_address)
        finally:
            self.shutdown_request(request)


if __name__ == "__main__":
    os.chdir(DIST_DIR)
    with ReuseTCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"Career Ops Dashboard serving on http://0.0.0.0:{PORT}")
        print(f"API proxy: /api -> {BACKEND}")
        print(f"Static files: {DIST_DIR}")
        httpd.serve_forever()
