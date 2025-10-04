import React from 'react'
import './WhyBrainTrust.css'

function WhyBrainTrust() {
  return (
    <div className="why-container">
      <h2 className="why-title">Why brain-trust?</h2>

      <div className="benefit-grid">
        <div className="benefit-card">
          <h3 className="benefit-title">Simple</h3>
          <div className="benefit-items">
            <div className="benefit-item">
              <strong>Only 3 tools</strong>
              <p>No complex setup or overwhelming options. Just three focused tools that solve real problems.</p>
            </div>
            <div className="benefit-item">
              <strong>Clear documentation</strong>
              <p>Comprehensive guides and examples to get you started in minutes.</p>
            </div>
            <div className="benefit-item">
              <strong>Easy integration</strong>
              <p>One-click install buttons and simple JSON configuration.</p>
            </div>
          </div>
        </div>

        <div className="benefit-card">
          <h3 className="benefit-title">Powerful</h3>
          <div className="benefit-items">
            <div className="benefit-item">
              <strong>Full GPT-4 access</strong>
              <p>Direct connection to OpenAI for intelligent responses.</p>
            </div>
            <div className="benefit-item">
              <strong>Master Review Framework</strong>
              <p>10-point structured analysis with 5 progressive depth levels.</p>
            </div>
            <div className="benefit-item">
              <strong>Context-aware</strong>
              <p>Provide context for more relevant and accurate answers.</p>
            </div>
          </div>
        </div>

        <div className="benefit-card">
          <h3 className="benefit-title">Reliable</h3>
          <div className="benefit-items">
            <div className="benefit-item">
              <strong>92% test coverage</strong>
              <p>Comprehensive test suite ensures reliability.</p>
            </div>
            <div className="benefit-item">
              <strong>Production-ready</strong>
              <p>Docker support, comprehensive logging, and security best practices.</p>
            </div>
            <div className="benefit-item">
              <strong>Secure by design</strong>
              <p>Per-request authentication, no stored API keys, non-root Docker user.</p>
            </div>
          </div>
        </div>
      </div>

      <div className="stats-container">
        <div className="stat-card">
          <div className="stat-number">3</div>
          <div className="stat-label">Simple Tools</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">92%</div>
          <div className="stat-label">Test Coverage</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">5</div>
          <div className="stat-label">Review Levels</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">8+</div>
          <div className="stat-label">IDE Support</div>
        </div>
      </div>
    </div>
  )
}

export default WhyBrainTrust
