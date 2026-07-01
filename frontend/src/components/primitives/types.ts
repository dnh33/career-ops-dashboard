export type MetricVariant = 'default' | 'primary' | 'warm' | 'success' | 'warning' | 'error';

export interface MetricCardProps {
  label: string;
  value: string | number;
  unit?: string;
  variant?: MetricVariant;
  trend?: string;
  trendDirection?: 'up' | 'down' | 'neutral';
  sparklineData?: number[];
  class?: string;
}

export interface DataTableColumn {
  key: string;
  label: string;
  mono?: boolean;
  sortable?: boolean;
  align?: 'left' | 'center' | 'right';
}

export type RichCell =
  | string
  | number
  | { kind: 'pill'; label: string; variant: StatusPillVariant; mono?: boolean }
  | { kind: 'link'; href: string; label: string }
  | { kind: 'code'; code: string; language?: string };

export interface DataTableRow {
  id: string;
  cells: Record<string, RichCell>;
}

export interface DataTableProps {
  columns: DataTableColumn[];
  rows: DataTableRow[];
  sortKey?: string;
  sortDirection?: 'asc' | 'desc';
  emptyMessage?: string;
  class?: string;
}

export interface SparklineProps {
  data: number[];
  width?: number;
  height?: number;
  strokeWidth?: number;
  tooltip?: boolean;
  class?: string;
}

export type StatusPillVariant = 'default' | 'primary' | 'success' | 'warning' | 'error' | 'warm' | 'info' | 'neutral';

export interface StatusPillProps {
  label: string;
  variant?: StatusPillVariant;
  mono?: boolean;
  class?: string;
}

export interface SearchFieldProps {
  name?: string;
  placeholder?: string;
  value?: string;
  ariaLabel?: string;
  class?: string;
}

export interface SegmentedOption {
  id: string;
  label: string;
  icon?: string;
}

export interface SegmentedControlProps {
  options: SegmentedOption[];
  value: string;
  name?: string;
  compact?: boolean;
  vertical?: boolean;
  ariaLabel?: string;
  class?: string;
}

export interface OverlayProps {
  open?: boolean;
  title?: string;
  dismissible?: boolean;
  class?: string;
}

export interface EmptyStateProps {
  title: string;
  description?: string;
  icon?: string;
  actionLabel?: string;
  actionHref?: string;
  class?: string;
}

export interface CodeBlockProps {
  code: string;
  language?: string;
  showLineNumbers?: boolean;
  copyable?: boolean;
  class?: string;
}

export interface LoaderProps {
  label?: string;
  size?: 'sm' | 'md' | 'lg';
  class?: string;
}

export interface ErrorStateProps {
  title?: string;
  message: string;
  retryLabel?: string;
  class?: string;
}

export interface SwitchProps {
  name: string;
  label: string;
  description?: string;
  checked?: boolean;
  disabled?: boolean;
  class?: string;
}
