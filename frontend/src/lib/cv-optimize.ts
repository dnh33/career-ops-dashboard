// CV Optimization Types & Scoring Logic
// Ported from backend/app/services/cv_optimize.py for client-side real-time feedback

export interface CvOptimizeRule {
  id: string;
  rule: string;
  category: string;
  currentCv: string;
  target: string;
  gap: number;
  gapLabel: string;
  priority: 'Critical' | 'High' | 'Medium' | 'Low';
  priorityVariant: 'warm' | 'error' | 'warning' | 'default';
  role: string;
  before: string;
  after: string;
  applied?: boolean;
}

export interface CvOptimizePayload {
  overallScore: number;
  keywordCoverage: number;
  criticalGaps: number;
  roleMatches: number;
  rules: CvOptimizeRule[];
}

export interface CvState {
  profile: {
    name: string;
    email: string;
    phone: string;
    roleTarget: string;
    linkedin: string;
    github: string;
    summary: string;
    location?: string;
    interests?: string;
    languages?: string;
  };
  experience: Array<{
    id: string;
    company: string;
    role: string;
    start: string;
    end: string;
    location: string;
    bullets: string;
  }>;
  skills: Array<{
    id: string;
    name: string;
    category: string;
    level: 'Expert' | 'Proficient' | 'Some' | 'Learning';
  }>;
  education: Array<{
    id: string;
    institution: string;
    degree: string;
    start: string;
    end: string;
  }>;
  appliedRuleIds?: string[];
}

const PRIORITY_VARIANTS: Record<string, 'warm' | 'error' | 'warning' | 'default'> = {
  Critical: 'warm',
  High: 'error',
  Medium: 'warning',
  Low: 'default',
};

const ROLE_SCORES: Record<string, number> = {
  frontend: 82,
  'ai-engineer': 68,
  fullstack: 74,
  all: 72,
};

