import { useState, useEffect } from 'react'
import './App.css'

const HEALTH_URL = '/api/v1/health'
const PLAN_URL = '/api/v1/plan'

function App() {
  const [health, setHealth] = useState(null)
  const [healthError, setHealthError] = useState(null)
  const [projectRequest, setProjectRequest] = useState('')
  const [plan, setPlan] = useState(null)
  const [planError, setPlanError] = useState(null)
  const [isPlanning, setIsPlanning] = useState(false)

  useEffect(() => {
    fetch(HEALTH_URL)
      .then((res) => res.json())
      .then((data) => setHealth(data))
      .catch((err) => setHealthError(err.message))
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsPlanning(true)
    setPlanError(null)
    setPlan(null)

    try {
      const response = await fetch(PLAN_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ project_request: projectRequest }),
      })
      const data = await response.json()
      if (response.ok) {
        setPlan(data)
      } else {
        setPlanError(data.detail || 'Failed to generate plan')
      }
    } catch (err) {
      setPlanError(err.message)
    } finally {
      setIsPlanning(false)
    }
  }

  return (
    <div className="app">
      <header>
        <h1>DevAI</h1>
        <p>Autonomous Software Development Team</p>
      </header>
      <main>
        <section className="status">
          <h2>Backend Status</h2>
          {health ? (
            <pre>{JSON.stringify(health, null, 2)}</pre>
          ) : healthError ? (
            <p className="error">{healthError}</p>
          ) : (
            <p>Connecting to backend...</p>
          )}
        </section>

        <section className="project-form">
          <h2>Create Project Plan</h2>
          <form onSubmit={handleSubmit}>
            <textarea
              value={projectRequest}
              onChange={(e) => setProjectRequest(e.target.value)}
              placeholder="Describe the software you want to build..."
              rows={6}
              required
            />
            <button type="submit" disabled={isPlanning}>
              {isPlanning ? 'Generating Full Project...' : 'Generate Full Project'}
            </button>
          </form>
        </section>

        {plan && (
          <>
            <section className="plan-result">
              <h2>Project ID</h2>
              <p>{plan.project_id}</p>
            </section>

            <section className="plan-result">
              <h2>Development Plan</h2>
              <div className="plan-content">
                <pre>{plan.development_plan}</pre>
              </div>
            </section>

            {plan.architecture && (
              <section className="plan-result">
                <h2>System Architecture</h2>
                <div className="plan-content">
                  <pre>{plan.architecture}</pre>
                </div>
              </section>
            )}

            {plan.files_changed && plan.files_changed.length > 0 && (
              <section className="plan-result">
                <h2>Files Changed</h2>
                <ul>
                  {plan.files_changed.map((file, index) => (
                    <li key={index}>{file}</li>
                  ))}
                </ul>
              </section>
            )}

            <section className="plan-result">
              <h2>Status</h2>
              <p>Frontend: {plan.frontend_status || 'N/A'}</p>
              <p>Backend: {plan.backend_status || 'N/A'}</p>
              <p>Overall: {plan.project_status}</p>
            </section>
          </>
        )}

        {planError && (
          <section className="error">
            <h2>Error</h2>
            <p>{planError}</p>
          </section>
        )}
      </main>
    </div>
  )
}

export default App
