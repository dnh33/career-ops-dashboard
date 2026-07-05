/**
 * Skill Gap Radar — Radar Sweep Signature Moment
 * SVG <circle> rings with animated stroke-dashoffset sweep
 * Grade-colored rings: --grade-high (emerald), --grade-mid (amber), --grade-low (crimson)
 * Respects prefers-reduced-motion (instant fill)
 * Data passed via data-gaps JSON attribute on container
 * Design System Foundation §3.3.1 & §4.2.1
 */

/**
 * @typedef {Object} SkillGapData
 * @property {string} skill
 * @property {number} demandPct
 * @property {number} yourPct
 * @property {number} gapPct
 * @property {'high'|'mid'|'low'} grade
 */

/**
 * @typedef {Object} SkillGapRadarData
 * @property {SkillGapData[]} gaps
 */

/**
 * @typedef {Object} RingConfig
 * @property {number} radius
 * @property {number} strokeWidth
 * @property {string} color
 * @property {string} label
 * @property {number} value
 * @property {number} maxValue
 */

/**
 * @param {HTMLElement} container
 * @returns {void}
 */
function initSkillGapRadar(container) {
  const rootStyles = getComputedStyle(document.documentElement);

  // Read ALL values via getComputedStyle — ZERO hardcoded
  const ringSize = parseFloat(rootStyles.getPropertyValue('--ring-size')) || 120;
  const ringStroke = parseFloat(rootStyles.getPropertyValue('--ring-stroke')) || 8;
  const ringGap = parseFloat(rootStyles.getPropertyValue('--ring-gap')) || 4;
  const durationSlow = rootStyles.getPropertyValue('--duration-slow').trim() || '300ms';
  const easeOut = rootStyles.getPropertyValue('--ease-out').trim() || 'cubic-bezier(0.16, 1, 0.3, 1)';

  // Grade tokens — Nordic signal colors (semantic, NOT color names)
  const gradeHigh = rootStyles.getPropertyValue('--grade-high').trim();    // emerald
  const gradeMid = rootStyles.getPropertyValue('--grade-mid').trim();      // amber
  const gradeLow = rootStyles.getPropertyValue('--grade-low').trim();      // red

  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Parse data from data-gaps attribute
  /** @type {SkillGapRadarData|null} */
  let data = null;
  try {
    const raw = container.getAttribute('data-gaps');
    if (raw) {
      data = JSON.parse(raw);
    }
  } catch (e) {
    console.error('[skill-gap-radar] Failed to parse data-gaps:', e);
    container.innerHTML = '<div class="radar-error" style="color: var(--text-muted); text-align: center; padding: var(--space-4);">Invalid gap data</div>';
    return;
  }

  if (!data || !data.gaps || data.gaps.length === 0) {
    container.innerHTML = '<div class="radar-empty" style="color: var(--text-muted); text-align: center; padding: var(--space-4);">No gap data</div>';
    return;
  }

  // Build ring configs — outermost = highest demand (grade-high), innermost = lowest (grade-low)
  // Sort by demand descending so highest demand = outermost ring
  const sortedGaps = [...data.gaps].sort((a, b) => b.demandPct - a.demandPct);

  const center = ringSize / 2;
  const maxRadius = center - ringStroke;
  const ringCount = sortedGaps.length;
  const availableRadius = maxRadius - ringStroke;
  const step = ringCount > 1 ? availableRadius / (ringCount - 1) : 0;

  /** @type {RingConfig[]} */
  const rings = sortedGaps.map((gap, index) => {
    const radius = maxRadius - index * step;
    let color;
    switch (gap.grade) {
      case 'high':
        color = gradeHigh;
        break;
      case 'mid':
        color = gradeMid;
        break;
      case 'low':
        color = gradeLow;
        break;
      default:
        color = gradeMid;
    }
    return {
      radius,
      strokeWidth: ringStroke,
      color,
      label: gap.skill,
      value: gap.demandPct,
      maxValue: 100,
    };
  });

  // Create SVG
  const svgNS = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(svgNS, 'svg');
  svg.setAttribute('viewBox', `0 0 ${ringSize} ${ringSize}`);
  svg.setAttribute('role', 'img');
  svg.setAttribute('aria-label', 'Skill gap radar — animated rings show market demand vs your coverage');
  svg.classList.add('skill-gap-radar-svg');

  // Create tooltip element
  const tooltip = document.createElement('div');
  tooltip.className = 'skill-gap-radar-tooltip';
  tooltip.setAttribute('role', 'tooltip');
  tooltip.hidden = true;
  container.appendChild(tooltip);

  // Build rings from outermost (index 0) to innermost (last)
  rings.forEach((ring, index) => {
    const circumference = 2 * Math.PI * ring.radius;
    const offset = circumference * (1 - ring.value / ring.maxValue);

    // Background ring (track) — muted
    const track = document.createElementNS(svgNS, 'circle');
    track.setAttribute('cx', String(center));
    track.setAttribute('cy', String(center));
    track.setAttribute('r', String(ring.radius));
    track.setAttribute('fill', 'none');
    track.setAttribute('stroke', 'var(--border-default)');
    track.setAttribute('stroke-width', String(ring.strokeWidth));
    track.setAttribute('stroke-opacity', '0.3');
    svg.appendChild(track);

    // Animated fill ring (grade-colored)
    const fill = document.createElementNS(svgNS, 'circle');
    fill.setAttribute('cx', String(center));
    fill.setAttribute('cy', String(center));
    fill.setAttribute('r', String(ring.radius));
    fill.setAttribute('fill', 'none');
    fill.setAttribute('stroke', ring.color);
    fill.setAttribute('stroke-width', String(ring.strokeWidth));
    fill.setAttribute('stroke-linecap', 'round');
    fill.setAttribute('stroke-dasharray', String(circumference));
    fill.setAttribute('stroke-dashoffset', prefersReduced ? '0' : String(circumference));
    fill.setAttribute('data-skill', ring.label);
    fill.setAttribute('data-demand', String(ring.value));
    fill.setAttribute('data-your', String(sortedGaps[index].yourPct));
    fill.setAttribute('data-gap', String(sortedGaps[index].gapPct));
    fill.setAttribute('data-grade', sortedGaps[index].grade);
    fill.style.transition = prefersReduced
      ? 'none'
      : `stroke-dashoffset ${durationSlow} ${easeOut}`;
    fill.classList.add('skill-gap-radar-ring');
    svg.appendChild(fill);

    // Trigger animation on next frame (allows transition to work)
    if (!prefersReduced) {
      requestAnimationFrame(() => {
        fill.setAttribute('stroke-dashoffset', String(offset));
      });
    }

    // Hover handlers for tooltip
    const showTooltip = (event) => {
      const demand = fill.getAttribute('data-demand');
      const your = fill.getAttribute('data-your');
      const gap = fill.getAttribute('data-gap');
      const skill = fill.getAttribute('data-skill');

      tooltip.innerHTML = `
        <strong>${skill}</strong>
        <div class="tooltip-row"><span class="tooltip-label">Demand</span><span class="tooltip-value">${demand}%</span></div>
        <div class="tooltip-row"><span class="tooltip-label">Your Coverage</span><span class="tooltip-value">${your}%</span></div>
        <div class="tooltip-row"><span class="tooltip-label">Gap</span><span class="tooltip-value">${gap}%</span></div>
      `;

      const rect = container.getBoundingClientRect();
      tooltip.style.left = `${event.clientX - rect.left + 12}px`;
      tooltip.style.top = `${event.clientY - rect.top - 12}px`;
      tooltip.hidden = false;
      tooltip.style.opacity = '1';
    };

    const hideTooltip = () => {
      tooltip.hidden = true;
      tooltip.style.opacity = '0';
    };

    fill.addEventListener('mouseenter', showTooltip);
    fill.addEventListener('mousemove', showTooltip);
    fill.addEventListener('mouseleave', hideTooltip);
    track.addEventListener('mouseenter', showTooltip);
    track.addEventListener('mousemove', showTooltip);
    track.addEventListener('mouseleave', hideTooltip);
  });

  // Center label
  const centerText = document.createElementNS(svgNS, 'text');
  centerText.setAttribute('x', String(center));
  centerText.setAttribute('y', String(center + 4));
  centerText.setAttribute('text-anchor', 'middle');
  centerText.setAttribute('dominant-baseline', 'middle');
  centerText.setAttribute('font-family', 'var(--font-display)');
  centerText.setAttribute('font-size', 'var(--text-xs)');
  centerText.setAttribute('fill', 'var(--text-muted)');
  centerText.textContent = 'SKILL GAP';
  svg.appendChild(centerText);

  // Clear container and append SVG
  container.innerHTML = '';
  container.appendChild(svg);
  container.appendChild(tooltip);

  // Handle resize (re-read tokens in case theme/density changed)
  const resizeObserver = new ResizeObserver(() => {
    // SVG is viewBox-based, so it scales automatically
  });
  resizeObserver.observe(container);

  // Cleanup on unmount (if needed)
  container._radarCleanup = () => {
    resizeObserver.disconnect();
  };
}

// Component registry registration
/**
 * @returns {void}
 */
export function registerSkillGapRadar() {
  if (typeof window !== 'undefined' && window.registerComponent) {
    window.registerComponent('skill-gap-radar', { init: initSkillGapRadar });
  }
}

// Auto-init for declarative usage: <div data-component="skill-gap-radar" data-gaps='...'>
if (typeof window !== 'undefined') {
  document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-component="skill-gap-radar"]').forEach((el) => {
      initSkillGapRadar(el);
    });
  });

  // Also handle pagelayout:ready for dynamic injection
  window.addEventListener('pagelayout:ready', () => {
    document.querySelectorAll('[data-component="skill-gap-radar"]').forEach((el) => {
      initSkillGapRadar(el);
    });
  });

  // Self-register
  registerSkillGapRadar();
}