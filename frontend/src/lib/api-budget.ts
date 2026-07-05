/**
 * API Budget Guard — 100 request budget enforcement
 * Design System Foundation §3.5 & §4.3
 * Components declare cost/priority, system enforces and evicts lower priority
 */

export interface BudgetEntry {
  component: string;
  cost: number;
  priority: 'high' | 'medium' | 'low';
}

export interface BudgetStatus {
  used: number;
  max: number;
  remaining: number;
  entries: BudgetEntry[];
}

const MAX_BUDGET = 100;
const budgetEntries: BudgetEntry[] = [];

let budgetUsed = 0;
let budgetMax = MAX_BUDGET;

/**
 * Request budget for a component operation
 * @param entry - Budget entry with component name, cost, and priority
 * @returns true if budget granted, false if denied
 */
export function requestBudget(entry: BudgetEntry): boolean {
  const totalAfter = budgetUsed + entry.cost;

  if (totalAfter <= budgetMax) {
    budgetEntries.push(entry);
    budgetUsed = totalAfter;
    dispatchBudgetChange();
    return true;
  }

  // Try to evict lower priority entries
  const sortedEntries = [...budgetEntries].sort((a, b) => {
    const priorityOrder = { low: 0, medium: 1, high: 2 };
    return priorityOrder[a.priority] - priorityOrder[b.priority];
  });

  let freed = 0;
  const toEvict: BudgetEntry[] = [];

  for (const existing of sortedEntries) {
    if (existing.priority === 'high') break; // Never evict high priority
    if (entry.priority === 'high' || existing.priority === 'low') {
      freed += existing.cost;
      toEvict.push(existing);
      if (budgetUsed + entry.cost - freed <= budgetMax) {
        break;
      }
    }
  }

  if (budgetUsed + entry.cost - freed <= budgetMax) {
    // Evict lower priority entries
    for (const evicted of toEvict) {
      const index = budgetEntries.indexOf(evicted);
      if (index !== -1) budgetEntries.splice(index, 1);
    }
    budgetUsed = budgetUsed + entry.cost - freed;
    budgetEntries.push(entry);
    dispatchBudgetChange();
    return true;
  }

  return false;
}

/**
 * Release budget for a component
 * @param component - Component name to release budget for
 */
export function releaseBudget(component: string): void {
  const index = budgetEntries.findIndex((e) => e.component === component);
  if (index !== -1) {
    budgetUsed -= budgetEntries[index].cost;
    budgetEntries.splice(index, 1);
    dispatchBudgetChange();
  }
}

/**
 * Get current budget status
 */
export function getBudgetStatus(): BudgetStatus {
  return {
    used: budgetUsed,
    max: budgetMax,
    remaining: budgetMax - budgetUsed,
    entries: [...budgetEntries],
  };
}

/**
 * Reset budget (for testing or session reset)
 */
export function resetBudget(): void {
  budgetUsed = 0;
  budgetEntries.length = 0;
  dispatchBudgetChange();
}

/**
 * Set max budget (for testing)
 */
export function setMaxBudget(max: number): void {
  budgetMax = max;
  dispatchBudgetChange();
}

function dispatchBudgetChange(): void {
  if (typeof window !== 'undefined') {
    window.dispatchEvent(new CustomEvent('budget:change', { detail: getBudgetStatus() }));
  }
}