#!/usr/bin/env node
/**
 * Dependency-free SSR stress tester for memory-leak verification.
 *
 * Usage:
 *   TARGET=https://www.wlw-staging.de \
 *   ROUTES='/en/my-account/business-insights/<uuid>,/en/my-account/business-insights/<uuid>/display' \
 *   COOKIE='session=...' \
 *   node stress.js [durationSec=600] [concurrency=20]
 *
 * Per-minute stats printed with ISO timestamps (correlate with CloudWatch).
 * Also appends per-minute JSON lines to stress-log.jsonl next to this file.
 */
const https = require('node:https')
const fs = require('node:fs')
const path = require('node:path')

const TARGET = process.env.TARGET || 'https://www.wlw-staging.de'
const ROUTES = (process.env.ROUTES || '').split(',').map((s) => s.trim()).filter(Boolean)
const COOKIE = process.env.COOKIE || ''
const DURATION = Number(process.argv[2] || 600)
const CONCURRENCY = Number(process.argv[3] || 20)
const LOG_FILE = path.join(__dirname, 'stress-log.jsonl')

if (!ROUTES.length) {
  console.error('ROUTES env var required (comma-separated paths)')
  process.exit(1)
}
if (!COOKIE) {
  console.error('COOKIE env var required (authenticated page returns 302 otherwise)')
  process.exit(1)
}

const base = new URL(TARGET)
const agent = new https.Agent({
  keepAlive: true,
  maxSockets: CONCURRENCY,
  maxFreeSockets: CONCURRENCY,
})

const t0 = Date.now()
const minutes = new Map()

function bucket() {
  const idx = Math.floor((Date.now() - t0) / 60000)
  if (!minutes.has(idx)) {
    minutes.set(idx, { count: 0, codes: {}, lat: [], err: 0, bytes: 0 })
  }
  return minutes.get(idx)
}

function pct(sorted, p) {
  if (!sorted.length) return 0
  const i = Math.min(sorted.length - 1, Math.floor((p / 100) * sorted.length))
  return sorted[i]
}

function fmtLine(m, idx) {
  const lats = [...m.lat].sort((a, b) => a - b)
  const codeStr = Object.entries(m.codes)
    .map(([c, n]) => `${c}x${n}`)
    .join(' ')
  return (
    `[min ${String(idx).padStart(2, '0')}] ${new Date(t0 + idx * 60000).toISOString()} ` +
    `req=${m.count} rps=${(m.count / 60).toFixed(1)} ` +
    `p50=${pct(lats, 50).toFixed(0)}ms p95=${pct(lats, 95).toFixed(0)}ms p99=${pct(lats, 99).toFixed(0)}ms ` +
    `codes=[${codeStr}] err=${m.err} mb=${(m.bytes / 1048576).toFixed(1)}`
  )
}

function requestOnce(pathname) {
  return new Promise((resolve) => {
    const start = process.hrtime.bigint()
    const req = https.request(
      {
        hostname: base.hostname,
        port: 443,
        path: pathname,
        method: 'GET',
        agent,
        timeout: 30000,
        headers: {
          cookie: COOKIE,
          accept: 'text/html,application/xhtml+xml',
          'user-agent': 'memleak-stress/1.0',
        },
      },
      (res) => {
        let bytes = 0
        res.on('data', (c) => (bytes += c.length))
        res.on('end', () => {
          const ms = Number(process.hrtime.bigint() - start) / 1e6
          const m = bucket()
          m.count++
          m.codes[res.statusCode] = (m.codes[res.statusCode] || 0) + 1
          m.lat.push(ms)
          m.bytes += bytes
          resolve(res.statusCode)
        })
      }
    )
    req.on('timeout', () => req.destroy(new Error('timeout')))
    req.on('error', () => {
      const m = bucket()
      m.err++
      m.codes['ERR'] = (m.codes['ERR'] || 0) + 1
      resolve('ERR')
    })
    req.end()
  })
}

async function worker(id) {
  let i = id
  while (Date.now() - t0 < DURATION * 1000) {
    await requestOnce(ROUTES[i++ % ROUTES.length])
  }
}

// per-minute reporter
let reported = -1
const reporter = setInterval(() => {
  const currentIdx = Math.floor((Date.now() - t0) / 60000)
  for (let idx = reported + 1; idx < currentIdx; idx++) {
    const m = minutes.get(idx)
    if (m) {
      console.log(fmtLine(m, idx))
      fs.appendFileSync(
        LOG_FILE,
        JSON.stringify({ minute: idx, ts: new Date(t0 + idx * 60000).toISOString(), ...m, lat: undefined, lat_p50: pct([...m.lat].sort((a, b) => a - b), 50), lat_p95: pct([...m.lat].sort((a, b) => a - b), 95), lat_p99: pct([...m.lat].sort((a, b) => a - b), 99) }) + '\n'
      )
    }
    reported = idx
  }
}, 5000)

;(async () => {
  console.log(`target=${TARGET} routes=${ROUTES.length} concurrency=${CONCURRENCY} duration=${DURATION}s start=${new Date(t0).toISOString()}`)
  console.log('HEADERS check — smoke request first:')
  const smoke = await requestOnce(ROUTES[0])
  if (smoke !== 200) {
    console.error(`SMOKE FAILED: first request returned ${smoke} — aborting (cookie invalid/expired?)`)
    clearInterval(reporter)
    agent.destroy()
    process.exit(2)
  }
  console.log(`smoke OK (${smoke}) — starting load`)
  await Promise.all(Array.from({ length: CONCURRENCY }, (_, i) => worker(i)))
  clearInterval(reporter)
  // report final partial minute
  const finalIdx = Math.floor((Date.now() - t0) / 60000)
  for (let idx = reported + 1; idx <= finalIdx; idx++) {
    const m = minutes.get(idx)
    if (m && m.count) console.log(fmtLine(m, idx))
  }
  const all = [...minutes.values()]
  const totalReq = all.reduce((s, m) => s + m.count, 0)
  const totalErr = all.reduce((s, m) => s + m.err, 0)
  const total3xx = all.reduce((s, m) => s + (m.codes['302'] || 0) + (m.codes['301'] || 0) + (m.codes['307'] || 0), 0)
  const allLat = all.flatMap((m) => m.lat).sort((a, b) => a - b)
  console.log('--- SUMMARY ---')
  console.log(`total=${totalReq} rps=${(totalReq / DURATION).toFixed(1)} err=${totalErr} redirects=${total3xx}`)
  console.log(`latency p50=${pct(allLat, 50).toFixed(0)}ms p95=${pct(allLat, 95).toFixed(0)}ms p99=${pct(allLat, 99).toFixed(0)}ms max=${(allLat[allLat.length - 1] || 0).toFixed(0)}ms`)
  if (total3xx > totalReq * 0.05) console.log('WARNING: >5% redirects — cookie likely expired mid-run, results invalid for SSR rendering')
  agent.destroy()
})()
