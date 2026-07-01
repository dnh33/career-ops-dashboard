// OptimizationPanel client-side logic
// Handles rule rendering, diff modal, apply/reject, real-time scoring

import { computeOptimizePayload, computeCvSummary } from '../lib/cv-optimize.ts';

/** @typedef {{ id: string; rule: string; category: string; currentCv: string; target: string; gap: number; gapLabel: string; priority: string; priorityVariant: string; role: string; before: string; after: string; applied?: boolean }} RuleWithApplied */

/** @typedef {{ profile: any; experience: any[]; skills: any[]; education: any[]; appliedRuleIds?: string[] }} CvState */

let currentRules = /** @type {RuleWithApplied[]} */ ([]);
let currentRole = 'ai-engineer';
let currentCategory = 'all';
let diffRule = null;
let cvState = /** @type {CvState} */ ({
  profile: {},
  experience: [],
  skills: [],
  education: [],
  appliedRuleIds: [],
});

const STORAGE_KEY = 'hermes-cv-builder';

function loadCvState() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      const state = JSON.parse(stored);
      return {
        profile: state.profile || {},
        experience: state.experience || [],
        skills: state.skills || [],
        education: state.education || [],
        appliedRuleIds: state.appliedRuleIds || [],
      };
    }
  } catch { }
  return { profile: {}, experience: [], skills: [], education: [], appliedRuleIds: [] };
}

function saveCvState(state) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function escapeHtml(text) {
  if (!text) return '';
  return text
    .replace(/&/g, '&')
    .replace(/</g, '<')
    .replace(/>/g, '>')
    .replace(/"/g, '"')
    .replace(/'/g, ''');
}

function getGapClass(gap) {
  if (gap >= 30) return 'critical';
  if (gap >= 20) return 'high';
  if (gap >= 10) return 'medium';
  return 'low';
}

function getRuleElement(rule) {
  const li = document.createElement('li');
  li.className = 'cv-rule-item' + (rule.applied ? ' applied' : '');
  li.dataset.ruleId = rule.id;
  li.innerHTML = `
    <div class="cv-rule-header">
      <div class="cv-rule-main">
        <div class="cv-rule-title">${escapeHtml(rule.rule)}</div>
        <div class="cv-rule-meta">
          <span class="cv-rule-category">${escapeHtml(rule.category)}</span>
          <span class="cv-rule-gap ${getGapClass(rule.gap)}">${escapeHtml(rule.gapLabel)} gap</span>
          <span class="cv-rule-role">${escapeHtml(rule.role === 'all' ? 'All roles' : rule.role)}</span>
        </div>
      </div>
      <div class="cv-rule-actions">
        ${rule.applied
          ? '<span class="cv-rule-applied-badge">✓ Applied</span>'
          : `<button type="button" class="cv-rule-action cv-rule-action--primary" data-action="apply" data-rule-id="${rule.id}">Apply</button>`
        }
        <button type="button" class="cv-rule-action" data-action="preview" data-rule-id="${rule.id}">Preview</button>
      </div>
    </div>
    <p class="cv-rule-description">${escapeHtml(rule.currentCv)} → ${escapeHtml(rule.target)}</p>
  `;
  return li;
}

function renderRules(rules) {
  const list = document.getElementById('cv-rules-list');
  const empty = document.getElementById('cv-optimization-empty');
  const loading = document.getElementById('cv-optimization-loading');

  if (loading) loading.hidden = true;
  list.hidden = false;

  if (!rules.length) {
    const emptyEl = document.getElementById('cv-optimization-empty');
    if (emptyEl) emptyEl.hidden = false;
    list.innerHTML = '';
    return;
  }

  if (empty) empty.hidden = true;

  list.innerHTML = '';
  rules.forEach(rule => {
    list.appendChild(getRuleElement(rule));
  });

  // Bind events
  list.querySelectorAll('[data-action="apply"]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const ruleId = e.currentTarget.dataset.ruleId;
      const rule = currentRules.find(r => r.id === ruleId);
      if (rule) openDiffModal(rule);
    });
  });

  list.querySelectorAll('[data-action="preview"]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const ruleId = e.currentTarget.dataset.ruleId;
      const rule = currentRules.find(r => r.id === ruleId);
      if (rule) openDiffModal(rule);
    });
  });
}

function filterRules() {
  return currentRules.filter(rule => {
    if (currentCategory !== 'all' && rule.category !== currentCategory) return false;
    return true;
  });
}

function refreshOptimization() {
  const payload = computeOptimizePayload(currentRole, cvState.appliedRuleIds || []);
  currentRules = payload.rules;
  updateMetrics(payload);
  renderRules(filterRules());
}

function updateMetrics(payload) {
  const scoreEl = document.getElementById('cv-score-value');
  const coverageEl = document.getElementById('cv-keyword-coverage');
  const gapsEl = document.getElementById('cv-critical-gaps');
  const matchesEl = document.getElementById('cv-role-matches');

  if (scoreEl) scoreEl.textContent = String(payload.overallScore);
  if (coverageEl) coverageEl.textContent = payload.keywordCoverage + '%';
  if (gapsEl) gapsEl.textContent = String(payload.criticalGaps);
  if (matchesEl) matchesEl.textContent = String(payload.roleMatches);

  // Color the score based on value
  const scoreEl_ = document.getElementById('cv-score-value');
  if (scoreEl_) {
    scoreEl_.classList.remove('score-low', 'score-medium', 'score-high');
    if (payload.overallScore >= 80) scoreEl_.classList.add('score-high');
    else if (payload.overallScore >= 60) scoreEl_.classList.add('score-medium');
    else scoreEl_.classList.add('score-low');
  }
}

