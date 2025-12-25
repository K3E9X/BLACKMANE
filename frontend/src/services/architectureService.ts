/**
 * API service for Architecture operations
 */

import { api } from './api';
import type { Architecture, ArchitectureCreate, ArchitectureUpdate } from '../types/architecture';

export const architectureService = {
  async create(data: ArchitectureCreate): Promise<Architecture> {
    return api.post<Architecture>('/architectures', data);
  },

  async getById(id: string): Promise<Architecture> {
    return api.get<Architecture>(`/architectures/${id}`);
  },

  async getByProjectId(projectId: string): Promise<Architecture> {
    return api.get<Architecture>(`/projects/${projectId}/architecture`);
  },

  async update(id: string, data: ArchitectureUpdate): Promise<Architecture> {
    return api.put<Architecture>(`/architectures/${id}`, data);
  },

  async delete(id: string): Promise<void> {
    return api.delete(`/architectures/${id}`);
  },
};
