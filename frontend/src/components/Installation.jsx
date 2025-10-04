import React, { useState } from 'react'
import { installConfigs } from '../data/installConfigs'
import CopyButton from './CopyButton'
import './Installation.css'

function Installation() {
  const [selectedPlatform, setSelectedPlatform] = useState('cursor')
  const platforms = Object.keys(installConfigs).sort((a, b) =>
    installConfigs[a].name.localeCompare(installConfigs[b].name)
  )
  const config = installConfigs[selectedPlatform]

  return (
    <div className="install-container">
      <h2 className="install-title">Get Started</h2>
      <p className="install-subtitle">
        Choose your IDE or AI agent to connect to Ask MCP in under 2 minutes
      </p>

      <div className="platform-tabs">
        {platforms.map((platform) => (
          <button
            key={platform}
            className={`platform-tab ${selectedPlatform === platform ? 'active' : ''}`}
            onClick={() => setSelectedPlatform(platform)}
          >
            {installConfigs[platform].name}
          </button>
        ))}
      </div>

      <div className="config-container">
        {config.installButton && (
          <div className="config-section">
            <h3 className="config-title">Quick Install</h3>
            <a href={config.installButton} target="_blank" rel="noopener noreferrer" className="install-button">
              Install in {config.name}
            </a>
          </div>
        )}

        <div className="config-section">
          <h3 className="config-title">Configuration</h3>
          <p className="config-description">{config.description}</p>
        </div>

        {config.steps.map((step, index) => (
          <div key={index} className="config-section">
            <h3 className="config-title">
              Step {index + 1}: {step.title}
            </h3>
            {step.description && (
              <p className="config-description">{step.description}</p>
            )}
            {step.code && (
              <div className="code-block">
                <CopyButton text={step.code} />
                <pre><code>{step.code}</code></pre>
              </div>
            )}
          </div>
        ))}

        <div className="config-section">
          <h3 className="config-title">Verify Connection</h3>
          <p className="config-description">
            {config.verification ||
             'Try calling one of the tools from your IDE to verify the connection.'}
          </p>
        </div>
      </div>
    </div>
  )
}

export default Installation
