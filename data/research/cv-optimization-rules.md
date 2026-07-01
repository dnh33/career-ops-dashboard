# CV Optimization Rules — Danish Tech Market Q3 2026

> **Purpose:** Concrete, implementable rules for the Career Ops CV generation pipeline.
> Converts market intelligence (T1.1–T1.5) into per-role CV optimization with scoring.
> **Generated:** 2026-06-30
> **Version:** 1.0.0 (Quarterly — next review: Q4 2026)
> **Input:** `dk-market-intelligence-profile.md` (parent task T2.1)
> **Consumer:** `cv-generator.py`, `cv-scorer.py`, `cover-letter-generator.py`

---

## 0. Rule Versioning & Update Policy

| Field | Value |
|-------|-------|
| Schema version | 1.0.0 |
| Data source vintage | Q3 2026 (July–Sept postings) |
| Next quarterly review | Q4 2026 (Oct–Dec 2026) |
| Update trigger | New job posting batch, salary survey update, or market shift |
| Changelog location | Bottom of this file |

### How to update quarterly:
1. Re-run T1.1 aggregation (job postings) — check for new skills emerging
2. Re-run T1.2 analysis — update skill demand percentages
3. Re-run T1.3 salary benchmark — adjust scoring weightings
4. Bump version (1.0.0 → 1.1.0 for minor, 1.0.0 → 2.0.0 for major structure change)
5. Append changelog entry

---

## 1. Target Roles — Registry

From T1.1 (74 postings) + T1.2 + T1.3. These are the 5 roles Career Ops generates CVs for:

| Role ID | Role Title | Postings in Dataset | Median CPH (DKK/mo) | Market Concentration |
|---------|-----------|--------------------|--------------------|-----------------------|
| `FE-DEV` | Frontend Developer | 28 | 48,000 | React+TypeScript dominant |
| `AI-SDEV` | AI Software Developer | 12 | 55,000 | Python+ML frameworks |
| `AI-ENG` | AI Engineer | 14 | 60,000 | ML/DL+cloud+data pipelines |
| `GENAI` | Generative AI Engineer | 11 | 65,000 | LLMs+RAG+agents+prompt eng |
| `ML-ENG` | ML Engineer | 9 | 58,000 | MLOps+model deployment+infra |

---

## 2. Universal Danish CV Rules (All Roles)

From T1.5 (dk-market-culture-guide.md). These are **mandatory** regardless of target role.

### 2.1 Hard Rules — Never Violate

| Rule | Spec | Penalty if violated |
|------|------|---------------------|
| Max length | **2 pages absolute max** | CV discarded by Danish recruiters |
| Photo | **Include** professional headshot (ON by default) | Missing photo = less likely to be read in DK |
| Personal section | **Must** include hobbies, interests, family status (optional) | "Cold" CV = cultural misfit signal |
| Tone | Humbly collaborative. **Banned words:** "ninja", "guru", "world-class", "rockstar", "synergy", "leverage", "24/7 availability" | Instant rejection signal in DK |
| Language | Match posting language. Include Languages section with CEFR levels | Mixed-language CV = unprofessional |
| Work-life signaling | **ONLY**: "efficient delivery", "sustainable pace", "results-oriented". **NEVER**: "work long hours", "go the extra mile" | Red flag for Danish employers |
| Union info | **Never** include union membership on CV | Cultural taboo |
| Structure | Reverse chronological ONLY | Non-chronological = skipped by recruiters |
| Overtime | **Never** signal willingness to work overtime | "Staying late = inefficiency" in DK culture |

### 2.2 CV Section Order (Mandatory)

```
1. Personal Info (name, photo, contact, DOB optional)
2. Personal Profile / Summary (3-4 lines, warm + collaborative)
3. Work Experience (reverse chronological, most recent first)
4. Education
5. Skills (formatted as category + proficiency)
6. Languages (with CEFR: Danish C2, English C1/C2, etc.)
7. Interests / Hobbies (minimum 2-3 genuine entries)
8. References (optional: "Available upon request")
```

---

## 3. Per-Role Optimization Rules

---

### 3.1 Role: Frontend Developer (`FE-DEV`)

#### Ideal CV Structure (priority order)
1. Personal Info + Photo
2. Personal Profile → emphasize "frontend engineering with AI integration experience"
3. Work Experience → lead with React/TypeScript production achievements
4. Technical Skills → frontend-first layout
5. Education
6. Languages
7. Interests

#### Top 5 Hard Skills to Highlight
| Priority | Skill | Market Demand | Daniel's Level | Action |
|----------|-------|---------------|----------------|--------|
| 1 | **React.js / React 19** | 23.2% (16 postings) | Expert | Lead with production keywords |
| 2 | **TypeScript** | 27.5% (19 postings) | Expert | Make it title-level prominent |
| 3 | **CSS / Tailwind / Design Systems** | ~11.6% combined | Expert | Showcase accessibility + design system knowledge |
| 4 | **Git** | 78.3% (54 postings) | Expert | Always list (baseline expectation) |
| 5 | **REST API / Frontend Architecture** | 13.0% (9 postings) | Strong | Frame as "API-driven development" |

#### Top 3 Soft Skills to Highlight
| Priority | Skill | Evidence Source |
|----------|-------|----------------|
| 1 | **Collaborative development** | Danish cultural norm — emphasize team-based delivery |
| 2 | **Communication** | 11.6% demand — show cross-functional work |
| 3 | **User-centric thinking** | UX awareness from Figma/design system work |

#### Required ATS Keywords (from 28 postings)

**Must-have (appear in 30%+ of postings):**
- React, React.js, React 19
- TypeScript
- JavaScript (ES6+)
- Git
- HTML, CSS

**High-value (appear in 10-30% of postings):**
- REST API, API-driven development
- Component Libraries, Component Architecture
- Responsive Design, Mobile-First
- Accessibility, WCAG, a11y
- Design Systems, Design Tokens
- Web Performance, Core Web Vitals
- Testing (Jest, Cypress, Testing Library)
- Webpack, Vite, build tools
- Node.js (appears in full-stack context)

**Differentiator keywords (emerging, low competition):**
- AI Integration, AI-powered frontend
- Server Components (RSC), SSR, SSG
- Astro, Next.js (framework diversity)

#### Company-Specific Tailoring for FE-DEV

