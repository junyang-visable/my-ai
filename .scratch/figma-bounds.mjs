const key = process.env.FIGMA_KEY
const fileKey = '4qMBXd6bdKCJmt7hwLAbRG'
const ids = process.argv[2]

const res = await fetch(`https://api.figma.com/v1/files/${fileKey}/nodes?ids=${ids}`, {
  headers: { 'X-Figma-Token': key },
})
const data = await res.json()

function hasText(n, s) {
  if (n.type === 'TEXT' && (n.characters || '').includes(s)) return true
  return (n.children || []).some((c) => hasText(c, s))
}
for (const [id, node] of Object.entries(data.nodes)) {
  let target = null
  const find = (n) => {
    if (n.type === 'FRAME' && n.name === 'My account' && hasText(n, 'Delete this account')) { target = n; return }
    for (const c of n.children || []) find(c)
  }
  find(node.document)
  if (!target) { console.log('card not found'); continue }
  const ox = target.absoluteBoundingBox.x, oy = target.absoluteBoundingBox.y
  console.log('CARD', target.width + 'x' + target.height)
  const walk = (n, d) => {
    const bb = n.absoluteBoundingBox || {}
    const rel = bb.x != null ? `x=${Math.round(bb.x - ox)} y=${Math.round(bb.y - oy)} w=${Math.round(bb.width)} h=${Math.round(bb.height)}` : ''
    console.log(`${'  '.repeat(d)}${n.type} "${n.name}" ${rel}${n.characters ? ' | ' + JSON.stringify(n.characters.slice(0, 50)) : ''}`)
    for (const c of n.children || []) walk(c, d + 1)
  }
  walk(target, 0)
}
