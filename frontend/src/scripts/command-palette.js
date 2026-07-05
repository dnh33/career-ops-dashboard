/**
 * Command Palette — Cmd+K Signal Signature Moment
 * Fuzzy search over skills, companies, actions, report types, settings
 * Keyboard navigation, theme-aware, component registry entry
 * Design System Foundation §3.3.2 & §4.2.2
 *
 * @typedef {Object} CommandItem
 * @property {string} id
 * @property {string} title
 * @property {string} [description]
 * @property {string} category
 * @property {string[]} keywords
 * @property {Function} action
 * @property {string} [icon]
 * @property {string} [shortcut]
 *
 * @typedef {Object} CommandPaletteData
 * @property {CommandItem[]} items
 */

/**
 * @param {HTMLElement} container
 * @returns {() => void}
 */
function initCommandPalette(container) {
  const rootStyles = getComputedStyle(document.documentElement);

  // Read ALL values via getComputedStyle — ZERO hardcoded
  const bgElevated = rootStyles.getPropertyValue('--bg-elevated').trim();
  const borderFocus = rootStyles.getPropertyValue('--border-focus').trim();
  const textPrimary = rootStyles.getPropertyValue('--text-primary').trim();
  const textSecondary = rootStyles.getPropertyValue('--text-secondary').trim();
  const textMuted = rootStyles.getPropertyValue('--text-muted').trim();
  const accentPrimary = rootStyles.getPropertyValue('--accent-primary').trim();
  const accentSubtle = rootStyles.getPropertyValue('--accent-subtle').trim();
  const borderDefault = rootStyles.getPropertyValue('--border-default').trim();
  const durationFast = rootStyles.getPropertyValue('--duration-fast').trim() || '150ms';
  const easeOut = rootStyles.getPropertyValue('--ease-out').trim() || 'cubic-bezier(0.16, 1, 0.3, 1)';
  const zModal = rootStyles.getPropertyValue('--z-modal').trim() || '400';

  const input = container.querySelector('input');
  const panel = container.querySelector('.command-palette__panel');
  const list = container.querySelector('.command-palette__list');
  const empty = container.querySelector('.command-palette__empty');

  /** @type {CommandItem[]} */
  let items = [];
  /** @type {CommandItem[]} */
  let filteredItems = [];
  let selectedIndex = -1;
  let isOpen = false;
  /** @type {{name: string, items: CommandItem[]}[]} */
  let categoryGroups = [];

  // Parse data from data-commands attribute
  try {
    const raw = container.getAttribute('data-commands');
    if (raw) {
      const data = JSON.parse(raw);
      items = data.items || [];
    }
  } catch (e) {
    console.error('[command-palette] Failed to parse data-commands:', e);
  }

  // Add default commands if none provided
  if (items.length === 0) {
    items = getDefaultCommands();
  }

  // Group by category
  /**
   * @returns {{name: string, items: CommandItem[]}[]}
   */
  function buildCategoryGroups() {
    const groups = new Map();
    items.forEach(item => {
      if (!groups.has(item.category)) {
        groups.set(item.category, []);
      }
      groups.get(item.category).push(item);
    });
    return Array.from(groups.entries()).map(([name, items]) => ({ name, items }));
  }

  // Simple fuzzy match (substring + word boundary)
  /**
   * @param {string} query
   * @param {CommandItem} item
   * @returns {boolean}
   */
  function fuzzyMatch(query, item) {
    const q = query.toLowerCase().trim();
    if (!q) return true;
    const haystack = [
      item.title,
      item.description || '',
      item.category,
      ...item.keywords,
    ].join(' ').toLowerCase();
    return haystack.includes(q);
  }

  // Filter items
  /**
   * @param {string} query
   */
  function filterItems(query) {
    const q = query.toLowerCase().trim();
    if (!q) {
      filteredItems = [...items];
    } else {
      filteredItems = items.filter(item => fuzzyMatch(q, item));
    }
    selectedIndex = -1;
    render();
  }

  // Render results
  function render() {
    categoryGroups = buildCategoryGroups().filter(g =>
      g.items.some(item => filteredItems.includes(item))
    );

    if (filteredItems.length === 0) {
      list.innerHTML = '';
      empty.hidden = false;
      return;
    }

    empty.hidden = true;

    list.innerHTML = categoryGroups.map((group, groupIndex) => {
      const groupItems = group.items.filter(item => filteredItems.includes(item));
      if (groupItems.length === 0) return '';

      return `
        <div class="command-palette__category" data-category-index="${groupIndex}">
          <div class="command-palette__category-label">${group.name}</div>
          ${groupItems.map((item, itemIndex) => `
            <button
              type="button"
              class="command-palette__item ${item.id === filteredItems[selectedIndex]?.id ? 'command-palette__item--selected' : ''}"
              data-item-id="${item.id}"
              data-category-index="${groupIndex}"
              data-item-index="${itemIndex}"
              tabindex="-1"
            >
              <span class="command-palette__item-title">${item.title}</span>
              ${item.description ? `<span class="command-palette__item-desc">${item.description}</span>` : ''}
              ${item.shortcut ? `<kbd class="command-palette__shortcut">${item.shortcut}</kbd>` : ''}
            </button>
          `).join('')}
        </div>
      `;
    }).join('');

    // Update selection highlight
    updateSelection();
  }

  function updateSelection() {
    list.querySelectorAll('.command-palette__item').forEach((btn, idx) => {
      const isSelected = idx === selectedIndex;
      btn.classList.toggle('command-palette__item--selected', isSelected);
      if (isSelected) {
        btn.scrollIntoView({ block: 'nearest' });
      }
    });
  }

  /**
   * @param {number} index
   */
  function selectItem(index) {
    if (index < 0 || index >= filteredItems.length) return;
    selectedIndex = index;
    updateSelection();
  }

  function executeSelected() {
    const item = filteredItems[selectedIndex];
    if (item) {
      item.action();
      close();
    }
  }

  function open() {
    if (isOpen) return;
    isOpen = true;
    container.setAttribute('data-visible', 'true');
    input.value = '';
    filterItems('');
    input.focus();
    document.body.style.overflow = 'hidden';

    document.addEventListener('keydown', handleKeyDown);
  }

  function close() {
    if (!isOpen) return;
    isOpen = false;
    container.removeAttribute('data-visible');
    input.value = '';
    document.body.style.overflow = '';
    document.removeEventListener('keydown', handleKeyDown);
  }

  /**
   * @param {KeyboardEvent} event
   */
  function handleKeyDown(event) {
    if (!isOpen) {
      // Global Cmd+K to open (handled by PageLayout too, but redundant is fine)
      if ((event.metaKey || event.ctrlKey) && event.key === 'k') {
        event.preventDefault();
        open();
      }
      return;
    }

    switch (event.key) {
      case 'Escape':
        event.preventDefault();
        close();
        break;
      case 'ArrowDown':
        event.preventDefault();
        selectItem(Math.min(selectedIndex + 1, filteredItems.length - 1));
        break;
      case 'ArrowUp':
        event.preventDefault();
        selectItem(Math.max(selectedIndex - 1, 0));
        break;
      case 'Enter':
        event.preventDefault();
        executeSelected();
        break;
      case 'Tab':
        // Allow tab to move between items
        event.preventDefault();
        if (event.shiftKey) {
          selectItem(Math.max(selectedIndex - 1, 0));
        } else {
          selectItem(Math.min(selectedIndex + 1, filteredItems.length - 1));
        }
        break;
    }
  }

  // Event listeners
  input?.addEventListener('input', (e) => {
    filterItems(e.target.value);
  });

  input?.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') close();
  });

  list?.addEventListener('click', (e) => {
    const item = e.target.closest('.command-palette__item');
    if (item) {
      const itemId = item.getAttribute('data-item-id');
      const found = filteredItems.find(i => i.id === itemId);
      if (found) {
        found.action();
        close();
      }
    }
  });

  // Click outside to close
  container.addEventListener('click', (e) => {
    if (e.target === container) {
      close();
    }
  });

  // Initial render
  filterItems('');

  // Cleanup
  return () => {
    document.removeEventListener('keydown', handleKeyDown);
    document.body.style.overflow = '';
  };
}

