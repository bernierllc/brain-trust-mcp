import React, { useState } from 'react'
import './InteractiveDemo.css'

function InteractiveDemo() {
  const [activeTab, setActiveTab] = useState('phone')
  const [apiKey, setApiKey] = useState('')
  const [question, setQuestion] = useState('')
  const [context, setContext] = useState('')
  const [planContent, setPlanContent] = useState('')
  const [reviewLevel, setReviewLevel] = useState('standard')
  const [response, setResponse] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handlePhoneAFriend = async () => {
    if (!apiKey || !question) return

    setLoading(true)
    setError(null)
    setResponse(null)

    try {
      const res = await fetch('/api/demo/phone-a-friend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          api_key: apiKey,
          question,
          context: context || undefined,
        }),
      })

      if (!res.ok) {
        const errorData = await res.json()
        throw new Error(errorData.detail || 'Request failed')
      }

      const data = await res.json()
      setResponse(data.answer)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleReviewPlan = async () => {
    if (!apiKey || !planContent) return

    setLoading(true)
    setError(null)
    setResponse(null)

    try {
      const res = await fetch('/api/demo/review-plan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          api_key: apiKey,
          plan_content: planContent,
          review_level: reviewLevel,
        }),
      })

      if (!res.ok) {
        const errorData = await res.json()
        throw new Error(errorData.detail || 'Request failed')
      }

      const data = await res.json()
      setResponse(JSON.stringify(data, null, 2))
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="demo-container">
      <h2 className="demo-title">Try It Now</h2>
      <p className="demo-subtitle">
        Test Ask MCP instantly in your browser
      </p>

      <div className="demo-tabs">
        <button
          className={`demo-tab ${activeTab === 'phone' ? 'active' : ''}`}
          onClick={() => setActiveTab('phone')}
        >
          phone_a_friend
        </button>
        <button
          className={`demo-tab ${activeTab === 'review' ? 'active' : ''}`}
          onClick={() => setActiveTab('review')}
        >
          review_plan
        </button>
      </div>

      <div className="form-container">
        <div className="warning">
          <p>
            This demo requires your OpenAI API key. Your key is only used for this request
            and is never stored or logged. For production use, configure the key in your
            MCP client instead.
          </p>
        </div>

        <div className="form-field">
          <label>OpenAI API Key *</label>
          <input
            type="password"
            placeholder="sk-..."
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
          />
        </div>

        {activeTab === 'phone' && (
          <>
            <div className="form-field">
              <label>Question *</label>
              <textarea
                placeholder="What is the best way to structure a Python project?"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
              />
            </div>

            <div className="form-field">
              <label>Context (optional)</label>
              <textarea
                placeholder="I'm building a FastAPI application with SQLAlchemy"
                value={context}
                onChange={(e) => setContext(e.target.value)}
              />
            </div>

            <button
              className="submit-button"
              onClick={handlePhoneAFriend}
              disabled={!apiKey || !question || loading}
            >
              {loading ? 'Asking...' : 'Ask Question'}
            </button>
          </>
        )}

        {activeTab === 'review' && (
          <>
            <div className="form-field">
              <label>Plan Content *</label>
              <textarea
                style={{ minHeight: '200px' }}
                placeholder="# Project Plan&#10;&#10;## Objectives&#10;- Build a new feature&#10;&#10;## Timeline&#10;- Week 1: Design&#10;- Week 2: Implementation"
                value={planContent}
                onChange={(e) => setPlanContent(e.target.value)}
              />
            </div>

            <div className="form-field">
              <label>Review Level</label>
              <select
                value={reviewLevel}
                onChange={(e) => setReviewLevel(e.target.value)}
              >
                <option value="quick">Quick</option>
                <option value="standard">Standard</option>
                <option value="comprehensive">Comprehensive</option>
                <option value="deep_dive">Deep Dive</option>
                <option value="expert">Expert</option>
              </select>
            </div>

            <button
              className="submit-button"
              onClick={handleReviewPlan}
              disabled={!apiKey || !planContent || loading}
            >
              {loading ? 'Reviewing...' : 'Review Plan'}
            </button>
          </>
        )}

        {error && (
          <div className="response-container error">
            Error: {error}
          </div>
        )}

        {response && (
          <div className="response-container">
            {response}
          </div>
        )}
      </div>
    </div>
  )
}

export default InteractiveDemo
