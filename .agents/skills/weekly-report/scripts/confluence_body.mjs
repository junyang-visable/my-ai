#!/usr/bin/env node
// Confluence weekly-report body toolkit.
//   prepare <fetched.json|raw.html> <new-section.html> <out-body.html> [out-wrapped.txt]
//     -> new section prepended to current page body (data-local-id stripped,
//        optional '>'-boundary newline wrap for easier Read/transcribe)
//   verify <fetched.json|raw.html> <expected-body.html>
//     -> normalized compare; ignores known server-side normalizations
//        (wiki URL title-slug removal, rowspan/data-colwidth attr reorder)
// Output: single-line JSON on stdout. exit 0 always; check the "equal"/"ok" field.

import { readFileSync, writeFileSync } from 'node:fs';

function extractBody(text) {
  const t = text.trim();
  if (!t.startsWith('{')) return text;
  const j = JSON.parse(t);
  return j.body ?? j.content?.nodes?.[0]?.body;
}

function stripLocalIds(s) {
  return s.replace(/ data-local-id="[^"]*"/g, '');
}

function sortAttrs(s) {
  return s.replace(/<[a-zA-Z][^<>]*>/g, (tag) => {
    const m = tag.match(/^(<[a-zA-Z][a-zA-Z0-9-]*)((?:\s[^<>]*?)?)(\/?)>$/);
    if (!m || !m[2].trim()) return tag;
    const tokens = m[2].match(/[^\s=]+=(?:"[^"]*"|[^\s]+)|[^\s=]+/g) ?? [];
    tokens.sort();
    return `${m[1]} ${tokens.join(' ')}${m[3]}>`;
  });
}

function norm(s) {
  return sortAttrs(stripLocalIds(s))
    .replace(/(\/wiki\/spaces\/[^"\s>]+\/pages\/\d+)\/[^"\s>]*/g, '$1')
    .replace(/\s+/g, '');
}

function diffHunks(a, b, max) {
  const hunks = [];
  let i = 0;
  let j = 0;
  while ((i < a.length || j < b.length) && hunks.length < max) {
    if (a[i] === b[j]) { i++; j++; continue; }
    let sync = -1;
    let mode = null;
    for (let d = 1; d <= 400; d++) {
      if (i + d <= a.length && a.slice(i + d, i + d + 60) === b.slice(j, j + 60)) { sync = d; mode = 'got-extra'; break; }
      if (j + d <= b.length && b.slice(j + d, j + d + 60) === a.slice(i, i + 60)) { sync = d; mode = 'want-extra'; break; }
    }
    if (sync < 0) {
      hunks.push({ type: 'mismatch', at: i, got: a.slice(i, i + 120), want: b.slice(j, j + 120) });
      break;
    }
    hunks.push(mode === 'got-extra'
      ? { type: 'got-extra', text: a.slice(i, i + sync) }
      : { type: 'want-extra', text: b.slice(j, j + sync) });
    if (mode === 'got-extra') i += sync; else j += sync;
  }
  if (i < a.length && hunks.length < max) hunks.push({ type: 'tail-got', text: a.slice(i, i + 200) });
  if (j < b.length && hunks.length < max) hunks.push({ type: 'tail-want', text: b.slice(j, j + 200) });
  return hunks;
}

const [cmd, ...args] = process.argv.slice(2);

if (cmd === 'prepare') {
  const [fetchedPath, newSecPath, outBody, outWrapped] = args;
  if (!fetchedPath || !newSecPath || !outBody) {
    console.log(JSON.stringify({ ok: false, error: 'usage: prepare <fetched> <new-section> <out-body> [out-wrapped]' }));
    process.exit(0);
  }
  const oldBody = stripLocalIds(extractBody(readFileSync(fetchedPath, 'utf8')));
  const newSec = stripLocalIds(readFileSync(newSecPath, 'utf8').trim());
  const body = newSec + oldBody;
  writeFileSync(outBody, body);
  let wrapped = null;
  let wrappedLines = 1;
  if (outWrapped) {
    wrapped = body.replace(/>(?=<)/g, '>\n');
    writeFileSync(outWrapped, wrapped);
    wrappedLines = wrapped.split('\n').length;
  }
  console.log(JSON.stringify({ ok: true, bodyLen: body.length, wrappedLines, roundtrip: wrapped ? wrapped.split('\n').join('') === body : undefined }));
  process.exit(0);
}

if (cmd === 'verify') {
  const [fetchedPath, expectedPath] = args;
  if (!fetchedPath || !expectedPath) {
    console.log(JSON.stringify({ ok: false, error: 'usage: verify <fetched> <expected>' }));
    process.exit(0);
  }
  const a = norm(extractBody(readFileSync(fetchedPath, 'utf8')));
  const b = norm(readFileSync(expectedPath, 'utf8'));
  const hunks = a === b ? [] : diffHunks(a, b, 5);
  console.log(JSON.stringify({ equal: hunks.length === 0 && a.length === b.length, gotLen: a.length, wantLen: b.length, hunks }, null, 1));
  process.exit(0);
}

console.log(JSON.stringify({ ok: false, error: 'unknown command; use prepare or verify' }));
