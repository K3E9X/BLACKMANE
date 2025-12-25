/**
 * Architecture view page with tabs for Zones, Components, and Flows
 */

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { projectService } from '../services/projectService';
import { architectureService } from '../services/architectureService';
import type { Project } from '../types/project';
import type { Architecture } from '../types/architecture';
import { ZonesTab } from '../components/ZonesTab';
import { ComponentsTab } from '../components/ComponentsTab';
import { FlowsTab } from '../components/FlowsTab';

type Tab = 'zones' | 'components' | 'flows';

export const ArchitectureView: React.FC = () => {
  const { projectId } = useParams<{ projectId: string }>();
  const navigate = useNavigate();
  const [project, setProject] = useState<Project | null>(null);
  const [architecture, setArchitecture] = useState<Architecture | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<Tab>('zones');

  useEffect(() => {
    loadData();
  }, [projectId]);

  async function loadData() {
    if (!projectId) return;

    try {
      setLoading(true);
      setError(null);

      // Load project
      const projectData = await projectService.getById(projectId);
      setProject(projectData);

      // Try to load existing architecture
      try {
        const archData = await architectureService.getByProjectId(projectId);
        setArchitecture(archData);
      } catch (err: any) {
        // If no architecture exists, create one
        if (err.statusCode === 404) {
          const newArch = await architectureService.create({
            project_id: projectId,
            description: 'Architecture for ' + projectData.name,
          });
          setArchitecture(newArch);
        } else {
          throw err;
        }
      }
    } catch (err: any) {
      setError(err.message || 'Failed to load architecture');
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-gray-400">Loading architecture...</div>
      </div>
    );
  }

  if (error || !project || !architecture) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen">
        <div className="text-red-400 mb-4">{error || 'Architecture not found'}</div>
        <button
          onClick={() => navigate('/projects')}
          className="text-blue-400 hover:text-blue-300"
        >
          ← Back to Projects
        </button>
      </div>
    );
  }

  const tabs: { id: Tab; label: string }[] = [
    { id: 'zones', label: 'Zones' },
    { id: 'components', label: 'Components' },
    { id: 'flows', label: 'Data Flows' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() => navigate(`/projects/${projectId}`)}
            className="text-gray-400 hover:text-white mb-4 flex items-center"
          >
            ← Back to Project
          </button>
          <h1 className="text-4xl font-bold text-white mb-2">{project.name}</h1>
          <p className="text-gray-400">Architecture Modeling</p>
        </div>

        {/* Tabs */}
        <div className="flex space-x-1 mb-8 border-b border-gray-700">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-6 py-3 font-medium transition-colors ${
                activeTab === tab.id
                  ? 'text-white border-b-2 border-blue-500'
                  : 'text-gray-400 hover:text-gray-300'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab content */}
        <div>
          {activeTab === 'zones' && (
            <ZonesTab architectureId={architecture.id} />
          )}
          {activeTab === 'components' && (
            <ComponentsTab architectureId={architecture.id} />
          )}
          {activeTab === 'flows' && (
            <FlowsTab architectureId={architecture.id} />
          )}
        </div>
      </div>
    </div>
  );
};
