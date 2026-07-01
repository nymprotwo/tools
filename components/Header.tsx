'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useState, useEffect } from 'react'
import { createClient } from '@/lib/supabase'

const nav = [
  { href: '/explore', label: 'Explore' },
  { href: '/tools', label: 'Tools' },
]

export default function Header() {
  const path = usePathname()
  const [user, setUser] = useState<any>(null)

  useEffect(() => {
    const sb = createClient()
    sb.auth.getUser().then(({ data }) => setUser(data.user))
    const { data: { subscription } } = sb.auth.onAuthStateChange((_, session) => {
      setUser(session?.user ?? null)
    })
    return () => subscription.unsubscribe()
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
        {nav.map(n => (
          <Link key={n.href} href={n.href} style={{
            padding: '5px 12px',
            borderRadius: '6px',
            fontSize: '13px',
            color: path.startsWith(n.href) ? 'var(--text)' : 'var(--muted)',
            background: path.startsWith(n.href) ? 'var(--surface)' : 'transparent',
            transition: 'color 0.15s',
          }}>
            {n.label}
          </Link>
        ))}
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
