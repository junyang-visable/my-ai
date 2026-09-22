const key = process.env.FIGMA_KEY
const fileKey = '4qMBXd6bdKCJmt7hwLAbRG'
const res = await fetch(`https://api.figma.com/v1/files/${fileKey}/nodes?ids=804:2795`, {
  headers: { 'X-Figma-Token': key },
})
const data = await res.json()
const node = Object.values(data.nodes)[0].document
const hex = (c) => {
  if (!c) return ''
  const p = (v) => Math.round(v * 255).toString(16).padStart(2, '0')
  return `#${p(c.r)}${p(c.g)}${p(c.b)}`
}
const ox = node.absoluteBoundingBox?.x ?? 0, oy = node.absoluteBoundingBox?.y ?? 0
console.log('CARD', node.width, 'x', node.height)
const walk = (n, d) => {
  const bb = n.absoluteBoundingBox || {}
  let line = `${'  '.repeat(d)}${n.visible === false ? 'HIDDEN ' : ''}${n.type} "${n.name}" x=${Math.round(bb.x - ox)} y=${Math.round(bb.y - oy)} w=${Math.round(bb.width)} h=${Math.round(bb.height)}`
  if (n.type === 'TEXT') line += ` | ${JSON.stringify(n.characters.slice(0, 70))} fills=${(n.fills||[]).filter(f=>f.type==='SOLID').map(f=>hex(f.color)).join(',')}`
  for (const f of n.fills || []) if (f.type === 'SOLID' && n.type !== 'TEXT') line += ` bg=${hex(f.color)}`
  console.log(line)
  for (const c of n.children || []) walk(c, d + 1)
}
walk(node, 0)
