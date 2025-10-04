import React from 'react'
import './Features.css'

function Features() {
  const features = [
    {
      icon: '📞',
      title: 'phone_a_friend',
      description: 'Ask OpenAI any question, with optional context for better answers.',
      items: [
        'Direct access to GPT-4',
        'Context-aware responses',
        'Configurable model & tokens',
      ],
    },
    {
      icon: '📋',
      title: 'review_plan',
      description: 'Get AI-powered feedback using the Master Review Framework with 5 progressive depth levels.',
      items: [
        'Quick to Expert review levels',
        '10-point structured analysis',
        'FMEA-style deep dives',
      ],
    },
    {
      icon: '❤️',
      title: 'health_check',
      description: 'Check server status and configuration with a simple health endpoint.',
      items: [
        'Server status monitoring',
        'Review count tracking',
        'Timestamp information',
      ],
    },
  ]

  return (
    <div className="features-container">
      <h2 className="features-title">Three Simple Tools</h2>

      <div className="features-grid">
        {features.map((feature, index) => (
          <div key={index} className="feature-card">
            <div className="feature-icon">{feature.icon}</div>
            <h3 className="feature-title">{feature.title}</h3>
            <p className="feature-description">{feature.description}</p>
            <ul className="feature-list">
              {feature.items.map((item, itemIndex) => (
                <li key={itemIndex}>{item}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Features
