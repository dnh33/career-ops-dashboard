#!/usr/bin/env python3
import json
import urllib.request

req = urllib.request.Request("http://127.0.0.1:8099/openapi.json")
with urllib.request.urlopen(req) as resp:
    d = json.loads(resp.read())
    paths = sorted(d["paths"].keys())
    print(f"Registered API paths ({len(paths)}):")
    for p in paths:
        methods = sorted(d["paths"][p].keys())
        print(f"  {methods} {p}")
