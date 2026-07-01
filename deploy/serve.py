#!/usr/bin/env python3
"""Serve Career Ops Dashboard static files + proxy /api to backend."""

import http.server
import socketserver
import urllib.request
import urllib.error
import os
import sys

BACKEND = "http://localhost:18000"
DIST_DIR = "/opt/career-ops-dashboard/frontend/dist"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8083


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIST_DIR, **kwargs)

    def do_GET(self):
        if self.path.startswith("/api/"):
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

    def proxy_request(self, method):
        target = BACKEND + self.path
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        req = urllib.request.Request(target, data=body, method=method)
        if body:
            req.add_header("Content-Type", self.headers.get("Content-Type", "application/json"))

        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                self.send_response(resp.status)
                for key, val in resp.getheaders():
                    if key.lower() not in ("transfer-encoding", "connection"):
                        self.send_header(key, val)
                self.end_headers()
                self.wfile.write(resp.read())
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            self.send_response(502)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(f'{{"error": "{str(e)}"}}'.encode())

    def log_message(self, format, *args):
        # Suppress request logs to keep output clean
        pass


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    os.chdir(DIST_DIR)
    with ReusableTCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"Career Ops Dashboard serving on http://0.0.0.0:{PORT}")
        print(f"API proxy: /api -> {BACKEND}")
        print(f"Static files: {DIST_DIR}")
        httpd.serve_forever()
