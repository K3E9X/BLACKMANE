import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { ProjectList } from './pages/ProjectList'
import { ProjectCreate } from './pages/ProjectCreate'
import { ProjectDetail } from './pages/ProjectDetail'

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-dark-bg">
        {/* Header */}
        <header className="border-b border-dark-border bg-dark-surface">
          <div className="container mx-auto px-4 py-4">
            <h1 className="text-2xl font-bold text-dark-text">
              BLACKMANE
            </h1>
            <p className="text-sm text-dark-text-secondary">
              Security by Design Architecture Analysis
            </p>
          </div>
        </header>

        {/* Main Content */}
        <main>
          <Routes>
            <Route path="/" element={<Navigate to="/projects" replace />} />
            <Route path="/projects" element={<ProjectList />} />
            <Route path="/projects/new" element={<ProjectCreate />} />
            <Route path="/projects/:id" element={<ProjectDetail />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
