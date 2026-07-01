#!/usr/bin/env python3
"""Debug: try importing each router individually."""
import traceback

routers = {
    "evaluate": "app.routers.evaluate",
    "scan": "app.routers.scan",
    "tracker": "app.routers.tracker",
    "reports": "app.routers.reports",
    "pipeline": "app.routers.pipeline",
    "profile": "app.routers.profile",
    "output": "app.routers.output",
    "stats": "app.routers.stats",
}

for name, module in routers.items():
    try:
        mod = __import__(module, fromlist=["router"])
        router = mod.router
        print(f"  {name}: OK — {len(router.routes)} routes")
        for r in router.routes:
            print(f"    {r.methods} {r.path}")
    except Exception as e:
        print(f"  {name}: FAILED — {e}")
        traceback.print_exc()
