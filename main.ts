// news-image-20261126 entry (Node 22, standard library only).
// The image is entry.png beside this file, rendered at build time by
// tools/draw_frontpage.py. This program copies it to <outDir>/entry.png
// and validates the PNG first, so a bad image can never be submitted.
//
// The output directory comes from argv[2] (the grader passes it), or
// from MAKEFUN_OUTPUT_DIR for local runs, or /output as a last resort.
// Nothing is deleted, nothing is fetched, no network is used.

import { copyFileSync, readFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const SRC = new URL('./entry.png', import.meta.url);
const outDir = process.argv[2] || process.env.MAKEFUN_OUTPUT_DIR || '/output';
const dest = join(outDir, 'entry.png');

const buf = readFileSync(SRC);

// Validate: PNG signature, IHDR dimensions, size limit, trailing IEND.
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (buf.length < 33 || !buf.subarray(0, 8).equals(PNG_SIG)) {
  throw new Error('entry.png: not a PNG');
}
if (buf.length > 1048576) {
  throw new Error(`entry.png: ${buf.length} bytes exceeds 1 MiB`);
}
const width = buf.readUInt32BE(16);
const height = buf.readUInt32BE(20);
if (width > 1024 || height > 1024 || width === 0 || height === 0) {
  throw new Error(`entry.png: ${width}x${height} exceeds 1024x1024`);
}
const IEND = Buffer.from([0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82]);
if (!buf.subarray(buf.length - 8).equals(IEND)) {
  throw new Error('entry.png: truncated PNG (no IEND)');
}

mkdirSync(outDir, { recursive: true });
copyFileSync(SRC, dest);
console.log(`wrote ${dest} (${buf.length} bytes, ${width}x${height})`);
