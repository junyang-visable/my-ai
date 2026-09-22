const key = process.env.FIGMA_KEY
const fileKey = '4qMBXd6bdKCJmt7hwLAbRG'
console.error('fetching file...')
const res = await fetch(`https://api.figma.com/v1/files/${fileKey}`, {
  headers: { 'X-Figma-Token': key },
})
const data = await res.json()
console.error('file fetched, walking...')

const needles = [
  'We are sorry to see you leave',
  'Alibaba account deletion request',
  'Do you really want to delete your Alibaba.com account',
  'unhappy with the quality of requests',
]
const hits = new Map()
function walk(n, ancestors) {
  if (n.type === 'TEXT' && needles.some((s) => (n.characters || '').includes(s))) {
    for (const a of ancestors) {
      if (a.type === 'FRAME' || a.type === 'COMPONENT' || a.type === 'SECTION') {
        const k = `${a.id}\t${a.name}\t${a.width|0}x${a.height|0}`
        hits.set(k, (hits.get(k) || 0) + 1)
      }
    }
  }
  const next = [...ancestors, n]
  for (const c of n.children || []) walk(c, next)
}
walk(data.document, [])
for (const [k, count] of hits) console.log(`${count}\t${k}`)
