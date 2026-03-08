export interface Analysis {
  id: string
  project_id: string
  status: string
  started_at: string
  completed_at?: string | null
  global_risk_score?: number | null
  total_findings: number
  critical_findings: number
  high_findings: number
  medium_findings: number
  low_findings: number
}

export interface Finding {
  id: string
  analysis_id: string
  rule_id: string
  rule_name: string
  category: string
  severity: 'critical' | 'high' | 'medium' | 'low'
  title: string
  description: string
  impact: string
  affected_component_id?: string | null
  affected_flow_id?: string | null
  created_at: string
}

export interface FindingList {
  findings: Finding[]
  total: number
}
