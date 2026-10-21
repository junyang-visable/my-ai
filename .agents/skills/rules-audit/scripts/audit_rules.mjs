#!/usr/bin/env node
// Deterministic checks for Qoder rules files. Zero dependencies, Node >= 18.
// Report-only: prints findings, never modifies anything.

import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';

const QUOTA = 100000;
const VALID_TRIGGERS = ['always_on', 'manual', 'model_decision', 'glob'];
const IGNORE_DIRS = new Set([
  '.git', 'node_modules', 'dist', 'build', 'coverage',
  '.next', '.nuxt', '.output', '.cache', '.turbo', 'target', 'vendor',
]);
const UNSUPPORTED_GLOB = /\\|\{|\}|\[|\]|\||!/;
const MAX_FILES = 50000;
const MAX_DEPTH = 20;

function usage() {
  process.stderr.write([
    'usage: audit_rules.mjs --base <project-root> [--project-rules] [--user-rules <dir>]',
    '',
    '  --base <project-root>   project root; glob patterns are matched against files under it',
    '  --project-rules         audit <base>/.qoder/rules/**/*.md',
    '  --user-rules <dir>      audit <dir>/**/*.md (normally ~/.qoder/rules)',
    '',
    'At least one of --project-rules / --user-rules is required.',
    'Report-only: exits 0 even with findings; exit 2 = usage error.',
  ].join('\n') + '\n');
  process.exit(2);
}

function fail(msg) {
  process.stderr.write('audit_rules: ' + msg + '\n');
  process.exit(2);
}

function walkFiles(root) {
  const files = [];
  let truncated = false;
  const stack = [{ dir: root, depth: 0 }];
  while (stack.length && !truncated) {
    const { dir, depth } = stack.pop();
    let entries;
    try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { continue; }
    for (const e of entries) {
      const full = path.join(dir, e.name);
      if (e.isDirectory()) {
        if (IGNORE_DIRS.has(e.name)) continue;
        if (depth + 1 > MAX_DEPTH) continue;
        stack.push({ dir: full, depth: depth + 1 });
      } else if (e.isFile()) {
        if (files.length >= MAX_FILES) { truncated = true; break; }
        files.push(path.relative(root, full).split(path.sep).join('/'));
      }
    }
  }
  return { files, truncated };
}

function collectRules(dir) {
  if (!fs.existsSync(dir)) return { files: [], other: 0, exists: false };
  const files = [];
  let other = 0;
  const stack = [dir];
  while (stack.length) {
    const d = stack.pop();
    let entries;
    try { entries = fs.readdirSync(d, { withFileTypes: true }); } catch { continue; }
    for (const e of entries) {
      const full = path.join(d, e.name);
      if (e.isDirectory()) stack.push(full);
      else if (e.isFile()) {
        if (/\.md$/i.test(e.name)) files.push(full);
        else other++;
      }
    }
  }
  files.sort();
  return { files, other, exists: true };
}

function splitFrontmatter(text) {
  const lines = text.split(/\r?\n/);
  if (lines[0].trim() !== '---') return { fmText: null, body: text };
  for (let i = 1; i < lines.length; i++) {
    if (lines[i].trim() === '---') {
      return { fmText: lines.slice(1, i).join('\n'), body: lines.slice(i + 1).join('\n') };
    }
  }
  return { fmText: null, body: text, unterminated: true };
}

