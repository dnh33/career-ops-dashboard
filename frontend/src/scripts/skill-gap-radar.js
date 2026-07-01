// Skill Gap Radar — market demand vs profile (T4.2)
// Data: GET /api/market/overview + research fallbacks from dk-market-intelligence-profile.md

const LEVEL_SCORES = {
  Expert: 90,
  Some: 55,
  Learning: 35,
  None: 10,
};

/** Daniel's profile levels (dk-market-intelligence-profile.md §1.2) */
const USER_SKILL_LEVELS = {
  TypeScript: 'Expert',
  React: 'Expert',
  'React.js': 'Expert',
  Docker: 'Expert',
  Python: 'Expert',
  Git: 'Expert',
  'LLM Integration': 'Expert',
  'Prompt Engineering': 'Expert',
  HTML: 'Some',
  CSS: 'Some',
  'CSS/Tailwind': 'Some',
  'Node.js': 'Some',
  SQL: 'Some',
  PostgreSQL: 'Some',
  Linux: 'Some',
  'Linux/VPS': 'Some',
  AWS: 'Learning',
  Kubernetes: 'Learning',
  Terraform: 'Learning',
  'CI/CD': 'Learning',
  PyTorch: 'None',
  TensorFlow: 'None',
  'Power BI': 'None',
  Figma: 'None',
  Statistics: 'None',
  'REST API': 'Some',
  Astro: 'Expert',
  Accessibility: 'Expert',
};

/** Top 20 market demand (dk-skill-demand-2026Q3.md) — supplements API */
const RESEARCH_MARKET = {
  Git: { category: 'devops', pct: 78.3 },
  Python: { category: 'backend', pct: 58.0 },
  Docker: { category: 'devops', pct: 47.8 },
  AWS: { category: 'cloud', pct: 37.7 },
  SQL: { category: 'data', pct: 34.8 },
  TypeScript: { category: 'frontend', pct: 27.5 },
  Kubernetes: { category: 'devops', pct: 24.6 },
  'React.js': { category: 'frontend', pct: 23.2 },
  Linux: { category: 'devops', pct: 14.5 },
  'REST API': { category: 'backend', pct: 13.0 },
  PyTorch: { category: 'ai', pct: 11.6 },
  CSS: { category: 'frontend', pct: 11.6 },
  Terraform: { category: 'devops', pct: 11.6 },
  'Power BI': { category: 'data', pct: 11.6 },
  Statistics: { category: 'data', pct: 10.1 },
  HTML: { category: 'frontend', pct: 10.1 },
  Figma: { category: 'frontend', pct: 10.1 },
  JavaScript: { category: 'frontend', pct: 10.1 },
  TensorFlow: { category: 'ai', pct: 8.7 },
  'CI/CD': { category: 'devops', pct: 8.7 },
};

const SKILL_ALIASES = {
  'React.js': 'React',
  SQL: 'PostgreSQL',
  CSS: 'CSS/Tailwind',
  Linux: 'Linux/VPS',
};

const CATEGORY_LABELS = {
  frontend: 'Frontend',
  backend: 'Backend',
  devops: 'DevOps',
  cloud: 'Cloud',
  data: 'Data',
  ai: 'AI/ML',
};

const ROLE_TARGETS = {
  'ai-engineer': [
    'Python', 'SQL', 'PyTorch', 'TensorFlow', 'Statistics', 'AWS', 'Kubernetes',
    'Docker', 'CI/CD', 'Git', 'LLM Integration', 'Prompt Engineering',
  ],
  'frontend-engineer': [
    'Git', 'TypeScript', 'React', 'HTML', 'CSS/Tailwind', 'REST API',
    'Figma', 'Node.js', 'Accessibility', 'Astro',
  ],
  'full-stack-engineer': [
    'Docker', 'AWS', 'TypeScript', 'React', 'SQL', 'REST API', 'Python',
    'Kubernetes', 'CI/CD', 'Git', 'Node.js', 'Linux/VPS',
  ],
};

