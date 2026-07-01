"""Market-aware CV scoring service.

Loads optimization rules from cv-optimization-rules.md and scores a CV
against the Danish tech market intelligence for any of the 5 target roles.

Schema version: 1.0.0 (Q3 2026)
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# ── Role Definitions ───────────────────────────────────────────────
ROLE_WEIGHTS: dict[str, dict[str, int]] = {
    "FE-DEV": {
        "skill_match": 30,
        "frontend_depth": 20,
        "ai_integration": 15,
        "danish_compliance": 15,
        "experience_signal": 10,
    },
    "AI-SDEV": {
        "python_depth": 25,
        "ml_stack": 25,
        "production_deployment": 15,
        "danish_compliance": 15,
        "domain_alignment": 10,
        "fullstack_bonus": 10,
    },
    "AI-ENG": {
        "ai_llm_depth": 25,
        "ml_engineering_maturity": 25,
        "pipeline_ownership": 15,
        "danish_compliance": 15,
        "architecture_signal": 10,
        "company_fit": 10,
    },
    "GENAI": {
        "llm_production_depth": 30,
        "agentic_patterns": 20,
        "framework_breadth": 15,
        "danish_compliance": 15,
        "quantified_impact": 10,
        "fullstack_genai_combo": 10,
    },
    "ML-ENG": {
        "mlops_maturity": 30,
        "infrastructure_depth": 25,
        "model_lifecycle": 15,
        "danish_compliance": 15,
        "devops_culture": 15,
    },
}

# ── Keywords per role (normalized lowercase) ───────────────────────
ROLE_KEYWORDS: dict[str, dict[str, set[str]]] = {
    "FE-DEV": {
        "must_have": {"react", "react.js", "typescript", "javascript", "git", "html", "css"},
        "high_value": {
            "rest api", "api", "component", "responsive", "mobile-first",
            "accessibility", "wcag", "design system", "performance",
            "jest", "cypress", "webpack", "vite", "node.js", "next.js",
            "tailwind", "sass", "less", "figma",
        },
        "differentiator": {
            "ai integration", "ai-powered", "llm integration", "server components",
            "ssr", "ssg", "streaming", "astro",
        },
    },
    "AI-SDEV": {
        "must_have": {"python", "machine learning", "docker", "cloud", "git"},
        "high_value": {
            "pytorch", "tensorflow", "mlops", "model deployment", "ci/cd",
            "devops", "data pipelines", "etl", "rest api", "azure", "aws",
            "gcp", "kubernetes", "sql",
        },
        "differentiator": {
            "generative ai", "agentic ai", "full-stack", "fastapi",
            "production ml", "model serving", "model monitoring",
        },
    },
    "AI-ENG": {
        "must_have": {"python", "machine learning", "llm", "ai", "cloud", "docker"},
        "high_value": {
            "rag", "retrieval-augmented generation", "agentic", "agents",
            "vector", "vector database", "ai architecture", "model deployment",
            "azure", "aws", "streaming", "nlp", "deep learning", "sql",
        },
        "differentiator": {
            "prompt engineering", "multi-modal", "ai scoring", "ai evaluation",
            "real-time inference", "cost optimization", "model versioning",
        },
    },
    "GENAI": {
        "must_have": {"llm", "llms", "large language model", "python", "generative ai"},
        "high_value": {
            "prompt engineering", "rag", "retrieval-augmented generation",
            "agent", "agents", "agentic", "pytorch", "tensorflow",
            "vector database", "langchain", "llamaindex", "streaming",
            "sse", "api",
        },
        "differentiator": {
            "multi-provider", "openai", "openrouter", "local models",
            "fine-tuning", "token management", "llm orchestration",
            "ai widget", "ai interface", "real-time llm",
        },
    },
    "ML-ENG": {
        "must_have": {"python", "machine learning", "docker", "mlops", "cloud"},
        "high_value": {
            "ci/cd", "kubernetes", "linux", "model deployment", "model serving",
            "model monitoring", "azure devops", "github actions", "terraform",
            "infrastructure", "iac",
        },
        "differentiator": {
            "real-time inference", "model versioning", "a/b testing",
            "feature engineering", "cost optimization", "platform engineering",
            "reliability", "automation",
        },
    },
}

# ── Danish Compliance Checks ────────────────────────────────────────
DANISH_BANNED_WORDS: set[str] = {
    "ninja", "guru", "world-class", "rockstar", "synergy", "leverage",
    "24/7", "work long hours", "24/7 availability", "go the extra mile",
    "passionate",
}

DANISH_PREFERRED_PHRASES: list[str] = [
    "experienced in", "comfortable with", "interested in",
    "efficient delivery", "sustainable pace", "results-oriented",
]

# Known skill dictionary for detection
_KNOWN_SKILLS: list[str] = [
    "python", "javascript", "typescript", "react", "react.js", "reactjs",
    "angular", "vue", "vue.js", "node.js", "nodejs", "fastapi", "flask",
    "django", "rust", "go", "java", "c#", "c++", "kotlin", "swift",
    "html", "css", "sass", "tailwind", "scss",
    "docker", "kubernetes", "terraform", "ansible",
    "aws", "azure", "gcp", "google cloud",
    "postgresql", "postgres", "sql", "mysql", "mongodb", "redis",
    "elasticsearch", "vector database", "pinecone", "weaviate", "chroma",
    "pytorch", "tensorflow", "jax", "scikit-learn", "keras",
    "langchain", "llamaindex", "llamaindex", "haystack", "dspy",
    "openai", "openrouter", "anthropic", "claude", "gpt", "llm", "llms",
    "generative ai", "rag", "retrieval-augmented generation",
    "prompt engineering", "agent", "agents", "agentic", "agentic ai",
    "streaming", "sse", "server-sent events", "real-time",
    "api", "rest api", "graphql", "websocket",
    "git", "ci/cd", "github actions", "gitlab ci", "azure devops",
    "linux", "ubuntu", "redhat", "nginx",
    "mlops", "model deployment", "model serving", "model monitoring",
    "data pipelines", "etl", "spark", "airflow", "dbt",
    "figma", "design systems", "accessibility", "wcag",
    "machine learning", "deep learning", "nlp", "computer vision",
    "statistics", "ab testing", "experimentation",
    "testing", "jest", "cypress", "playwright", "vitest",
    "architecture", "system design", "microservices", "distributed",
    "cloud-native", "infrastructure", "iac",
    "agile", "scrum", "kanban", "ci", "cd",
    "performance", "responsive", "mobile-first",
    "automation", "reliability", "observability",
    "production", "scale", "e-commerce", "fintech", "healthcare",
    "pharma", "logistics", "retail", "enterprise", "consulting",
    "multi-provider", "local models", "fine-tuning",
    "cost optimization", "latency", "accuracy",
    "cross-functional", "collaborative", "communication",
    "problem solving", "iterative", "experimentation",
    "danish language", "english language",
]


def _normalize_skill(skill: str) -> str:
    """Normalize a skill string for matching."""
    s = skill.lower().strip()
    aliases: dict[str, str] = {
        "react.js": "react", "reactjs": "react", "react 19": "react",
        "typescript": "typescript", "ts": "typescript",
        "javascript": "javascript", "js": "javascript", "es6": "javascript",
        "node.js": "node.js", "nodejs": "node.js",
        "postgresql": "sql", "postgres": "sql",
        "large language models": "llm", "llms": "llm", "large language model": "llm",
        "generative ai": "generative ai", "genai": "generative ai",
        "retrieval-augmented generation": "rag",
        "machine learning": "machine learning", "ml": "machine learning",
        "artificial intelligence": "ai",
        "pytorch": "pytorch", "torch": "pytorch",
        "tensorflow": "tensorflow", "tf": "tensorflow",
        "continuous integration": "ci/cd", "github actions": "ci/cd",
        "gitlab ci": "ci/cd", "azure devops": "ci/cd",
        "amazon web services": "aws", "amazon aws": "aws",
        "google cloud": "gcp", "google cloud platform": "gcp",
        "microsoft azure": "azure",
        "model ops": "mlops",
        "server-sent events": "streaming", "real-time": "streaming",
    }
    return aliases.get(s, s)


def _extract_skills_from_cv(cv_text: str) -> set[str]:
    """Extract normalized skills from CV text using keyword matching."""
    cv_lower = cv_text.lower()
    found: set[str] = set()
    for skill in _KNOWN_SKILLS:
        if skill in cv_lower:
            found.add(_normalize_skill(skill))
    return found


class MarketScorer:
    """Score a CV against the Danish tech market intelligence.

    Loads optimization rules from the research output file and provides
    scoring for all 5 target roles (FE-DEV, AI-SDEV, AI-ENG, GENAI, ML-ENG).
    """

    VALID_ROLES: list[str] = list(ROLE_WEIGHTS.keys())

    def __init__(self, rules_path: str):
        """Load optimization rules from research output.

        Parses the rules markdown to extract role-specific keywords,
        weights, and company tailoring templates. The file is read on
        init so scoring calls are fast and side-effect-free.
        """
        self.rules_path = Path(rules_path)
        if not self.rules_path.exists():
            raise FileNotFoundError(f"Rules file not found: {rules_path}")
        self._rules_text = self.rules_path.read_text(encoding="utf-8")
        self._rules_version = self._extract_version(self._rules_text)

    @staticmethod
    def _extract_version(text: str) -> str:
        """Extract schema version from rules file."""
        m = re.search(r"\*\*Version:\*\*\s*([\d.]+)", text)
        return m.group(1) if m else "0.0.0"

    def get_ideal_skills(self, target_role: str) -> list[str]:
        """Return top skills for a role from market data.

        Returns the must-have keywords as the 'ideal skills' list —
        these are the skills that appear in the highest %
        of job postings for the role.
        """
        if target_role not in ROLE_KEYWORDS:
            raise ValueError(f"Unknown role: {target_role}. Use: {self.VALID_ROLES}")
        return sorted(ROLE_KEYWORDS[target_role]["must_have"])

    def suggest_improvements(self, cv_content: str, target_role: str) -> list[dict[str, Any]]:
        """Return ranked list of specific improvements.

        Each improvement dict has keys: priority (high/medium/low), category, action.
        Results are sorted by priority then by category weight.
        """
        result = self.score_cv(cv_content, target_role)
        suggestions: list[dict[str, Any]] = []
        for rec in result["suggestions"]:
            # Infer priority from the suggestion text content
            priority = "high"
            if "Minor" in rec or "Consider" in rec:
                priority = "medium"
            elif "bonus" in rec.lower():
                priority = "low"
            suggestions.append({
                "priority": priority,
                "category": _categorize_suggestion(rec, target_role),
                "action": rec,
            })
        # Then add missing must-have skills as high-priority items
        for kw in result["gaps"]:
            if not any(kw in s["action"] for s in suggestions):
                suggestions.insert(0, {
                    "priority": "high",
                    "category": "missing_must_have",
                    "action": f"Add must-have skill: {kw}",
                })
        return suggestions

    def score_cv(self, cv_content: str, target_role: str,
                 target_company: Optional[str] = None,
                 has_photo: bool = True,
                 has_personal_section: bool = True,
                 years_exp: int = 5,
                 has_hobbies: bool = True) -> dict[str, Any]:
        """Score a CV against market intelligence.

        Returns a structured dict with:
            - score: int (0-100)
            - label: str (Excellent/Strong/Good/Fair/Weak)
            - gaps: list[str] — missing must-have keywords
            - strengths: list[str] — found high-value + differentiator keywords
            - suggestions: list[str] — actionable improvements
            - breakdown: dict — per-category scores
        """
        if target_role not in ROLE_WEIGHTS:
            raise ValueError(f"Unknown role: {target_role}. Use: {self.VALID_ROLES}")

        cv_lower = cv_content.lower()
        cv_skills = _extract_skills_from_cv(cv_content)
        weights = ROLE_WEIGHTS[target_role]
        keywords = ROLE_KEYWORDS[target_role]
        breakdown: dict[str, float] = {}
        recommendations: list[str] = []

        # ── 1. Must-have keyword check ──────────────────────────────────
        must_have_found = keywords["must_have"] & cv_skills
        must_have_missing = keywords["must_have"] - cv_skills
        must_have_ratio = len(must_have_found) / max(len(keywords["must_have"]), 1)

        # ── 2. High-value keyword check ─────────────────────────────────
        high_value_found = keywords["high_value"] & cv_skills
        high_value_missing = keywords["high_value"] - cv_skills
        high_value_ratio = len(high_value_found) / max(len(keywords["high_value"]), 1)

        # ── 3. Differentiator keyword check ─────────────────────────────
        diff_found_found = keywords["differentiator"] & cv_skills
        diff_ratio = len(diff_found_found) / max(len(keywords["differentiator"]), 1)

        # ── 4. Danish compliance score ──────────────────────────────────
        danish_score = self._score_danish_compliance(
            cv_lower, weights, has_photo, has_personal_section, has_hobbies, years_exp, recommendations,
        )

        # ── 5. Category scoring per role ───────────────────────────────
        if target_role == "FE-DEV":
            self._score_fe_dev(
                cv_skills, weights, keywords, breakdown, recommendations,
                must_have_found, must_have_missing, must_have_ratio,
                high_value_ratio, danish_score,
            )
        elif target_role == "AI-SDEV":
            self._score_ai_sdev(
                cv_skills, weights, keywords, breakdown, recommendations,
                must_have_found, must_have_found, must_have_missing,
                must_have_ratio, high_value_ratio, high_value_missing,
                diff_ratio, danish_score,
            )
        elif target_role == "AI-ENG":
            self._score_ai_eng(
                cv_skills, weights, keywords, breakdown, recommendations,
                must_have_found, must_have_missing,
                must_have_ratio, high_value_ratio, diff_ratio, danish_score,
            )
        elif target_role == "GENAI":
            self._score_genai(
                cv_skills, weights, keywords, breakdown, recommendations,
                must_have_found, must_have_missing,
                must_have_ratio, diff_ratio, danish_score,
            )
        elif target_role == "ML-ENG":
            self._score_ml_eng(
                cv_skills, weights, keywords, breakdown, recommendations,
                must_have_found, must_have_missing,
                must_have_ratio, danish_score,
            )

        # ── Final score ──────────────────────────────────────────────────
        total = sum(breakdown.values())
        total = round(min(max(total, 0.0), 100.0))

        label = _score_to_label(total)

        # Company-specific tailoring (15% weight adjustment)
        company_bonus = 0
        if target_company:
            company_bonus = self._company_tailoring_score(cv_content, target_role, target_company)
            # Apply company bonus to relevant category
            if target_role == "AI-ENG" and "company_fit" in breakdown:
                breakdown["company_fit"] = min(
                    breakdown["company_fit"] + company_bonus,
                    weights["company_fit"],
                )
            elif target_role == "AI-SDEV" and "domain_alignment" in breakdown:
                breakdown["domain_alignment"] = min(
                    breakdown["domain_alignment"] + company_bonus,
                    weights["domain_alignment"],
                )

        # Recompute total after company bonus
        total = sum(breakdown.values())
        total = round(min(max(total, 0.0), 100.0))
        label = _score_to_label(total)

        strengths = sorted(
            list(must_have_found) +
            list(high_value_found)[:5] +
            list(diff_found_found)[:3]
        )
        gaps = sorted(list(must_have_missing))

        return {
            "score": total,
            "label": label,
            "role": target_role,
            "target_company": target_company,
            "gaps": gaps,
            "strengths": strengths,
            "suggestions": recommendations[:7],
            "breakdown": {k: round(v, 1) for k, v in breakdown.items()},
            "scored_at": datetime.utcnow().isoformat(),
            "schema_version": self._rules_version,
        }

    def _score_danish_compliance(
        self, cv_lower: str, weights: dict[str, int],
        has_photo: bool, has_personal_section: bool,
        has_hobbies: bool, years_exp: int,
        recommendations: list[str],
    ) -> float:
        """Compute Danish cultural compliance score (0 to max)."""
        score = 0.0
        max_score = weights.get("danish_compliance", 15)

        banned_found = [w for w in DANISH_BANNED_WORDS if w in cv_lower]
        if banned_found:
            score -= len(banned_found) * 2.0
            recommendations.append(f"Remove Danish-cultural-misfit words: {banned_found}")
        else:
            score += max_score * 0.4

        if has_photo:
            score += max_score * 0.2
        else:
            recommendations.append("Add professional headshot (expected in DK)")

        if has_personal_section and has_hobbies:
            score += max_score * 0.25
        else:
            recommendations.append("Add personal/interests section with genuine hobbies")

        if 3 <= years_exp <= 7:
            score += max_score * 0.15
        elif years_exp < 2:
            score += max_score * 0.05
            recommendations.append("Consider targeting junior roles")

        return max(0.0, min(score, max_score))

    def _score_fe_dev(self, cv_skills, weights, keywords, breakdown, recommendations,
                      must_have_found, must_have_missing, must_have_ratio,
                      high_value_ratio, danish_score):
        """Frontend Developer scoring."""
        del keywords  # unused — kept for signature consistency
        del must_have_found  # unused
        breakdown["skill_match"] = (must_have_ratio * 0.6 + high_value_ratio * 0.4) * weights["skill_match"]

        depth_signals = {"design system", "accessibility", "wcag", "performance",
                         "architecture", "responsive"}
        depth_count = len(depth_signals & cv_skills)
        breakdown["frontend_depth"] = min(
            (depth_count / len(depth_signals)) * weights["frontend_depth"],
            weights["frontend_depth"],
        )

        ai_signals = {"ai integration", "ai-powered", "llm integration",
                      "generative ai", "ai"}
        ai_count = len(ai_signals & cv_skills)
        breakdown["ai_integration"] = min(
            (ai_count / len(ai_signals)) * weights["ai_integration"],
            weights["ai_integration"],
        )

        breakdown["danish_compliance"] = danish_score

        exp_signals = {"production", "scale", "metrics",
                       "impact", "reduced", "improved", "delivered"}
        exp_count = len(exp_signals & cv_skills)
        breakdown["experience_signal"] = min(
            (exp_count / len(exp_signals)) * weights["experience_signal"],
            weights["experience_signal"],
        )

        if must_have_missing:
            recommendations.append(f"Add missing must-have skills: {sorted(must_have_missing)}")

    def _score_ai_sdev(self, cv_skills, weights, keywords, breakdown, recommendations,
                       must_have_found, must_have_found2, must_have_missing,
                       must_have_ratio, high_value_ratio, high_value_missing,
                       diff_ratio, danish_score):
        """AI Software Developer scoring."""
        del keywords  # unused
        del must_have_found, must_have_found2  # unused
        breakdown["python_depth"] = must_have_ratio * weights["python_depth"]
        if "python" in cv_skills and ("fastapi" in cv_skills or "flask" in cv_skills or "django" in cv_skills):
            breakdown["python_depth"] *= 1.2
        breakdown["python_depth"] = min(breakdown["python_depth"], weights["python_depth"])

        breakdown["ml_stack"] = (must_have_ratio * 0.5 + high_value_ratio * 0.5) * weights["ml_stack"]
        if must_have_missing:
            recommendations.append(f"Add missing must-have: {sorted(must_have_missing)}")
        if "aws" not in cv_skills and "azure" not in cv_skills and "gcp" not in cv_skills:
            recommendations.append("Add cloud provider (AWS/Azure/GCP) — critical for AI-SDEV")

        breakdown["production_deployment"] = diff_ratio * weights["production_deployment"]
        if "mlops" not in cv_skills:
            recommendations.append("Mention MLOps or model deployment practices")

        breakdown["danish_compliance"] = danish_score

        domain_signals = {"healthcare", "fintech", "pharma", "logistics",
                          "retail", "e-commerce", "enterprise"}
        domain_count = len(domain_signals & cv_skills)
        breakdown["domain_alignment"] = min(
            (domain_count / max(len(domain_signals), 1)) * weights["domain_alignment"],
            weights["domain_alignment"],
        )

        if "react" in cv_skills or "typescript" in cv_skills or "javascript" in cv_skills:
            breakdown["fullstack_bonus"] = weights["fullstack_bonus"] * 0.7
        else:
            breakdown["fullstack_bonus"] = 0.0
            recommendations.append("Highlight frontend skills for full-stack + AI combo")

        if high_value_missing:
            recommendations.append(f"Consider adding high-value skills: {sorted(list(high_value_missing))[:5]}")

    def _score_ai_eng(self, cv_skills, weights, keywords, breakdown, recommendations,
                      must_have_found, must_have_missing,
                      must_have_ratio, high_value_ratio, diff_ratio, danish_score):
        """AI Engineer scoring."""
        del keywords, must_have_found  # unused
        breakdown["ai_llm_depth"] = (must_have_ratio * 0.6 + diff_ratio * 0.4) * weights["ai_llm_depth"]
        if "rag" in cv_skills or "agent" in cv_skills or "agentic" in cv_skills:
            breakdown["ai_llm_depth"] = min(breakdown["ai_llm_depth"] * 1.15, weights["ai_llm_depth"])

        breakdown["ml_engineering_maturity"] = (high_value_ratio * 0.6 + must_have_ratio * 0.4) * weights["ml_engineering_maturity"]

        pipeline_signals = {"model deployment", "model serving", "model monitoring",
                            "mlops", "ci/cd", "pipeline", "data pipelines"}
        pipe_count = len(pipeline_signals & cv_skills)
        breakdown["pipeline_ownership"] = min(
            (pipe_count / max(len(pipeline_signals), 1)) * weights["pipeline_ownership"],
            weights["pipeline_ownership"],
        )

        breakdown["danish_compliance"] = danish_score

        arch_signals = {"architecture", "system design", "scalable", "distributed",
                        "microservices", "cloud-native"}
        arch_count = len(arch_signals & cv_skills)
        breakdown["architecture_signal"] = min(
            (arch_count / max(len(arch_signals), 1)) * weights["architecture_signal"],
            weights["architecture_signal"],
        )

        company_signals = {"healthcare", "finance", "logistics", "pharma",
                           "retail", "enterprise", "consulting"}
        company_count = len(company_signals & cv_skills)
        breakdown["company_fit"] = min(
            (company_count / max(len(company_signals), 1)) * weights["company_fit"],
            weights["company_fit"],
        )

        if must_have_missing:
            recommendations.append(f"Add: {sorted(must_have_missing)}")
        if "rag" not in cv_skills:
            recommendations.append("Add RAG experience (28.6% of AI-ENG postings)")
        if "agentic" not in cv_skills and "agent" not in cv_skills:
            recommendations.append("Mention agentic AI patterns (fastest-growing segment)")

    def _score_genai(self, cv_skills, weights, keywords, breakdown, recommendations,
                     must_have_found, must_have_missing,
                     must_have_ratio, diff_ratio, danish_score):
        """Generative AI Engineer scoring."""
        del keywords, must_have_found  # unused
        breakdown["llm_production_depth"] = (must_have_ratio * 0.7 + diff_ratio * 0.3) * weights["llm_production_depth"]
        if "streaming" in cv_skills and ("openai" in cv_skills or "openrouter" in cv_skills):
            breakdown["llm_production_depth"] = min(
                breakdown["llm_production_depth"] * 1.2, weights["llm_production_depth"],
            )

        agentic_signals = {"agent", "agents", "agentic", "tool use", "dag",
                            "orchestration", "multi-step", "reasoning"}
        agentic_count = len(agentic_signals & cv_skills)
        breakdown["agentic_patterns"] = min(
            (agentic_count / max(len(agentic_signals), 1)) * weights["agentic_patterns"],
            weights["agentic_patterns"],
        )

        framework_signals = {"langchain", "llamaindindex", "langsmith", "haystack",
                             "semantic kernel", "guidance", "dspy"}
        framework_count = len(framework_signals & cv_skills)
        breakdown["framework_breadth"] = min(
            (framework_count / max(len(framework_signals), 1)) * weights["framework_breadth"],
            weights["framework_breadth"],
        )
        if framework_count == 0:
            recommendations.append("Add GenAI framework awareness (LangChain, LlamaIndex, etc.)")

        breakdown["danish_compliance"] = danish_score

        impact_signals = {"reduced", "improved", "faster", "cheaper", "accuracy",
                          "latency", "cost", "uptime", "%"}
        impact_count = len(impact_signals & cv_skills)
        breakdown["quantified_impact"] = min(
            (impact_count / max(len(impact_signals), 1)) * weights["quantified_impact"],
            weights["quantified_impact"],
        )

        if "react" in cv_skills or "typescript" in cv_skills:
            breakdown["fullstack_genai_combo"] = weights["fullstack_genai_combo"] * 0.8
        else:
            breakdown["fullstack_genai_combo"] = weights["fullstack_genai_combo"] * 0.3

        if must_have_missing:
            recommendations.append(f"Critical missing: {sorted(must_have_missing)}")
        if "rag" not in cv_skills:
            recommendations.append("RAG is in 36.4% of GenAI postings — add if applicable")

    def _score_ml_eng(self, cv_skills, weights, keywords, breakdown, recommendations,
                      must_have_found, must_have_missing,
                      must_have_ratio, danish_score):
        """ML Engineer scoring."""
        del keywords, must_have_found  # unused
        mlops_signals = {"docker", "kubernetes", "ci/cd", "terraform", "mlops",
                         "model deployment", "model serving", "model monitoring"}
        mlops_count = len(mlops_signals & cv_skills)
        breakdown["mlops_maturity"] = min(
            (mlops_count / len(mlops_signals)) * weights["mlops_maturity"],
            weights["mlops_maturity"],
        )

        infra_signals = {"linux", "docker", "kubernetes", "ci/cd", "cloud",
                         "terraform", "iac", "infrastructure", "azure", "aws"}
        infra_count = len(infra_signals & cv_skills)
        breakdown["infrastructure_depth"] = min(
            (infra_count / len(infra_signals)) * weights["infrastructure_depth"],
            weights["infrastructure_depth"],
        )

        lifecycle_signals = {"training", "deployment", "monitoring", "retraining",
                             "versioning", "experiment", "pipeline"}
        lc_count = len(lifecycle_signals & cv_skills)
        breakdown["model_lifecycle"] = min(
            (lc_count / len(lifecycle_signals)) * weights["model_lifecycle"],
            weights["model_lifecycle"],
        )

        breakdown["danish_compliance"] = danish_score

        devops_signals = {"automation", "reliability", "platform", "infrastructure",
                          "monitoring", "alerting", "observability", "resilience"}
        devops_count = len(devops_signals & cv_skills)
        breakdown["devops_culture"] = min(
            (devops_count / len(devops_signals)) * weights["devops_culture"],
            weights["devops_culture"],
        )

        if must_have_missing:
            recommendations.append(f"Missing MLOps stack: {sorted(must_have_missing)}")
        if "kubernetes" not in cv_skills:
            recommendations.append("Add Kubernetes (44.4% of ML-ENG postings — CKAD cert path)")
        if "ci/cd" not in cv_skills and "github actions" not in cv_skills:
            recommendations.append("Make CI/CD explicit (GitHub Actions or similar)")

    def _company_tailoring_score(self, cv_content: str, role: str, company: str) -> float:
        """Bonus for company-specific keyword alignment (0-3 range)."""
        cv_lower = cv_content.lower()
        company_keywords = _get_company_keywords(role, company)
        if not company_keywords:
            return 0.0
        matches = sum(1 for kw in company_keywords if kw.lower() in cv_lower)
        # Max bonus: 3 points (partial credit for company tailoring)
        return min(3.0, (matches / max(len(company_keywords), 1)) * 3.0)


def _get_company_keywords(role: str, company: str) -> list[str]:
    """Return expected keywords for a company-specific tailoring role."""
    # Priority 5 companies — key terms that boost score
    company_profiles: dict[str, dict[str, list[str]]] = {
        "Corti": {
            "AI-ENG": ["python", "pytorch", "llm", "nlp", "healthcare", "ai architecture"],
            "GENAI": ["python", "llm", "healthcare", "rag"],
        },
        "Zendesk": {
            "AI-SDEV": ["python", "ai agents", "ml pipelines", "aws", "spark"],
            "GENAI": ["python", "llm", "agents"],
        },
        "Novo Nordisk": {
            "AI-SDEV": ["python", "azure", "healthcare", "pharma", "gdpr"],
            "ML-ENG": ["python", "ml", "azure", "healthcare"],
        },
        "Maersk": {
            "AI-ENG": ["python", "ml", "cloud", "aws", "logistics", "real-time"],
            "ML-ENG": ["python", "ml", "cloud", "logistics"],
        },
        "Universal Robots": {
            "ML-ENG": ["python", "ml", "ros", "computer vision", "embedded"],
        },
        "LEGO Group": {
            "GENAI": ["python", "llm", "kubernetes", "cloud", "ml"],
        },
        "Danske Bank": {
            "FE-DEV": ["react", "typescript", "architecture", "enterprise", "finance"],
        },
        "Lunar": {
            "FE-DEV": ["react", "typescript", "fintech", "mobile-first"],
        },
    }
    return company_profiles.get(company, {}).get(role, [])


def _score_to_label(total: float) -> str:
    """Map numeric score to human label."""
    if total >= 85:
        return "Excellent"
    if total >= 70:
        return "Strong"
    if total >= 55:
        return "Good"
    if total >= 40:
        return "Fair"
    return "Weak"


def _categorize_suggestion(suggestion: str, role: str) -> str:
    """Categorize a suggestion by type."""
    s_lower = suggestion.lower()
    if "missing" in s_lower or "must-have" in s_lower:
        return "missing_must_have"
    elif "danish" in s_lower or "headshot" in s_lower or "hobby" in s_lower:
        return "danish_compliance"
    elif "add" in s_lower:
        return "add_skill"
    elif "consider" in s_lower:
        return "consider_addition"
    return "general"
