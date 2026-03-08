/**
 * API service for Component operations
 */

import { api } from './api';
import type { Component, ComponentCreate, ComponentUpdate, ComponentList } from '../types/component';

export const componentService = {
  async create(data: ComponentCreate): Promise<Component> {
    return api.post<Component>('/api/v1/components', data);
  },

  async getById(id: string): Promise<Component> {
    return api.get<Component>(`/api/v1/components/${id}`);
  },

  async getByArchitecture(architectureId: string): Promise<ComponentList> {
    return api.get<ComponentList>(`/api/v1/architectures/${architectureId}/components`);
  },

  async getByZone(zoneId: string): Promise<ComponentList> {
    return api.get<ComponentList>(`/api/v1/zones/${zoneId}/components`);
  },

  async update(id: string, data: ComponentUpdate): Promise<Component> {
    return api.put<Component>(`/api/v1/components/${id}`, data);
  },

  async delete(id: string): Promise<void> {
    return api.delete(`/api/v1/components/${id}`);
  },
};
