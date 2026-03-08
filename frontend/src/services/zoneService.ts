/**
 * API service for Zone operations
 */

import { api } from './api';
import type { Zone, ZoneCreate, ZoneUpdate, ZoneList } from '../types/zone';

export const zoneService = {
  async create(data: ZoneCreate): Promise<Zone> {
    return api.post<Zone>('/api/v1/zones', data);
  },

  async getById(id: string): Promise<Zone> {
    return api.get<Zone>(`/api/v1/zones/${id}`);
  },

  async getByArchitecture(architectureId: string): Promise<ZoneList> {
    return api.get<ZoneList>(`/api/v1/architectures/${architectureId}/zones`);
  },

  async update(id: string, data: ZoneUpdate): Promise<Zone> {
    return api.put<Zone>(`/api/v1/zones/${id}`, data);
  },

  async delete(id: string): Promise<void> {
    return api.delete(`/api/v1/zones/${id}`);
  },
};