/** Section 3 — Top 10 skills to add/highlight (dk-market-intelligence-profile.md) */
const LEARNING_PATH_ITEMS = [
  {
    title: 'LLM Application Patterns (RAG, agents, streaming)',
    category: 'AI/ML',
    duration: 'CV rewrite',
    resource: 'https://react.dev',
    gap: 'low',
    roles: ['ai-engineer', 'full-stack-engineer'],
  },
  {
    title: 'TypeScript + React patterns (server components, streaming)',
    category: 'Frontend',
    duration: '2–3 weeks',
    resource: 'https://react.dev/learn',
    gap: 'none',
    roles: ['frontend-engineer', 'full-stack-engineer'],
  },
  {
    title: 'Python (production grade)',
    category: 'Programming',
    duration: 'Highlight on CV',
    resource: 'https://fastapi.tiangolo.com/',
    gap: 'none',
    roles: ['ai-engineer', 'full-stack-engineer'],
  },
  {
    title: 'AWS fundamentals',
    category: 'Cloud',
    duration: '2–4 weeks',
    resource: 'https://aws.amazon.com/certification/cloud-practitioner/',
    gap: 'high',
    roles: ['ai-engineer', 'full-stack-engineer'],
  },
  {
    title: 'Docker + container orchestration (K8s)',
    category: 'DevOps',
    duration: '8–12 weeks',
    resource: 'https://kodekloud.com/courses/certified-kubernetes-application-developer/',
    gap: 'high',
    roles: ['ai-engineer', 'full-stack-engineer'],
  },
  {
    title: 'CI/CD (GitHub Actions)',
    category: 'DevOps',
    duration: '1–2 weeks',
    resource: 'https://docs.github.com/en/actions',
    gap: 'medium',
    roles: ['ai-engineer', 'full-stack-engineer'],
  },
  {
    title: 'SQL / PostgreSQL (explicit CV naming)',
    category: 'Data',
    duration: 'CV update',
    resource: 'https://use-the-index-luke.com/',
    gap: 'medium',
    roles: ['ai-engineer', 'full-stack-engineer'],
  },
  {
    title: 'Prompt engineering / LLM ops',
    category: 'AI/ML',
    duration: 'CV terminology',
    resource: 'https://platform.openai.com/docs/guides/prompt-engineering',
    gap: 'low',
    roles: ['ai-engineer'],
  },
  {
    title: 'Accessibility (WCAG) + Design Systems',
    category: 'Frontend',
    duration: '2–3 weeks',
    resource: 'https://web.dev/accessible/',
    gap: 'low',
    roles: ['frontend-engineer'],
  },
  {
    title: 'Danish language (competitive edge)',
    category: 'Language',
    duration: 'Keep prominent',
    resource: null,
    gap: 'none',
    roles: ['ai-engineer', 'frontend-engineer', 'full-stack-engineer'],
  },
];

const STORAGE_PREFIX = 'skill-gap-learning-';
const FOCUS_STORAGE_KEY = 'skill-gap-cv-focus';

class SkillGapRadar {
  constructor() {
    this.apiBase = '';
    this.marketData = null;
    this.currentRole = 'frontend-engineer';
    this.radarCategories = [];
    this.hoveredAxis = -1;
    this.prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    this.canvas = null;
    this.ctx = null;
    this.tooltip = null;
    this.colors = {};
    this.abortController = new AbortController();
    this.init();
  }

  async init() {
    try {
      const roleSelect = document.getElementById('roleTarget');
      if (roleSelect) this.currentRole = roleSelect.value;

      await this.fetchMarketData();
      this.resolveColors();
      this.renderAll();
      this.setupEventListeners();
    } catch (error) {
      console.error('Failed to initialize skill gap radar:', error);
      this.showErrorState();
    }
  }

  async fetchMarketData() {
    const response = await fetch(`${this.apiBase}/api/market/overview`, { cache: 'no-store' });
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    this.marketData = await response.json();
  }

