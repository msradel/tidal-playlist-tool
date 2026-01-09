/**
 * AudioArchitect - React Main Component
 * Gold/Black Theme
 */

import React, { useState, useEffect } from 'react';
import './App.css';
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

function App() {
  const [backendStatus, setBackendStatus] = useState('checking...');
  const [appInfo, setAppInfo] = useState(null);

  useEffect(() => {
    checkBackend();
  }, []);

  const checkBackend = async () => {
    try {
      const response = await axios.get(`${API_URL}/`);
      setAppInfo(response.data);
      setBackendStatus('online');
    } catch (error) {
      setBackendStatus('offline');
      console.error('Backend connection failed:', error);
    }
  };

  return (
    <div className="App">
      {/* Header */}
      <header className="App-header">
        <div className="logo">
          <span className="logo-icon">🎵</span>
          <h1>AudioArchitect</h1>
        </div>
        <div className={`status ${backendStatus}`}>
          <span className="status-dot"></span>
          Backend: {backendStatus}
        </div>
      </header>

      {/* Main Content */}
      <main className="App-main">
        <div className="welcome-card">
          <h2>Build Your Perfect Music Library</h2>
          {appInfo && (
            <p className="version">Version {appInfo.version}</p>
          )}
          
          {backendStatus === 'online' ? (
            <div className="feature-grid">
              <FeatureCard
                icon="🎲"
                title="Randomize"
                description="Fix broken shuffle algorithms"
                status="coming-soon"
              />
              <FeatureCard
                icon="🔄"
                title="Transfer"
                description="Copy playlists across platforms"
                status="coming-soon"
              />
              <FeatureCard
                icon="🔗"
                title="Sync"
                description="Keep playlists in sync"
                status="coming-soon"
              />
              <FeatureCard
                icon="🧹"
                title="Deduplicate"
                description="Remove duplicate tracks"
                status="coming-soon"
              />
            </div>
          ) : (
            <div className="error-message">
              <p>⚠️ Backend server not running</p>
              <p className="help-text">
                Start the backend: <code>python -m backend.run</code>
              </p>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="App-footer">
        <p>Made with ❤️ by msradel | Open Source | MIT License</p>
      </footer>
    </div>
  );
}

function FeatureCard({ icon, title, description, status }) {
  return (
    <div className={`feature-card ${status}`}>
      <div className="feature-icon">{icon}</div>
      <h3>{title}</h3>
      <p>{description}</p>
      {status === 'coming-soon' && (
        <span className="badge">Coming Soon</span>
      )}
    </div>
  );
}

export default App;
