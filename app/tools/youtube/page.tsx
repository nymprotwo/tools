'use client'

import { useState } from 'react'

function getVideoId(input: string): string | null {
  const patterns = [
    /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\s?]+)/,
  ]
  for (const p of patterns) {
    const m = input.match(p)
    if (m) return m[1]
  }
  // bare ID
  if (/^[a-zA-Z0-9_-]{11}$/.test(input.trim())) return input.trim()
  return null
}

export default function YouTubePage() {
  const [input, setInput] = useState('')
  const [videoId, setVideoId] = useState<string | null>(null)
  const [error, setError] = useState('')

  function load() {
    const id = getVideoId(input)
    if (!id) { setError('Paste a YouTube link or video ID'); return }
    setError('')
    setVideoId(id)
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 52px)' }}>
      <div style={{
        padding: '16px 24px',
        borderBottom: '1px solid var(--border)',
        display: 'flex',
        gap: '8px',
        alignItems: 'center',
        background: 'var(--bg)',
      }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && load()}
          placeholder="Paste YouTube link..."
          style={{
            flex: 1,
            background: 'var(--surface)',
            border: '1px solid var(--border)',
            borderRadius: '7px',
            padding: '8px 14px',
            fontSize: '13px',
            color: 'var(--text)',
            outline: 'none',
          }}
        />
        <button onClick={load} style={{
          background: 'var(--accent)',
          color: '#fff',
          border: 'none',
          borderRadius: '7px',
          padding: '8px 20px',
          fontSize: '13px',
          fontWeight: 600,
          cursor: 'pointer',
        }}>
          Play
        </button>
        {error && <span style={{ fontSize: '12px', color: 'var(--accent)' }}>{error}</span>}
      </div>

      {videoId ? (
        <div style={{ flex: 1, background: '#000' }}>
          <iframe
            src={`https://www.youtube.com/embed/${videoId}?autoplay=1&rel=0&modestbranding=1`}
            style={{ width: '100%', height: '100%', border: 'none' }}
            allow="autoplay; fullscreen"
            allowFullScreen
          />
        </div>
      ) : (
        <div style={{
          flex: 1,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          flexDirection: 'column',
          gap: '8px',
        }}>
          <p style={{ color: 'var(--muted)', fontSize: '13px' }}>Paste a link above to watch.</p>
          <p style={{ color: 'var(--muted2)', fontSize: '11px' }}>No recommendations. No comments. Just the video.</p>
        </div>
      )}
    </div>
  )
}
