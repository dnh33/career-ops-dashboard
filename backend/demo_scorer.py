"""Demo: score a CV and print the result."""
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from app.services.market_scorer import MarketScorer

scorer = MarketScorer("/opt/career-ops-dashboard/data/research/cv-optimization-rules.md")

cv = """John Hansen
Frontend Developer, Copenhagen
Personal Profile: Experienced in frontend development with AI integration. React TypeScript production.
Work Experience: Senior Frontend Developer - React, TypeScript, JavaScript, Git, HTML, CSS, Design Systems,
Accessibility, REST API, Node.js, Next.js, Jest, Production, Scale, Performance, Reduced, Improved, Delivered
Skills: React TypeScript Git HTML CSS Docker Python LangChain AWS RAG Agents LlamaIndex
Education: CS Degree
Languages: Danish C2 English C2
Interests: Hiking, photography"""

result = scorer.score_cv(cv, "FE-DEV")
print(json.dumps(result, indent=2, ensure_ascii=False))