// Hardcoded rules - must match backend/app/services/cv_optimize.py
const CV_RULES: Omit<CvOptimizeRule, 'priorityVariant' | 'applied'>[] = [
  {
    id: 'uni-aws',
    rule: 'Add explicit AWS cloud credential',
    category: 'Cloud',
    currentCv: 'Self-hosted VPS only',
    target: 'AWS Cloud Practitioner (in progress)',
    gap: 38,
    gapLabel: '38%',
    priority: 'Critical',
    role: 'all',
    before: 'Infrastructure: Linux VPS, Docker, self-hosted deployments',
    after: 'Cloud: AWS (Cloud Practitioner in progress), Docker, Linux VPS, self-hosted + cloud hybrid',
  },
  {
    id: 'uni-k8s',
    rule: 'Document Kubernetes learning path',
    category: 'DevOps',
    currentCv: 'Docker only',
    target: 'Kubernetes (CKAD path, 8 weeks)',
    gap: 25,
    gapLabel: '25%',
    priority: 'Critical',
    role: 'ai-engineer',
    before: 'Containerization: Docker, docker-compose',
    after: 'Container orchestration: Docker, Kubernetes (CKAD in progress), docker-compose',
  },
  {
    id: 'uni-cicd',
    rule: 'Add CI/CD pipeline evidence',
    category: 'DevOps',
    currentCv: 'Git workflows only',
    target: 'GitHub Actions CI/CD pipelines',
    gap: 18,
    gapLabel: '18%',
    priority: 'High',
    role: 'all',
    before: 'Version control: Git, feature branches, code review',
    after: 'CI/CD: GitHub Actions workflows, automated testing, Git feature branches',
  },
  {
    id: 'fe-testing',
    rule: 'Add frontend testing keywords',
    category: 'Frontend',
    currentCv: 'No testing frameworks listed',
    target: 'Jest + Testing Library',
    gap: 12,
    gapLabel: '12%',
    priority: 'Medium',
    role: 'frontend',
    before: 'Skills: React, TypeScript, Tailwind CSS, Astro',
    after: 'Skills: React 19, TypeScript, Testing Library, Jest, Tailwind CSS, Astro',
  },
  {
    id: 'fe-a11y',
    rule: 'Highlight accessibility expertise',
    category: 'Frontend',
    currentCv: 'Accessibility mentioned briefly',
    target: 'WCAG 2.1 AA + a11y audit experience',
    gap: 10,
    gapLabel: '10%',
    priority: 'Medium',
    role: 'frontend',
    before: 'Built responsive UI components with React and Tailwind',
    after: 'Built WCAG 2.1 AA compliant components; accessibility audits with axe-core',
  },
  {
    id: 'fe-ai-integration',
    rule: 'Frame AI-powered frontend work',
    category: 'Frontend',
    currentCv: 'LLM integration in backend context',
    target: 'AI Integration + Server Components',
    gap: 8,
    gapLabel: '8%',
    priority: 'Medium',
    role: 'frontend',
    before: 'Integrated OpenRouter API for job evaluation features',
    after: 'AI-powered frontend: LLM integration, streaming UI, React Server Components',
  },
  {
    id: 'ai-pytorch',
    rule: 'Explicit PyTorch production framing',
    category: 'AI/ML',
    currentCv: 'PyTorch as user-level',
    target: 'Production ML with PyTorch',
    gap: 22,
    gapLabel: '22%',
    priority: 'High',
    role: 'ai-engineer',
    before: 'Used PyTorch models via Hugging Face APIs',
    after: 'Production ML: PyTorch inference pipelines, model serving, Hugging Face integration',
  },
  {
    id: 'ai-terraform',
    rule: 'Document infrastructure-as-code',
    category: 'DevOps',
    currentCv: 'Manual deployment scripts',
    target: 'Terraform + Docker workflow',
    gap: 15,
    gapLabel: '15%',
    priority: 'High',
    role: 'ai-engineer',
    before: 'Deployed services via shell scripts and Docker',
    after: 'IaC: Terraform modules, Docker, automated provisioning workflows',
  },
  {
    id: 'ai-architecture',
    rule: 'Add AI architecture framing',
    category: 'AI/ML',
    currentCv: 'Feature-level AI work',
    target: 'End-to-end AI system architecture',
    gap: 20,
    gapLabel: '20%',
    priority: 'High',
    role: 'ai-engineer',
    before: 'Built RAG pipeline for job description analysis',
    after: 'AI Architecture: RAG pipelines, vector stores, LLM routing, observability',
  },
  {
    id: 'genai-metrics',
    rule: 'Quantify LLM project impact',
    category: 'Generative AI',
    currentCv: 'Qualitative LLM descriptions',
    target: 'Latency + cost metrics on LLM features',
    gap: 6,
    gapLabel: '6%',
    priority: 'Low',
    role: 'ai-engineer',
    before: 'Implemented LLM-powered job evaluation',
    after: 'LLM evaluation pipeline: 2.1s p95 latency, 40% cost reduction via model routing',
  },
  {
    id: 'genai-rag',
    rule: 'Expand RAG stack keywords',
    category: 'Generative AI',
    currentCv: 'Basic RAG mention',
    target: 'RAG + embeddings + vector DB',
    gap: 9,
    gapLabel: '9%',
    priority: 'Medium',
    role: 'ai-engineer',
    before: 'RAG for document retrieval in career tools',
    after: 'RAG stack: embeddings, vector retrieval, chunking strategies, prompt templates',
  },
  {
    id: 'ml-mlops',
    rule: 'Add MLOps deployment keywords',
    category: 'MLOps',
    currentCv: 'No MLOps section',
    target: 'Model deployment + monitoring',
    gap: 35,
    gapLabel: '35%',
    priority: 'Critical',
    role: 'ai-engineer',
    before: 'Machine learning experiments with Python',
    after: 'MLOps: model deployment, experiment tracking, monitoring, rollback strategies',
  },
  {
    id: 'ml-k8s',
    rule: 'Kubernetes for ML workloads',
    category: 'MLOps',
    currentCv: 'Not listed',
    target: 'K8s model serving (KServe/Kubeflow awareness)',
    gap: 28,
    gapLabel: '28%',
    priority: 'Critical',
    role: 'ai-engineer',
    before: 'Deployed ML models via Docker containers',
    after: 'ML serving: Docker, Kubernetes (CKAD path), containerized inference',
  },
  {
    id: 'fs-node',
    rule: 'Balance fullstack with Node.js depth',
    category: 'Fullstack',
    currentCv: 'Python-primary backend',
    target: 'Node.js + Python polyglot backend',
    gap: 14,
    gapLabel: '14%',
    priority: 'Medium',
    role: 'fullstack',
    before: 'Backend: FastAPI, Python, PostgreSQL',
    after: 'Backend: FastAPI + Node.js, Python, PostgreSQL, REST + GraphQL APIs',
  },
  {
    id: 'fs-api',
    rule: 'API-driven architecture keywords',
    category: 'Fullstack',
    currentCv: 'REST API mentioned',
    target: 'API-first + microservices awareness',
    gap: 11,
    gapLabel: '11%',
    priority: 'Medium',
    role: 'fullstack',
    before: 'Built REST APIs with FastAPI',
    after: 'API-driven architecture: REST, OpenAPI, service boundaries, event-driven patterns',
  },
  {
    id: 'dk-photo',
    rule: 'Include professional headshot',
    category: 'Danish CV',
    currentCv: 'No photo on CV',
    target: 'Professional headshot (DK norm)',
    gap: 100,
    gapLabel: '100%',
    priority: 'High',
    role: 'all',
    before: '[Name]\n[Contact details]',
    after: '[Photo]\n[Name]\n[Contact details]',
  },
  {
    id: 'dk-hobbies',
    rule: 'Add interests/hobbies section',
    category: 'Danish CV',
    currentCv: 'No hobbies section',
    target: '2–3 genuine hobby entries',
    gap: 100,
    gapLabel: '100%',
    priority: 'High',
    role: 'all',
    before: 'Languages: Danish C2, English C1',
    after: 'Languages: Danish C2, English C1\nInterests: Open-source contributions, cycling, board games',
  },
  {
    id: 'dk-tone',
    rule: 'Remove hype language from profile',
    category: 'Danish CV',
    currentCv: 'Uses "passionate" and "innovative"',
    target: 'Humbly collaborative tone',
    gap: 50,
    gapLabel: '50%',
    priority: 'Medium',
    role: 'all',
    before: 'Passionate innovator building world-class AI solutions',
    after: 'Collaborative engineer delivering efficient, sustainable AI-powered tools',
  },
  {
    id: 'fe-tailwind',
    rule: 'Design system + Tailwind prominence',
    category: 'Frontend',
    currentCv: 'CSS listed generically',
    target: 'Design tokens + Tailwind v4',
    gap: 7,
    gapLabel: '7%',
    priority: 'Low',
    role: 'frontend',
    before: 'CSS, responsive layouts',
    after: 'Design systems, Tailwind CSS v4, design tokens, component libraries',
  },
  {
    id: 'ai-sql',
    rule: 'Explicit PostgreSQL on CV',
    category: 'Data',
    currentCv: 'SQL listed without engine',
    target: 'SQL / PostgreSQL + query optimization',
    gap: 13,
    gapLabel: '13%',
    priority: 'Medium',
    role: 'ai-engineer',
    before: 'SQL for data queries',
    after: 'SQL / PostgreSQL: schema design, indexing, query optimization',
  },
  {
    id: 'uni-git',
    rule: 'Git as baseline expectation',
    category: 'DevOps',
    currentCv: 'Git implied but not prominent',
    target: 'Git + branching strategy explicit',
    gap: 5,
    gapLabel: '5%',
    priority: 'Low',
    role: 'all',
    before: 'Collaborative development workflows',
    after: 'Git: trunk-based development, PR reviews, conventional commits',
  },
  {
    id: 'zendesk-tailor',
    rule: 'Zendesk-specific AI Agents framing',
    category: 'Tailoring',
    currentCv: 'Generic AI experience',
    target: 'AI Agents + ML Pipelines for support',
    gap: 16,
    gapLabel: '16%',
    priority: 'High',
    role: 'ai-engineer',
    before: 'Built AI evaluation tools for job applications',
    after: 'AI Agents: automated support workflows, ML pipelines, Python + Spark awareness',
  },
  {
    id: 'corti-tailor',
    rule: 'Corti healthcare AI framing',
    category: 'Tailoring',
    currentCv: 'No healthcare domain signal',
    target: 'MedTech / clinical AI interest',
    gap: 19,
    gapLabel: '19%',
    priority: 'Medium',
    role: 'ai-engineer',
    before: 'AI tools for career optimization',
    after: 'Healthcare AI interest: clinical NLP, responsible AI, real-time inference',
  },
  {
    id: 'fe-perf',
    rule: 'Web performance metrics',
    category: 'Frontend',
    currentCv: 'No Core Web Vitals mention',
    target: 'LCP/FID/CLS optimization',
    gap: 11,
    gapLabel: '11%',
    priority: 'Medium',
    role: 'frontend',
    before: 'Optimized frontend performance',
    after: 'Core Web Vitals: LCP < 2.5s, code splitting, lazy loading, bundle analysis',
  },
];

