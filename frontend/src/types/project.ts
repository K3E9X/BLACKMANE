/**
 * Project types for BLACKMANE
 */

export enum ProjectType {
  CLOUD = 'cloud',
  ON_PREMISE = 'on-premise',
  HYBRID = 'hybrid',
}

export enum CriticalityLevel {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical',
}

export interface Project {
  id: string
  name: string
  project_type: ProjectType
  business_context?: string
  criticality_level: CriticalityLevel
  created_at: string
  updated_at: string
}

export interface ProjectCreate {
  name: string
  project_type: ProjectType
  business_context?: string
  criticality_level: CriticalityLevel
}

export interface ProjectUpdate {
  name?: string
  business_context?: string
  criticality_level?: CriticalityLevel
}

export interface ProjectList {
  projects: Project[]
  total: number
}
