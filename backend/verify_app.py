#!/usr/bin/env python3
"""Debug router registration issues."""
from app.main import app

# Check each router individually
for route in app.routes:
    if hasattr(route, 'path'):
        methods = getattr(route, 'methods', None)
        name = getattr(route, 'name', '?')
        print(f"  {methods} {route.path} ({name})")

# Check if routers have routes at all
from app.routers import evaluate, scan, tracker, reports, pipeline, profile, output, stats
print(f"\nRouter route counts:")
for r, name in [(evaluate, 'evaluate'), (scan, 'scan'), (tracker, 'tracker'),
                 (reports, 'reports'), (pipeline, 'pipeline'), (profile, 'profile'),
                 (output, 'output'), (stats, 'stats')]:
    print(f"  {name}: {len(r.router.routes)} routes")
    for route in r.router.routes:
        print(f"    {route.methods} {route.path}")