function toPriorityVariant(priority: string): 'warm' | 'error' | 'warning' | 'default' {
  return PRIORITY_VARIANTS[priority] || 'default';
}

function rulesForRole(role: string): typeof CV_RULES {
  if (role === 'all') return CV_RULES;
  return CV_RULES.filter(rule => rule.role === role || rule.role === 'all');
}

function keywordCoverage(rules: typeof CV_RULES): number {
  if (!rules.length) return 0;
  const lowGap = rules.filter(rule => rule.gap <= 10).length;
  return Math.round((lowGap / rules.length) * 100);
}

function computeOptimizePayload(role: string, appliedRuleIds: string[] = []): CvOptimizePayload {
  const baseRules = rulesForRole(role);
  const rules = baseRules.map(rule => ({
    ...rule,
    priorityVariant: toPriorityVariant(rule.priority),
    applied: appliedRuleIds.includes(rule.id),
  }));
  const critical = rules.filter(r => r.priority === 'Critical').length;
  const roleMatches = Object.values(ROLE_SCORES).filter(score => score >= 70).length;
  const overall = ROLE_SCORES[role] || ROLE_SCORES.all;
  const coverage = keywordCoverage(rules);

  return {
    overallScore: overall,
    keywordCoverage: coverage,
    criticalGaps: critical,
    roleMatches,
    rules,
  };
}

function computeCvSummary(state: CvState): string {
  const parts: string[] = [];
  if (state.profile.summary) {
    parts.push(state.profile.summary);
  }
  if (state.experience.length) {
    const recent = state.experience[0];
    parts.push(`${recent.role} at ${recent.company}`);
  }
  const skillNames = state.skills.map(s => s.name).slice(0, 5).join(', ');
  if (skillNames) parts.push(`Skills: ${skillNames}`);
  return parts.join('. ');
}

export {
  CV_RULES,
  ROLE_SCORES,
  PRIORITY_VARIANTS,
  rulesForRole,
  keywordCoverage,
  computeOptimizePayload,
  computeCvSummary,
  type CvOptimizeRule,
  type CvOptimizePayload,
  type CvState,
};