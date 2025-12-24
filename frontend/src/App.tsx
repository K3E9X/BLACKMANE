import React from 'react'

function App() {
  return (
    <div className="min-h-screen bg-dark-bg">
      <div className="container mx-auto px-4 py-8">
        <header className="mb-8">
          <h1 className="text-4xl font-bold text-dark-text mb-2">
            BLACKMANE
          </h1>
          <p className="text-dark-text-secondary">
            Security by Design Architecture Analysis
          </p>
        </header>

        <main className="bg-dark-surface border border-dark-border rounded-lg p-6">
          <p className="text-dark-text-secondary">
            Application en cours de développement...
          </p>
          <p className="text-dark-text-secondary mt-2">
            Consultez la documentation dans /docs pour plus d'informations.
          </p>
        </main>
      </div>
    </div>
  )
}

export default App
