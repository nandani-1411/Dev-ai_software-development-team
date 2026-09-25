import { useState, useEffect } from 'react'
import './App.css'

const API_URL = 'http://127.0.0.1:8000/api/v1/health'

function App() {
  const [health, setHealth] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch(API_URL)
      .then((res) => res.json())
      .then((data) => setHealth(data))
      .catch((err) => setError(err.message))
  }, [])

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
          ) : error ? (
            <p className="error">{error}</p>
          ) : (
            <p>Connecting to backend...</p>
          )}
        </section>
      </main>
    </div>
  )
}

export default App