function openDiffModal(rule) {
  diffRule = rule;
  const overlay = document.getElementById('cv-rule-diff-overlay');
  const titleEl = document.getElementById('cv-rule-diff-title');
  const priorityEl = document.getElementById('cv-rule-diff-priority');
  const categoryEl = document.getElementById('cv-rule-diff-category');
  const ruleEl = document.getElementById('cv-rule-diff-rule');
  const beforeEl = document.getElementById('cv-rule-diff-before');
  const afterEl = document.getElementById('cv-rule-diff-after');
  const noteEl = document.getElementById('cv-rule-diff-note');

  if (titleEl) titleEl.textContent = rule.rule;
  if (priorityEl) {
    priorityEl.textContent = rule.priority;
    priorityEl.className = 'status-pill status-pill--' + (rule.priorityVariant || 'default') + ' status-pill--sm';
  }
  if (categoryEl) categoryEl.textContent = rule.category;
  if (ruleEl) ruleEl.textContent = `Current: ${rule.currentCv}\nTarget: ${rule.target}`;
  if (beforeEl) beforeEl.textContent = rule.before;
  if (afterEl) afterEl.textContent = rule.after;
  if (noteEl) {
    if (rule.applied) {
      noteEl.textContent = 'This rule has already been applied. You can review the changes or re-apply if needed.';
    } else {
      noteEl.textContent = 'Click "Accept & Apply" to apply this optimization to your CV. This will update the relevant section and recalculate your score.';
    }
  }

  if (overlay) overlay.hidden = false;
}

function closeDiffModal() {
  const overlay = document.getElementById('cv-rule-diff-overlay');
  if (overlay) overlay.hidden = true;
  diffRule = null;
}

async function applyRule(rule) {
  // Apply the rule to the CV state
  rule.applied = true;
  cvState.appliedRuleIds = cvState.appliedRuleIds || [];
  if (!cvState.appliedRuleIds.includes(rule.id)) {
    cvState.appliedRuleIds.push(rule.id);
  }
  saveCvState(cvState);
  
  // Re-run optimization
  refreshOptimization();
  closeDiffModal();
  
  // Dispatch event for live preview update
  window.dispatchEvent(new CustomEvent('cv-state-changed', { detail: cvState }));
}

function rejectRule() {
  closeDiffModal();
}

function initOptimizationPanel() {
  cvState = loadCvState();
  
  // Get role from profile or default
  const profileRole = cvState.profile?.roleTarget || 'ai-engineer';
  currentRole = profileRole;
  
  // Initial load
  refreshOptimization();
  
  // Bind tab events
  document.querySelectorAll('.cv-optimization-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.cv-optimization-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      currentCategory = tab.dataset.category || 'all';
      renderRules(filterRules());
    });
  });
  
  // Bind role filter (SegmentedControl emits change event)
  const roleFilter = document.getElementById('cv-role-filter');
  if (roleFilter) {
    roleFilter.addEventListener('change', (e) => {
      const value = e.detail?.value || 'ai-engineer';
      currentRole = value;
      refreshOptimization();
    });
  }
  
  // Bind refresh button
  const refreshBtn = document.getElementById('cv-refresh-optimization');
  if (refreshBtn) {
    refreshBtn.addEventListener('click', () => {
      refreshBtn.disabled = true;
      refreshBtn.innerHTML = '<i class="codicon codicon-loading codicon-modifier-spin" aria-hidden="true"></i> Refreshing...';
      
      // Fetch from server
      fetch('/api/cv/optimize?role=' + currentRole, {
        headers: { 'X-API-Key': 'Ojy29OB8AJwvBAXZuF-244Su_L9RswRzpKSM5u8I2xE' }
      })
        .then(res => res.json())
        .then(data => {
          // Merge server rules with local applied state
          const serverRules = data.rules || [];
          currentRules = serverRules.map(r => ({
            ...r,
            applied: cvState.appliedRuleIds?.includes(r.id) || false,
          }));
          updateMetrics({
            overallScore: data.overallScore,
            keywordCoverage: data.keywordCoverage,
            criticalGaps: data.criticalGaps,
            roleMatches: data.roleMatches,
          });
          renderRules(filterRules());
        })
        .catch(err => {
          console.error('Failed to refresh optimization:', err);
        })
        .finally(() => {
          refreshBtn.disabled = false;
          refreshBtn.innerHTML = '<i class="codicon codicon-refresh" aria-hidden="true"></i> Refresh from Server';
        });
    });
  }
  
  // Diff modal events
  const closeBtn = document.getElementById('cv-rule-diff-close');
  const rejectBtn = document.getElementById('cv-rule-diff-reject');
  const acceptBtn = document.getElementById('cv-rule-diff-accept');
  const overlay = document.getElementById('cv-rule-diff-overlay');
  
  if (closeBtn) closeBtn.addEventListener('click', closeDiffModal);
  if (rejectBtn) rejectBtn.addEventListener('click', () => { closeDiffModal(); });
  if (acceptBtn) acceptBtn.addEventListener('click', () => { if (diffRule) applyRule(diffRule); });
  if (overlay) {
    overlay.addEventListener('click', (e) => { if (e.target === overlay) closeDiffModal(); });
  }
  
  // Keyboard: Escape closes modal
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeDiffModal(); });
  
  // Listen for CV state changes from builder
  window.addEventListener('cv-state-changed', (e) => {
    cvState = e.detail;
    refreshOptimization();
  });
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initOptimizationPanel);
} else {
  initOptimizationPanel();
}

export { initOptimizationPanel, refreshOptimization, loadCvState };