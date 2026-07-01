#!/usr/bin/env node
/**
 * Performance budget check using Lighthouse (1440p).
 * Usage: node scripts/perf-budget.mjs [baseUrl]
 */
import lighthouse from 'lighthouse';
import * as chromeLauncher from 'chrome-launcher';

const BASE = process.argv[2] || 'http://localhost:4321';
const URL = `${BASE}/`;

const BUDGET = {
  lcp: 2500,
  cls: 0.1,
  tbt: 200,
};

const chrome = await chromeLauncher.launch({ chromeFlags: ['--headless', '--no-sandbox'] });
const options = {
  logLevel: 'error',
  output: 'json',
  onlyCategories: ['performance'],
  port: chrome.port,
  formFactor: 'desktop',
  screenEmulation: { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false },
  throttlingMethod: 'provided',
  throttling: {
    rttMs: 40,
    throughputKbps: 10240,
    cpuSlowdownMultiplier: 1,
  },
};

const runnerResult = await lighthouse(URL, options);
await chrome.kill();

const lhr = runnerResult?.lhr;
if (!lhr) {
  console.error('Lighthouse failed to produce results');
  process.exit(1);
}

const perf = lhr.audits;
const lcp = perf['largest-contentful-paint']?.numericValue ?? Infinity;
const cls = perf['cumulative-layout-shift']?.numericValue ?? Infinity;
const tbt = perf['total-blocking-time']?.numericValue ?? Infinity;

console.log('=== Performance Budget (1440p) ===\n');
console.log(`LCP: ${(lcp / 1000).toFixed(2)}s  (budget < ${BUDGET.lcp / 1000}s)  ${lcp < BUDGET.lcp ? 'PASS' : 'FAIL'}`);
console.log(`CLS: ${cls.toFixed(3)}     (budget < ${BUDGET.cls})       ${cls < BUDGET.cls ? 'PASS' : 'FAIL'}`);
console.log(`TBT: ${tbt.toFixed(0)}ms    (budget < ${BUDGET.tbt}ms)     ${tbt < BUDGET.tbt ? 'PASS' : 'FAIL'}`);

const pass = lcp < BUDGET.lcp && cls < BUDGET.cls && tbt < BUDGET.tbt;
process.exit(pass ? 0 : 1);
