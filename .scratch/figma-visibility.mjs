const key = process.env.FIGMA_KEY
const fileKey = '4qMBXd6bdKCJmt7hwLAbRG'
const res = await fetch(`https://api.figma.com/v1/files/${fileKey}/nodes?ids=579:5385`, {
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

const walk = (n, path) => {
  const p = [...path, n.name]
  if (n.type === 'INSTANCE' || n.type === 'VECTOR') {
    console.log(`${n.visible === false ? 'HIDDEN ' : 'visible'} ${n.type} ${p.join('>')} id=${n.id}`)
  }
  for (const c of n.children || []) walk(c, p)
}
walk(card, [])
