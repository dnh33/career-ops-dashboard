export interface MarketMetrics {
  avgSalary: number;
  avgSalarySparkline: number[];
  topSkill: string;
  topSkillSparkline: number[];
  topCity: string;
  topCitySparkline: number[];
  velocity: number;
  velocitySparkline: number[];
  postingCount: number;
}

export interface MarketPosting {
  id: string;
  company: string;
  companySlug: string;
  role: string;
  seniority: string;
  location: string;
  salary: number | null;
  salaryLabel: string;
  skills: string[];
  skillsLabel: string;
  postedDaysAgo: number;
  postedLabel: string;
  gap: number;
  gapLabel: string;
  url?: string;
}

export interface MarketOverview {
  metrics: MarketMetrics;
  postings: MarketPosting[];
  marketHealth?: { score: number; trendPct: number; sparkline: number[] };
}

export interface SkillGapRow {
  skill: string;
  demandPct: number;
  yourPct: number;
  gap: number;
  trend: string;
}

export interface RadarPoint {
  skill: string;
  demand: number;
  coverage: number;
  gap: number;
}

export interface SkillGapResponse {
  skills: SkillGapRow[];
  radarData: RadarPoint[];
}

export interface CompanyPageCompany {
  slug: string;
  name: string;
  tier: string;
  employees: string;
  avgSalary: number;
  openRoles: number;
  hiringVelocity: number[];
  location?: string;
  techStack?: string[];
}

export interface CompanyPosting {
  id: string;
  role: string;
  seniority: string;
  salary: number | null;
  salaryLabel: string;
  yourSkills: string;
  gap: number;
  gapLabel: string;
  fitScore: number;
  action: string;
}

export interface CompanyPageResponse {
  company: CompanyPageCompany;
  postings: CompanyPosting[];
  profile?: {
    name: string;
    location: string;
    techStack: string[];
    culture: string;
    links?: Record<string, string>;
  };
}
