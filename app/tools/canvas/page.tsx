export default function CanvasPage() {
  return (
    <div style={{ height: 'calc(100vh - 52px)', width: '100%' }}>
      <iframe
        src="https://excalidraw.com"
        style={{ width: '100%', height: '100%', border: 'none' }}
        title="Canvas"
      />
    </div>
  )
}
