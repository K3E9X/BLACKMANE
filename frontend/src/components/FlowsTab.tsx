/**
 * Flows management tab
 */

import React, { useState, useEffect } from 'react';
import { flowService } from '../services/flowService';
import { componentService } from '../services/componentService';
import type { Flow, FlowCreate, FlowProtocol } from '../types/flow';
import type { Component } from '../types/component';
import { Modal } from './Modal';
import { Input } from './Input';
import { Select } from './Select';
import { Textarea } from './Textarea';
import { Checkbox } from './Checkbox';
import { Button } from './Button';
import { Card } from './Card';

interface FlowsTabProps {
  architectureId: string;
}

export const FlowsTab: React.FC<FlowsTabProps> = ({ architectureId }) => {
  const [flows, setFlows] = useState<Flow[]>([]);
  const [components, setComponents] = useState<Component[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState<FlowCreate>({
    architecture_id: architectureId,
    source_component_id: '',
    target_component_id: '',
    protocol: 'https' as FlowProtocol,
    port: 443,
    is_authenticated: false,
    is_encrypted: false,
    description: '',
  });
  const [formError, setFormError] = useState<string | null>(null);
  const [formLoading, setFormLoading] = useState(false);

  useEffect(() => {
    loadData();
  }, [architectureId]);

  async function loadData() {
    try {
      setLoading(true);
      setError(null);
      const [flowsData, componentsData] = await Promise.all([
        flowService.getByArchitecture(architectureId),
        componentService.getByArchitecture(architectureId),
      ]);
      setFlows(flowsData.flows);
      setComponents(componentsData.components);
    } catch (err: any) {
      setError(err.message || 'Failed to load flows');
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (formData.source_component_id === formData.target_component_id) {
      setFormError('Source and target components must be different');
      return;
    }

    try {
      setFormLoading(true);
      setFormError(null);
      await flowService.create(formData);
      setIsModalOpen(false);
      resetForm();
      loadData();
    } catch (err: any) {
      setFormError(err.message || 'Failed to create flow');
    } finally {
      setFormLoading(false);
    }
  }

  async function handleDelete(id: string) {
    if (!confirm('Are you sure you want to delete this flow?')) {
      return;
    }
    try {
      await flowService.delete(id);
      loadData();
    } catch (err: any) {
      alert(err.message || 'Failed to delete flow');
    }
  }

  function resetForm() {
    setFormData({
      architecture_id: architectureId,
      source_component_id: '',
      target_component_id: '',
      protocol: 'https' as FlowProtocol,
      port: 443,
      is_authenticated: false,
      is_encrypted: false,
      description: '',
    });
    setFormError(null);
  }

  function getComponentName(id: string): string {
    const component = components.find((c) => c.id === id);
    return component ? component.name : 'Unknown';
  }

  function getProtocolColor(protocol: FlowProtocol): string {
    const colors: Record<FlowProtocol, string> = {
      https: 'bg-green-900 text-green-200',
      http: 'bg-orange-900 text-orange-200',
      ssh: 'bg-blue-900 text-blue-200',
      rdp: 'bg-purple-900 text-purple-200',
      sql: 'bg-pink-900 text-pink-200',
      ldap: 'bg-indigo-900 text-indigo-200',
      dns: 'bg-cyan-900 text-cyan-200',
      smtp: 'bg-yellow-900 text-yellow-200',
      other: 'bg-gray-700 text-gray-300',
    };
    return colors[protocol] || colors.other;
  }

  if (loading) {
    return <div className="text-gray-400">Loading flows...</div>;
  }

  if (error) {
    return <div className="text-red-400">{error}</div>;
  }

  if (components.length < 2) {
    return (
      <Card>
        <p className="text-gray-400 text-center py-8">
          Please create at least two components before adding data flows.
        </p>
      </Card>
    );
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-white">Data Flows</h2>
        <Button onClick={() => { setIsModalOpen(true); resetForm(); }}>
          + Add Flow
        </Button>
      </div>

      {flows.length === 0 ? (
        <Card>
          <p className="text-gray-400 text-center py-8">
            No flows yet. Create data flows to document communication between components.
          </p>
        </Card>
      ) : (
        <div className="grid gap-4">
          {flows.map((flow) => (
            <Card key={flow.id}>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center mb-3">
                    <div className="bg-blue-900 text-blue-200 px-3 py-1 rounded text-sm font-medium">
                      {getComponentName(flow.source_component_id)}
                    </div>
                    <svg className="w-6 h-6 text-gray-400 mx-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                    </svg>
                    <div className="bg-purple-900 text-purple-200 px-3 py-1 rounded text-sm font-medium">
                      {getComponentName(flow.target_component_id)}
                    </div>
                  </div>

                  <div className="flex flex-wrap gap-2 text-xs mb-2">
                    <span className={`px-2 py-1 rounded ${getProtocolColor(flow.protocol)}`}>
                      {flow.protocol.toUpperCase()}
                      {flow.port && `:${flow.port}`}
                    </span>
                    {flow.is_authenticated && (
                      <span className="bg-green-900 text-green-200 px-2 py-1 rounded">
                        Authenticated
                      </span>
                    )}
                    {flow.is_encrypted && (
                      <span className="bg-green-900 text-green-200 px-2 py-1 rounded">
                        Encrypted
                      </span>
                    )}
                    {!flow.is_encrypted && (
                      <span className="bg-red-900 text-red-200 px-2 py-1 rounded">
                        ⚠️ Not Encrypted
                      </span>
                    )}
                  </div>

                  {flow.description && (
                    <p className="text-sm text-gray-500">{flow.description}</p>
                  )}
                </div>

                <button
                  onClick={() => handleDelete(flow.id)}
                  className="text-red-400 hover:text-red-300 ml-4"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </Card>
          ))}
        </div>
      )}

      <Modal isOpen={isModalOpen} onClose={() => { setIsModalOpen(false); resetForm(); }} title="Create Data Flow">
        <form onSubmit={handleSubmit} className="space-y-4">
          {formError && (
            <div className="bg-red-900 bg-opacity-50 border border-red-500 text-red-200 px-4 py-3 rounded">
              {formError}
            </div>
          )}

          <Select
            label="Source Component"
            value={formData.source_component_id}
            onChange={(e) => setFormData({ ...formData, source_component_id: e.target.value })}
            options={[
              { value: '', label: 'Select source component...' },
              ...components.map((c) => ({ value: c.id, label: c.name }))
            ]}
            required
          />

          <Select
            label="Target Component"
            value={formData.target_component_id}
            onChange={(e) => setFormData({ ...formData, target_component_id: e.target.value })}
            options={[
              { value: '', label: 'Select target component...' },
              ...components.map((c) => ({ value: c.id, label: c.name }))
            ]}
            required
          />

          <Select
            label="Protocol"
            value={formData.protocol}
            onChange={(e) => setFormData({ ...formData, protocol: e.target.value as FlowProtocol })}
            options={[
              { value: 'https', label: 'HTTPS' },
              { value: 'http', label: 'HTTP' },
              { value: 'ssh', label: 'SSH' },
              { value: 'rdp', label: 'RDP' },
              { value: 'sql', label: 'SQL' },
              { value: 'ldap', label: 'LDAP' },
              { value: 'dns', label: 'DNS' },
              { value: 'smtp', label: 'SMTP' },
              { value: 'other', label: 'Other' },
            ]}
            required
          />

          <Input
            label="Port"
            type="number"
            value={formData.port?.toString() || ''}
            onChange={(e) => setFormData({ ...formData, port: e.target.value ? parseInt(e.target.value) : undefined })}
            placeholder="e.g., 443, 80, 22"
          />

          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-300">Security Features</label>
            <Checkbox
              label="Authenticated"
              checked={formData.is_authenticated || false}
              onChange={(checked) => setFormData({ ...formData, is_authenticated: checked })}
            />
            <Checkbox
              label="Encrypted"
              checked={formData.is_encrypted || false}
              onChange={(checked) => setFormData({ ...formData, is_encrypted: checked })}
            />
          </div>

          <Textarea
            label="Description"
            value={formData.description || ''}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            placeholder="Describe the purpose and characteristics of this data flow"
            rows={3}
          />

          <div className="flex justify-end space-x-3 pt-4">
            <Button
              type="button"
              variant="secondary"
              onClick={() => { setIsModalOpen(false); resetForm(); }}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={formLoading}>
              {formLoading ? 'Creating...' : 'Create Flow'}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