  resolveColors() {
    const root = getComputedStyle(document.documentElement);
    this.colors = {
      gradeHigh: root.getPropertyValue('--grade-high').trim(),
      accentPrimary: root.getPropertyValue('--accent-primary').trim(),
      borderDefault: root.getPropertyValue('--border-default').trim(),
      textMuted: root.getPropertyValue('--text-muted').trim(),
      textPrimary: root.getPropertyValue('--text-primary').trim(),
      error: root.getPropertyValue('--error').trim(),
    };
  }

  normalizeSkillName(name) {
    return SKILL_ALIASES[name] || name;
  }

  canonicalSkill(name) {
    const normalized = this.normalizeSkillName(name);
    if (USER_SKILL_LEVELS[normalized] !== undefined) return normalized;
    if (USER_SKILL_LEVELS[name] !== undefined) return name;
    return normalized;
  }

  findSkillDemand(skill) {
    const canonical = this.canonicalSkill(skill);
    const fromApi = this.marketData?.skillDemand?.find((item) => {
      const key = this.canonicalSkill(item.skill);
      return key === canonical || item.skill === skill;
    });
    if (fromApi) return fromApi;

    const research = RESEARCH_MARKET[skill] || RESEARCH_MARKET[canonical];
    if (research) {
      return { skill: canonical, category: research.category, pct: research.pct, gap: null };
    }
    return null;
  }

  findSkillGap(skill) {
    const canonical = this.canonicalSkill(skill);
    return this.marketData?.skillGaps?.find((item) => {
      const key = this.canonicalSkill(item.skill);
      return key === canonical || item.skill === skill;
    }) || null;
  }

  getUserLevelLabel(skill) {
    const canonical = this.canonicalSkill(skill);
    return USER_SKILL_LEVELS[canonical] || USER_SKILL_LEVELS[skill] || 'None';
  }

  getUserLevelScore(skill) {
    return LEVEL_SCORES[this.getUserLevelLabel(skill)] ?? LEVEL_SCORES.None;
  }

  getMarketPct(skill) {
    const demand = this.findSkillDemand(skill);
    if (demand) return demand.pct;
    const gap = this.findSkillGap(skill);
    return gap?.marketPct ?? 0;
  }

  getCategory(skill) {
    const demand = this.findSkillDemand(skill);
    if (demand?.category) return demand.category;
    const research = RESEARCH_MARKET[skill] || RESEARCH_MARKET[this.canonicalSkill(skill)];
    return research?.category ?? 'other';
  }

  computeGapSeverity(skill) {
    const demand = this.findSkillDemand(skill);
    if (demand?.gap) return demand.gap;

    const gapEntry = this.findSkillGap(skill);
    if (gapEntry) return gapEntry.severity;

    const level = this.getUserLevelLabel(skill);
    const marketPct = this.getMarketPct(skill);

    if (level === 'Expert') return 'none';
    if (level === 'Some') return marketPct >= 30 ? 'medium' : 'low';
    if (level === 'Learning') return marketPct >= 25 ? 'medium' : 'low';
    if (level === 'None') return marketPct >= 20 ? 'high' : marketPct >= 10 ? 'medium' : 'low';
    return 'low';
  }

  getAction(skill) {
    const gapEntry = this.findSkillGap(skill);
    if (gapEntry?.action) return gapEntry.action;

    const severity = this.computeGapSeverity(skill);
    const level = this.getUserLevelLabel(skill);
    if (level === 'Expert' || severity === 'none') return 'Strength — highlight on CV';
    if (level === 'Some') return `Rename/highlight "${skill}" explicitly on CV`;
    if (level === 'Learning') return `Continue learning — add "${skill}" to skills section`;
    return `Prioritize acquiring ${skill}`;
  }

  severityToStars(severity) {
    const map = { high: 5, medium: 3, low: 2, none: 1 };
    return map[severity] ?? 1;
  }

