import React, { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { Button } from '../components/Button'
import { Card } from '../components/Card'
import { analysisService } from '../services/analysisService'
import { projectService } from '../services/projectService'
import type { Analysis, Finding } from '../types/analysis'
import type { Project } from '../types/project'

export function AnalysisView() {
  const { projectId } = useParams<{ projectId: string }>()
  const navigate = useNavigate()

  const [project, setProject] = useState<Project | null>(null)
  const [analysis, setAnalysis] = useState<Analysis | null>(null)
  const [findings, setFindings] = useState<Finding[]>([])
  const [loading, setLoading] = useState(true)
  const [running, setRunning] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (projectId) {
      loadData(projectId)
    }
  }, [projectId])

  async function loadData(id: string) {
    try {
      setLoading(true)
      setError(null)
      const p = await projectService.getById(id)
      setProject(p)

      try {
        const a = await analysisService.getLatest(id)
        const f = await analysisService.getFindings(id)
        setAnalysis(a)
        setFindings(f.findings)
      } catch (err: any) {
        if (err.status === 404) {
          setAnalysis(null)
          setFindings([])
        } else {
          throw err
        }
      }
    } catch (err: any) {
      setError(err.message || 'Erreur lors du chargement de l’analyse')
    } finally {
      setLoading(false)
    }
  }

  async function runAnalysis() {
    if (!projectId) return

    try {
      setRunning(true)
      setError(null)
      const a = await analysisService.run(projectId)
      const f = await analysisService.getFindings(projectId)
      setAnalysis(a)
      setFindings(f.findings)
    } catch (err: any) {
      setError(err.message || 'Erreur lors de l’analyse')
    } finally {
      setRunning(false)
    }
  }

  function severityClass(severity: Finding['severity']) {
    if (severity === 'critical') return 'text-severity-critical border-severity-critical/30 bg-severity-critical/10'
    if (severity === 'high') return 'text-severity-high border-severity-high/30 bg-severity-high/10'
    if (severity === 'medium') return 'text-severity-medium border-severity-medium/30 bg-severity-medium/10'
    return 'text-severity-low border-severity-low/30 bg-severity-low/10'
  }

  if (loading) {
    return <div className="container mx-auto px-4 py-8 text-dark-text-secondary">Chargement...</div>
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-6xl">
      <div className="mb-8 flex items-center justify-between gap-4">
        <div>
          <Button variant="secondary" size="sm" onClick={() => navigate(`/projects/${projectId}`)} className="mb-4">
            ← Retour au projet
          </Button>
          <h1 className="text-3xl font-bold text-dark-text">Analyse sécurité</h1>
          <p className="text-dark-text-secondary">{project?.name}</p>
        </div>
        <Button onClick={runAnalysis} disabled={running}>
          {running ? 'Analyse en cours...' : 'Lancer une nouvelle analyse'}
        </Button>
      </div>

      {error && (
        <div className="mb-6 bg-severity-critical/10 border border-severity-critical text-severity-critical px-4 py-3 rounded">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
        <Card><p className="text-dark-text-secondary text-sm">Total</p><p className="text-2xl font-bold text-dark-text">{analysis?.total_findings ?? 0}</p></Card>
        <Card><p className="text-dark-text-secondary text-sm">Critical</p><p className="text-2xl font-bold text-severity-critical">{analysis?.critical_findings ?? 0}</p></Card>
        <Card><p className="text-dark-text-secondary text-sm">High</p><p className="text-2xl font-bold text-severity-high">{analysis?.high_findings ?? 0}</p></Card>
        <Card><p className="text-dark-text-secondary text-sm">Medium</p><p className="text-2xl font-bold text-severity-medium">{analysis?.medium_findings ?? 0}</p></Card>
        <Card><p className="text-dark-text-secondary text-sm">Risk score</p><p className="text-2xl font-bold text-dark-text">{analysis?.global_risk_score ?? 0}</p></Card>
      </div>

      <Card>
        <h2 className="text-xl font-semibold text-dark-text mb-4">Findings</h2>
        {findings.length === 0 ? (
          <p className="text-dark-text-secondary">Aucun finding. Lance une analyse pour détecter les écarts de sécurité.</p>
        ) : (
          <div className="space-y-4">
            {findings.map((finding) => (
              <div key={finding.id} className={`rounded-lg border p-4 ${severityClass(finding.severity)}`}>
                <div className="flex items-center justify-between gap-3 mb-2">
                  <p className="font-semibold">{finding.title}</p>
                  <span className="uppercase text-xs tracking-wide">{finding.severity}</span>
                </div>
                <p className="text-sm mb-2">[{finding.rule_id}] {finding.rule_name}</p>
                <p className="text-sm mb-2">{finding.description}</p>
                <p className="text-sm opacity-90">Impact: {finding.impact}</p>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  )
}
