const key = process.env.FIGMA_KEY
const fileKey = '4qMBXd6bdKCJmt7hwLAbRG'
const wanted = {
  'alibaba-mark': '579:6114',
  'wlw-mark': '579:6077',
  'ep-mark': '579:6082',
  'btn-icon-left': 'I579:6088;6344:4220;1843:405',
  'btn-icon-right': 'I579:6088;6344:4221;1843:405',
}
const idList = Object.values(wanted).map(encodeURIComponent).join(',')
const res = await fetch(`https://api.figma.com/v1/images/${fileKey}?ids=${idList}&format=svg`, {
  headers: { 'X-Figma-Token': key },
})
const data = await res.json()
if (data.err) { console.error('err', data.err); process.exit(1) }
for (const [name, id] of Object.entries(wanted)) {
  const url = data.images[id]
  if (!url) { console.log(name, id, 'NO URL'); continue }
  const svg = await (await fetch(url)).text()
  console.log(`===== ${name} (${id}) =====`)
  console.log(svg.slice(0, 600))
}
