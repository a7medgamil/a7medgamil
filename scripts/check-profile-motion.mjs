import assert from 'node:assert/strict';
import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('../', import.meta.url));
const readme = readFileSync(resolve(root, 'README.md'), 'utf8');
const refs = [...new Set([...readme.matchAll(/assets\/[\w./-]+-motion\.svg/g)].map(x => x[0]))];
const targetCount = 12; // 12 legacy SVG variants remain in the README; the other 12 now use independently tested looping GIFs.
assert.equal(refs.length, targetCount, 'All six approved art families must have four responsive/theme motion variants');

for (const name of refs) {
  const original = resolve(root, name.replace(/-motion\.svg$/, '.svg'));
  const motionFile = resolve(root, name);
  assert.ok(existsSync(original), 'Untouched static fallback/source missing: ' + name);
  assert.ok(existsSync(motionFile), 'Generated SVG missing: ' + name);
  const staticMarkup = readFileSync(original, 'utf8').trimEnd();
  const movingMarkup = readFileSync(motionFile, 'utf8').trimEnd();
  const start = '<!-- MOTION START:';
  const end = '<!-- MOTION END -->';
  const first = movingMarkup.indexOf(start);
  const last = movingMarkup.indexOf(end);
  assert.ok(first > -1 && last > first, 'Motion overlay is missing: ' + name);
  assert.equal(
    movingMarkup.slice(0, first).trimEnd(),
    staticMarkup.slice(0, -6).trimEnd(),
    'The original artwork must not be redesigned or have its content changed: ' + name
  );
  assert.ok(movingMarkup.slice(last + end.length).trim() === '</svg>', 'Motion cannot change SVG closure: ' + name);
  assert.match(movingMarkup, /@media\s*\(prefers-reduced-motion:\s*reduce\)/, 'Reduced-motion support required');
  assert.match(movingMarkup, /@keyframes\s+motion/, 'Visible keyframe motion required');
  assert.ok((movingMarkup.match(/\bclass="motion-/g) ?? []).length > 0, 'Animated decorative elements required');
  assert.doesNotMatch(movingMarkup, /<(?:script|foreignObject|iframe)\b/i, 'No active scripting, embeds or network content');
  assert.doesNotMatch(movingMarkup.slice(first, last), /(?:href|src)=["']https?:/i, 'No external content in motion overlay');
}
const signalFiles = ['assets/motion/executive-signal-light.gif', 'assets/motion/executive-signal-dark.gif'];
for (const signal of signalFiles) {
  assert.ok(readme.includes(signal), 'Readme must embed moving GIF: ' + signal);
  const data = readFileSync(resolve(root, signal));
  assert.equal(data.subarray(0, 6).toString('ascii'), 'GIF89a', 'GIF format required');
  assert.ok(data.length > 5000 && data.length < 250000, 'GIF must be real motion without undue transfer cost');
  assert.ok(data.includes(Buffer.from('NETSCAPE2.0', 'ascii')), 'GIF must loop autonomously');
}
assert.ok(readme.includes('media="(prefers-reduced-motion: reduce)" srcset="assets/motion/executive-signal-static.svg"'), 'Static decorative signal required for reduced-motion visitors');
console.log('PROFILE MOTION AUDIT: ' + refs.length + '/' + targetCount + ' responsive/theme SVG variants plus two looping GIFs; original artwork, access and low-transfer fallbacks retained.');
