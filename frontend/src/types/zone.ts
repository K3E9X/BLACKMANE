/**
 * TypeScript types for Zone entity
 */

export enum TrustLevel {
  UNTRUSTED = 'untrusted',
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
}

export interface ZoneCreate {
  architecture_id: string;
  name: string;
  trust_level: TrustLevel;
  description?: string;
}

export interface ZoneUpdate {
  name?: string;
  trust_level?: TrustLevel;
  description?: string;
}

export interface Zone {
  id: string;
  architecture_id: string;
  name: string;
  trust_level: TrustLevel;
  description: string | null;
  created_at: string;
}

export interface ZoneList {
  zones: Zone[];
  total: number;
}
