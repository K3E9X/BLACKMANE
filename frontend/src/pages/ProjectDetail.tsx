/**
 * Project Detail Page
 */

import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { projectService } from '../services/projectService'
import type { Project } from '../types/project'
import { Button } from '../components/Button'
import { Card } from '../components/Card'

export function ProjectDetail() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [project, setProject] = useState<Project | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (id) {
      loadProject(id)
    }
  }, [id])

  async function loadProject(projectId: string) {
    try {
      setLoading(true)
      setError(null)
      const data = await projectService.getById(projectId)
      setProject(data)
    } catch (err: any) {
      setError(err.message || 'Failed to load project')
      console.error('Error loading project:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <p className="text-dark-text-secondary">Chargement...</p>
      </div>
    )
  }

  if (error || !project) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-severity-critical/10 border border-severity-critical text-severity-critical px-4 py-3 rounded mb-4">
          {error || 'Projet non trouvé'}
        </div>
        <Button onClick={() => navigate('/projects')}>
          Retour aux projets
        </Button>
      </div>
    )
  }

  const getProjectTypeLabel = (type: string) => {
    const labels = {
      cloud: 'Cloud',
      'on-premise': 'On-Premise',
      hybrid: 'Hybride',
    }
    return labels[type as keyof typeof labels] || type
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <div className="mb-8">
        <Button
          variant="secondary"
          size="sm"
          onClick={() => navigate('/projects')}
          className="mb-4"
        >
          ← Retour
        </Button>
        <h1 className="text-3xl font-bold text-dark-text mb-2">
          {project.name}
        </h1>
        <p className="text-dark-text-secondary">
          Créé le {new Date(project.created_at).toLocaleDateString('fr-FR')}
        </p>
      </div>

      <div className="space-y-6">
        <Card>
          <h2 className="text-xl font-semibold text-dark-text mb-4">
            Informations générales
          </h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-dark-text-secondary mb-1">Type</p>
              <p className="text-dark-text font-medium">
                {getProjectTypeLabel(project.project_type)}
              </p>
            </div>
            <div>
              <p className="text-sm text-dark-text-secondary mb-1">Criticité</p>
              <p className="text-dark-text font-medium capitalize">
                {project.criticality_level}
              </p>
            </div>
          </div>
          {project.business_context && (
            <div className="mt-4">
              <p className="text-sm text-dark-text-secondary mb-1">
                Contexte métier
              </p>
              <p className="text-dark-text">{project.business_context}</p>
            </div>
          )}
        </Card>

        <Card>
          <div className="text-center py-12">
            <p className="text-dark-text-secondary mb-4">
              L'architecture et les analyses seront disponibles prochainement
            </p>
            <p className="text-sm text-dark-text-secondary">
              (Semaine 2-3 du MVP)
            </p>
          </div>
        </Card>
      </div>
    </div>
  )
}
