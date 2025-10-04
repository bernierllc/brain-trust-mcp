import React from 'react'
import './Footer.css'

function Footer() {
  return (
    <footer className="footer-container">
      <div className="footer-content">
        <div className="footer-top">
          <div className="footer-section">
            <h3 className="footer-title">brain-trust</h3>
            <p className="footer-text">
              Your trusted brain trust for getting AI help with questions and plan reviews.
            </p>
            <p className="footer-text" style={{ marginTop: '16px' }}>
              Built with FastMCP and OpenAI
            </p>
          </div>

          <div className="footer-section">
            <h3 className="footer-title">Resources</h3>
            <a href="https://github.com/bernierllc/brain-trust-mcp" target="_blank" rel="noopener noreferrer" className="footer-link">
              GitHub Repository
            </a>
            <a href="https://github.com/bernierllc/brain-trust-mcp/issues" target="_blank" rel="noopener noreferrer" className="footer-link">
              Issues & Support
            </a>
            <a href="https://gofastmcp.com" target="_blank" rel="noopener noreferrer" className="footer-link">
              FastMCP Documentation
            </a>
            <a href="https://modelcontextprotocol.io/" target="_blank" rel="noopener noreferrer" className="footer-link">
              MCP Specification
            </a>
          </div>

          <div className="footer-section">
            <h3 className="footer-title">Project</h3>
            <p className="footer-text">Version: 0.1.2</p>
            <p className="footer-text">Python 3.12+</p>
            <p className="footer-text">Test Coverage: 92%</p>
            <p className="footer-text">License: MIT</p>
          </div>

          <div className="footer-section">
            <h3 className="footer-title">Features</h3>
            <p className="footer-text">3 Simple Tools</p>
            <p className="footer-text">5 Review Levels</p>
            <p className="footer-text">Master Review Framework</p>
            <p className="footer-text">8+ IDE Support</p>
          </div>
        </div>

        <div className="footer-bottom">
          <p className="footer-copyright">
            MIT License - The code is <a href="https://github.com/bernierllc/brain-trust-mcp">Open source</a> and free to use
          </p>
          <p className="footer-copyright">
            Built by <a href="https://mbernier.com">Matt Bernier</a> in Colorado <br />
            Built with <a href="https://cursor.com/" target="_blank">Cursor</a>, <a href="https://bolt.new/?rid=bmy46m" target="_blank">Bolt.new</a>, <a href="https://gofastmcp.com/getting-started/welcome" target="_blank">FastMCP</a>, <a href="https://chat.openai.com" target="_blank">OpenAi</a>, and <a href="https://react.dev">React</a>
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
