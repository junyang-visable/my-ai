const key = process.env.FIGMA_KEY
const fileKey = '4qMBXd6bdKCJmt7hwLAbRG'
const ids = '590:6713,590:6956,804:2795'
const res = await fetch(`https://api.figma.com/v1/files/${fileKey}/nodes?ids=${ids}`, {
  headers: { 'X-Figma-Token': key },
})
const data = await res.json()
const hex = (c) => {
  if (!c) return ''
  const p = (v) => Math.round(v * 255).toString(16).padStart(2, '0')
  return `#${p(c.r)}${p(c.g)}${p(c.b)}`
}
for (const [id, node] of Object.entries(data.nodes)) {
  console.log(`\n===== ${id} =====`)
  const walk = (n, d) => {
    if (n.type === 'INSTANCE' || n.type === 'TEXT' || n.type === 'BUTTON') {
      let line = `${'  '.repeat(d)}${n.visible === false ? 'HIDDEN  ' : 'visible '} ${n.type} "${n.name}"`
      if (n.type === 'TEXT') line += ` | ${JSON.stringify(n.characters.slice(0, 80))} fills=${(n.fills||[]).filter(f=>f.type==='SOLID').map(f=>hex(f.color)).join(',')}`
      const bg = (n.fills || []).filter((f) => f.type === 'SOLID' && f.visible !== false).map((f) => hex(f.color)).join(',')
      if (n.type === 'INSTANCE' && bg) line += ` bg=${bg}`
      console.log(line)
    }
    for (const c of n.children || []) walk(c, d + 1)
  }
  walk(node.document, 0)
}
