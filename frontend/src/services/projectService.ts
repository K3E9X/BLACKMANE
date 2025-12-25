/**
 * Project Service - API calls for project management
 */

import { api } from './api'
import type { Project, ProjectCreate, ProjectUpdate, ProjectList } from '../types/project'

export const projectService = {
  /**
   * Get all projects
   */
  async getAll(skip: number = 0, limit: number = 100): Promise<ProjectList> {
    return api.get<ProjectList>(`/api/v1/projects?skip=${skip}&limit=${limit}`)
  },

  /**
   * Get a single project by ID
   */
  async getById(id: string): Promise<Project> {
    return api.get<Project>(`/api/v1/projects/${id}`)
  },

  /**
   * Create a new project
   */
  async create(data: ProjectCreate): Promise<Project> {
    return api.post<Project>('/api/v1/projects', data)
  },

  /**
   * Update a project
   */
  async update(id: string, data: ProjectUpdate): Promise<Project> {
    return api.put<Project>(`/api/v1/projects/${id}`, data)
  },

  /**
   * Delete a project
   */
  async delete(id: string): Promise<void> {
    return api.delete<void>(`/api/v1/projects/${id}`)
  },
}
