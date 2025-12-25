/**
 * TypeScript types for Component entity
 */

export enum ComponentType {
  FIREWALL = 'firewall',
  LOAD_BALANCER = 'load_balancer',
  SERVER = 'server',
  DATABASE = 'database',
  IAM = 'iam',
  BASTION = 'bastion',
  API_GATEWAY = 'api_gateway',
  VPN = 'vpn',
  OTHER = 'other',
}

export interface ComponentCreate {
  architecture_id: string;
  zone_id: string;
  name: string;
  component_type: ComponentType;
  has_admin_interface?: boolean;
  requires_mfa?: boolean;
  has_logging?: boolean;
  encryption_at_rest?: boolean;
  encryption_in_transit?: boolean;
  description?: string;
}

export interface ComponentUpdate {
  name?: string;
  component_type?: ComponentType;
  zone_id?: string;
  has_admin_interface?: boolean;
  requires_mfa?: boolean;
  has_logging?: boolean;
  encryption_at_rest?: boolean;
  encryption_in_transit?: boolean;
  description?: string;
}

export interface Component {
  id: string;
  architecture_id: string;
  zone_id: string;
  name: string;
  component_type: ComponentType;
  has_admin_interface: boolean;
  requires_mfa: boolean;
  has_logging: boolean;
  encryption_at_rest: boolean;
  encryption_in_transit: boolean;
  description: string | null;
  created_at: string;
}

export interface ComponentList {
  components: Component[];
  total: number;
}