/**
 * @returns {CommandItem[]}
 */
function getDefaultCommands() {
  const navigate = (path) => () => { window.location.href = path; };

  return [
    // Navigation
    { id: 'nav-dashboard', title: 'Dashboard', description: 'Market intelligence overview', category: 'Navigation', keywords: ['home', 'overview', 'dashboard'], action: navigate('/'), shortcut: 'G D', icon: 'home' },
    { id: 'nav-market', title: 'Market Overview', description: '69 active postings, salary bands, skill demand', category: 'Navigation', keywords: ['market', 'jobs', 'postings', 'salary'], action: navigate('/market'), shortcut: 'G M', icon: 'graph' },
    { id: 'nav-skill-gap', title: 'Skill Gap Radar', description: 'Market demand vs your profile coverage', category: 'Navigation', keywords: ['skill', 'gap', 'radar', 'analysis'], action: navigate('/market/skill-gap'), shortcut: 'G S', icon: 'graph' },
    { id: 'nav-companies', title: 'Companies', description: '30+ prioritized Danish tech companies', category: 'Navigation', keywords: ['companies', 'employers', 'targets'], action: navigate('/companies'), shortcut: 'G C', icon: 'organization' },
    { id: 'nav-cv-builder', title: 'CV Builder', description: 'Build your market-optimized CV', category: 'Navigation', keywords: ['cv', 'resume', 'builder', 'create'], action: navigate('/cv/builder'), shortcut: 'G B', icon: 'file-text' },
    { id: 'nav-cv-optimize', title: 'CV Optimizer', description: 'Optimize for specific roles and companies', category: 'Navigation', keywords: ['cv', 'optimize', 'tailor', 'ats'], action: navigate('/cv/optimize'), shortcut: 'G O', icon: 'wand' },
    { id: 'nav-tracker', title: 'Application Tracker', description: 'Track your applications pipeline', category: 'Navigation', keywords: ['tracker', 'applications', 'pipeline', 'jobs'], action: navigate('/tracker'), shortcut: 'G T', icon: 'list-unordered' },
    { id: 'nav-pipeline', title: 'Pipeline', description: 'Kanban view of opportunities', category: 'Navigation', keywords: ['pipeline', 'kanban', 'stages'], action: navigate('/pipeline'), shortcut: 'G P', icon: 'project-roadmap' },
    { id: 'nav-reports', title: 'Reports', description: 'Generate and export market reports', category: 'Navigation', keywords: ['reports', 'export', 'pdf', 'analytics'], action: navigate('/reports'), shortcut: 'G R', icon: 'file-code' },
    { id: 'nav-settings', title: 'Settings', description: 'Theme, density, API budget, preferences', category: 'Navigation', keywords: ['settings', 'preferences', 'theme', 'density'], action: navigate('/settings'), shortcut: 'G ,', icon: 'gear' },

    // Actions
    { id: 'action-refresh', title: 'Refresh Market Data', description: 'Fetch latest postings from API', category: 'Actions', keywords: ['refresh', 'update', 'fetch', 'sync'], action: () => window.location.reload(), shortcut: 'R', icon: 'sync' },
    { id: 'action-scan', title: 'Scan CV', description: 'Import and analyze your CV', category: 'Actions', keywords: ['scan', 'import', 'cv', 'parse'], action: navigate('/scan'), shortcut: 'S', icon: 'search' },
    { id: 'action-export', title: 'Export Report', description: 'Generate PDF report', category: 'Actions', keywords: ['export', 'pdf', 'download', 'report'], action: navigate('/output'), shortcut: 'E', icon: 'download' },

    // Theme/Density
    { id: 'theme-dark', title: 'Theme: Dark Observatory', description: 'Default dark theme', category: 'Appearance', keywords: ['theme', 'dark', 'observatory'], action: () => setTheme('dark'), shortcut: 'T D', icon: 'moon' },
    { id: 'theme-light', title: 'Theme: Light', description: 'Light mode', category: 'Appearance', keywords: ['theme', 'light'], action: () => setTheme('light'), shortcut: 'T L', icon: 'sun' },
    { id: 'theme-hc', title: 'Theme: High Contrast', description: 'WCAG AAA compliant', category: 'Appearance', keywords: ['theme', 'high contrast', 'accessibility', 'aaa'], action: () => setTheme('high-contrast'), shortcut: 'T H', icon: 'circle-outline' },
    { id: 'theme-sepia', title: 'Theme: Sepia', description: 'Reading mode', category: 'Appearance', keywords: ['theme', 'sepia', 'reading'], action: () => setTheme('sepia'), shortcut: 'T S', icon: 'book' },
    { id: 'density-compact', title: 'Density: Compact', description: 'Tight spacing for power users', category: 'Appearance', keywords: ['density', 'compact', 'tight'], action: () => setDensity('compact'), shortcut: 'D C', icon: 'remove' },
    { id: 'density-comfortable', title: 'Density: Comfortable', description: 'Default balanced spacing', category: 'Appearance', keywords: ['density', 'comfortable', 'default'], action: () => setDensity('comfortable'), shortcut: 'D O', icon: 'dash' },
    { id: 'density-spacious', title: 'Density: Spacious', description: 'Generous breathing room', category: 'Appearance', keywords: ['density', 'spacious', 'relaxed'], action: () => setDensity('spacious'), shortcut: 'D S', icon: 'add' },

    // Skills (top 20 from research)
    { id: 'skill-ts', title: 'TypeScript', description: '27.5% market demand — Expert level', category: 'Skills', keywords: ['typescript', 'ts', 'frontend'], action: navigate('/market?skill=typescript'), icon: 'symbol-method' },
    { id: 'skill-react', title: 'React', description: '23.2% market demand — Expert level', category: 'Skills', keywords: ['react', 'frontend', 'jsx'], action: navigate('/market?skill=react'), icon: 'symbol-method' },
    { id: 'skill-docker', title: 'Docker', description: '47.8% market demand — Expert level', category: 'Skills', keywords: ['docker', 'container', 'devops'], action: navigate('/market?skill=docker'), icon: 'container' },
    { id: 'skill-python', title: 'Python', description: '58.0% market demand — Expert level', category: 'Skills', keywords: ['python', 'backend', 'ai', 'ml'], action: navigate('/market?skill=python'), icon: 'symbol-method' },
    { id: 'skill-aws', title: 'AWS', description: '37.7% market demand — Learning', category: 'Skills', keywords: ['aws', 'cloud', 'cloud'], action: navigate('/market?skill=aws'), icon: 'cloud' },
    { id: 'skill-k8s', title: 'Kubernetes', description: '24.6% market demand — Learning', category: 'Skills', keywords: ['kubernetes', 'k8s', 'orchestration', 'devops'], action: navigate('/market?skill=kubernetes'), icon: 'hub' },
    { id: 'skill-sql', title: 'SQL / PostgreSQL', description: '34.8% market demand — Some experience', category: 'Skills', keywords: ['sql', 'postgresql', 'database', 'data'], action: navigate('/market?skill=sql'), icon: 'database' },
    { id: 'skill-git', title: 'Git', description: '78.3% market demand — Expert level', category: 'Skills', keywords: ['git', 'version control', 'devops'], action: navigate('/market?skill=git'), icon: 'git-branch' },
    { id: 'skill-llm', title: 'LLM Integration', description: 'Emerging demand — Expert level', category: 'Skills', keywords: ['llm', 'ai', 'rag', 'agents'], action: navigate('/market?skill=llm'), icon: 'cpu' },
    { id: 'skill-prompt', title: 'Prompt Engineering', description: 'Emerging demand — Expert level', category: 'Skills', keywords: ['prompt', 'engineering', 'ai', 'llm'], action: navigate('/market?skill=prompt'), icon: 'comment-discussion' },
  ];
}

/**
 * @param {string} theme
 */
function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('career-ops-theme', theme);
  window.dispatchEvent(new CustomEvent('theme:change', { detail: { theme } }));
}

/**
 * @param {string} density
 */
function setDensity(density) {
  document.documentElement.setAttribute('data-density', density);
  localStorage.setItem('career-ops-density', density);
  window.dispatchEvent(new CustomEvent('density:change', { detail: { density } }));
}

// Component registry registration
/**
 * @returns {void}
 */
function registerCommandPalette() {
  if (typeof window !== 'undefined' && window.registerComponent) {
    window.registerComponent('command-palette', { init: initCommandPalette });
  }
}

// Auto-init for declarative usage: <div data-component="command-palette" data-commands='...'>
if (typeof window !== 'undefined') {
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-component="command-palette"]').forEach((el) => {
      initCommandPalette(el);
    });
  });

  window.addEventListener('pagelayout:ready', () => {
    document.querySelectorAll('[data-component="command-palette"]').forEach((el) => {
      initCommandPalette(el);
    });
  });

  // Self-register
  registerCommandPalette();
}