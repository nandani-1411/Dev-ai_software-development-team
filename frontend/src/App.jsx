import { useState, useEffect } from 'react'
import './App.css'

const HEALTH_URL = '/api/v1/health'
const PLAN_URL = '/api/v1/plan'
const APPROVAL_URL = '/api/v1/approve'
const STREAM_URL = '/api/v1/stream'

function App() {
  const [health, setHealth] = useState(null)
  const [healthError, setHealthError] = useState(null)
  const [projectRequest, setProjectRequest] = useState('')
  const [plan, setPlan] = useState(null)
  const [planError, setPlanError] = useState(null)
  const [isPlanning, setIsPlanning] = useState(false)
  const [events, setEvents] = useState([])

  useEffect(() => {
    fetch(HEALTH_URL)
      .then((res) => res.json())
      .then((data) => setHealth(data))
      .catch((err) => setHealthError(err.message))
  }, [])

  useEffect(() => {
    if (isPlanning) {
      setEvents([])
      const eventSource = new EventSource(STREAM_URL)
      eventSource.onmessage = (e) => {
        setEvents((prev) => [...prev, e.data])
      }
      eventSource.onerror = () => {
        eventSource.close()
      }
      return () => eventSource.close()
    }
  }, [isPlanning])

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

        {events.length > 0 && (
          <section className="plan-result">
            <h2>Agent Activity</h2>
            <ul>
              {events.map((event, index) => (
                <li key={index}>{event}</li>
              ))}
            </ul>
          </section>
        )}

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

            {plan.test_results && (
              <section className="plan-result">
                <h2>Test Results</h2>
                <p>Total: {plan.test_results.total || 0}</p>
                <p>Passed: {plan.test_results.passed || 0}</p>
                <p>Failed: {plan.test_results.failed || 0}</p>
              </section>
            )}

            {plan.review_result && (
              <section className="plan-result">
                <h2>Code Review</h2>
                <p>Status: {plan.review_result.status || 'N/A'}</p>
              </section>
            )}

            {plan.documentation && (
              <section className="plan-result">
                <h2>Documentation</h2>
                <p>{plan.documentation}</p>
              </section>
            )}

            {plan.project_status === 'git_initialized' && (
              <section className="plan-result">
                <h2>Git Status</h2>
                <p>Repository initialized with initial commit</p>
              </section>
            )}
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
