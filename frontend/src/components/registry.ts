/**
 * Component Registry — Dynamic Component Loading
 * Design System Foundation §3.4 & §4.2.3
 * 
 * Pattern: registerComponent('name', { init: initFunction })
 * Usage: <div data-component="name" data-component-props='{}' />
 */

export interface ComponentModule {
  init: (root: HTMLElement) => (() => void) | void;
}

const componentRegistry = new Map<string, ComponentModule>();

/**
 * Register a component for dynamic loading via data-component attributes
 * @param name - Component name (e.g., 'signal-card', 'command-palette', 'skill-gap-radar')
 * @param module - Component module with init function
 */
export function registerComponent(name: string, module: ComponentModule): void {
  if (componentRegistry.has(name)) {
    console.warn(`[registry] Component "${name}" already registered, overwriting`);
  }
  componentRegistry.set(name, module);
}

/**
 * Get a registered component module
 * @param name - Component name
 * @returns Component module or undefined if not registered
 */
export function getComponent(name: string): ComponentModule | undefined {
  return componentRegistry.get(name);
}

/**
 * Initialize all components within a root element
 * Scans for [data-component] attributes and calls their init functions
 * @param root - Root element to scan (default: document.body)
 * @returns Cleanup function that calls all component cleanup functions
 */
export function initComponents(root: HTMLElement = document.body): () => void {
  const cleanupFunctions: (() => void)[] = [];

  const components = root.querySelectorAll('[data-component]');
  components.forEach((element) => {
    const name = element.getAttribute('data-component');
    if (!name) return;

    const module = componentRegistry.get(name);
    if (!module) {
      console.warn(`[registry] Component "${name}" not registered`);
      return;
    }

    try {
      const cleanup = module.init(element as HTMLElement);
      if (cleanup) {
        cleanupFunctions.push(cleanup);
      }
    } catch (error) {
      console.error(`[registry] Failed to initialize component "${name}":`, error);
    }
  });

  // Return combined cleanup function
  return () => {
    cleanupFunctions.forEach((cleanup) => {
      try {
        cleanup();
      } catch (error) {
        console.error('[registry] Cleanup error:', error);
      }
    });
  };
}

/**
 * Auto-initialize components on pagelayout:ready event
 * This is fired by PageLayout.astro when the page is ready
 */
if (typeof document !== 'undefined') {
  document.addEventListener('pagelayout:ready', ((event: CustomEvent) => {
    const root = event.detail?.root || document.body;
    initComponents(root);
  }) as EventListener);

  // Also auto-init on DOMContentLoaded for static components
  document.addEventListener('DOMContentLoaded', () => {
    initComponents(document.body);
  });
}

/**
 * Re-initialize components after dynamic content insertion
 * Call this after injecting new HTML with data-component attributes
 * @param root - Root element to scan (default: document.body)
 */
export function reinitComponents(root: HTMLElement = document.body): () => void {
  return initComponents(root);
}

// Export registry for debugging
export { componentRegistry };

// Make registry globally available for self-registration from module scripts
if (typeof window !== 'undefined') {
  window.registerComponent = registerComponent;
  window.getComponent = getComponent;
  window.initComponents = initComponents;
  window.reinitComponents = reinitComponents;
  window.componentRegistry = componentRegistry;
}

// Built-in component registrations
// These are imported and registered by their respective Astro components
// to avoid circular dependencies

// Example registration pattern (components self-register in their module scripts):
// import { initSignalCard } from './ui/Card.astro?script';
// registerComponent('signal-card', { init: initSignalCard });

// Self-registration: Card.astro script exports initSignalCard and registers itself
// This avoids circular imports - the script runs in the browser and calls registerComponent
if (typeof window !== 'undefined') {
  // Components self-register via their module scripts when loaded
  // See Card.astro script block for initSignalCard registration
}