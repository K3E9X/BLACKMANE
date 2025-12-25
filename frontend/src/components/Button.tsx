/**
 * Button Component
 */

import React from 'react'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  children: React.ReactNode
}

export function Button({
  variant = 'primary',
  size = 'md',
  children,
  className = '',
  ...props
}: ButtonProps) {
  const baseStyles = 'font-medium rounded focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-dark-bg transition-colors'

  const variantStyles = {
    primary: 'bg-accent-primary hover:bg-accent-hover text-white focus:ring-accent-primary',
    secondary: 'bg-dark-surface hover:bg-dark-border text-dark-text border border-dark-border focus:ring-dark-border',
    danger: 'bg-severity-critical hover:bg-red-600 text-white focus:ring-severity-critical',
  }

  const sizeStyles = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  }

  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${className} disabled:opacity-50 disabled:cursor-not-allowed`}
      {...props}
    >
      {children}
    </button>
  )
}
