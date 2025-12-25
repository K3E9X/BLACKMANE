/**
 * Components management tab
 */

import React, { useState, useEffect } from 'react';
import { componentService } from '../services/componentService';
import { zoneService } from '../services/zoneService';
import type { Component, ComponentCreate, ComponentType } from '../types/component';
import type { Zone } from '../types/zone';
import { Modal } from './Modal';
import { Input } from './Input';
import { Select } from './Select';
import { Textarea } from './Textarea';
import { Checkbox } from './Checkbox';
import { Button } from './Button';
import { Card } from './Card';

interface ComponentsTabProps {
  architectureId: string;
}

export const ComponentsTab: React.FC<ComponentsTabProps> = ({ architectureId }) => {
  const [components, setComponents] = useState<Component[]>([]);
  const [zones, setZones] = useState<Zone[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState<ComponentCreate>({
    architecture_id: architectureId,
    zone_id: '',
    name: '',
    component_type: 'server' as ComponentType,
    has_admin_interface: false,
    requires_mfa: false,
    has_logging: false,
    encryption_at_rest: false,
    encryption_in_transit: false,
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
      const [componentsData, zonesData] = await Promise.all([
        componentService.getByArchitecture(architectureId),
        zoneService.getByArchitecture(architectureId),
      ]);
      setComponents(componentsData.components);
      setZones(zonesData.zones);
    } catch (err: any) {
      setError(err.message || 'Failed to load components');
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    try {
      setFormLoading(true);
      setFormError(null);
      await componentService.create(formData);
      setIsModalOpen(false);
      resetForm();
      loadData();
    } catch (err: any) {
      setFormError(err.message || 'Failed to create component');
    } finally {
      setFormLoading(false);
    }
  }

  async function handleDelete(id: string) {
    if (!confirm('Are you sure you want to delete this component? All flows involving it will also be deleted.')) {
      return;
    }
    try {
      await componentService.delete(id);
      loadData();
    } catch (err: any) {
      alert(err.message || 'Failed to delete component');
    }
  }

  function resetForm() {
    setFormData({
      architecture_id: architectureId,
      zone_id: zones.length > 0 ? zones[0].id : '',
      name: '',
      component_type: 'server' as ComponentType,
      has_admin_interface: false,
      requires_mfa: false,
      has_logging: false,
      encryption_at_rest: false,
      encryption_in_transit: false,
      description: '',
    });
    setFormError(null);
  }

  function getComponentsByZone(zoneId: string): Component[] {
    return components.filter((c) => c.zone_id === zoneId);
  }

  function getComponentTypeLabel(type: ComponentType): string {
    const labels: Record<ComponentType, string> = {
      firewall: '🛡️ Firewall',
      load_balancer: '⚖️ Load Balancer',
      server: '🖥️ Server',
      database: '🗄️ Database',
      iam: '🔐 IAM',
      bastion: '🚪 Bastion',
      api_gateway: '🌐 API Gateway',
      vpn: '🔒 VPN',
      other: '📦 Other',
    };
    return labels[type] || type;
  }

  if (loading) {
    return <div className="text-gray-400">Loading components...</div>;
  }

  if (error) {
    return <div className="text-red-400">{error}</div>;
  }

  if (zones.length === 0) {
    return (
      <Card>
        <p className="text-gray-400 text-center py-8">
          Please create at least one zone before adding components.
        </p>
      </Card>
    );
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-white">Components</h2>
        <Button onClick={() => { setIsModalOpen(true); resetForm(); }}>
          + Add Component
        </Button>
      </div>

      {zones.map((zone) => {
        const zoneComponents = getComponentsByZone(zone.id);
        return (
          <div key={zone.id} className="mb-8">
            <h3 className="text-lg font-semibold text-white mb-4">
              {zone.name} ({zoneComponents.length} components)
            </h3>
            {zoneComponents.length === 0 ? (
              <Card>
                <p className="text-gray-500 text-center py-4 text-sm">
                  No components in this zone yet
                </p>
              </Card>
            ) : (
              <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                {zoneComponents.map((component) => (
                  <Card key={component.id}>
                    <div className="flex items-start justify-between mb-3">
                      <h4 className="text-lg font-semibold text-white">
                        {component.name}
                      </h4>
                      <button
                        onClick={() => handleDelete(component.id)}
                        className="text-red-400 hover:text-red-300"
                      >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                    <p className="text-sm text-gray-400 mb-3">
                      {getComponentTypeLabel(component.component_type)}
                    </p>
                    <div className="flex flex-wrap gap-2 text-xs">
                      {component.has_admin_interface && <span className="bg-blue-900 text-blue-200 px-2 py-1 rounded">Admin UI</span>}
                      {component.requires_mfa && <span className="bg-green-900 text-green-200 px-2 py-1 rounded">MFA</span>}
                      {component.has_logging && <span className="bg-purple-900 text-purple-200 px-2 py-1 rounded">Logging</span>}
                      {component.encryption_at_rest && <span className="bg-yellow-900 text-yellow-200 px-2 py-1 rounded">Encrypted (rest)</span>}
                      {component.encryption_in_transit && <span className="bg-yellow-900 text-yellow-200 px-2 py-1 rounded">Encrypted (transit)</span>}
                    </div>
                    {component.description && (
                      <p className="text-sm text-gray-500 mt-2">{component.description}</p>
                    )}
                  </Card>
                ))}
              </div>
            )}
          </div>
        );
      })}

      <Modal isOpen={isModalOpen} onClose={() => { setIsModalOpen(false); resetForm(); }} title="Create Component">
        <form onSubmit={handleSubmit} className="space-y-4">
          {formError && (
            <div className="bg-red-900 bg-opacity-50 border border-red-500 text-red-200 px-4 py-3 rounded">
              {formError}
            </div>
          )}

          <Input
            label="Component Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            placeholder="e.g., Web Application Server"
            required
          />

          <Select
            label="Zone"
            value={formData.zone_id}
            onChange={(e) => setFormData({ ...formData, zone_id: e.target.value })}
            options={zones.map((z) => ({ value: z.id, label: z.name }))}
            required
          />

          <Select
            label="Component Type"
            value={formData.component_type}
            onChange={(e) => setFormData({ ...formData, component_type: e.target.value as ComponentType })}
            options={[
              { value: 'server', label: 'Server' },
              { value: 'database', label: 'Database' },
              { value: 'firewall', label: 'Firewall' },
              { value: 'load_balancer', label: 'Load Balancer' },
              { value: 'api_gateway', label: 'API Gateway' },
              { value: 'iam', label: 'IAM' },
              { value: 'bastion', label: 'Bastion' },
              { value: 'vpn', label: 'VPN' },
              { value: 'other', label: 'Other' },
            ]}
            required
          />

          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-300">Security Features</label>
            <Checkbox
              label="Has Admin Interface"
              checked={formData.has_admin_interface || false}
              onChange={(checked) => setFormData({ ...formData, has_admin_interface: checked })}
            />
            <Checkbox
              label="Requires MFA"
              checked={formData.requires_mfa || false}
              onChange={(checked) => setFormData({ ...formData, requires_mfa: checked })}
            />
            <Checkbox
              label="Has Logging"
              checked={formData.has_logging || false}
              onChange={(checked) => setFormData({ ...formData, has_logging: checked })}
            />
            <Checkbox
              label="Encryption at Rest"
              checked={formData.encryption_at_rest || false}
              onChange={(checked) => setFormData({ ...formData, encryption_at_rest: checked })}
            />
            <Checkbox
              label="Encryption in Transit"
              checked={formData.encryption_in_transit || false}
              onChange={(checked) => setFormData({ ...formData, encryption_in_transit: checked })}
            />
          </div>

          <Textarea
            label="Description"
            value={formData.description || ''}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            placeholder="Describe the component's purpose and configuration"
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
              {formLoading ? 'Creating...' : 'Create Component'}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
