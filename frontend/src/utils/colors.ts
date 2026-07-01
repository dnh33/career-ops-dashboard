/**
 * Shared grade → color utilities for Career Ops Dashboard.
 *
 * Maps letter grades (A–G) to three semantic tiers that align with
 * the CSS custom properties defined in globals.css:
 *   high  → --grade-high-*   (excellent / strong)
 *   mid   → --grade-mid-*    (good / cautionary)
 *   low   → --grade-low-*    (below expectations / mismatch)
 */

/** Convert a numeric score (0-5) to a letter grade (A-G). */
export function scoreToGrade(score: number | null | undefined): string {
  if (score == null || score === 0) return 'G';
  if (score >= 4.5) return 'A';
  if (score >= 3.75) return 'B';
  if (score >= 3.0) return 'C';
  if (score >= 2.25) return 'D';
  if (score >= 1.5) return 'E';
  if (score >= 0.75) return 'F';
  return 'G';
}

/** Map a letter grade to its semantic tier key. */
export function toGradeTier(grade: string): 'high' | 'mid' | 'low' {
  const g = grade.toUpperCase();
  if (g === 'A' || g === 'B') return 'high';
  if (g === 'C') return 'mid';
  return 'low'; // D, E, F, G
}

/** Return the CSS class string for a grade badge element. */
export function gradeClass(grade: string): string {
  return `grade-badge grade-badge-${toGradeTier(grade)}`;
}

/** Return CSS custom property references for a grade tier (for JS-driven styling). */
export function gradeColorVars(grade: string): { bg: string; text: string; stroke: string } {
  const tier = toGradeTier(grade);
  return {
    bg: `var(--grade-${tier}-bg)`,
    text: `var(--grade-${tier}-text)`,
    stroke: `var(--grade-${tier})`,
  };
}