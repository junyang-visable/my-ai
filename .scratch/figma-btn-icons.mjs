const key = process.env.FIGMA_KEY
const fileKey = '4qMBXd6bdKCJmt7hwLAbRG'
const res = await fetch(`https://api.figma.com/v1/files/${fileKey}/nodes?ids=579:5385&geometry=paths`, {
  headers: { 'X-Figma-Token': key },
})
const data = await res.json()
const node = Object.values(data.nodes)[0].document

function hasText(n, s) {
  if (n.type === 'TEXT' && (n.characters || '').includes(s)) return true
  return (n.children || []).some((c) => hasText(c, s))
}
let card = null
const find = (n) => {
  if (n.type === 'FRAME' && n.name === 'My account' && hasText(n, 'Delete this account')) { card = n; return }
  for (const c of n.children || []) find(c)
}
find(node)

const hex = (c) => {
  if (!c) return ''
  const p = (v) => Math.round(v * 255).toString(16).padStart(2, '0')
  return `#${p(c.r)}${p(c.g)}${p(c.b)}`
}
const walk = (n, path) => {
  const p = [...path, n.name]
  if (n.type === 'VECTOR' && (n.name === 'Icon')) {
    const bb = n.absoluteBoundingBox || {}
    console.log(`--- ${p.join('>')} id=${n.id} w=${Math.round(bb.width)} h=${Math.round(bb.height)}`)
    for (const f of n.fills || []) {
      if (f.type === 'SOLID') console.log('    fill', hex(f.color), 'op', f.opacity)
    }
    const g = n.fillGeometry || []
    for (const seg of g) console.log('    path', seg.path.slice(0, 400))
  }
  for (const c of n.children || []) walk(c, p)
}
walk(card, [])
