/**
 * Input Component
 */

import React from 'react'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
}

export function Input({ label, error, className = '', ...props }: InputProps) {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-sm font-medium text-dark-text mb-2">
          {label}
        </label>
      )}
      <input
        className={`
          w-full px-4 py-2
          bg-dark-bg border border-dark-border rounded
          text-dark-text placeholder-dark-text-secondary
          focus:outline-none focus:ring-2 focus:ring-accent-primary focus:border-transparent
          ${error ? 'border-severity-critical' : ''}
          ${className}
        `}
        {...props}
      />
      {error && (
        <p className="mt-1 text-sm text-severity-critical">{error}</p>
      )}
    </div>
  )
}
