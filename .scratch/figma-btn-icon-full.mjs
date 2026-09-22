import { writeFileSync } from 'node:fs'
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

let icon = null
const walk = (n, inLeft) => {
  if (n.type === 'VECTOR' && n.name === 'Icon' && !icon) icon = n
  for (const c of n.children || []) walk(c)
}
walk(card)

const hex = (c) => {
  const p = (v) => Math.round(v * 255).toString(16).padStart(2, '0')
  return `#${p(c.r)}${p(c.g)}${p(c.b)}`
}
const fill = (icon.fills || []).filter((f) => f.type === 'SOLID').map((f) => hex(f.color))[0] ?? 'currentColor'
const paths = (icon.fillGeometry || []).map((g) => g.path)
const svg = `<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">\n${paths
  .map((d) => `  <path d="${d}" fill="${fill}"/>`)
  .join('\n')}\n</svg>\n`
writeFileSync('/tmp/figma-btn-delete-icon.svg', svg)
console.log('fill=', fill, 'paths=', paths.length, 'bytes=', svg.length)
