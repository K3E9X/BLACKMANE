/**
 * API service for Component operations
 */

import { api } from './api';
import type { Component, ComponentCreate, ComponentUpdate, ComponentList } from '../types/component';

export const componentService = {
  async create(data: ComponentCreate): Promise<Component> {
    return api.post<Component>('/components', data);
  },

  async getById(id: string): Promise<Component> {
    return api.get<Component>(`/components/${id}`);
  },

  async getByArchitecture(architectureId: string): Promise<ComponentList> {
    return api.get<ComponentList>(`/architectures/${architectureId}/components`);
  },

  async getByZone(zoneId: string): Promise<ComponentList> {
    return api.get<ComponentList>(`/zones/${zoneId}/components`);
  },

  async update(id: string, data: ComponentUpdate): Promise<Component> {
    return api.put<Component>(`/components/${id}`, data);
  },

  async delete(id: string): Promise<void> {
    return api.delete(`/components/${id}`);
  },
};