  renderStars(count) {
    const filled = '★'.repeat(count);
    const empty = '☆'.repeat(5 - count);
    return `<span class="priority-stars" aria-label="${count} of 5 priority"><span class="filled">${filled}</span><span class="empty">${empty}</span></span>`;
  }

  getRoleSkills() {
    return ROLE_TARGETS[this.currentRole] || [];
  }

  getCategoryRadarData() {
    const roleSkills = this.getRoleSkills();
    const categories = new Map();

    for (const skill of roleSkills) {
      const category = this.getCategory(skill);
      if (!categories.has(category)) {
        categories.set(category, { market: [], profile: [] });
      }
      const bucket = categories.get(category);
      bucket.market.push(this.getMarketPct(skill));
      bucket.profile.push(this.getUserLevelScore(skill));
    }

    return Array.from(categories.entries())
      .map(([category, values]) => ({
        category,
        label: CATEGORY_LABELS[category] || category,
        marketAvg: values.market.length
          ? values.market.reduce((a, b) => a + b, 0) / values.market.length
          : 0,
        profileAvg: values.profile.length
          ? values.profile.reduce((a, b) => a + b, 0) / values.profile.length
          : 0,
        severity: this.categoryGapSeverity(values.market, values.profile),
      }))
      .sort((a, b) => b.marketAvg - a.marketAvg);
  }

  categoryGapSeverity(marketValues, profileValues) {
    const marketAvg = marketValues.reduce((a, b) => a + b, 0) / marketValues.length;
    const profileAvg = profileValues.reduce((a, b) => a + b, 0) / profileValues.length;
    const delta = marketAvg - profileAvg;
    if (delta >= 25) return 'high';
    if (delta >= 12) return 'medium';
    if (delta >= 5) return 'low';
    return 'none';
  }

  getGapTableRows() {
    const roleSkills = new Set(this.getRoleSkills());
    const rows = new Map();

    const addRow = (skill) => {
      const canonical = this.canonicalSkill(skill);
      if (rows.has(canonical)) return;
      rows.set(canonical, {
        skill: canonical,
        category: this.getCategory(skill),
        marketPct: this.getMarketPct(skill),
        userLevel: this.getUserLevelLabel(skill),
        severity: this.computeGapSeverity(skill),
        action: this.getAction(skill),
      });
    };

    for (const item of this.marketData?.skillDemand ?? []) {
      const canonical = this.canonicalSkill(item.skill);
      if (roleSkills.has(canonical) || roleSkills.has(item.skill)) {
        addRow(item.skill);
      }
    }

    for (const skill of roleSkills) addRow(skill);

    const severityOrder = { high: 0, medium: 1, low: 2, none: 3 };
    return Array.from(rows.values()).sort((a, b) => {
      const sevDiff = (severityOrder[a.severity] ?? 4) - (severityOrder[b.severity] ?? 4);
      if (sevDiff !== 0) return sevDiff;
      return b.marketPct - a.marketPct;
    });
  }

  renderAll() {
    if (!this.marketData) return;
    this.radarCategories = this.getCategoryRadarData();
    this.renderRadar();
    this.renderGapTable();
    this.renderLearningPath();
  }

  renderRadar() {
    this.canvas = document.getElementById('skillRadar');
    this.tooltip = document.getElementById('radarTooltip');
    if (!this.canvas) return;

    this.canvas.setAttribute('role', 'img');
    this.canvas.setAttribute(
      'aria-label',
      'Radar chart comparing market demand and your profile across skill categories',
    );
    this.canvas.classList.add('cursor-pointer');

    this.ctx = this.canvas.getContext('2d');
    this.resizeCanvas();
    this.drawRadar();
  }

