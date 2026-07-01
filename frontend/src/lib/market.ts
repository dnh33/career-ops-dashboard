import type { StatusPillVariant } from '../components/primitives/types';

export function gapVariant(gap: number): StatusPillVariant {
  if (gap > 20) return 'warm';
  if (gap >= 10) return 'warning';
  return 'success';
}

export function fitVariant(score: number): StatusPillVariant {
  if (score >= 80) return 'success';
  if (score >= 60) return 'warning';
  return 'error';
}

export function actionVariant(action: string): StatusPillVariant {
  if (action === 'Apply') return 'success';
  if (action === 'Tailor') return 'warning';
  return 'default';
}

export function formatSalary(value: number | null | undefined): string {
  if (value == null) return '—';
  return value.toLocaleString('en-DK');
}

export async function fetchMarketOverview(apiBase = ''): Promise<Response> {
  return fetch(`${apiBase}/api/market/overview`, { cache: 'no-store' });
}

export async function fetchSkillGap(apiBase = ''): Promise<Response> {
  return fetch(`${apiBase}/api/market/skill-gap`, { cache: 'no-store' });
}

export async function fetchCompany(slug: string, apiBase = ''): Promise<Response> {
  return fetch(`${apiBase}/api/market/company/${slug}`, { cache: 'no-store' });
}
