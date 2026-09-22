const key = process.env.FIGMA_KEY
const fileKey = '4qMBXd6bdKCJmt7hwLAbRG'
const ids = '579:5385'

const res = await fetch(`https://api.figma.com/v1/files/${fileKey}/nodes?ids=${ids}`, {
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
if (!card) { console.log('card not found'); process.exit(1) }

// collect interesting icon nodes with ids
const out = []
const walk = (n, path) => {
  const p = [...path, n.name]
  if (n.type === 'INSTANCE' || n.type === 'VECTOR') {
    const bb = n.absoluteBoundingBox || {}
    out.push({ path: p.join('>'), name: n.name, type: n.type, id: n.id, w: Math.round(bb.width), h: Math.round(bb.height) })
  }
  for (const c of n.children || []) walk(c, p)
}
walk(card, [])
for (const o of out) console.log(`${o.id}  ${o.type} ${o.w}x${o.h}  ${o.path}`)