  resizeCanvas() {
    const wrapper = this.canvas.parentElement;
    const size = Math.min(wrapper?.clientWidth || 500, 500);
    const dpr = window.devicePixelRatio || 1;

    this.canvas.width = size * dpr;
    this.canvas.height = size * dpr;
    this.canvas.style.width = `${size}px`;
    this.canvas.style.height = `${size}px`;
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    this.radarSize = size;
    this.radarCenter = size / 2;
    this.radarRadius = size * 0.36;
    this.labelOffset = 22;
  }

  getAxisPoint(index, value, maxRadius) {
    const count = this.radarCategories.length || 1;
    const angle = (Math.PI * 2 * index) / count - Math.PI / 2;
    const radius = (value / 100) * maxRadius;
    return {
      x: this.radarCenter + Math.cos(angle) * radius,
      y: this.radarCenter + Math.sin(angle) * radius,
      angle,
    };
  }

  colorToRgba(color, alpha) {
    const trimmed = (color || '').trim();
    if (trimmed.startsWith('rgb')) {
      const parts = trimmed.match(/[\d.]+/g);
      if (parts?.length >= 3) {
        return `rgba(${parts[0]}, ${parts[1]}, ${parts[2]}, ${alpha})`;
      }
    }
    const cleaned = trimmed.replace('#', '');
    const full = cleaned.length === 3
      ? cleaned.split('').map((c) => c + c).join('')
      : cleaned;
    const num = parseInt(full, 16);
    if (Number.isNaN(num)) return `rgba(148, 163, 184, ${alpha})`;
    const r = (num >> 16) & 255;
    const g = (num >> 8) & 255;
    const b = num & 255;
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  }

  drawRadar() {
    const { ctx } = this;
    const size = this.radarSize;
    ctx.clearRect(0, 0, size, size);

    const count = this.radarCategories.length;
    if (count === 0) {
      ctx.font = '0.875rem var(--font-sans, Inter, system-ui, sans-serif)';
      ctx.fillStyle = this.colors.textMuted;
      ctx.textAlign = 'center';
      ctx.fillText('No category data for this role', this.radarCenter, this.radarCenter);
      return;
    }

    const ticks = [20, 40, 60, 80, 100];
    ctx.strokeStyle = this.colors.borderDefault;
    ctx.lineWidth = 1;

    for (const tick of ticks) {
      ctx.beginPath();
      for (let i = 0; i <= count; i++) {
        const point = this.getAxisPoint(i % count, tick, this.radarRadius);
        if (i === 0) ctx.moveTo(point.x, point.y);
        else ctx.lineTo(point.x, point.y);
      }
      ctx.closePath();
      ctx.stroke();
    }

    for (let i = 0; i < count; i++) {
      const outer = this.getAxisPoint(i, 100, this.radarRadius);
      ctx.beginPath();
      ctx.moveTo(this.radarCenter, this.radarCenter);
      ctx.lineTo(outer.x, outer.y);
      ctx.stroke();
    }

    const marketValues = this.radarCategories.map((c) => c.marketAvg);
    const profileValues = this.radarCategories.map((c) => c.profileAvg);

    this.drawPolygon(marketValues, this.colors.gradeHigh, 0.2, 2);
    this.drawPolygon(profileValues, this.colors.accentPrimary, 0.2, 2);

    ctx.font = '0.75rem var(--font-display, Sora, system-ui, sans-serif)';
    ctx.fillStyle = this.colors.textMuted;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    for (let i = 0; i < count; i++) {
      const outer = this.getAxisPoint(i, 100, this.radarRadius + this.labelOffset);
      const label = this.radarCategories[i].label;
      ctx.fillText(label, outer.x, outer.y);

      if (i === this.hoveredAxis) {
        const axisOuter = this.getAxisPoint(i, 100, this.radarRadius);
        ctx.beginPath();
        ctx.arc(axisOuter.x, axisOuter.y, 5, 0, Math.PI * 2);
        ctx.fillStyle = this.colors.accentPrimary;
        ctx.fill();
      }
    }
  }

