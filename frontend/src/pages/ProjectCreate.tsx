/**
 * Project Create Page
 */

import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { projectService } from '../services/projectService'
import { ProjectType, CriticalityLevel } from '../types/project'
import { Button } from '../components/Button'
import { Card } from '../components/Card'
import { Input } from '../components/Input'
import { Select } from '../components/Select'
import { Textarea } from '../components/Textarea'

export function ProjectCreate() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const [formData, setFormData] = useState({
    name: '',
    project_type: ProjectType.CLOUD,
    business_context: '',
    criticality_level: CriticalityLevel.MEDIUM,
  })

  const [errors, setErrors] = useState<Record<string, string>>({})

  function validateForm(): boolean {
    const newErrors: Record<string, string> = {}

    if (!formData.name.trim()) {
      newErrors.name = 'Le nom du projet est requis'
    } else if (formData.name.length > 200) {
      newErrors.name = 'Le nom ne peut pas dépasser 200 caractères'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()

    if (!validateForm()) {
      return
    }

    try {
      setLoading(true)
      setError(null)

      const project = await projectService.create({
        name: formData.name.trim(),
        project_type: formData.project_type,
        business_context: formData.business_context.trim() || undefined,
        criticality_level: formData.criticality_level,
      })

      navigate(`/projects/${project.id}`)
    } catch (err: any) {
      setError(err.message || 'Erreur lors de la création du projet')
      console.error('Error creating project:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-dark-text mb-2">
          Nouveau Projet
        </h1>
        <p className="text-dark-text-secondary">
          Créez un nouveau projet d'analyse d'architecture sécurisée
        </p>
      </div>

      <Card>
        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="bg-severity-critical/10 border border-severity-critical text-severity-critical px-4 py-3 rounded">
              {error}
            </div>
          )}

          <Input
            label="Nom du projet *"
            placeholder="Ex: Production API Platform"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            error={errors.name}
            required
          />

          <Select
            label="Type d'infrastructure *"
            value={formData.project_type}
            onChange={(e) =>
              setFormData({
                ...formData,
                project_type: e.target.value as ProjectType,
              })
            }
            options={[
              { value: ProjectType.CLOUD, label: 'Cloud' },
              { value: ProjectType.ON_PREMISE, label: 'On-Premise' },
              { value: ProjectType.HYBRID, label: 'Hybride' },
            ]}
            required
          />

          <Textarea
            label="Contexte métier"
            placeholder="Décrivez le contexte et les objectifs métier de ce projet..."
            value={formData.business_context}
            onChange={(e) =>
              setFormData({ ...formData, business_context: e.target.value })
            }
            rows={4}
          />

          <Select
            label="Niveau de criticité *"
            value={formData.criticality_level}
            onChange={(e) =>
              setFormData({
                ...formData,
                criticality_level: e.target.value as CriticalityLevel,
              })
            }
            options={[
              { value: CriticalityLevel.LOW, label: 'Faible' },
              { value: CriticalityLevel.MEDIUM, label: 'Moyen' },
              { value: CriticalityLevel.HIGH, label: 'Élevé' },
              { value: CriticalityLevel.CRITICAL, label: 'Critique' },
            ]}
            required
          />

          <div className="flex gap-4 pt-4">
            <Button type="submit" disabled={loading}>
              {loading ? 'Création...' : 'Créer le projet'}
            </Button>
            <Button
              type="button"
              variant="secondary"
              onClick={() => navigate('/projects')}
              disabled={loading}
            >
              Annuler
            </Button>
          </div>
        </form>
      </Card>
    </div>
  )
}
