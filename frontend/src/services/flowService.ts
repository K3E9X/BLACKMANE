/**
 * API service for Flow operations
 */

import { api } from './api';
import type { Flow, FlowCreate, FlowUpdate, FlowList } from '../types/flow';

export const flowService = {
  async create(data: FlowCreate): Promise<Flow> {
    return api.post<Flow>('/api/v1/flows', data);
  },

  async getById(id: string): Promise<Flow> {
    return api.get<Flow>(`/api/v1/flows/${id}`);
  },

  async getByArchitecture(architectureId: string): Promise<FlowList> {
    return api.get<FlowList>(`/api/v1/architectures/${architectureId}/flows`);
  },

  async getByComponent(componentId: string): Promise<FlowList> {
    return api.get<FlowList>(`/api/v1/components/${componentId}/flows`);
  },

  async update(id: string, data: FlowUpdate): Promise<Flow> {
    return api.put<Flow>(`/api/v1/flows/${id}`, data);
  },

  async delete(id: string): Promise<void> {
    return api.delete(`/api/v1/flows/${id}`);
  },
};
