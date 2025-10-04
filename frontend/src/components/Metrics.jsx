import React, { useEffect, useState } from 'react'
import './Metrics.css'

function formatTallies(tallies) {
  const rows = []
  let total = 0
  Object.entries(tallies || {}).forEach(([tool, statuses]) => {
    const success = Number(statuses.success || 0)
    const error = Number(statuses.error || 0)
    const sum = success + error
    total += sum
    rows.push({ tool, success, error, sum })
  })
  rows.sort((a, b) => b.sum - a.sum)
  return { rows, total }
}

export default function Metrics() {
  const [data, setData] = useState({ tallies: {}, source: 'memory', generated_at: '' })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  async function fetchSummary(signal) {
    try {
      const res = await fetch('/api/metrics/summary', { signal })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const json = await res.json()
      setData(json)
      setError('')
    } catch (e) {
      setError('Unable to load metrics')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    const ac = new AbortController()
    fetchSummary(ac.signal)
    const id = setInterval(() => fetchSummary(ac.signal), 10000)
    return () => { ac.abort(); clearInterval(id) }
  }, [])

  const { rows, total } = formatTallies(data.tallies)

  return (
    <section className="metrics">
      <div className="metrics__container">
        <div className="metrics__header">
          <h2>Service Metrics</h2>
          <div className="metrics__meta">
            <span className={`metrics__badge metrics__badge--${data.source}`}>{data.source}</span>
            {data.generated_at && <span className="metrics__time">{new Date(data.generated_at).toLocaleString()}</span>}
          </div>
        </div>
        {loading && <div className="metrics__loading">Loading...</div>}
        {error && <div className="metrics__error">{error}</div>}
        {!loading && !error && (
          <>
            <div className="metrics__kpis">
              <div className="metrics__kpi">
                <div className="metrics__kpi-value">{total}</div>
                <div className="metrics__kpi-label">Total requests</div>
              </div>
            </div>
            <div className="metrics__table">
              <div className="metrics__row metrics__row--head">
                <div>Tool</div>
                <div>Success</div>
                <div>Error</div>
                <div>Total</div>
              </div>
              {rows.length === 0 && (
                <div className="metrics__row metrics__row--empty">No requests yet</div>
              )}
              {rows.map(r => (
                <div className="metrics__row" key={r.tool}>
                  <div className="metrics__tool">{r.tool}</div>
                  <div className="metrics__num metrics__num--success">{r.success}</div>
                  <div className="metrics__num metrics__num--error">{r.error}</div>
                  <div className="metrics__num">{r.sum}</div>
                </div>
              ))}
            </div>
          </>
        )}
      </div>
    </section>
  )
}


