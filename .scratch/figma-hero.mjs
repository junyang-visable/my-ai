const key = process.env.FIGMA_KEY
const fileKey = '4qMBXd6bdKCJmt7hwLAbRG'
const res = await fetch(`https://api.figma.com/v1/files/${fileKey}/nodes?ids=590:6713`, {
  headers: { 'X-Figma-Token': key },
})
const data = await res.json()
const node = Object.values(data.nodes)[0].document
let hero = null
const walk = (n) => {
  if (n.type === 'INSTANCE' && n.name.includes('Hero/Feedback')) hero = n
  if (!hero) for (const c of n.children || []) walk(c)
}
walk(node)
if (!hero) { console.log('hero not found'); process.exit(1) }
const bb = hero.absoluteBoundingBox
console.log('hero id=', hero.id, `${Math.round(bb.width)}x${Math.round(bb.height)}`)

const res2 = await fetch(`https://api.figma.com/v1/images/${fileKey}?ids=${encodeURIComponent(hero.id)}&format=svg`, {
  headers: { 'X-Figma-Token': key },
})
const data2 = await res2.json()
console.log('url=', data2.images[hero.id] ?? 'NO_URL')