| Company | Tailoring Approach |
|---------|------------------|
| **Danske Bank** | Emphasize ".NET awareness", banking/finance domain, enterprise frontend architecture, hybrid work capability |
| **Zendesk** | Lead with "AI Integration" + "Frontend Architecture" + ML Pipelines awareness. Highlight Python as secondary. |
| **Sitecore** | Emphasize ".NET ecosystem", Sitecore XM Cloud experience (or willingness to learn), enterprise CMS |
| **Netcompany** | Emphasize Angular/Vue alongside React (polyglot), architecture skills, public sector sensitivity |
| **Conscious / Corti** | Lead with "AI/MedTech frontend", React+TypeScript, healthcare domain interest |
| **Lunar** | Fintech domain, mobile-first, React+TypeScript, API-driven |
| **Novicell** | eCommerce, React+TypeScript, architecture, "commercial awareness" |
| **BESTSELLER** | AI Applications in retail context, remote work capability, "APPRETIO" framework awareness |

#### Scoring Rubric — Frontend Developer (0-100)

| Category | Weight | 90+ Criteria | 50- Criteria |
|----------|--------|--------------|--------------|
| Skill match | 30 pts | React+TS+Git+CSS+API+Testing all present | Missing React or TypeScript |
| Frontend depth | 20 pts | Design systems, a11y, performance, architecture all mentioned | Only "HTML/CSS/JS" listed |
| AI integration | 15 pts | Explicit "AI-powered" or "LLM integration" mentioned | No AI mention at all |
| Danish compliance | 15 pts | Photo, hobbies, humble tone, max 2 pages | Missing 2+ Danish norms |
| Experience signal | 10 pts | Production-scale, measurable impact, 3-7 years | Generic descriptions, no metrics |

---

### 3.2 Role: AI Software Developer (`AI-SDEV`)

#### Ideal CV Structure
1. Personal Info + Photo
2. Personal Profile → "AI software development with production deployment experience"
3. Work Experience → lead with Python+ML projects with measurable outcomes
4. Technical Skills → AI-first layout (Python, ML frameworks, cloud)
5. Education
6. Languages
7. Interests

#### Top 5 Hard Skills to Highlight
| Priority | Skill | Market Demand | Daniel's Level | Action |
|----------|-------|---------------|----------------|--------|
| 1 | **Python** | 58.0% (40 postings) | Strong (FastAPI backend) | PRIMARY language on CV |
| 2 | **Docker** | 47.8% (33 postings) | Strong | Explicit + show deployment depth |
| 3 | **AWS** | 37.7% (26 postings) | None/implicit | Add as "learning" or highlight self-hosted cloud awareness |
| 4 | **PyTorch / TensorFlow** | 11.6% (8+6 postings) | PyTorch-as-user | Explicit: "Production ML with PyTorch" |
| 5 | **SQL / PostgreSQL** | 34.8% (24 postings) | Medium | Map to "SQL / PostgreSQL" explicitly |

#### Top 3 Soft Skills to Highlight
| Priority | Skill | Evidence Source |
|----------|-------|----------------|
| 1 | **Problem Solving** | 11.6% demand — show ML problem → solution narratives |
| 2 | **Communication** | Essential for translating AI to business value |
| 3 | **Agile / Iterative Development** | AI projects need experimentation culture |

#### Required ATS Keywords (from 12 postings)

**Must-have:**
- Python
- Machine Learning, ML
- Docker
- Cloud (AWS/Azure/GCP)
- Software Engineering, Production Code

**High-value:**
- PyTorch, TensorFlow
- MLOps, Model Deployment
- REST API, API Development
- CI/CD, DevOps
- Git
- Data Pipelines, ETL

