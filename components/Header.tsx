'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useState, useEffect, useRef } from 'react'
import { createClient } from '@/lib/supabase'

const tools = [
  { name: 'Anonymous YouTube', href: 'https://invidious.nympro.studio', external: true },
  { name: 'Canvas', href: '/tools/canvas', external: false },
  { name: 'VideoPrinter', href: null },
  { name: 'ViralCut', href: null },
  { name: 'Farm Studio', href: null },
]

export default function Header() {
  const path = usePathname()
  const [user, setUser] = useState<any>(null)
  const [toolsOpen, setToolsOpen] = useState(false)
  const toolsRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const sb = createClient()
    sb.auth.getUser().then(({ data }) => setUser(data.user))
    const { data: { subscription } } = sb.auth.onAuthStateChange((_, session) => {
      setUser(session?.user ?? null)
    })
    return () => subscription.unsubscribe()
  }, [])

  useEffect(() => {
    function onClick(e: MouseEvent) {
      if (toolsRef.current && !toolsRef.current.contains(e.target as Node)) {
        setToolsOpen(false)
      }
    }
    document.addEventListener('mousedown', onClick)
    return () => document.removeEventListener('mousedown', onClick)
  }, [])

  async function signOut() {
    const sb = createClient()
    await sb.auth.signOut()
  }

  return (
    <header style={{
      borderBottom: '1px solid var(--border)',
      background: 'var(--bg)',
      padding: '0 32px',
      display: 'flex',
      alignItems: 'center',
      height: '52px',
      gap: '32px',
      position: 'sticky',
      top: 0,
      zIndex: 50,
    }}>
      <Link href="/" style={{ fontWeight: 700, fontSize: '13px', letterSpacing: '-0.01em', color: 'var(--text)' }}>
        nympro
      </Link>

      <nav style={{ display: 'flex', gap: '4px', flex: 1 }}>
        <Link href="/explore" style={{
          padding: '5px 12px',
          borderRadius: '6px',
          fontSize: '13px',
          color: path.startsWith('/explore') ? 'var(--text)' : 'var(--muted)',
          background: path.startsWith('/explore') ? 'var(--surface)' : 'transparent',
        }}>
          Explore
        </Link>

        {/* Tools with dropdown */}
        <div ref={toolsRef} style={{ position: 'relative' }}
          onMouseEnter={() => setToolsOpen(true)}
          onMouseLeave={() => setToolsOpen(false)}
        >
          <button style={{
            padding: '5px 12px',
            borderRadius: '6px',
            fontSize: '13px',
            color: path.startsWith('/tools') ? 'var(--text)' : 'var(--muted)',
            background: path.startsWith('/tools') ? 'var(--surface)' : 'transparent',
            border: 'none',
            cursor: 'pointer',
          }}>
            Tools
          </button>

          {toolsOpen && (
            <div style={{
              position: 'absolute',
              top: 'calc(100% + 8px)',
              left: 0,
              background: 'var(--surface)',
              border: '1px solid var(--border)',
              borderRadius: '8px',
              padding: '6px',
              minWidth: '200px',
              boxShadow: '0 8px 24px rgba(0,0,0,0.4)',
            }}>
              {tools.map(t => t.href ? (
                <a
                  key={t.name}
                  href={t.href}
                  target={t.external ? '_blank' : '_self'}
                  rel="noreferrer"
                  onClick={() => setToolsOpen(false)}
                  style={{
                    display: 'block',
                    padding: '8px 12px',
                    fontSize: '13px',
                    color: 'var(--text)',
                    borderRadius: '5px',
                    cursor: 'pointer',
                  }}
                  onMouseEnter={e => (e.currentTarget.style.background = 'var(--surface2)')}
                  onMouseLeave={e => (e.currentTarget.style.background = 'transparent')}
                >
                  {t.name}
                </a>
              ) : (
                <div key={t.name} style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '8px 12px',
                  fontSize: '13px',
                  color: 'var(--muted2)',
                  borderRadius: '5px',
                }}>
                  {t.name}
                  <span style={{ fontSize: '10px', letterSpacing: '0.04em' }}>SOON</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </nav>

      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        {user ? (
          <>
            <span style={{ fontSize: '12px', color: 'var(--muted)' }}>{user.email}</span>
            <button onClick={signOut} style={{
              fontSize: '12px',
              color: 'var(--muted)',
              background: 'none',
              border: '1px solid var(--border)',
              borderRadius: '6px',
              padding: '4px 12px',
              cursor: 'pointer',
            }}>
              Sign out
            </button>
          </>
        ) : (
          <Link href="/login" style={{
            fontSize: '12px',
            color: 'var(--muted)',
            border: '1px solid var(--border)',
            borderRadius: '6px',
            padding: '4px 12px',
          }}>
            Sign in
          </Link>
        )}
      </div>
    </header>
  )
}
