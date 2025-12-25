/**
 * Project List Page
 */

import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { projectService } from '../services/projectService'
import type { Project } from '../types/project'
import { Button } from '../components/Button'
import { Card } from '../components/Card'

export function ProjectList() {
  const navigate = useNavigate()
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    loadProjects()
  }, [])

  async function loadProjects() {
    try {
      setLoading(true)
      setError(null)
      const data = await projectService.getAll()
      setProjects(data.projects)
    } catch (err: any) {
      setError(err.message || 'Failed to load projects')
      console.error('Error loading projects:', err)
    } finally {
      setLoading(false)
    }
  }

  async function handleDelete(id: string, name: string) {
    if (!confirm(`Êtes-vous sûr de vouloir supprimer le projet "${name}" ?`)) {
      return
    }

    try {
      await projectService.delete(id)
      await loadProjects()
    } catch (err: any) {
      alert(`Erreur lors de la suppression : ${err.message}`)
    }
  }

  const getCriticalityColor = (level: string) => {
    const colors = {
      low: 'text-accent-primary',
      medium: 'text-severity-medium',
      high: 'text-severity-high',
      critical: 'text-severity-critical',
    }
    return colors[level as keyof typeof colors] || 'text-dark-text'
  }

  const getProjectTypeLabel = (type: string) => {
    const labels = {
      cloud: 'Cloud',
      'on-premise': 'On-Premise',
      hybrid: 'Hybride',
    }
    return labels[type as keyof typeof labels] || type
  }

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <p className="text-dark-text-secondary">Chargement...</p>
      </div>
    )
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-dark-text mb-2">Projets</h1>
          <p className="text-dark-text-secondary">
            {projects.length} projet{projects.length > 1 ? 's' : ''}
          </p>
        </div>
        <Button onClick={() => navigate('/projects/new')}>
          Nouveau Projet
        </Button>
      </div>

      {error && (
        <div className="bg-severity-critical/10 border border-severity-critical text-severity-critical px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {projects.length === 0 ? (
        <Card>
          <div className="text-center py-12">
            <p className="text-dark-text-secondary mb-4">
              Aucun projet pour le moment
            </p>
            <Button onClick={() => navigate('/projects/new')}>
              Créer votre premier projet
            </Button>
          </div>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {projects.map((project) => (
            <Card
              key={project.id}
              onClick={() => navigate(`/projects/${project.id}`)}
            >
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-xl font-semibold text-dark-text">
                  {project.name}
                </h3>
                <span className={`text-sm font-medium ${getCriticalityColor(project.criticality_level)}`}>
                  {project.criticality_level.toUpperCase()}
                </span>
              </div>

              <div className="space-y-2 mb-4">
                <p className="text-sm text-dark-text-secondary">
                  <span className="font-medium">Type :</span>{' '}
                  {getProjectTypeLabel(project.project_type)}
                </p>
                {project.business_context && (
                  <p className="text-sm text-dark-text-secondary line-clamp-2">
                    {project.business_context}
                  </p>
                )}
              </div>

              <div className="flex gap-2 pt-4 border-t border-dark-border">
                <Button
                  size="sm"
                  variant="secondary"
                  onClick={(e) => {
                    e.stopPropagation()
                    navigate(`/projects/${project.id}`)
                  }}
                >
                  Voir
                </Button>
                <Button
                  size="sm"
                  variant="danger"
                  onClick={(e) => {
                    e.stopPropagation()
                    handleDelete(project.id, project.name)
                  }}
                >
                  Supprimer
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
