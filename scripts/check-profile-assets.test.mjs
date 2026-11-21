import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { auditAssetReferences, referencedAssets } from './check-profile-assets.mjs';

test('extracts HTML src/srcset and Markdown assets without duplicates', () => {
  const text = '<img src="assets/a.svg"><source srcset="assets/b.webp 1x, assets/c.webp 2x">'
    + '[cover](assets/a.svg) <a href="https://example.com">external</a>';
  assert.deepEqual(referencedAssets(text), ['assets/a.svg', 'assets/b.webp', 'assets/c.webp']);
});

test('present local visuals produce an auditable count by format', () => {
  const root = mkdtempSync(join(tmpdir(), 'profile-assets-'));
  try {
    mkdirSync(join(root, 'assets'));
    writeFileSync(join(root, 'assets', 'a.svg'), '<svg/>');
    writeFileSync(join(root, 'assets', 'b.webp'), 'synthetic');
    const result = auditAssetReferences('<img src="assets/a.svg"><img src="assets/b.webp">', root);
    assert.equal(result.checked, 2);
    assert.equal(result.present, 2);
    assert.deepEqual(result.kinds, { svg: 1, webp: 1 });
  } finally { rmSync(root, { recursive: true, force: true }); }
});

test('missing asset is not silently treated as success', () => {
  const root = mkdtempSync(join(tmpdir(), 'profile-assets-'));
  try {
    const result = auditAssetReferences('<img src="assets/missing.svg">', root);
    assert.equal(result.present, 0);
    assert.deepEqual(result.missing, ['assets/missing.svg']);
  } finally { rmSync(root, { recursive: true, force: true }); }
});

test('rejects assets/../ path escapes and unsupported extensions', () => {
  const root = mkdtempSync(join(tmpdir(), 'profile-assets-'));
  try {
    const result = auditAssetReferences('<img src="assets/../private.svg"><img src="assets/shell.exe">', root);
    assert.equal(result.present, 0);
    assert.equal(result.invalid.length, 2);
  } finally { rmSync(root, { recursive: true, force: true }); }
});

test('unexpected removal of every visual reference fails closed', () => {
  assert.throws(() => auditAssetReferences('No referenced visuals', '/tmp'), /No profile visual references/);
});