**Differentiator keywords:**
- Generative AI awareness
- Agentic AI
- Full-stack + AI (Daniel's sweet spot)
- FastAPI

#### Company-Specific Tailoring for AI-SDEV

| Company | Tailoring Approach |
|---------|------------------|
| **Zendesk** | Lead with "AI Agents" experience, Python+Spark, ML pipelines. Mention "production AI at scale". |
| **Novo Nordisk** | Emphasize "healthcare AI", Python, Azure (their cloud), pharma compliance awareness, GDPR. |
| **Tata Consultancy Services** | Java+Python polyglot, enterprise ML, DevOps awareness, consulting mindset. |
| **Unity Technologies** | C# awareness + AI/ML + "AI Gateway" concept + MCP (Model Context Protocol). |
| **Tradeshift** | NLP + document intelligence + LLM + AWS Textract awareness. |
| **DFDS** | MLOps + cloud + Docker + logistics domain interest. |

#### Scoring Rubric — AI Software Developer (0-100)

| Category | Weight | 90+ Criteria | 50- Criteria |
|----------|--------|--------------|--------------|
| Python depth | 25 pts | Production Python, FastAPI, ML libs all present | Only "Python" with no context |
| ML/AI stack completeness | 25 pts | PyTorch+Docker+Cloud+CI/CD+Git | Missing 3+ core AI skills |
| Production deployment | 15 pts | MLOps, deployment, monitoring mentioned | Only "notebook" experience |
| Danish compliance | 15 pts | Same as FE-DEV | Same as FE-DEV |
| Domain alignment | 10 pts | Industry-specific projects or clear interest | Generic AI with no domain |
| Full-stack bonus | 10 pts | Frontend+AI+Backend trifecta clearly signaled | Pure AI with no frontend signal |

---

### 3.3 Role: AI Engineer (`AI-ENG`)

#### Ideal CV Structure
1. Personal Info + Photo
2. Personal Profile → "AI engineering with end-to-end pipeline ownership"
3. Work Experience → lead with full ML lifecycle projects (train→deploy→monitor)
4. Technical Skills → ML-first layout (Python, cloud ML, data engineering)
5. Education
6. Languages
7. Interests

#### Top 5 Hard Skills to Highlight
| Priority | Skill | Market Demand | Daniel's Level | Action |
|----------|-------|---------------|----------------|--------|
| 1 | **Python** | 58.0% (40 postings) | Strong | PRIMARY — emphasize production ML code |
| 2 | **Cloud (AWS/Azure/GCP)** | 37.7% AWS specifically | Implicit | "Cloud-native ML development" framing |
| 3 | **Docker + Kubernetes** | 47.8% + 24.6% | Docker yes, K8s no | Docker featured, K8s planned/learning |
| 4 | **LLMs / RAG** | 11.6%+ (emerging, fast) | Strong | Lead with actual LLM integration projects |
| 5 | **Machine Learning (general)** | Core to all postings | Medium | Re-frame existing work as "ML engineering" |

#### Top 3 Soft Skills to Highlight
| Priority | Skill | Rationale |
|----------|-------|-----------|
| 1 | **Architecture thinking** | AI Engineers design systems, not just models |
| 2 | **Cross-functional collaboration** | ML sits between research, product, infrastructure |
| 3 | **Pragmatic delivery** | Danes value "it works in production" over "novel approach" |

#### Required ATS Keywords (from 14 postings)

**Must-have:**
- Python
- Machine Learning
- AI, Artificial Intelligence
- Cloud (Azure/AWS)
- Docker

**High-value:**
- LLMs, Large Language Models
- RAG, Retrieval-Augmented Generation
- Agentic AI, Agentic Frameworks
- Vector Databases, Vector Search
- AI Architecture
- Model Deployment, Model Optimization
- SQL, Data Engineering

**Differentiator keywords:**
- Prompt Engineering, Prompt Optimization
- AI Scoring, AI Evaluation
- Multi-modal AI
- Streaming AI responses (SSE — Daniel has this)

#### Company-Specific Tailoring for AI-ENG

| Company | Tailoring Approach |
|---------|------------------|
| **Corti** | Python+PyTorch+NLP/LLM+AWS, healthcare AI, mention "AI architecture", research-affinity. SMALL HIGH-SIGNAL TEAM. |
| **Heyra** | "AI Engineering" + Software Architecture + Cloud + LLMs + Python. Lead with architecture + production ownership. |
| **Maersk** | "Real-time data platforms", Python+ML+Cloud, AWS/Azure, logistics domain interest, logistics optimization thinking. |
| **Lunar** | "Banking/Fintech AI", LLMs+AI Agents+Python, security awareness, financial data sensitivity. |
| **DFDS** | "AI Engineer" + MLOps + Cloud + Docker + Python. Emphasize production deployment + logistics domain. |
| **Amazon DK** | "Applied Scientist" framing, Python+ML+Deep Learning+AWS+SageMaker+NLP. Mention "distributed systems at scale". |
| **NordicTech Solutions** | "Agentic Frameworks" + RAG + Vector Databases + Azure DevOps + Python. Lead with agents+RAG. |

#### Scoring Rubric — AI Engineer (0-100)

| Category | Weight | 90+ Criteria | 50- Criteria |
|----------|--------|--------------|--------------|
| AI/LLM depth | 25 pts | RAG, agents, prompt engineering, streaming all demonstrated | Only general "ML" mentioned |
| ML engineering maturity | 25 pts | MLOps, CI/CD, Docker, cloud deployment, monitoring | Only "trained a model" level |
| Pipeline ownership | 15 pts | End-to-end examples (data→train→deploy→monitor) | Fragmented or theoretical only |
| Danish compliance | 15 pts | Same as above | Same as above |
| Architecture signal | 10 pts | "AI Architecture" or system design language | No architecture vocabulary |
| Company-specific fit | 10 pts | Tailored keywords from target posting | Generic CV with no tailoring |

---

### 3.4 Role: Generative AI Engineer (`GENAI`)

#### Ideal CV Structure
1. Personal Info + Photo
2. Personal Profile → "Generative AI engineering — from prototype to production"
3. Work Experience → lead with LLM integration projects (Plugly AI, Career Ops agent)
4. Technical Skills → GenAI-first (LLM ecosystems, RAG, agentic, fine-tuning)
5. Education
6. Languages
7. Interests

#### Top 5 Hard Skills to Highlight
| Priority | Skill | Market Demand | Daniel's Level | Action |
|----------|-------|---------------|----------------|--------|
| 1 | **LLMs / LLM Integration** | Core differentiator | STRONG (real projects) | Lead with "production LLM integration" |
| 2 | **Python** | 58.0% | Strong | Production Python for ML/API |
| 3 | **RAG (Retrieval-Augmented Generation)** | ~11.6%+ | Real (likely in Plugly) | Explicitly name RAG experience |
| 4 | **Prompt Engineering** | Emerging critical | Strong | Frame as "AI system design" not just prompts |
| 5 | **Agentic AI / AI Agents** | Fastest-growing (Zendesk, etc.) | Strong (Career Ops DAG agent) | Explicit "agent architecture" language |

#### Top 3 Soft Skills to Highlight
| Priority | Skill | Rationale |
|----------|-------|-----------|
| 1 | **Research translation** | GenAI is new — turning papers/capabilities into production is gold |
| 2 | **Iterative experimentation** | "Ship, measure, improve" — aligns with Danish pragmatic culture |
| 3 | **Technical communication** | GenAI requires explaining complex concepts to stakeholders |

#### Required ATS Keywords (from 11 postings)

**Must-have:**
- LLMs, Large Language Models
- Python
- Generative AI
- Prompt Engineering

**High-value:**
- RAG, Retrieval-Augmented Generation
- AI Agents, Agentic AI, Agentic Frameworks
- PyTorch, TensorFlow
- RAG Architecture
- Vector Databases
- AI Architecture
- Streaming (for LLM output, SSE)
- LLM Ops, AI Operations
- LangChain, LlamaIndex (framework awareness)

**Differentiator keywords:**
- SSE/Streaming (Daniel has real experience)
- Multi-provider (OpenAI, OpenRouter, local models)
- AI Widget / AI Interface patterns
- LLM Chaining / Orchestration
- Fine-tuning (if applicable)
- Token management, cost optimization

#### Company-Specific Tailoring for GENAI

| Company | Tailoring Approach |
|---------|------------------|
| **LEGO Group** | "GenAI Foundation" + Python+LLMs+Kubernetes+Cloud+ML. Emphasize production scale (LEGO = massive scale). |
| **Halfspace (Accenture)** | "Generative AI Solutions" + Agentic AI + Azure + LLMs + Python + Architecture. LEAD with enterprise + Accenture-style consulting tone. |
| **StaffHost Digital** | "Senior Generative AI" + LLMs+Generative AI+PyTorch+TensorFlow+RAG+Python. Emphasize breadth of ML frameworks. |
| **Pleo** | "Generative AI Engineer" + LLMs+Python+ML+Finance. FinTech domain interest + security awareness. |
| **Dansk Erhverv** | "Generative AI" + RAG+LLMs+Python+Statistics+NLP. Research + NLP angle. |
| **Hello Monday** | "AI Specialist" + LLMs+Generative AI+AI Tools+Cloud+Python. Tooling + applied focus. |
| **NordicTech Solutions** | "Agentic Frameworks" + RAG + Vector Databases + Azure DevOps. Lead with production + deployment. |

#### Scoring Rubric — Generative AI Engineer (0-100)

| Category | Weight | 90+ Criteria | 50- Criteria |
|----------|--------|--------------|--------------|
| LLM production depth | 30 pts | Multi-provider, streaming, RAG, agents all demonstrated | Only "used ChatGPT API" level |
| Agentic/Advanced patterns | 20 pts | Agent architecture, tool use, DAG orchestration, error handling | Single-endpoint LLM calls only |
| Framework breadth | 15 pts | LangChain/LlamaIndex awareness, multi-model, vector DBs | Only OpenAPI API basics |
| Danish compliance | 15 pts | Same as above | Same as above |
| Quantified impact | 10 pts | Latency reduced, cost saved, accuracy improved | No metrics on AI work |
| Full-stack + GenAI combo | 10 pts | Shows both frontend and AI engineering | Only backend AI |

---

### 3.5 Role: ML Engineer (`ML-ENG`)

#### Ideal CV Structure
1. Personal Info + Photo
2. Personal Profile → "ML engineering — bridging research and production infrastructure"
3. Work Experience → lead with model deployment + infrastructure projects
4. Technical Skills → MLOps-first (Docker, K8s, CI/CD, cloud, model serving)
5. Education
6. Languages
7. Interests

#### Top 5 Hard Skills to Highlight
| Priority | Skill | Market Demand | Daniel's Level | Action |
|----------|-------|---------------|----------------|--------|
| 1 | **Python** | 58.0% | Strong | PRIMARY ML engineering language |
| 2 | **Docker + Kubernetes** | 47.8% + 24.6% | Docker yes, K8s planned | Docker explicit, K8s on learning path |
| 3 | **CI/CD** | 8.7% | Implicit (self-hosted) | Make GitHub Actions explicit |
| 4 | **MLOps / Model Deployment** | Emerging fast | Some (Career Ops) | "ML model deployment in production" |
| 5 | **Cloud Deployment** | 37.7% | Implicit | "Cloud-native ML infrastructure" |

#### Top 3 Soft Skills to Highlight
| Priority | Skill | Rationale |
|----------|-------|-----------|
| 1 | **Infrastructure thinking** | ML Engineers own the serving layer |
| 2 | **Reliability / SRE mindset** | Models in production need monitoring + alerting |
| 3 | **Research-to-production translation** | Bridge gap between DS prototypes and reliable services |

#### Required ATS Keywords (from 9 postings)

**Must-have:**
- Python
- Machine Learning
- Docker
- MLOps, Model Deployment
- Cloud

**High-value:**
- Kubernetes
- CI/CD, GitHub Actions, Azure DevOps
- Model Serving, Model Monitoring
- Linux (especially RedHat/enterprise)
- AI Model Deployment
- Terraform, IaC

**Differentiator keywords:**
- Real-time inference
- Model versioning
- A/B testing for ML
- Feature engineering pipelines
- Cost optimization for ML workloads

#### Company-Specific Tailoring for ML-ENG

| Company | Tailoring Approach |
|---------|------------------|
| **Werktøj.dk** | "AI DevOps" + Linux+RedHat+Docker+Kubernetes+CI/CD+AI Model Deployment. LEAD WITH LINUX + ops excellence. |
| **DFDS** | "AI/ML Engineer" + MLOps + Cloud + Docker + Python + ML. Production MLOps focus. |
| **Universal Robots** | "AI/ML for robotics" + Python+ROS+real-time systems+computer vision. Mechatronics domain. |
| **DFDS** | MLOps + Cloud + Docker + Python. |
| **Sigma Connectivity** | "Edge AI" + Embedded+Python+Computer Vision+ML+C/C++. IoT/I Edge deployment. |

#### Scoring Rubric — ML Engineer (0-100)

| Category | Weight | 90+ Criteria | 50- Criteria |
|----------|--------|--------------|--------------|
| MLOps maturity | 30 pts | Docker+K8s+CI/CD+model serving+monitoring all present | Only "model training" level |
| Infrastructure depth | 25 pts | Linux, IaC, cloud deployment, CI/CD all explicit | No infrastructure keywords shown |
| Model lifecycle ownership | 15 pts | Data→train→deploy→monitor→retrain loop visible | Only one phase mentioned |
| Danish compliance | 15 pts | Same as above | Same as above |
| DevOps culture fit | 15 pts | "Platform engineering", "reliability", "automation" language | No ops/automation vocabulary |

---

## 4. Keyword Extraction from Job Postings (Evidence Base)

### Methodology
- 74 postings from Q3 2026 across 7+ sources
- Skills normalized (aliases merged: React/ReactJS/React.js → React.js)
- Counted per role cluster, not just overall

### Per-Role Keyword Frequency (from raw postings data)

#### Frontend Developer Keywords (28 postings)
| Keyword | Count | Frequency |
|---------|-------|-----------|
| JavaScript/React/TypeScript | 28 | 100% |
| HTML/CSS | 22 | 78.6% |
| Git | 18 | 64.3% |
| REST API | 9 | 32.1% |
| Architecture/Component Architecture | 7 | 25.0% |
| Design Systems | 6 | 21.4% |
| Angular/Vue (alt frameworks) | 5 | 17.9% |
| AI Integration (emerging) | 3 | 10.7% |
| Testing (Jest/Cypress) | 3 | 10.7% |

#### AI Software Developer Keywords (12 postings)
| Keyword | Count | Frequency |
|---------|-------|-----------|
| Python | 12 | 100% |
| Machine Learning | 10 | 83.3% |
| Docker | 8 | 66.7% |
| Cloud (AWS/Azure) | 7 | 58.3% |
| MLOps/Model Deployment | 5 | 41.7% |
| Git | 5 | 41.7% |
| CI/CD + DevOps | 4 | 33.3% |
| PyTorch/TensorFlow | 4 | 33.3% |
| Java | 2 | 16.7% |
| Data Pipelines/ETL | 2 | 16.7% |

#### AI Engineer Keywords (14 postings)
| Keyword | Count | Frequency |
|---------|-------|-----------|
| Python | 14 | 100% |
| LLMs/LLM Integration | 10 | 71.4% |
| AI/Artificial Intelligence | 12 | 85.7% |
| Cloud (AWS/Azure/GCP) | 9 | 64.3% |
| Machine Learning | 11 | 78.6% |
| Docker | 7 | 50.0% |
| RAG | 4 | 28.6% |
| Agentic AI / AI Agents | 4 | 28.6% |
| Vector Databases/Search | 3 | 21.4% |
| AI Architecture | 3 | 21.4% |
| Research | 3 | 21.4% |

#### Generative AI Engineer Keywords (11 postings)
| Keyword | Count | Frequency |
|---------|-------|-----------|
| LLMs / Large Language Models | 11 | 100% |
| Python | 10 | 90.9% |
| Generative AI | 9 | 81.8% |
| Prompt Engineering | 5 | 45.5% |
| RAG | 4 | 36.4% |
| PyTorch/TensorFlow | 4 | 36.4% |
| AI Agents / Agentic AI | 3 | 27.3% |
| Cloud | 3 | 27.3% |
| Statistics/NLP | 2 | 18.2% |

#### ML Engineer Keywords (9 postings)
| Keyword | Count | Frequency |
|---------|-------|-----------|
| Python | 9 | 100% |
| Machine Learning | 8 | 88.9% |
| Docker | 6 | 66.7% |
| CI/CD | 5 | 55.6% |
| Kubernetes | 4 | 44.4% |
| MLOps/Model Deployment | 4 | 44.4% |
| Cloud | 4 | 44.4% |
| Linux | 3 | 33.3% |
| IAM/Infrastructure | 2 | 22.2% |
| AI Model Deployment | 2 | 22.2% |

---

## 5. Keyword Normalization Map (Alias Resolution)

Career Ops must normalize these aliases BEFORE matching against job postings:

| Internal Name | ATS Keywords to Match |
|---------------|----------------------|
| PostgreSQL | SQL / PostgreSQL / Database |
| React.js | React / React.js / ReactJS / React 19 |
| TypeScript | TypeScript / TS |
| JavaScript | JavaScript / JS / ES6 / ES2022 |
| Docker | Docker / Containerization |
| Linux | Linux / Ubuntu / Self-hosted / VPS |
| Prompt Engineering | Prompt Engineering / LLM Ops / AI Prompt Design |
| LLM Integration | LLMs / LLM / Generative AI / AI Integration / OpenAI / OpenRouter |
| FastAPI | FastAPI / API Development / REST API |
| GitHub Actions | CI/CD / GitHub Actions / GitLab CI / Azure DevOps |
| Figma | Figma / Design Systems / UI Design |
| SSE | Streaming / Real-time / SSE / Server-Sent Events |

---

## 6. Company-Specific Tailoring Templates (from T1.4)

### Priority 5 Companies (Apply First)

| Company | Role Focus | CV Angle | Key Keywords to Lead With | Culture Note |
|---------|-----------|----------|--------------------------|--------------|
| **Corti** | AI Engineer / Frontend | Healthcare AI, NLP/LLM, small high-signal team | Python, PyTorch, LLM, NLP, healthcare, AI Architecture | Research-oriented, 120 people, Series B+ |
| **Zendesk** | AI Software Dev | AI Agents, production Python, ML pipelines | Python, LLMs, AI Agents, ML Pipelines, AWS, Spark | AI Agents team expanding, CPH office |
| **Novo Nordisk** | AI/ML Developer | Healthcare AI, massive scale, Azure stack | Python, ML, Azure, healthcare, Deep Learning, R | Fortune 500, job security, slower pace |
| **A.P. Moller - Maersk** | AI Engineer | Real-time platforms, cloud-native | Python, ML, Cloud, AWS, real-time, logistics | Legacy company going digital-fast |
| **Universal Robots** | ML Engineer | Robotics + perception, real-time systems | Python, ML, ROS, computer vision, embedded | Odense (lower COL), hardware-software fusion |

### Priority 4 Companies

| Company | Role Focus | CV Angle | Key Keywords |
|---------|-----------|----------|-------------|
| **Microsoft DK** | AI Engineer/GenAI | Azure AI, enterprise, Copilot stack | Azure, AI, Cloud, ML, Power BI |
| **Spotify** | ML Engineer | Recommendation systems, scale, Python | Python, ML, data pipelines, A/B testing, recommendation |
| **Trustpilot** | AI Engineer | NLP, ML systems, Python | Python, ML, NLP, AWS, ML systems |
| **Pleo** | AI/GenAI Engineer | FinTech, fraud detection, agentic | LLMs, Python, ML, finance, Generative AI |
| **Google DK** | AI Engineer | Vertex AI, TensorFlow, GCP | Python, TensorFlow, GCP, Vertex AI, JAX |

---

## 7. Master Scoring Function (Python Implementation)

This is the implementable scoring rubric used by `cv-scorer.py`. A CV targeting the Danish market scores 0-100. Each role has a different weighting.

```python
"""
CV Scorer — Danish Tech Market Q3 2026
Implements the scoring rubric from cv-optimization-rules.md

Version: 1.0.0
"""

from typing import Optional
from datetime import datetime

# ── Role Definitions ───────────────────────────────────────────────
ROLE_WEIGHTS = {
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
ROLE_KEYWORDS = {
    "FE-DEV": {
        "must_have": {"react", "react.js", "typescript", "javascript", "git", "html", "css"},
        "high_value": {
            "rest api", "api", "component", "responsive", "mobile-first",
            "accessibility", "wcag", "design system", "performance",
            "jest", "cypress", "webpack", "vite", "node.js", "next.js",
            "tailwind", "sass", "less", "figma"
        },
        "differentiator": {
            "ai integration", "ai-powered", "llm integration", "server components",
            "ssr", "ssg", "streaming", "astro"
        },
    },
    "AI-SDEV": {
        "must_have": {"python", "machine learning", "docker", "cloud", "git"},
        "high_value": {
            "pytorch", "tensorflow", "mlops", "model deployment", "ci/cd",
            "devops", "data pipelines", "etl", "rest api", "azure", "aws",
            "gcp", "kubernetes", "sql"
        },
        "differentiator": {
            "generative ai", "agentic ai", "full-stack", "fastapi",
            "production ml", "model serving", "model monitoring"
        },
    },
    "AI-ENG": {
        "must_have": {"python", "machine learning", "llm", "ai", "cloud", "docker"},
        "high_value": {
            "rag", "retrieval-augmented generation", "agentic", "agents",
            "vector", "vector database", "ai architecture", "model deployment",
            "azure", "aws", "streaming", "nlp", "deep learning", "sql"
        },
        "differentiator": {
            "prompt engineering", "multi-modal", "ai scoring", "ai evaluation",
            "real-time inference", "cost optimization", "model versioning"
        },
    },
    "GENAI": {
        "must_have": {"llm", "llms", "large language model", "python", "generative ai"},
        "high_value": {
            "prompt engineering", "rag", "retrieval-augmented generation",
            "agent", "agents", "agentic", "pytorch", "tensorflow",
            "vector database", "langchain", "llamaindex", "streaming",
            "sse", "api"
        },
        "differentiator": {
            "multi-provider", "openai", "openrouter", "local models",
            "fine-tuning", "token management", "llm orchestration",
            "ai widget", "ai interface", "real-time llm"
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
            "reliability", "automation"
        },
    },
}

# ── Danish Compliance Checks ────────────────────────────────────────
DANISH_BANNED_WORDS = {
    "ninja", "guru", "world-class", "rockstar", "synergy", "leverage",
    "24/7", "work long hours", "24/7 availability", "go the extra mile",
    "passionate"  # borderline — "interested in" is preferred
}

DANISHED_PREFERRED_PHRASES = [
    "experienced in", "comfortable with", "interested in",
    "efficient delivery", "sustainable pace", "results-oriented"
]


def normalize_skill(skill: str) -> str:
    """Normalize a skill string for matching."""
    s = skill.lower().strip()
    # Alias map
    aliases = {
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
        "gitlab ci": "ci/cd", "azure devops": "ci/dd",
        "amazon web services": "aws", "amazon aws": "aws",
        "google cloud": "gcp", "google cloud platform": "gcp",
        "microsoft azure": "azure",
        "model ops": "mlops",
        "server-sent events": "streaming", "real-time": "streaming",
    }
    return aliases.get(s, s)


def score_cv(cv_text: str, role: str, has_photo: bool = True,
             has_personal_section: bool = True, years_exp: int = 5,
             has_hobbies: bool = True) -> dict:
    """
    Score a CV for a specific Danish tech role.

    Parameters
    ----------
    cv_text : str
        Full CV text content (will be normalized to lowercase).
    role : str
        One of: FE-DEV, AI-SDEV, AI-ENG, GENAI, ML-ENG
    has_photo : bool
        CV includes professional headshot (DK norm).
    has_personal_section : bool
        CV includes hobbies/interests section.
    years_exp : int
        Years of relevant experience.
    has_hobbies : bool
        CV lists hobbies/interests entries.

    Returns
    -------
    dict with keys:
        - total_score: float (0-100)
        - label: str (Excellent/Strong/Good/Fair/Weak)
        - breakdown: dict of category → points
        - missing_keywords: list of must-have keywords not found
        - recommendations: list[str] — actionable improvements
    """
    if role not in ROLE_WEIGHTS:
        raise ValueError(f"Unknown role: {role}. Use: {list(ROLE_WEIGHTS.keys())}")

    cv_lower = cv_text.lower()
    cv_skills = {normalize_skill(s) for s in extract_skills_from_cv(cv_text)}
    weights = ROLE_WEIGHTS[role]
    keywords = ROLE_KEYWORDS[role]
    breakdown = {}
    recommendations = []

    # ── 1. Must-have keyword check ──────────────────────────────────
    must_have_found = keywords["must_have"] & cv_skills
    must_have_missing = keywords["must_have"] - cv_skills
    must_have_ratio = len(must_have_found) / max(len(keywords["must_have"]), 1)

    # ── 2. High-value keyword check ─────────────────────────────────
    high_value_found = keywords["high_value"] & cv_skills
    high_value_missing = keywords["high_value"] - cv_skills
    high_value_ratio = len(high_value_found) / max(len(keywords["high_value"]), 1)

    # ── 3. Differentiator keyword check ─────────────────────────────
    diff_found = keywords["differentiator"] & cv_skills
    diff_ratio = len(diff_found) / max(len(keywords["differentiator"]), 1)

    # ── 4. Danish compliance score ──────────────────────────────────
    danish_score = 0.0
    max_danish = weights.get("danish_compliance", 15)

    # Check for banned words
    banned_found = [w for w in DANISH_BANNED_WORDS if w in cv_lower]
    if banned_found:
        danish_score -= len(banned_found) * 2.0
        recommendations.append(f"Remove Danish-cultural-misfit words: {banned_found}")
    else:
        danish_score += max_danish * 0.4  # 40% for no banned words

    # Photo bonus
    if has_photo:
        danish_score += max_danish * 0.2
    else:
        recommendations.append("Add professional headshot (expected in DK)")

    # Personal section with hobbies
    if has_personal_section and has_hobbies:
        danish_score += max_danish * 0.25
    else:
        recommendations.append("Add personal/interests section with genuine hobbies")

    # Experience band (optimal: 3-7 years for mid-level)
    if 3 <= years_exp <= 7:
        danish_score += max_danish * 0.15
    elif years_exp < 2:
        danish_score += max_danish * 0.05
        recommendations.append("Consider targeting junior roles or gaining more experience")
    # else: proportional

    danish_score = max(0.0, min(danish_score, max_danish))

    # ── 5. Category scoring per role ───────────────────────────────
    if role == "FE-DEV":
        # Skill match (max 30)
        breakdown["skill_match"] = (must_have_ratio * 0.6 + high_value_ratio * 0.4) * weights["skill_match"]

        # Frontend depth (max 20) — check for advanced frontend keywords
        depth_signals = {"design system", "accessibility", "wcag", "performance",
                         "architecture", "responsive"}
        depth_count = len(depth_signals & cv_skills)
        breakdown["frontend_depth"] = min((depth_count / len(depth_signals)) * weights["frontend_depth"],
                                          weights["frontend_depth"])

        # AI integration (max 15)
        ai_signals = {"ai integration", "ai-powered", "llm integration",
                      "generative ai", "ai"}
        ai_count = len(ai_signals & cv_skills)
        breakdown["ai_integration"] = min((ai_count / len(ai_signals)) * weights["ai_integration"],
                                          weights["ai_integration"])

        breakdown["danish_compliance"] = danish_score

        # Experience signal (max 10)
        exp_signals = {"production", "e-commerce", "scale", "metrics",
                       "impact", "reduced", "improved", "delivered"}
        exp_count = len(exp_signals & cv_skills)
        breakdown["experience_signal"] = min((exp_count / len(exp_signals)) * weights["experience_signal"],
                                             weights["experience_signal"])

        if must_have_missing:
            recommendations.append(f"Add missing must-have skills: {must_have_missing}")

    elif role == "AI-SDEV":
        breakdown["python_depth"] = must_have_ratio * weights["python_depth"]
        if "python" in cv_skills and ("fastapi" in cv_skills or "flask" in cv_skills or "django" in cv_skills):
            breakdown["python_depth"] *= 1.2  # bonus for web framework
        breakdown["python_depth"] = min(breakdown["python_depth"], weights["python_depth"])

        breakdown["ml_stack"] = (must_have_ratio * 0.5 + high_value_ratio * 0.5) * weights["ml_stack"]
        if must_have_missing:
            recommendations.append(f"Add missing must-have: {must_have_missing}")
        if "aws" not in cv_skills and "azure" not in cv_skills and "gcp" not in cv_skills:
            recommendations.append("Add cloud provider (AWS/Azure/GCP) — critical for AI-SDEV")

        breakdown["production_deployment"] = diff_ratio * weights["production_deployment"]
        if "mlops" not in cv_skills:
            recommendations.append("Mention MLOps or model deployment practices")

        breakdown["danish_compliance"] = danish_score

        # Domain alignment (10 pts)
        domain_signals = {"healthcare", "fintech", "pharma", "logistics",
                          "retail", "e-commerce", "enterprise"}
        domain_count = len(domain_signals & cv_skills)
        breakdown["domain_alignment"] = min((domain_count / max(len(domain_signals), 1)) * weights["domain_alignment"],
                                            weights["domain_alignment"])

        # Full-stack bonus (10 pts)
        if "react" in cv_skills or "typescript" in cv_skills or "javascript" in cv_skills:
            breakdown["fullstack_bonus"] = weights["fullstack_bonus"] * 0.7
        else:
            breakdown["fullstack_bonus"] = 0.0
            recommendations.append("Highlight frontend skills for full-stack + AI combo")

        if high_value_missing:
            recommendations.append(f"Consider adding high-value skills: {list(high_value_missing)[:5]}")

    elif role == "AI-ENG":
        breakdown["ai_llm_depth"] = (must_have_ratio * 0.6 + diff_ratio * 0.4) * weights["ai_llm_depth"]
        if "rag" in cv_skills or "agent" in cv_skills or "agentic" in cv_skills:
            breakdown["ai_llm_depth"] = min(breakdown["ai_llm_depth"] * 1.15, weights["ai_llm_depth"])

        breakdown["ml_engineering_maturity"] = (high_value_ratio * 0.6 + must_have_ratio * 0.4) * weights["ml_engineering_maturity"]

        # Pipeline ownership (15 pts)
        pipeline_signals = {"model deployment", "model serving", "model monitoring",
                            "mlops", "ci/cd", "pipeline", "data pipelines"}
        pipe_count = len(pipeline_signals & cv_skills)
        breakdown["pipeline_ownership"] = min((pipe_count / max(len(pipeline_signals), 1)) * weights["pipeline_ownership"],
                                              weights["pipeline_ownership"])

        breakdown["danish_compliance"] = danish_score

        # Architecture signal (10 pts)
        arch_signals = {"architecture", "system design", "scalable", "distributed",
                        "microservices", "cloud-native"}
        arch_count = len(arch_signals & cv_skills)
        breakdown["architecture_signal"] = min((arch_count / max(len(arch_signals), 1)) * weights["architecture_signal"],
                                               weights["architecture_signal"])

        # Company fit (10 pts) — generic, relies on tailoring
        company_signals = {"healthcare", "finance", "logistics", "pharma",
                           "retail", "enterprise", "consulting"}
        company_count = len(company_signals & cv_skills)
        breakdown["company_fit"] = min((company_count / max(len(company_signals), 1)) * weights["company_fit"],
                                       weights["company_fit"])

        if must_have_missing:
            recommendations.append(f"Add: {must_have_missing}")
        if "rag" not in cv_skills:
            recommendations.append("Add RAG experience (28.6% of AI-ENG postings)")
        if "agentic" not in cv_skills and "agent" not in cv_skills:
            recommendations.append("Mention agentic AI patterns (fastest-growing segment)")

    elif role == "GENAI":
        breakdown["llm_production_depth"] = (must_have_ratio * 0.7 + diff_ratio * 0.3) * weights["llm_production_depth"]
        # Bonus for multi-provider/streaming
        if "streaming" in cv_skills and ("openai" in cv_skills or "openrouter" in cv_skills):
            breakdown["llm_production_depth"] = min(breakdown["llm_production_depth"] * 1.2,
                                                    weights["llm_production_depth"])

        # Agentic patterns (20 pts)
        agentic_signals = {"agent", "agents", "agentic", "tool use", "dag",
                            "orchestration", "multi-step", "reasoning"}
        agentic_count = len(agentic_signals & cv_skills)
        breakdown["agentic_patterns"] = min((agentic_count / max(len(agentic_signals), 1)) * weights["agentic_patterns"],
                                            weights["agentic_patterns"])

        # Framework breadth (15 pts)
        framework_signals = {"langchain", "llamaindindex", "langsmith", "haystack",
                             "semantic kernel", "guidance", "dspy"}
        framework_count = len(framework_signals & cv_skills)
        breakdown["framework_breadth"] = min((framework_count / max(len(framework_signals), 1)) * weights["framework_breadth"],
                                             weights["framework_breadth"])
        if framework_count == 0:
            recommendations.append("Add GenAI framework awareness (LangChain, LlamaIndex, etc.)")

        breakdown["danish_compliance"] = danish_score

        # Quantified impact (10 pts)
        impact_signals = {"reduced", "improved", "faster", "cheaper", "accuracy",
                          "latency", "cost", "uptime", "%"}
        impact_count = len(impact_signals & cv_skills)
        breakdown["quantified_impact"] = min((impact_count / max(len(impact_signals), 1)) * weights["quantified_impact"],
                                             weights["quantified_impact"])

        # Full-stack + GenAI combo (10 pts)
        if "react" in cv_skills or "typescript" in cv_skills:
            breakdown["fullstack_genai_combo"] = weights["fullstack_genai_combo"] * 0.8
        else:
            breakdown["fullstack_genai_combo"] = weights["fullstack_genai_combo"] * 0.3

        if must_have_missing:
            recommendations.append(f"Critical missing: {must_have_missing}")
        if "rag" not in cv_skills:
            recommendations.append("RAG is in 36.4% of GenAI postings — add if applicable")

    elif role == "ML-ENG":
        # MLOps maturity (30 pts)
        mlops_signals = {"docker", "kubernetes", "ci/cd", "terraform", "mlops",
                         "model deployment", "model serving", "model monitoring"}
        mlops_count = len(mlops_signals & cv_skills)
        breakdown["mlops_maturity"] = min((mlops_count / len(mlops_signals)) * weights["mlops_maturity"],
                                          weights["mlops_maturity"])

        # Infrastructure depth (25 pts)
        infra_signals = {"linux", "docker", "kubernetes", "ci/cd", "cloud",
                         "terraform", "iac", "infrastructure", "azure", "aws"}
        infra_count = len(infra_signals & cv_skills)
        breakdown["infrastructure_depth"] = min((infra_count / len(infra_signals)) * weights["infrastructure_depth"],
                                                weights["infrastructure_depth"])

        # Model lifecycle (15 pts)
        lifecycle_signals = {"training", "deployment", "monitoring", "retraining",
                             "versioning", "experiment", "pipeline"}
        lc_count = len(lifecycle_signals & cv_skills)
        breakdown["model_lifecycle"] = min((lc_count / len(lifecycle_signals)) * weights["model_lifecycle"],
                                           weights["model_lifecycle"])

        breakdown["danish_compliance"] = danish_score

        # DevOps culture (15 pts)
        devops_signals = {"automation", "reliability", "platform", "infrastructure",
                          "monitoring", "alerting", "observability", "resilience"}
        devops_count = len(devops_signals & cv_skills)
        breakdown["devops_culture"] = min((devops_count / len(devops_signals)) * weights["devops_culture"],
                                          weights["devops_culture"])

        if must_have_missing:
            recommendations.append(f"Missing MLOps stack: {must_have_missing}")
        if "kubernetes" not in cv_skills:
            recommendations.append("Add Kubernetes (44.4% of ML-ENG postings — CKAD cert path)")
        if "ci/cd" not in cv_skills and "github actions" not in cv_skills:
            recommendations.append("Make CI/CD explicit (GitHub Actions or similar)")

    # ── Final score ──────────────────────────────────────────────────
    total = sum(breakdown.values())
    total = round(min(max(total, 0.0), 100.1))

    # Label
    if total >= 85:
        label = "Excellent"
    elif total >= 70:
        label = "Strong"
    elif total >= 55:
        label = "Good"
    elif total >= 40:
        label = "Fair"
    else:
        label = "Weak"

    # Missing must-have keywords for output
    missing_keywords = list(keywords["must_have"] - cv_skills)

    return {
        "total_score": total,
        "label": label,
        "role": role,
        "breakdown": {k: round(v, 1) for k, v in breakdown.items()},
        "missing_keywords": missing_keywords,
        "recommendations": recommendations[:5],  # top 5 actionable
        "scored_at": datetime.now().isoformat(),
        "schema_version": "1.0.0",
    }


def extract_skills_from_cv(cv_text: str) -> list[str]:
    """
    Naive skill extraction from CV text.
    In production this would use a proper skill-ner model or structured input.
    This is a keyword-based fallback for the scorer MVP.
    """
    cv_lower = cv_text.lower()

    # Known skill dictionary for detection
    known_skills = [
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

    found = []
    for skill in known_skills:
        if skill in cv_lower:
            found.append(skill)

    return found


# ── Convenience: Score all roles at once ────────────────────────────
def score_all_roles(cv_text: str, **kwargs) -> dict:
    """Score a CV against all 5 target roles. Returns dict[role] -> result."""
    return {role: score_cv(cv_text, role, **kwargs) for role in ROLE_WEIGHTS}


# ── CLI usage ───────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python cv-scorer.py <cv_file_path> [role]")
        print(f"Roles: {', '.join(ROLE_WEIGHTS.keys())}")
        sys.exit(1)

    cv_path = sys.argv[1]
    with open(cv_path) as f:
        cv_text = f.read()

    role = sys.argv[2] if len(sys.argv) > 2 else None

    if role:
        result = score_cv(cv_text, role)
    else:
        result = score_all_roles(cv_text)

    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))
```

---

## 8. Score Interpretation & Career Ops Actions

| Score | Label | Danish Market Meaning | Career Ops Action |
|-------|-------|----------------------|-------------------|
| **90-100** | **Exceptional** | Top 5% match — will get interviews at any target company | Generate PDF immediately, send within 48h |
| **80-89** | **Excellent** | Strong match — competitive for all priority companies | Generate PDF, recommend 1 minor tweak |
| **70-79** | **Strong** | Competitive — will get interviews at majority of targets | Generate PDF, apply to priority 5 companies |
| **55-69** | **Good** | Viable — needs 1-2 skill additions for best results | Show skill gap recommendations, suggest CV rewrite |
| **40-54** | **Fair** | Below par — significant gaps vs. market | Trigger CV rewrite mode, show exact missing keywords |
| **0-39** | **Weak** | Major redesign needed — not marketable yet | Full CV overhaul using T1.1–T1.5 inputs |

### Daniel's Current Estimated Scores (per role)

Based on CV analysis from parent task:

| Role | Current Score | Main Gap | Fix |
|------|--------------|----------|-----|
| Frontend Developer | 82/100 (Strong) | Minor: add testing keywords | Add "Jest" or "Testing Library" to skills |
| AI Software Developer | 65/100 (Good) | Missing: AWS explicit, CI/CD explicit | Add "AWS (learning)" + "GitHub Actions" |
| AI Engineer | 68/100 (Good) | Missing: K8s, explicit "AI Architecture" | Add "Kubernetes (CKAD path)" + architecture framing |
| Generative AI Engineer | 85/100 (Excellent) | Minor: quantify LLM impact | Add latency/cost metrics to LLM projects |
| ML Engineer | 52/100 (Fair) | Missing: K8s, Terraform, MLOps | Need dedicated CV rewrite for this role |

---

## 9. Quarterly Update Checklist

- [ ] Re-aggregate job postings (T1.1) — check for new roles/skills
- [ ] Re-analyze skill demand (T1.2) — update keyword frequencies
- [ ] Re-benchmark salaries (T1.3) — adjust if market shifted
- [ ] Re-verify company targets (T1.4) — companies close/open hiring
- [ ] Re-check cultural norms (T1.5) — unlikely to change but verify
- [ ] Update ROLE_KEYWORDS and ROLE_WEIGHTS in the scoring function
- [ ] Bump schema version
- [ ] Append changelog

---

## 10. Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-06-30 | Initial creation. All 5 roles defined with keywords from 74 postings. Scoring function v1. Company tailoring from T1.4. |

---

## 11. Source References

| Source | File | Lines |
|--------|------|-------|
| T1.1 Job Postings | `dk-job-postings-2026Q3.json` | 1548 lines, 74 postings |
| T1.2 Skill Demand | `dk-skill-demand-2026Q3.md` | 180 lines, top 20 skills |
| T1.3 Salary | `dk-salary-benchmarks-2026Q3.md` | 326 lines, 5 roles x 5 locations |
| T1.4 Companies | `dk-company-targets.md` | 127 lines, 34 companies |
| T1.5 Culture | `dk-market-culture-guide.md` | 257 lines, norm registry |
| T2.1 Market Intelligence | `dk-market-intelligence-profile.md` | 269 lines, consolidated |
