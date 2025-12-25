/**
 * TypeScript types for Flow entity
 */

export enum FlowProtocol {
  HTTP = 'http',
  HTTPS = 'https',
  SSH = 'ssh',
  RDP = 'rdp',
  SQL = 'sql',
  LDAP = 'ldap',
  DNS = 'dns',
  SMTP = 'smtp',
  OTHER = 'other',
}

export interface FlowCreate {
  architecture_id: string;
  source_component_id: string;
  target_component_id: string;
  protocol: FlowProtocol;
  port?: number;
  is_authenticated?: boolean;
  is_encrypted?: boolean;
  description?: string;
}

export interface FlowUpdate {
  protocol?: FlowProtocol;
  port?: number;
  is_authenticated?: boolean;
  is_encrypted?: boolean;
  description?: string;
}

export interface Flow {
  id: string;
  architecture_id: string;
  source_component_id: string;
  target_component_id: string;
  protocol: FlowProtocol;
  port: number | null;
  is_authenticated: boolean;
  is_encrypted: boolean;
  description: string | null;
  created_at: string;
}

export interface FlowList {
  flows: Flow[];
  total: number;
}
