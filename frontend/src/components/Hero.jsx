import React from 'react'
import './Hero.css'

function Hero() {
  return (
    <div className="hero-container">
      <div className="badge-container">
        <span className="badge">v0.1.2</span>
        <span className="badge">92% Coverage</span>
        <span className="badge">18 Tests</span>
        <span className="badge">Python 3.12+</span>
      </div>

      <h1 className="hero-title">brain-trust</h1>

      <p className="hero-subtitle">
        Your trusted brain trust for getting AI help with questions and plan reviews.
        A simple, powerful MCP server that connects your IDE to OpenAI.
      </p>

      <p className="hero-tagline">
        Phone a friend when you need help
      </p>
    </div>
  )
}

export default Hero
