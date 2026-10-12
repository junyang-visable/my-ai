#!/usr/bin/env node
'use strict';

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

function fail(msg) {
  console.error(`ERROR: ${msg}`);
  process.exit(1);
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '-o' || a === '--out') args.out = argv[++i];
    else if (a === '--stdin') args.stdin = true;
    else args._.push(a);
  }
  return args;
}

function b64(str) {
  return Buffer.from(str, 'utf8').toString('base64');
}

function encodeSubject(subject) {
  if (/^[\x20-\x7e]*$/.test(subject)) return subject;
  return `=?UTF-8?B?${b64(subject)}?=`;
}

function encodeAddress(entry) {
  const m = String(entry).match(/^\s*(.*?)\s*<([^>]+)>\s*$/);
  if (!m) return String(entry).trim();
  let name = m[1];
  const addr = m[2];
  if (!name) return addr;
  if (/[^\x20-\x7e]/.test(name)) name = `=?UTF-8?B?${b64(name)}?=`;
  else if (/[,;"<>]/.test(name)) name = `"${name.replace(/"/g, '\\"')}"`;
  return `${name} <${addr}>`;
}

function wrapBase64(b64str) {
  return (b64str.match(/.{1,76}/g) || []).join('\r\n');
}

function esc(html) {
  return String(html)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function linkOrText(value) {
  const s = String(value || '').trim();
  if (/^https?:\/\//i.test(s)) return `<a href="${esc(s)}">${esc(s)}</a>`;
  return esc(s);
}

function buildHtml(f) {
  const trackingImpacted = String(f.trackingImpacted || 'No').trim();
  const trackingContent = /^yes$/i.test(trackingImpacted)
    ? `Tracking impacted: ${esc(f.trackingNote || '(details pending)')}`
    : 'No tracking impacted';
  const regressionContent = /^yes$/i.test(trackingImpacted)
    ? esc(f.regressionCheck || '(regression check pending)')
    : 'No tracking impacted';

  const prReviewedStatus = f.prReviewed === false ? '\\' : '✅';

  const rows = [
    { item: 'Group', status: '\\', content: esc(f.group || '') },
    { item: 'Reason for the changes', status: '\\', content: esc(f.reason || '') },
    { item: 'Change type: Git PR / Others', status: '\\', content: linkOrText(f.prUrl) },
    { item: 'Change executor', status: '\\', content: esc(f.executor || '') },
    { item: 'Code reviewer', status: '\\', content: esc(f.reviewer || '') },
    { item: 'QA engineer', status: '\\', content: esc(f.qaEngineer || '') },
    { item: 'Can it be rolled back if it fails', status: '\\', content: esc(f.canRollback || '') },
    { item: 'PR Reviewed', status: prReviewedStatus, content: '' },
    { item: 'Is tracking impacted', status: '✅', content: trackingContent },
    { item: 'Regression check done by WA/DA (if tracking impacted)', status: '✅', content: regressionContent },
  ];

  const trs = rows
    .map(
      (r) => `<tr>
<td style="border:1px solid #b8b8b8;padding:6px 10px;vertical-align:top;">${r.item}</td>
<td style="border:1px solid #b8b8b8;padding:6px 10px;text-align:center;">${r.status}</td>
<td style="border:1px solid #b8b8b8;padding:6px 10px;vertical-align:top;">${r.content}</td>
</tr>`
    )
    .join('\n');

  return `<p>Hello,</p>
<p>I am planning to release: <b>${esc(f.name)}</b>, please review it.</p>
<table style="border-collapse:collapse;font-family:sans-serif;font-size:14px;">
<thead>
<tr>
<th style="border:1px solid #b8b8b8;padding:6px 10px;background-color:#f0f1f2;text-align:left;">Items</th>
<th style="border:1px solid #b8b8b8;padding:6px 10px;background-color:#f0f1f2;text-align:left;">Status</th>
<th style="border:1px solid #b8b8b8;padding:6px 10px;background-color:#f0f1f2;text-align:left;">Content</th>
</tr>
</thead>
<tbody>
${trs}
</tbody>
</table>`;
}

function readFields(args) {
  if (args.stdin) {
    return JSON.parse(fs.readFileSync(0, 'utf8'));
  }
  const file = args._[0];
  if (!file) fail('usage: build-eml.mjs <fields.json> -o <output.eml>   (or --stdin)');
  return JSON.parse(fs.readFileSync(file, 'utf8'));
}

const args = parseArgs(process.argv.slice(2));
const fields = readFields(args);

for (const key of ['name', 'prUrl', 'reviewer']) {
  if (!fields[key] || !String(fields[key]).trim()) fail(`missing required field "${key}"`);
}

const subject = `Release approval: ${fields.name}`;
const html = buildHtml(fields);

const to = (fields.to || []).map(String).filter(Boolean);
const cc = (fields.cc || []).map(String).filter(Boolean);
if (!to.length) fail('no recipients: provide "to" in fields or config');

const outPath = args.out || path.join(os.homedir(), 'Desktop', `${String(fields.name).replace(/[^\w.-]+/g, '-').replace(/^-+|-+$/g, '')}.eml`);

const headers = [
  `From: ${fields.from || 'release-approval'}`,
  `To: ${to.map(encodeAddress).join(', ')}`,
  cc.length ? `Cc: ${cc.map(encodeAddress).join(', ')}` : null,
  `Subject: ${encodeSubject(subject)}`,
  `Date: ${new Date().toUTCString()}`,
  `Message-ID: <${Date.now()}.${Math.random().toString(36).slice(2)}@release-approval.local>`,
  'MIME-Version: 1.0',
  'Content-Type: text/html; charset=UTF-8',
  'Content-Transfer-Encoding: base64',
]
  .filter(Boolean)
  .join('\r\n');

const eml = `${headers}\r\n\r\n${wrapBase64(b64(html))}\r\n`;
fs.writeFileSync(outPath, eml, 'utf8');

console.log(`OK eml written: ${outPath}`);
console.log(`Subject: ${subject}`);
console.log(`To: ${to.join(', ')}${cc.length ? `\nCc: ${cc.join(', ')}` : ''}`);
