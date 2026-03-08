import { api } from './api'
import type { Analysis, FindingList } from '../types/analysis'

export const analysisService = {
  async run(projectId: string): Promise<Analysis> {
    return api.post<Analysis>(`/api/v1/projects/${projectId}/analyze`, {})
  },

  async getLatest(projectId: string): Promise<Analysis> {
    return api.get<Analysis>(`/api/v1/projects/${projectId}/analysis/latest`)
  },

  async getFindings(projectId: string): Promise<FindingList> {
    return api.get<FindingList>(`/api/v1/projects/${projectId}/findings`)
  },
}
