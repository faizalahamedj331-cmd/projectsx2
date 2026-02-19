import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [message, setMessage] = useState('')

  const fetchMessage = () => {
    axios.get('http://127.0.0.1:8000/api/test/')
      .then(response => {
        setMessage(response.data.message)
      })
      .catch(error => {
        console.error('Error fetching data:', error)
        setMessage('Error fetching data. Ensure Django server is running on port 8000.')
      })
  }

  return (
    <div className="App">
      <h1>React + Django Integration</h1>
      <div className="card">
        <button onClick={fetchMessage}>
          Fetch Message from Django
        </button>
        {message && <p style={{ marginTop: '20px', fontWeight: 'bold' }}>{message}</p>}
      </div>
      <p className="read-the-docs">
        Ensure both Django (port 8000) and Vite (port 5173) servers are running.
      </p>
    </div>
  )
}

export default App
