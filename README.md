# Career Ops Dashboard

Web dashboard for the [career-ops](https://github.com) CLI — visualize job applications, pipeline status, evaluations, and reports.

## Quick Start

```bash
# 1. Install dependencies
./scripts/setup.sh

# 2. Start both servers
./scripts/start.sh

# 3. Open http://localhost:4321
```

## Architecture

- **Frontend**: Astro 7 + Tailwind CSS v4 (dark observatory theme)
- **Backend**: FastAPI (Python 3.11+)
- **Data**: Reads from `/opt/career-ops/` (existing career-ops CLI data tree)

## License
MIT