  drawPolygon(values, strokeColor, fillAlpha, lineWidth) {
    const { ctx } = this;
    const count = values.length;

    ctx.beginPath();
    for (let i = 0; i < count; i++) {
      const point = this.getAxisPoint(i, values[i], this.radarRadius);
      if (i === 0) ctx.moveTo(point.x, point.y);
      else ctx.lineTo(point.x, point.y);
    }
    ctx.closePath();

    ctx.fillStyle = this.colorToRgba(strokeColor, fillAlpha);
    ctx.fill();
    ctx.strokeStyle = strokeColor;
    ctx.lineWidth = lineWidth;
    ctx.stroke();
  }

  getAxisFromMouse(event) {
    const rect = this.canvas.getBoundingClientRect();
    const scaleX = this.radarSize / rect.width;
    const scaleY = this.radarSize / rect.height;
    const x = (event.clientX - rect.left) * scaleX;
    const y = (event.clientY - rect.top) * scaleY;
    const dx = x - this.radarCenter;
    const dy = y - this.radarCenter;
    const dist = Math.sqrt(dx * dx + dy * dy);

    if (dist > this.radarRadius + 40) return -1;

    let angle = Math.atan2(dy, dx) + Math.PI / 2;
    if (angle < 0) angle += Math.PI * 2;

    const count = this.radarCategories.length;
    if (count === 0) return -1;
    const slice = (Math.PI * 2) / count;
    return Math.round(angle / slice) % count;
  }

  showTooltip(index, event) {
    if (!this.tooltip || index < 0 || !this.radarCategories[index]) return;

    const cat = this.radarCategories[index];
    this.tooltip.innerHTML = `
      <strong>${cat.label}</strong>
      <div class="tooltip-row">
        <span class="tooltip-label">Market avg</span>
        <span class="tooltip-value">${cat.marketAvg.toFixed(1)}%</span>
      </div>
      <div class="tooltip-row">
        <span class="tooltip-label">Your profile</span>
        <span class="tooltip-value">${cat.profileAvg.toFixed(0)}%</span>
      </div>
      <div class="tooltip-row">
        <span class="tooltip-label">Gap</span>
        <span class="tooltip-value">${cat.severity}</span>
      </div>
    `;

    const wrapper = this.canvas.parentElement;
    const rect = wrapper.getBoundingClientRect();
    this.tooltip.style.left = `${event.clientX - rect.left + 12}px`;
    this.tooltip.style.top = `${event.clientY - rect.top - 12}px`;
    this.tooltip.classList.add('visible');
    this.tooltip.style.opacity = '1';
  }

  hideTooltip() {
    if (!this.tooltip) return;
    this.tooltip.classList.remove('visible');
    this.tooltip.style.opacity = '0';
  }

  renderGapTable() {
    const tbody = document.getElementById('gapTableBody');
    if (!tbody) return;

    const rows = this.getGapTableRows();

    if (rows.length === 0) {
      tbody.innerHTML = '<tr><td colspan="7" class="empty-row" style="padding: 2rem; text-align: center; font-style: italic; color: var(--text-muted);">No gap data for this role</td></tr>';
      return;
    }

    tbody.innerHTML = rows.map((row) => {
      const categoryLabel = CATEGORY_LABELS[row.category] || row.category;
      const stars = this.severityToStars(row.severity);

      return `
        <tr>
          <td style="font-weight: 600;">${row.skill}</td>
          <td><span style="font-size: 0.75rem; color: var(--text-muted);">${categoryLabel}</span></td>
          <td style="font-family: var(--font-mono);">${row.marketPct > 0 ? `${row.marketPct.toFixed(1)}%` : '—'}</td>
          <td><span class="level-badge level-${row.userLevel.toLowerCase()}">${row.userLevel}</span></td>
          <td><span class="gap-badge ${row.severity}">${row.severity}</span></td>
          <td>${this.renderStars(stars)}</td>
          <td style="font-size: 0.8125rem; color: var(--text-secondary);">${row.action}</td>
        </tr>
      `;
    }).join('');
  }

