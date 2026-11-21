import { existsSync, readFileSync, statSync } from 'node:fs';
import { resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

// Zero-dependency check for the GitHub profile's own visual references.
// External HTTP links are deliberately not fetched by CI.
export function referencedAssets(markdown) {
  const found = new Set();
  for (const match of markdown.matchAll(/\b(?:src|srcset|href)=["']([^"']+)["']/g)) {
    for (const part of match[1].split(',')) {
      const src = part.trim().split(/\s+/)[0];
      if (src.startsWith('assets/')) found.add(src);
    }
  }
  for (const match of markdown.matchAll(/\]\((assets\/[^)\s]+)\)/g)) {
    found.add(match[1]);
  }
  return [...found].sort();
}

export function auditAssetReferences(markdown, repoRoot) {
  const assetsRoot = resolve(repoRoot, 'assets');
  const names = referencedAssets(markdown);
  if (!names.length) throw new Error('No profile visual references found: check README parsing or accidental removal.');
  const invalid = [];
  const missing = [];
  const kinds = {};
  for (const name of names) {
    if (!/^assets\/[a-zA-Z0-9_./-]+\.(?:svg|webp|png|jpe?g|avif|gif)$/i.test(name)) {
      invalid.push(name);
      continue;
    }
    const file = resolve(repoRoot, name);
    // A path containing assets/../ or a traversal must not pass the audit.
    if (!file.startsWith(assetsRoot + sep)) {
      invalid.push(name);
      continue;
    }
    if (!existsSync(file) || !statSync(file).isFile()) {
      missing.push(name);
      continue;
    }
    const ext = name.slice(name.lastIndexOf('.') + 1).toLowerCase();
    kinds[ext] = (kinds[ext] ?? 0) + 1;
  }
  return { checked: names.length, present: names.length - invalid.length - missing.length, invalid, missing, kinds };
}

const invoked = process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url);
if (invoked) {
  const root = resolve(fileURLToPath(new URL('..', import.meta.url)));
  const markdown = readFileSync(resolve(root, 'README.md'), 'utf8');
  const result = auditAssetReferences(markdown, root);
  console.log('PROFILE ASSET AUDIT: ' + result.present + '/' + result.checked + ' files exist; types=' + JSON.stringify(result.kinds));
  if (result.invalid.length || result.missing.length) {
    for (const x of result.invalid) console.error('Invalid asset reference: ' + x);
    for (const x of result.missing) console.error('Missing asset reference: ' + x);
    process.exitCode = 1;
  }
}
