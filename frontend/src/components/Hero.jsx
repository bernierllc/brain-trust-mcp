import React from 'react'
import './Hero.css'

function Hero() {
  return (
    <div className="hero-container">
      <h1 className="hero-title">Ask MCP</h1>

      <p className="hero-subtitle">
        Connect your IDE directly to OpenAI for intelligent question answering and
        structured plan reviews. No local server needed.
      </p>

      <p className="hero-tagline">
        Phone a friend when you need help
      </p>
    </div>
  )
}

export default Hero
