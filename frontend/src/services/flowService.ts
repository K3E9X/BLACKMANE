/**
 * API service for Flow operations
 */

import { api } from './api';
import type { Flow, FlowCreate, FlowUpdate, FlowList } from '../types/flow';

export const flowService = {
  async create(data: FlowCreate): Promise<Flow> {
    return api.post<Flow>('/flows', data);
  },

  async getById(id: string): Promise<Flow> {
    return api.get<Flow>(`/flows/${id}`);
  },

  async getByArchitecture(architectureId: string): Promise<FlowList> {
    return api.get<FlowList>(`/architectures/${architectureId}/flows`);
  },

  async getByComponent(componentId: string): Promise<FlowList> {
    return api.get<FlowList>(`/components/${componentId}/flows`);
  },

  async update(id: string, data: FlowUpdate): Promise<Flow> {
    return api.put<Flow>(`/flows/${id}`, data);
  },

  async delete(id: string): Promise<void> {
    return api.delete(`/flows/${id}`);
  },
};
