/**
 * TypeScript types for Architecture entity
 */

export interface ArchitectureCreate {
  project_id: string;
  description?: string;
}

export interface ArchitectureUpdate {
  description?: string;
}

export interface Architecture {
  id: string;
  project_id: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}
