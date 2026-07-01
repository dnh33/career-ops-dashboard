// Market Overview Page JavaScript
// Handles data fetching, filtering, and component updates

class MarketOverview {
  constructor() {
    this.apiBase = ''; // Relative to current origin
    this.marketData = null;
    this.currentRoleFilter = 'all';
    this.currentLocationFilter = 'all';
    this.init();
  }

  async init() {
    try {
      await this.fetchMarketData();
      this.renderAllComponents();
      this.setupEventListeners();
    } catch (error) {
      console.error('Failed to initialize market overview:', error);
      this.showErrorState();
    }
  }

  async fetchMarketData() {
    const response = await fetch(`${this.apiBase}/api/market/overview`, {
      cache: 'no-store'
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    this.marketData = await response.json();
  }

  renderAllComponents() {
    if (!this.marketData) return;
    
    this.renderSkillChart();
    this.renderSalaryCards();
    this.renderCompanyHeatmap();
    this.renderGapAlert();
    this.updateHeroSection();
  }

  updateHeroSection() {
    // Update market health score
    const scoreRing = document.querySelector('.score-ring');
    if (scoreRing) {
      const score = this.marketData.marketHealth.score;
      scoreRing.style.background = `conic-gradient(
        var(--grade-high) 0% ${score}%,
        var(--border-default) ${score}% 100%
      )`;
      
      // Add inner circle
      scoreRing.innerHTML = `
        <div style="
          position: absolute;
          width: 80%;
          height: 80%;
          background: var(--bg-secondary);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 1.5rem;
          font-weight: 700;
          color: var(--text-primary);
        ">
          ${score}
        </div>
      `;
    }
    
    // Update trend sparkline
    const trendSparkline = document.getElementById('trendSparkline');
    if (trendSparkline) {
      trendSparkline.innerHTML = '';
      const sparklineData = this.marketData.marketHealth.sparkline;
      const maxValue = Math.max(...sparklineData);
      
      sparklineData.forEach(value => {
        const bar = document.createElement('div');
        const height = (value / maxValue) * 100;
        bar.style.height = `${height}%`;
        bar.style.background = 'var(--grade-high)';
        trendSparkline.appendChild(bar);
      });
    }
  }

  renderSkillChart() {
    const container = document.getElementById('skillChartContainer');
    if (!container) return;
    
    container.innerHTML = `
      <div class="skill-bars" style="display: flex; flex-direction: column; gap: 0.75rem;">
        ${this.marketData.skillDemand.map(skill => {
          const categoryColors = {
            frontend: 'var(--accent-primary)',
            backend: 'var(--info)',
            devops: 'var(--success)',
            cloud: 'var(--warning)',
            data: 'var(--info)'
          };
          
          const gapClasses = {
            none: 'tag-gray',
            low: 'tag-green',
            medium: 'tag-amber',
            high: 'tag-red'
          };
          
          return `
            <div class="skill-bar">
              <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                <span>${skill.skill}</span>
                <span class="skill-category">[${skill.category}]</span>
              </div>
              <div class="bar-container">
                <div class="bar-fill" style="
                  width: ${skill.pct}%; 
                  background: ${categoryColors[skill.category] || 'var(--text-muted)'}; 
                  height: 28px; 
                  border-radius: 4px;
                "></div>
              </div>
              <div style="display: flex; justify-content: space-between; font-size: 0.875rem; color: var(--text-muted);">
                <span>${skill.pct}%</span>
                <span class="tag ${gapClasses[skill.gap] || 'tag-gray'}">${skill.gap}</span>
              </div>
            </div>
          `;
        }).join('')}
      </div>
    `;
  }

  renderSalaryCards() {
      const container = document.getElementById('salaryCardsContainer');
      if (!container || !this.marketData) return;

      // Filter data based on current selections
      const filteredData = this.filterSalaryData();

      container.innerHTML = `
        <div class="salary-cards-grid">
          ${filteredData.map(role => {
            const locations = Object.keys(role.value);

            return locations.map(location => {
              const range = role.value[location];
              return `
                <div class="salary-card">
                  <div class="salary-card-header">
                    <span class="salary-card-title">${role.key}</span>
                    <span class="salary-card-location">${location}</span>
                  </div>
                  <div class="salary-card-ranges">
                    <div class="salary-range">
                      <div class="salary-range-label">p25</div>
                      <div class="salary-range-value">${this.formatDKK(range.p25)}/mo</div>
                    </div>
                    <div class="salary-range">
                      <div class="salary-range-label">p50</div>
                      <div class="salary-range-value">${this.formatDKK(range.p50)}/mo</div>
                    </div>
                    <div class="salary-range">
                      <div class="salary-range-label">p75</div>
                      <div class="salary-range-value">${this.formatDKK(range.p75)}/mo</div>
                    </div>
                  </div>
                  <div class="salary-card-footer">
                    DKK ${this.formatDKK(range.p25)} - ${this.formatDKK(range.p75)} / mo
                  </div>
                </div>
              `;
            }).join('');
          }).join('')}
        </div>
      `;
    }

  filterSalaryData() {
    if (!this.marketData) return [];
    
    const roleFilter = this.currentRoleFilter;
    const locationFilter = this.currentLocationFilter;
    
    return Object.entries(this.marketData.salaryRanges).filter(([role]) => {
      if (roleFilter === 'all') return true;
      
      const roleMap = {
        'frontend': 'Frontend Engineer',
        'backend': 'AI Engineer', // Simplified mapping
        'ai': 'AI Engineer',
        'fullstack': 'Full-Stack Engineer'
      };
      
      return role === roleMap[roleFilter];
    }).map(([roleKey, roleData]) => {
      if (locationFilter === 'all') {
        return { key: roleKey, value: roleData };
      }
      
      const filteredLocations = {};
      if (roleData[locationFilter]) {
        filteredLocations[locationFilter] = roleData[locationFilter];
      }
      return { key: roleKey, value: filteredLocations };
    });
  }

  renderCompanyHeatmap() {
    const container = document.getElementById('companyGridContainer');
    if (!container || !this.marketData) return;
    
    container.innerHTML = this.marketData.companies.map(company => {
      const temperatureClasses = {
        hot: 'hot',
        warm: 'warm',
        cool: 'cool'
      };
      
      return `
        <div class="company-card" data-slug="${company.slug}" onclick="window.location.href='/market/company/${company.slug}'">
          <div class="company-card-header">
            <span class="company-card-title">${company.name}</span>
            <span class="company-card-temperature ${temperatureClasses[company.temperature]}">
              ${company.temperature === 'hot' ? '🔥 HOT' : company.temperature === 'warm' ? '🟡 WARM' : '❄️ COOL'}
            </span>
          </div>
          <div class="company-card-roles">
            ${company.topRoles.map(role => `<span>${role}</span>`).join('')}
          </div>
          <div class="company-card-salary">${this.formatDKK(company.medianSalary)}/mo</div>
          <div class="company-card-footer">
            <span>${company.location}</span>
            <span class="company-card-view">[View]</span>
          </div>
        </div>
      `;
    }).join('');
    
    // Update company count
    const companyCount = document.getElementById('company-count');
    if (companyCount) {
      companyCount.textContent = `${this.marketData.companies.length} companies`;
    }
  }

  renderGapAlert() {
    const container = document.getElementById('gapListContainer');
    if (!container || !this.marketData) return;
    
    container.innerHTML = this.marketData.skillGaps.map(gap => {
      const severityClasses = {
        high: 'high',
        medium: 'medium',
        low: 'low'
      };
      
      return `
        <div class="gap-item">
          <div class="gap-item-severity ${severityClasses[gap.severity]}">
            ${gap.severity.toUpperCase()}
          </div>
          <div class="gap-item-content">
            <div class="gap-item-skill">${gap.skill}</div>
            <div class="gap-item-market">${gap.marketPct}% demand</div>
            <div class="gap-item-action">${gap.action}</div>
          </div>
        </div>
      `;
    }).join('');
    
    // Update gap count
    const gapCount = document.getElementById('gap-count');
    if (gapCount) {
      gapCount.textContent = `${this.marketData.skillGaps.length} gaps`;
    }
  }

  setupEventListeners() {
    // Role filter
    const roleFilter = document.getElementById('roleFilter');
    if (roleFilter) {
      roleFilter.addEventListener('change', (e) => {
        this.currentRoleFilter = e.target.value;
        this.renderSalaryCards();
      });
    }
    
    // Location filter
    const locationFilter = document.getElementById('locationFilter');
    if (locationFilter) {
      locationFilter.addEventListener('change', (e) => {
        this.currentLocationFilter = e.target.value;
        this.renderSalaryCards();
        this.renderCompanyHeatmap(); // Also filter companies by location
      });
    }
    
    // Salary filters (if they exist)
    const salaryRoleFilter = document.getElementById('salaryRoleFilter');
    if (salaryRoleFilter) {
      salaryRoleFilter.addEventListener('change', (e) => {
        // Could implement separate salary filtering if needed
      });
    }
    
    const salaryLocationFilter = document.getElementById('salaryLocationFilter');
    if (salaryLocationFilter) {
      salaryLocationFilter.addEventListener('change', (e) => {
        // Could implement separate salary filtering if needed
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
    // Show error message in each component
    const errorMsg = '<div class="empty-row">Failed to load market data</div>';
    
    const containers = [
      document.getElementById('salaryCardsContainer'),
      document.getElementById('companyGridContainer'),
      document.getElementById('gapListContainer')
    ];
    
    containers.forEach(container => {
      if (container) {
        container.innerHTML = errorMsg;
      }
    });
  }
}

// Initialize when page loads
document.addEventListener('astro:page-load', () => {
  new MarketOverview();
});

// Export for Astro module import
export { MarketOverview };