  getLearningPathForRole() {
    return LEARNING_PATH_ITEMS.filter(
      (item) => item.roles.includes(this.currentRole),
    );
  }

  getCompletedItems() {
    try {
      const stored = localStorage.getItem(`${STORAGE_PREFIX}${this.currentRole}`);
      return stored ? JSON.parse(stored) : [];
    } catch {
      return [];
    }
  }

  setCompletedItems(items) {
    localStorage.setItem(`${STORAGE_PREFIX}${this.currentRole}`, JSON.stringify(items));
  }

  renderLearningPath() {
    const panel = document.getElementById('learningPathPanel');
    if (!panel) return;

    const items = this.getLearningPathForRole();
    const completed = this.getCompletedItems();

    if (items.length === 0) {
      panel.innerHTML = '<div class="empty-row" style="padding: 1rem; text-align: center; color: var(--text-muted);">No learning path defined for this role</div>';
      return;
    }

    panel.innerHTML = items.map((item, index) => {
      const isCompleted = completed.includes(index);
      const resourceLink = item.resource
        ? `<a class="lp-resource cursor-pointer" href="${item.resource}" target="_blank" rel="noopener noreferrer">Resource →</a>`
        : '<span class="lp-resource-static">CV section</span>';

      return `
        <div class="learning-path-item${isCompleted ? ' completed' : ''}" data-index="${index}">
          <div class="lp-checkbox cursor-pointer" role="checkbox" aria-checked="${isCompleted}" tabindex="0" aria-label="Mark ${item.title} as complete"></div>
          <div class="lp-content">
            <div class="lp-title">${item.title}</div>
            <div class="lp-meta">
              <span class="lp-category">${item.category}</span>
              <span class="lp-duration">${item.duration}</span>
              ${resourceLink}
            </div>
          </div>
          <div class="lp-gap-indicator ${item.gap}" title="Gap severity: ${item.gap}"></div>
        </div>
      `;
    }).join('');

    panel.querySelectorAll('.lp-checkbox').forEach((checkbox) => {
      const toggle = () => {
        const itemEl = checkbox.closest('.learning-path-item');
        const idx = parseInt(itemEl.dataset.index, 10);
        const current = this.getCompletedItems();
        const pos = current.indexOf(idx);
        if (pos >= 0) current.splice(pos, 1);
        else current.push(idx);
        this.setCompletedItems(current);
        this.renderLearningPath();
      };

      checkbox.addEventListener('click', toggle);
      checkbox.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          toggle();
        }
      });
    });
  }

  buildCvFocusPayload() {
    const roleLabel = this.currentRole.replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());
    const rows = this.getGapTableRows();
    const strengths = rows.filter((r) => r.severity === 'none' || r.userLevel === 'Expert');
    const gaps = rows.filter((r) => r.severity === 'high' || r.severity === 'medium');

    return {
      role: roleLabel,
      strengths: strengths.map((r) => r.skill),
      gaps: gaps.map((r) => ({ skill: r.skill, severity: r.severity, action: r.action })),
      learningPath: this.getLearningPathForRole().map((i) => i.title),
    };
  }

  generateCvFocus() {
    const payload = this.buildCvFocusPayload();
    const lines = [
      `# CV Focus — ${payload.role}`,
      '',
      '## Highlight (strengths)',
      ...payload.strengths.map((s) => `- ${s}`),
      '',
      '## Address (gaps)',
      ...payload.gaps.map((g) => `- [${g.severity.toUpperCase()}] ${g.skill}: ${g.action}`),
      '',
      '## Learning path priorities',
      ...payload.learningPath.map((t) => `- ${t}`),
    ];

    const markdown = lines.join('\n');
    sessionStorage.setItem(FOCUS_STORAGE_KEY, JSON.stringify(payload));

    navigator.clipboard.writeText(markdown).then(() => {
      const btn = document.getElementById('generateCvBtn');
      if (btn) {
        const original = btn.textContent;
        btn.textContent = 'Copied to clipboard';
        const delay = this.prefersReducedMotion ? 1500 : 2000;
        setTimeout(() => { btn.textContent = original; }, delay);
      }
    }).catch((err) => {
      console.error('Failed to copy CV focus:', err);
    });
  }

  copyLearningPathAsMarkdown() {
    const items = this.getLearningPathForRole();
    const completed = this.getCompletedItems();
    const roleLabel = this.currentRole.replace(/-/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase());

    const lines = items.map((item, index) => {
      const check = completed.includes(index) ? 'x' : ' ';
      const resource = item.resource ? `\n  - Resource: ${item.resource}` : '';
      return `- [${check}] **${item.title}** (${item.duration}) — ${item.category}${resource}`;
    });

    const markdown = `## Learning Path — ${roleLabel}\n\n${lines.join('\n')}`;

    navigator.clipboard.writeText(markdown).then(() => {
      const btn = document.getElementById('copyPathBtn');
      if (btn) {
        const original = btn.textContent;
        btn.textContent = 'Copied!';
        const delay = this.prefersReducedMotion ? 1500 : 2000;
        setTimeout(() => { btn.textContent = original; }, delay);
      }
    }).catch((err) => {
      console.error('Failed to copy learning path:', err);
    });
  }

  applyFocusRing(el) {
    el.classList.add('focus-ring-visible');
  }

  setupEventListeners() {
    const { signal } = this.abortController;

    const roleSelect = document.getElementById('roleTarget');
    if (roleSelect) {
      this.applyFocusRing(roleSelect);
      roleSelect.addEventListener('change', (e) => {
        this.currentRole = e.target.value;
        this.renderAll();
      }, { signal });
    }

    const copyBtn = document.getElementById('copyPathBtn');
    if (copyBtn) {
      this.applyFocusRing(copyBtn);
      copyBtn.addEventListener('click', () => this.copyLearningPathAsMarkdown(), { signal });
    }

    const genCvBtn = document.getElementById('generateCvBtn');
    if (genCvBtn) {
      this.applyFocusRing(genCvBtn);
      genCvBtn.addEventListener('click', () => this.generateCvFocus(), { signal });
    }

    if (this.canvas) {
      this.canvas.addEventListener('mousemove', (e) => {
        const index = this.getAxisFromMouse(e);
        if (index !== this.hoveredAxis) {
          this.hoveredAxis = index;
          this.drawRadar();
        }
        if (index >= 0) this.showTooltip(index, e);
        else this.hideTooltip();
      }, { signal });

      this.canvas.addEventListener('mouseleave', () => {
        this.hoveredAxis = -1;
        this.drawRadar();
        this.hideTooltip();
      }, { signal });
    }

    window.addEventListener('resize', () => {
      if (this.canvas && this.ctx) {
        this.resizeCanvas();
        this.drawRadar();
      }
    }, { signal });
  }

  showErrorState() {
    const errorRow = '<tr><td colspan="7" class="empty-row" style="padding: 2rem; text-align: center; color: var(--error);">Failed to load gap data</td></tr>';

    const tbody = document.getElementById('gapTableBody');
    if (tbody) tbody.innerHTML = errorRow;

    const panel = document.getElementById('learningPathPanel');
    if (panel) {
      panel.innerHTML = '<div class="empty-row" style="padding: 1rem; text-align: center; color: var(--error);">Failed to load learning path</div>';
    }

    if (this.canvas && this.ctx) {
      this.resolveColors();
      this.resizeCanvas();
      this.ctx.clearRect(0, 0, this.radarSize, this.radarSize);
      this.ctx.font = '0.875rem var(--font-sans, Inter, system-ui, sans-serif)';
      this.ctx.fillStyle = this.colors.error;
      this.ctx.textAlign = 'center';
      this.ctx.fillText('Failed to load radar data', this.radarCenter, this.radarCenter);
    }
  }
}

export { SkillGapRadar };
