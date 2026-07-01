import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = { title: 'Tools — nympro' }

const tools = [
  { name: 'Anonymous YouTube', desc: 'YouTube without tracking. Search anything, no ads, no history.', href: 'https://invidious.nympro.studio', live: true, external: true },
  { name: 'Canvas', desc: 'Open whiteboard — draw anything', href: '/tools/canvas', live: true },
  { name: 'VideoPrinter', desc: 'Auto video creation with subtitles', href: null, live: false },
  { name: 'ViralCut', desc: 'AI short-form clips from any video', href: null, live: false },
  { name: 'Farm Studio', desc: 'Automated content pipeline', href: null, live: false },
]

export default function ToolsPage() {
  return (
    <div style={{ maxWidth: '860px', margin: '0 auto', padding: '56px 32px' }}>
      <div style={{ marginBottom: '40px' }}>
        <h1 style={{ fontSize: '22px', fontWeight: 700, letterSpacing: '-0.02em' }}>Tools</h1>
        <p style={{ color: 'var(--muted)', fontSize: '13px', marginTop: '6px' }}>Pick something.</p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1px', background: 'var(--border)' }}>
        {tools.map(t => (
          <div key={t.name} style={{
            background: 'var(--bg)',
            padding: '20px 24px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}>
            <div>
              <div style={{ fontSize: '13px', fontWeight: 600, marginBottom: '3px' }}>{t.name}</div>
              <div style={{ fontSize: '12px', color: 'var(--muted)' }}>{t.desc}</div>
            </div>
            {t.live && t.href ? (
              <a href={t.href} target={(t as any).external ? '_blank' : '_self'} rel="noreferrer" style={{
                fontSize: '12px',
                color: 'var(--accent)',
                border: '1px solid #3a1515',
                borderRadius: '6px',
                padding: '6px 16px',
              }}>
                Open
              </a>
            ) : (
              <span style={{ fontSize: '11px', color: 'var(--muted2)', letterSpacing: '0.04em' }}>SOON</span>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
