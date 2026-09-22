const key = process.env.FIGMA_KEY
const fileKey = '4qMBXd6bdKCJmt7hwLAbRG'
const ids = process.argv[2] || '558:2316,560:2369'

const res = await fetch(`https://api.figma.com/v1/files/${fileKey}/nodes?ids=${ids}`, {
  headers: { 'X-Figma-Token': key },
})
if (!res.ok) {
  console.error(res.status, await res.text())
  process.exit(1)
}
const data = await res.json()

const hex = (c) => {
  if (!c) return ''
  const p = (v) => Math.round(v * 255).toString(16).padStart(2, '0')
  return `#${p(c.r)}${p(c.g)}${p(c.b)}${c.a != null && c.a < 1 ? `/${Math.round(c.a * 100)}%` : ''}`
}
const fillsOf = (n) =>
  (n.fills || [])
    .filter((f) => f.visible !== false)
    .map((f) => (f.type === 'SOLID' ? hex(f.color) : f.type))

function walk(n, depth) {
  const pad = '  '.repeat(depth)
  let line = `${pad}${n.type} "${n.name}"`
  const fl = fillsOf(n)
  if (fl.length) line += ` fills=[${fl.join(',')}]`
  if (n.strokes?.length) {
    const st = n.strokes.filter((s) => s.visible !== false).map((s) => (s.type === 'SOLID' ? hex(s.color) : s.type))
    if (st.length) line += ` strokes=[${st.join(',')}] strokeW=${n.strokeWeight}`
  }
  if (n.cornerRadius != null && n.cornerRadius !== 0) line += ` r=${n.cornerRadius}`
  if (n.type === 'TEXT') {
    line += ` | size=${n.style?.fontSize} ${n.style?.fontFamily} ${n.style?.fontWeight} lh=${n.style?.lineHeightPx}`
    line += `\n${pad}>> ${JSON.stringify(n.characters)}`
  }
  console.log(line)
  for (const c of n.children || []) walk(c, depth + 1)
}

for (const [id, node] of Object.entries(data.nodes)) {
  console.log(`\n===== ${id} :: ${node.name} (${node.type}) ${node.width}x${node.height} =====`)
  walk(node.document, 0)
}
