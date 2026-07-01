// Company Deep-Dive Page JavaScript
// Handles data fetching, rendering, and interactions

class CompanyDeepDive {
  constructor(slug) {
    this.slug = slug;
    this.apiBase = '';
    this.data = null;
    this.init();
  }

  async init() {
    try {
      await this.fetchCompanyData();
      this.renderAllComponents();
      this.setupEventListeners();
    } catch (error) {
      console.error('Failed to initialize company deep-dive:', error);
      this.showErrorState();
    }
  }

  async fetchCompanyData() {
    const response = await fetch(`${this.apiBase}/api/market/company/${this.slug}`, {
      cache: 'no-store'
    });

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error(`Company '${this.slug}' not found`);
      }
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    this.data = await response.json();
  }

  renderAllComponents() {
    if (!this.data) return;

    this.renderProfile();
    this.renderRoles();
    this.renderSalaryComparison();
    this.renderCultureFit();
    this.renderApplication();
  }

  renderProfile() {
    const { profile } = this.data;

    // Company name
    const nameEl = document.getElementById('companyName');
    if (nameEl) nameEl.textContent = profile.name;

    // Description
    const descEl = document.getElementById('companyDescription');
    if (descEl) descEl.textContent = profile.culture;

    // Location, size, funding, founded
    const locEl = document.getElementById('companyLocation');
    if (locEl) locEl.textContent = `📍 ${profile.location}`;

    const sizeEl = document.getElementById('companySize');
    if (sizeEl) sizeEl.textContent = `👥 ${profile.size}`;

    const fundingEl = document.getElementById('companyFunding');
    if (fundingEl) fundingEl.textContent = `💰 ${profile.funding}`;

    const foundedEl = document.getElementById('companyFounded');
    if (foundedEl) foundedEl.textContent = `📅 ${profile.founded}`;

    // Tech stack chips
    const techEl = document.getElementById('techStack');
    if (techEl) {
      techEl.innerHTML = profile.techStack.map(tech =>
        `<span class="tech-chip">${tech}</span>`
      ).join('');
    }

    // Culture
    const cultureEl = document.getElementById('companyCulture');
    if (cultureEl) cultureEl.textContent = profile.culture;

    // External links
    const websiteLink = document.getElementById('websiteLink');
    const linkedinLink = document.getElementById('linkedinLink');
    const glassdoorLink = document.getElementById('glassdoorLink');
    const applyLink = document.getElementById('applyDirectBtn');

    if (websiteLink && profile.links?.website) websiteLink.href = profile.links.website;
    if (linkedinLink && profile.links?.linkedin) linkedinLink.href = profile.links.linkedin;
    if (glassdoorLink && profile.links?.glassdoor) glassdoorLink.href = profile.links.glassdoor;
    if (applyLink && profile.links?.careers) applyLink.href = profile.links.careers;

    // Temperature badge
    const tempBadge = document.getElementById('temperatureBadge');
    if (tempBadge) {
      // Temperature is not in deep-dive data, use a default or fetch from overview
      tempBadge.textContent = '🔥 HIRING';
      tempBadge.className = 'tag tag-hot';
    }
  }

  renderRoles() {
    const container = document.getElementById('rolesTableBody');
    if (!container || !this.data) return;

    const { matchedRoles } = this.data;

    container.innerHTML = matchedRoles.map(role => {
      const matchClass = role.matchScore >= 85 ? 'green' : role.matchScore >= 70 ? 'amber' : 'red';
      const workModeLabel = role.workMode === 'hybrid' ? '🏢 Hybrid' : role.workMode === 'remote' ? '🏠 Remote' : '🏢 Onsite';

      return `
        <tr style="cursor: pointer; transition: background-color 150ms ease;" onmouseover="this.style.backgroundColor='var(--bg-tertiary)'" onmouseout="this.style.backgroundColor=''">
          <td>
            <div style="font-weight: 600; color: var(--text-primary);">${role.title}</div>
            <div class="requirements-list">
              ${role.requirements.map(req => `<span class="req-badge">${req}</span>`).join('')}
            </div>
          </td>
          <td>
            <div class="match-score">
              <div class="match-ring ${matchClass}" style="--score: ${role.matchScore / 100};">
                ${role.matchScore}%
              </div>
            </div>
          </td>
          <td>
            <div style="font-family: var(--font-mono); font-size: 0.875rem; font-weight: 600;">
              ${this.formatDKK(role.salary.min)} - ${this.formatDKK(role.salary.max)} / mo
            </div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">Median: ${this.formatDKK(role.salary.median)}</div>
          </td>
          <td>
            <div>${role.location}</div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">${workModeLabel}</div>
          </td>
          <td>
            <div style="font-size: 0.75rem; color: var(--text-secondary);">
              ${role.postedDaysAgo === 1 ? '1 day ago' : `${role.postedDaysAgo} days ago`}
            </div>
          </td>
          <td>
            <button class="toolbar-btn" style="padding: 0.375rem 0.75rem; font-size: 0.75rem;" onclick="alert('Role detail modal - to be implemented')">View Details</button>
          </td>
        </tr>
      `;
    }).join('');

    // Add click handler for role rows
    container.querySelectorAll('tr').forEach((row, index) => {
      row.addEventListener('click', (e) => {
        if (!e.target.closest('button')) {
          const role = matchedRoles[index];
          alert(`Role detail modal for: ${role.title}\nRequirements: ${role.requirements.join(', ')}\nWork mode: ${role.workMode}`);
        }
      });
    });
  }

  renderSalaryComparison() {
    const container = document.getElementById('salaryComparison');
    if (!container || !this.data) return;

    const { salaryComparison } = this.data;
    const delta = salaryComparison.deltaPct;
    const deltaClass = delta > 0 ? 'positive' : delta < 0 ? 'negative' : 'neutral';
    const deltaSign = delta > 0 ? '+' : '';

    // Calculate bar widths (p75 as 100%)
    const maxVal = Math.max(salaryComparison.company.p75, salaryComparison.market.p75);
    const companyP25W = (salaryComparison.company.p25 / maxVal) * 100;
    const companyP50W = (salaryComparison.company.p50 / maxVal) * 100;
    const companyP75W = (salaryComparison.company.p75 / maxVal) * 100;
    const marketP25W = (salaryComparison.market.p25 / maxVal) * 100;
    const marketP50W = (salaryComparison.market.p50 / maxVal) * 100;
    const marketP75W = (salaryComparison.market.p75 / maxVal) * 100;

    container.innerHTML = `
      <div>
        <h4 style="margin: 0 0 1rem; font-size: 0.875rem; font-weight: 600; color: var(--text-primary);">${this.data.profile.name} ${this.data.matchedRoles[0]?.title || 'AI Engineer'}</h4>
        <div class="salary-bar-container">
          <div class="salary-bar-row">
            <span class="salary-bar-label">p25</span>
            <div class="salary-bar-track">
              <div class="salary-bar-fill" style="width: ${companyP25W}%; background: var(--grade-high);"></div>
            </div>
            <span class="salary-bar-value">${this.formatDKK(salaryComparison.company.p25)}/mo</span>
          </div>
          <div class="salary-bar-row">
            <span class="salary-bar-label">p50</span>
            <div class="salary-bar-track">
              <div class="salary-bar-fill" style="width: ${companyP50W}%; background: var(--grade-high);"></div>
            </div>
            <span class="salary-bar-value">${this.formatDKK(salaryComparison.company.p50)}/mo</span>
          </div>
          <div class="salary-bar-row">
            <span class="salary-bar-label">p75</span>
            <div class="salary-bar-track">
              <div class="salary-bar-fill" style="width: ${companyP75W}%; background: var(--grade-high);"></div>
            </div>
            <span class="salary-bar-value">${this.formatDKK(salaryComparison.company.p75)}/mo</span>
          </div>
        </div>
      </div>
      <div>
        <h4 style="margin: 0 0 1rem; font-size: 0.875rem; font-weight: 600; color: var(--text-primary);">Market Median (${this.data.matchedRoles[0]?.title || 'AI Engineer'})</h4>
        <div class="salary-bar-container">
          <div class="salary-bar-row">
            <span class="salary-bar-label">p25</span>
            <div class="salary-bar-track">
              <div class="salary-bar-fill" style="width: ${marketP25W}%; background: var(--text-muted);"></div>
            </div>
            <span class="salary-bar-value">${this.formatDKK(salaryComparison.market.p25)}/mo</span>
          </div>
          <div class="salary-bar-row">
            <span class="salary-bar-label">p50</span>
            <div class="salary-bar-track">
              <div class="salary-bar-fill" style="width: ${marketP50W}%; background: var(--text-muted);"></div>
            </div>
            <span class="salary-bar-value">${this.formatDKK(salaryComparison.market.p50)}/mo</span>
          </div>
          <div class="salary-bar-row">
            <span class="salary-bar-label">p75</span>
            <div class="salary-bar-track">
              <div class="salary-bar-fill" style="width: ${marketP75W}%; background: var(--text-muted);"></div>
            </div>
            <span class="salary-bar-value">${this.formatDKK(salaryComparison.market.p75)}/mo</span>
          </div>
        </div>
        <div style="margin-top: 1rem; text-align: center;">
          <div class="salary-delta ${deltaClass}">
            ${deltaSign}${delta}% ${delta > 0 ? 'above market' : delta < 0 ? 'below market' : 'at market'}
          </div>
        </div>
      </div>
    `;
  }

  renderCultureFit() {
    const container = document.getElementById('cultureFactorsPanel');
    const scoreRing = document.getElementById('cultureFitRing');
    const scoreText = document.getElementById('cultureFitScore');

    if (!container || !this.data) return;

    const { cultureFit } = this.data;

    // Update score ring
    if (scoreRing) {
      scoreRing.style.background = `conic-gradient(var(--grade-high) 0% ${cultureFit.score}%, var(--border-default) ${cultureFit.score}% 100%)`;
    }
    if (scoreText) scoreText.textContent = cultureFit.score;

    // Render factors
    container.innerHTML = cultureFit.factors.map(factor => {
      const icon = factor.status === 'match' ? '✅' : factor.status === 'gap' ? '⚠️' : '➖';
      return `
        <div class="culture-factor">
          <span class="culture-factor-icon">${icon}</span>
          <div class="culture-factor-content">
            <span class="culture-factor-name">${factor.name}</span>
            <span class="culture-factor-weight">Weight: ${Math.round(factor.weight * 100)}%</span>
          </div>
          <span class="culture-factor-status ${factor.status}">${factor.status === 'match' ? '✓' : factor.status === 'gap' ? '✗' : '−'}</span>
        </div>
      `;
    }).join('');
  }

  renderApplication() {
    if (!this.data) return;

    const applyBtn = document.getElementById('applyDirectBtn');
    if (applyBtn && this.data.profile.links?.careers) {
      applyBtn.href = this.data.profile.links.careers;
    }

    // Update prefill note with role
    const prefillNote = document.getElementById('prefillNote');
    const role = this.data.matchedRoles[0]?.title || 'AI Engineer';
    if (prefillNote) {
      prefillNote.textContent = `Pre-filled with: ${role} role, ${this.data.profile.name} keywords, your LLM/RAG experience, Danish location`;
    }
  }

  setupEventListeners() {
    // Back button
    const backBtn = document.getElementById('backBtn');
    if (backBtn) {
      backBtn.addEventListener('click', () => {
        history.back();
      });
    }

    // Priority filter
    const priorityFilter = document.getElementById('priorityFilter');
    if (priorityFilter) {
      priorityFilter.addEventListener('change', async (e) => {
        const priority = parseInt(e.target.value, 10);
        try {
          await fetch(`${this.apiBase}/api/market/company/${this.slug}/priority`, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ priority })
          });
          // Update badge
          const badge = document.getElementById('priorityBadge');
          if (badge) badge.textContent = '★'.repeat(priority) + '☆'.repeat(5 - priority);
        } catch (err) {
          console.error('Failed to update priority:', err);
        }
      });
    }

    // Role filter
    const roleFilter = document.getElementById('roleFilter');
    if (roleFilter) {
      roleFilter.addEventListener('change', (e) => {
        const filter = e.target.value;
        const rows = document.querySelectorAll('#rolesTableBody tr');
        rows.forEach(row => {
          if (filter === 'all') {
            row.style.display = '';
          } else {
            const text = row.textContent.toLowerCase();
            const filterText = filter.toLowerCase();
            row.style.display = text.includes(filterText) ? '' : 'none';
          }
        });
      });
    }

    // Generate CV button
    const genCVBtn = document.getElementById('generateCVBtn');
    if (genCVBtn) {
      genCVBtn.addEventListener('click', () => {
        alert('Generate tailored CV - POST /api/cv/generate with company+role context');
      });
    }

    // Generate Cover Letter button
    const genCoverBtn = document.getElementById('generateCoverBtn');
    if (genCoverBtn) {
      genCoverBtn.addEventListener('click', () => {
        alert('Generate cover letter - POST /api/cv/cover-letter with company+role context');
      });
    }

    // View breakdown button
    const viewBreakdownBtn = document.getElementById('viewBreakdownBtn');
    if (viewBreakdownBtn) {
      viewBreakdownBtn.addEventListener('click', () => {
        alert('View full culture fit breakdown modal - to be implemented');
      });
    }

    // Compare profile button
    const compareProfileBtn = document.getElementById('compareProfileBtn');
    if (compareProfileBtn) {
      compareProfileBtn.addEventListener('click', () => {
        alert('Compare to my profile - navigate to evaluate with company context');
      });
    }
  }

  formatDKK(amount) {
    return new Intl.NumberFormat('da-DK', {
      maximumFractionDigits: 0,
      minimumFractionDigits: 0
    }).format(amount);
  }

  showErrorState() {
    const errorMsg = '<div class="empty-row" style="padding: 2rem; text-align: center; color: var(--error);">Failed to load company data</div>';
    const containers = [
      document.getElementById('rolesTableBody'),
      document.getElementById('salaryComparison'),
      document.getElementById('cultureFactorsPanel')
    ];
    containers.forEach(container => {
      if (container) container.innerHTML = errorMsg;
    });
  }
}

// Export for Astro module import
export { CompanyDeepDive };