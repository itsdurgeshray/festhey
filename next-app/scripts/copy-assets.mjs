// Copies the shared design-system assets (css, js, images, icons) from the static site into public/assets.
import { cpSync, rmSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
const here = dirname(fileURLToPath(import.meta.url));
const from = resolve(here, '../../assets');
const to = resolve(here, '../public/assets');
if (existsSync(to)) rmSync(to, { recursive: true });
cpSync(from, to, { recursive: true, filter: s => !s.includes('/src') });
console.log('assets copied to public/assets');