function parseScalar(t) {
  t = t.trim();
  if (t.length > 1 && ((t[0] === '"' && t.endsWith('"')) || (t[0] === "'" && t.endsWith("'")))) {
    return t.slice(1, -1);
  }
  t = t.replace(/\s#.*$/, '');
  if (t === 'true') return true;
  if (t === 'false') return false;
  return t;
}

function parseYamlSubset(text) {
  const map = {};
  let key = null;
  let partial = false;
  for (const raw of text.split(/\r?\n/)) {
    if (!raw.trim()) continue;
    const li = raw.match(/^\s*-\s+(.*)$/);
    if (li) {
      if (key !== null && Array.isArray(map[key])) map[key].push(parseScalar(li[1]));
      else return { ok: false, reason: `list item outside an array ('${raw.trim()}')` };
      continue;
    }
    const kv = raw.match(/^([A-Za-z][A-Za-z0-9_-]*):\s*(.*)$/);
    if (kv) {
      key = kv[1];
      const v = kv[2].trim();
      if (v === '') { map[key] = []; continue; }
      if (v.startsWith('[')) {
        const m = v.match(/^\[(.*)\]\s*$/);
        if (!m) return { ok: false, reason: `malformed inline array for '${key}'` };
        map[key] = m[1] === '' ? [] : m[1].split(',').map(s => parseScalar(s));
      } else {
        map[key] = parseScalar(v);
      }
      continue;
    }
    if (/^\s/.test(raw)) { partial = true; continue; }
    return { ok: false, reason: `unparseable line '${raw.trim()}'` };
  }
  return { ok: true, map, partial };
}

function globToRegex(pattern) {
  const segs = pattern.split('/');
  let re = '';
  segs.forEach((seg, i) => {
    const last = i === segs.length - 1;
    if (seg === '**') {
      re += last ? '.*' : '(?:[^/]+/)*';
    } else {
      re += seg
        .replace(/[.+^${}()|[\]\\]/g, '\\$&')
        .replace(/\*/g, '[^/]*')
        .replace(/\?/g, '[^/]');
      if (!last) re += '/';
    }
  });
  try { return new RegExp('^' + re + '$'); } catch { return null; }
}

function userDisplayPath(file) {
  const home = os.homedir();
  return file.startsWith(home) ? '~' + file.slice(home.length) : file;
}

function auditRuleFile(add, file, rel) {
  let text;
  try { text = fs.readFileSync(file, 'utf8'); }
  catch (e) { add('ERROR', rel, 'cannot read file: ' + e.message); return null; }
  const rec = { rel, chars: text.length, trigger: null, alwaysApply: false, globs: [] };

  const { fmText, body, unterminated } = splitFrontmatter(text);
  if (unterminated) {
    add('ERROR', rel, 'frontmatter starts with --- but is never closed');
    return rec;
  }
  if (fmText === null) {
    add('WARN', rel, 'no frontmatter: activation trigger is undefined (rule may never activate). Add frontmatter with trigger/alwaysApply/paths');
    return rec;
  }

  const parsed = parseYamlSubset(fmText);
  if (!parsed.ok) {
    add('ERROR', rel, 'frontmatter could not be parsed: ' + parsed.reason);
    return rec;
  }
  const fm = parsed.map;
  if (parsed.partial) {
    add('WARN', rel, 'frontmatter uses nested/unsupported syntax; checks below may be incomplete — verify manually');
  }

  if (fm.trigger !== undefined && typeof fm.trigger !== 'string') {
    add('WARN', rel, 'trigger value is not a string');
  }
  let trigger = typeof fm.trigger === 'string' ? fm.trigger.trim() : null;
  let invalidTrigger = false;
  if (trigger && !VALID_TRIGGERS.includes(trigger)) {
    add('ERROR', rel, `invalid trigger '${trigger}' (expected one of: ${VALID_TRIGGERS.join(', ')})`);
    trigger = null;
    invalidTrigger = true;
  }

  const hasGlob = Array.isArray(fm.glob) ? fm.glob.length > 0 : typeof fm.glob === 'string' && fm.glob.trim() !== '';
  const hasPaths = Array.isArray(fm.paths) ? fm.paths.length > 0 : typeof fm.paths === 'string' && fm.paths.trim() !== '';
  const desc = typeof fm.description === 'string' ? fm.description.trim() : '';
  rec.alwaysApply = fm.alwaysApply === true;

  let effTrigger = trigger;
  if (!effTrigger && hasPaths) effTrigger = 'glob';
  if (!effTrigger && rec.alwaysApply) effTrigger = 'always_on';
  if (!effTrigger && !invalidTrigger) {
    add('WARN', rel, 'no trigger/alwaysApply/paths in frontmatter: activation is undefined — rule may never activate');
  }
  rec.trigger = effTrigger;

  const patterns = [];
  for (const src of [fm.glob, fm.paths]) {
    const list = Array.isArray(src) ? src : [src];
    for (const p of list) if (typeof p === 'string' && p.trim() !== '') patterns.push(p.trim());
  }
  rec.globs = patterns;

  if (trigger === 'glob' && !hasGlob && !hasPaths) {
    add('ERROR', rel, 'trigger: glob but no glob/paths pattern — rule body is never auto-injected (silent failure)');
  }
  if (trigger === 'model_decision' && !desc) {
    add('ERROR', rel, 'trigger: model_decision but no description — the model cannot decide to load this rule');
  } else if (trigger === 'model_decision' && desc.length < 20) {
    add('INFO', rel, `model_decision description is very short (${desc.length} chars); make it specific so the model can reliably decide relevance`);
  }
  if (rec.alwaysApply && trigger) {
    add('WARN', rel, `alwaysApply and trigger:${trigger} are both set — behavior is ambiguous; keep only one`);
  }
  if (rec.alwaysApply && (hasGlob || hasPaths)) {
    add('WARN', rel, 'alwaysApply and glob/paths are both set — behavior is ambiguous; keep only one');
  }
  if ((hasGlob || hasPaths) && trigger && trigger !== 'glob') {
    add('WARN', rel, `glob/paths patterns are present but trigger is '${trigger}' — the patterns may be ignored; use trigger: glob`);
  }
  if (hasGlob && hasPaths) {
    add('INFO', rel, 'both glob and paths are set — redundant; keep one');
  }
  if (body.trim().length === 0) {
    add('WARN', rel, 'rule body is empty — the rule does nothing');
  }
  return rec;
}

function evalGlobs(add, rec, scan, baseLabel) {
  for (const raw of rec.globs) {
    if (UNSUPPORTED_GLOB.test(raw)) {
      if (/\\/.test(raw)) {
        add('WARN', rec.rel, `glob '${raw}' uses backslash separators — will not match POSIX paths`);
      }
      add('INFO', rec.rel, `glob '${raw}' uses syntax this auditor cannot statically match; manually confirm it matches the intended files`);
      continue;
    }
    const p = raw.replace(/^\.\//, '').replace(/^\//, '');
    const re = globToRegex(p);
    if (!re) {
      add('INFO', rec.rel, `glob '${raw}' could not be converted to a matcher; manually confirm it matches the intended files`);
      continue;
    }
    const full = scan.files.filter(f => re.test(f)).length;
    const byBasename = !p.includes('/') ? scan.files.filter(f => re.test(f.split('/').pop())).length : null;
    if (full === 0 && (byBasename === null || byBasename === 0)) {
      const sev = scan.truncated ? 'INFO' : 'WARN';
      const note = scan.truncated ? ' (scan truncated at cap — verify manually)' : '';
      add(sev, rec.rel, `glob '${raw}' matches no files under ${baseLabel} (checked ${scan.files.length} files) → rule never triggers${note}`);
    } else if (full === 0 && byBasename > 0) {
      add('INFO', rec.rel, `glob '${raw}' matches 0 files by full path but ${byBasename} by basename — whether these trigger depends on Qoder's matcher; verify intent`);
    }
  }
}

function run() {
  const args = process.argv.slice(2);
  let base = null, projectRules = false, userRules = null;
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '--base') { if (i + 1 >= args.length) usage(); base = args[++i]; }
    else if (a === '--project-rules') projectRules = true;
    else if (a === '--user-rules') { if (i + 1 >= args.length) usage(); userRules = args[++i]; }
    else usage();
  }
  if (!base || (!projectRules && !userRules)) usage();
  base = path.resolve(base);
  try {
    if (!fs.statSync(base).isDirectory()) fail(`--base is not a directory: ${base}`);
  } catch { fail(`--base not found: ${base}`); }
  if (userRules) userRules = path.resolve(userRules.replace(/^~(?=\/|$)/, os.homedir()));

  const findings = [];
  const add = (sev, file, msg) => findings.push({ sev, file, msg });

  const scan = walkFiles(base);
  const scopes = [];
  if (projectRules) scopes.push({ label: 'project', dir: path.join(base, '.qoder', 'rules') });
  if (userRules) scopes.push({ label: 'user-level', dir: userRules });

  const recs = [];
  for (const s of scopes) {
    const { files, other, exists } = collectRules(s.dir);
    s.count = files.length;
    s.exists = exists;
    s.other = other;
    if (other > 0) {
      add('INFO', `[${s.label}]`, `${other} non-markdown file(s) in ${s.dir} are ignored (rules must be .md)`);
    }
    for (const f of files) {
      const rel = s.label === 'project' ? path.relative(base, f) : userDisplayPath(f);
      const rec = auditRuleFile(add, f, rel);
      if (rec) recs.push({ rec, scope: s });
    }
  }

  for (const { rec } of recs) {
    if (rec.globs.length > 0 && rec.trigger === 'glob') evalGlobs(add, rec, scan, base);
  }

  if (userRules && recs.some(r => r.scope.label === 'user-level' && r.rec.globs.length > 0 && r.rec.trigger === 'glob')) {
    add('INFO', '[user-level]', 'user-level glob patterns resolve relative to the CURRENT project root — a pattern may fire in one repo and never in another');
  }

  const totalChars = recs.reduce((n, r) => n + r.rec.chars, 0);
  const alwaysRecs = recs.filter(r => r.rec.trigger === 'always_on');
  const alwaysChars = alwaysRecs.reduce((n, r) => n + r.rec.chars, 0);

  if (totalChars > QUOTA) {
    add('ERROR', '[quota]', `total ${totalChars} chars exceeds the 100000-char limit — active rules will be truncated`);
  } else if (totalChars >= QUOTA * 0.8) {
    add('WARN', '[quota]', `total ${totalChars}/100000 chars (${Math.round(totalChars / QUOTA * 100)}%) — approaching the limit`);
  }
  if (alwaysChars >= 20000) {
    add('WARN', '[quota]', `always_on rules total ${alwaysChars} chars, paid on every turn — move detail to glob/model_decision rules (heuristic threshold: 20000)`);
  }

  const agentsPath = path.join(base, 'AGENTS.md');
  let agentsChars = 0;
  let agentsPresent = false;
  try {
    agentsChars = fs.readFileSync(agentsPath, 'utf8').length;
    agentsPresent = true;
  } catch { /* absent */ }

  const SEV_ORDER = { ERROR: 0, WARN: 1, INFO: 2 };
  findings.sort((a, b) => SEV_ORDER[a.sev] - SEV_ORDER[b.sev]);

  const out = [];
  out.push('=== RULES AUDIT (deterministic layer) ===');
  out.push('scope:');
  for (const s of scopes) {
    out.push(`  ${s.label}: ${s.dir} — ${s.count} rule file(s)` + (s.exists ? '' : ' (not found)'));
  }
  out.push(`  agents_md: ${agentsPath} — ${agentsPresent ? `present (${agentsChars} chars)` : 'absent'}`);
  out.push('stats:');
  out.push(`  scanned_files: ${scan.files.length} under ${base}${scan.truncated ? ' (scan truncated at cap — zero-match results downgraded)' : ''}`);
  out.push(`  total_chars: ${totalChars} / 100000 (${Math.round(totalChars / QUOTA * 100)}%)`);
  if (alwaysRecs.length > 0) {
    out.push(`  always_on_chars: ${alwaysChars} across ${alwaysRecs.length} file(s) — paid on every turn`);
  }
  out.push('');
  if (findings.length > 0) {
    out.push('findings:');
    for (const f of findings) out.push(`${f.sev.padEnd(5)} ${f.file}: ${f.msg}`);
    const ne = findings.filter(f => f.sev === 'ERROR').length;
    const nw = findings.filter(f => f.sev === 'WARN').length;
    const ni = findings.filter(f => f.sev === 'INFO').length;
    out.push('');
    out.push(`summary: ${ne} error(s), ${nw} warning(s), ${ni} info(s)`);
  } else {
    out.push('findings: none');
  }
  console.log(out.join('\n'));
}

try { run(); } catch (e) {
  process.stderr.write('audit_rules: internal error — ' + (e && e.message ? e.message : e) + '\n');
  process.exit(1);
}
