/**
 * Select Component
 */

import React from 'react'

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string
  error?: string
  options: { value: string; label: string }[]
}

export function Select({ label, error, options, className = '', ...props }: SelectProps) {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-dark-text mb-2">
          {label}
        </label>
      )}
      <select
        className={`
          w-full px-4 py-2
          bg-dark-bg border border-dark-border rounded
          text-dark-text
          focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-transparent
          ${error ? 'border-severity-critical' : ''}
          ${className}
        `}
        {...props}
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {error && (
        <p className="mt-1 text-sm text-severity-critical">{error}</p>
      )}
    </div>
  )
}
