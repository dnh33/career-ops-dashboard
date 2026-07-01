#!/usr/bin/env node
/**
 * axe-core accessibility audit for Hermes Terminal routes.
 * Usage: node scripts/a11y-audit.mjs [baseUrl]
 * Requires: npm run preview (or dev) running on baseUrl
 */
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';

const BASE = process.argv[2] || 'http://localhost:4321';

const ROUTES = [
  '/',
  '/market',
  '/market/skill-gap',
  '/companies',
  '/cv/builder',
  '/cv/optimize',
  '/settings',
  '/market/company/corti',
];

let totalViolations = 0;

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });

console.log(`=== axe-core audit @ ${BASE} ===\n`);

for (const route of ROUTES) {
  const url = `${BASE}${route}`;
  const page = await context.newPage();
  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    const violations = results.violations;
    totalViolations += violations.length;

    if (violations.length === 0) {
      console.log(`PASS  ${route}`);
    } else {
      console.log(`FAIL  ${route} (${violations.length} violations)`);
      for (const v of violations) {
        console.log(`  - [${v.impact}] ${v.id}: ${v.description}`);
        for (const node of v.nodes.slice(0, 3)) {
          console.log(`      ${node.target.join(' > ')}`);
        }
      }
    }
  } catch (err) {
    console.log(`ERROR ${route}: ${err.message}`);
    totalViolations += 1;
  } finally {
    await page.close();
  }
}

await browser.close();

console.log(`\n=== Total violations: ${totalViolations} ===`);
process.exit(totalViolations > 0 ? 1 : 0);
