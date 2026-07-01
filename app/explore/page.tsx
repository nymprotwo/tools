'use client'

const items = [
  {
    name: 'ViralCut',
    badge: 'Tool',
    stack: 'Python · Whisper · GPT-4o · OpenCV',
    desc: 'Paste a YouTube link, get back short-form clips with karaoke captions, smart face crop, and AI-selected moments. Runs locally.',
    url: null,
    status: 'dev',
  },
  {
    name: 'Farm Studio',
    badge: 'Tool',
    stack: 'n8n · Telegram · GPT-4o',
    desc: 'Automated content pipeline for social media. Generates, schedules, and posts — driven by n8n workflows on the server.',
    url: null,
    status: 'dev',
  },
  {
    name: 'Canvas',
    badge: 'Tool',
    stack: 'Excalidraw',
    desc: 'Open whiteboard, no login required. Draw, diagram, wireframe — everything saves locally in your browser.',
    url: '/tools/canvas',
    status: 'live',
  },
  {
    name: 'Anonymous YouTube',
    badge: 'Tool',
    stack: 'Invidious · PostgreSQL',
    desc: 'YouTube without Google tracking. Search anything, watch any video — no ads, no recommendation poisoning, no history sent to Google.',
    url: 'https://invidious.nympro.studio',
    status: 'live',
  },
  {
    name: 'VideoPrinter',
    badge: 'Tool',
    stack: 'Python · Whisper · ffmpeg',
    desc: 'Automatic video creation with subtitles. Feed it content, get back a ready-to-publish video with burned-in captions.',
    url: null,
    status: 'dev',
  },
]

export default function ExplorePage() {
  return (
    <div style={{ maxWidth: '860px', margin: '0 auto', padding: '56px 32px' }}>
      <div style={{ marginBottom: '48px' }}>
        <h1 style={{ fontSize: '28px', fontWeight: 700, letterSpacing: '-0.03em', lineHeight: 1.1, marginBottom: '10px' }}>
          See what&apos;s <span style={{ color: 'var(--accent)' }}>inside.</span>
        </h1>
        <p style={{ color: 'var(--muted)', fontSize: '13px' }}>
          Tools, apps, and experiments. Some live, some in progress.
        </p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1px', background: 'var(--border)' }}>
        {items.map(item => (
          <div key={item.name} style={{
            background: 'var(--bg)',
            padding: '24px 28px',
            display: 'flex',
            flexDirection: 'column',
            gap: '10px',
            transition: 'background 0.15s',
          }}
            onMouseEnter={e => (e.currentTarget.style.background = 'var(--surface)')}
            onMouseLeave={e => (e.currentTarget.style.background = 'var(--bg)')}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span style={{ fontSize: '13px', fontWeight: 600 }}>{item.name}</span>
              <span style={{
                fontSize: '10px',
                padding: '2px 6px',
                borderRadius: '3px',
                background: 'var(--surface)',
                color: 'var(--muted)',
                letterSpacing: '0.04em',
                textTransform: 'uppercase',
              }}>{item.badge}</span>
              {item.status === 'dev' && (
                <span style={{
                  fontSize: '10px',
                  padding: '2px 6px',
                  borderRadius: '3px',
                  background: '#1a1200',
                  color: '#a07020',
                  letterSpacing: '0.04em',
                  textTransform: 'uppercase',
                }}>dev</span>
              )}
            </div>
            <p style={{ fontSize: '12px', color: 'var(--muted)', lineHeight: 1.6 }}>{item.desc}</p>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginTop: 'auto', paddingTop: '6px' }}>
              <span style={{ fontSize: '11px', color: 'var(--muted2)' }}>{item.stack}</span>
              {item.url && (
                <a href={item.url} target={item.url.startsWith('http') ? '_blank' : '_self'} rel="noreferrer" style={{
                  fontSize: '11px',
                  color: 'var(--accent)',
                  border: '1px solid #3a1515',
                  borderRadius: '4px',
                  padding: '3px 10px',
                }}>
                  Open
                </a>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
