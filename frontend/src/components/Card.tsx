/**
 * Card Component
 */

import React from 'react'

interface CardProps {
  children: React.ReactNode
  className?: string
  onClick?: () => void
}

export function Card({ children, className = '', onClick }: CardProps) {
  const baseStyles = 'bg-dark-surface border border-dark-border rounded-lg p-6'
  const interactiveStyles = onClick ? 'cursor-pointer hover:border-accent-primary transition-colors' : ''

  return (
    <div
      className={`${baseStyles} ${interactiveStyles} ${className}`}
      onClick={onClick}
    >
      {children}
    </div>
  )
}
