/**
 * Zones management tab
 */

import React, { useState, useEffect } from 'react';
import { zoneService } from '../services/zoneService';
import type { Zone, ZoneCreate, TrustLevel } from '../types/zone';
import { Modal } from './Modal';
import { Input } from './Input';
import { Select } from './Select';
import { Textarea } from './Textarea';
import { Button } from './Button';
import { Card } from './Card';

interface ZonesTabProps {
  architectureId: string;
}

export const ZonesTab: React.FC<ZonesTabProps> = ({ architectureId }) => {
  const [zones, setZones] = useState<Zone[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState<ZoneCreate>({
    architecture_id: architectureId,
    name: '',
    trust_level: 'medium' as TrustLevel,
    description: '',
  });
  const [formError, setFormError] = useState<string | null>(null);
  const [formLoading, setFormLoading] = useState(false);

  useEffect(() => {
    loadZones();
  }, [architectureId]);

  async function loadZones() {
    try {
      setLoading(true);
      setError(null);
      const data = await zoneService.getByArchitecture(architectureId);
      setZones(data.zones);
    } catch (err: any) {
      setError(err.message || 'Failed to load zones');
    } finally {
      setLoading(false);
    }
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    try {
      setFormLoading(true);
      setFormError(null);
      await zoneService.create(formData);
      setIsModalOpen(false);
      resetForm();
      loadZones();
    } catch (err: any) {
      setFormError(err.message || 'Failed to create zone');
    } finally {
      setFormLoading(false);
    }
  }

  async function handleDelete(id: string) {
    if (!confirm('Are you sure you want to delete this zone? All components within it will also be deleted.')) {
      return;
    }
    try {
      await zoneService.delete(id);
      loadZones();
    } catch (err: any) {
      alert(err.message || 'Failed to delete zone');
    }
  }

  function resetForm() {
    setFormData({
      architecture_id: architectureId,
      name: '',
      trust_level: 'medium' as TrustLevel,
      description: '',
    });
    setFormError(null);
  }

  function getTrustLevelColor(level: TrustLevel): string {
    const colors = {
      untrusted: 'bg-red-500',
      low: 'bg-orange-500',
      medium: 'bg-yellow-500',
      high: 'bg-green-500',
    };
    return colors[level] || 'bg-gray-500';
  }

  if (loading) {
    return <div className="text-gray-400">Loading zones...</div>;
  }

  if (error) {
    return <div className="text-red-400">{error}</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-white">Security Zones</h2>
        <Button onClick={() => setIsModalOpen(true)}>
          + Add Zone
        </Button>
      </div>

      {zones.length === 0 ? (
        <Card>
          <p className="text-gray-400 text-center py-8">
            No zones yet. Create your first security zone to organize components.
          </p>
        </Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {zones.map((zone) => (
            <Card key={zone.id}>
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center">
                  <div className={`w-3 h-3 rounded-full ${getTrustLevelColor(zone.trust_level)} mr-2`} />
                  <h3 className="text-xl font-semibold text-white">{zone.name}</h3>
                </div>
                <button
                  onClick={() => handleDelete(zone.id)}
                  className="text-red-400 hover:text-red-300"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
              <p className="text-sm text-gray-400 mb-2 capitalize">
                Trust Level: {zone.trust_level}
              </p>
              {zone.description && (
                <p className="text-sm text-gray-500">{zone.description}</p>
              )}
            </Card>
          ))}
        </div>
      )}

      <Modal isOpen={isModalOpen} onClose={() => { setIsModalOpen(false); resetForm(); }} title="Create Zone">
        <form onSubmit={handleSubmit} className="space-y-4">
          {formError && (
            <div className="bg-red-900 bg-opacity-50 border border-red-500 text-red-200 px-4 py-3 rounded">
              {formError}
            </div>
          )}

          <Input
            label="Zone Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            placeholder="e.g., DMZ, Internal Network, Public Zone"
            required
          />

          <Select
            label="Trust Level"
            value={formData.trust_level}
            onChange={(e) => setFormData({ ...formData, trust_level: e.target.value as TrustLevel })}
            options={[
              { value: 'untrusted', label: 'Untrusted' },
              { value: 'low', label: 'Low' },
              { value: 'medium', label: 'Medium' },
              { value: 'high', label: 'High' },
            ]}
            required
          />

          <Textarea
            label="Description"
            value={formData.description || ''}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            placeholder="Describe the purpose and security characteristics of this zone"
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
              {formLoading ? 'Creating...' : 'Create Zone'}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
