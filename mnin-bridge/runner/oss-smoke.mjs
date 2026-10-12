// Integration smoke on generated PUBLIC fixtures only. Not WordPress, not user assets.
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { HtmlValidate } from 'html-validate';
import { optimize } from 'svgo';
import sharp from 'sharp';
import prettier from 'prettier';

const root = process.cwd();
const fixtureHtml = path.resolve(root, 'preview/oss-smoke.html');
const fixtureSvg = path.resolve(root, 'preview/oss-smoke.svg');
const output = path.resolve(root, 'mnin-bridge-qa-results');
fs.mkdirSync(output, { recursive: true });

const html = fs.readFileSync(fixtureHtml, 'utf8');
const originalSvg = fs.readFileSync(fixtureSvg);
const sha256 = data => createHash('sha256').update(data).digest('hex');

const checks = [];
async function check(id, fn) {
  try {
    const details = await fn();
    checks.push({ id, status: 'PASS', ...details });
  } catch (error) {
    checks.push({ id, status: 'FAIL', error: String(error.message || error).slice(0, 1000) });
  }
}

await check('html_validate', async () => {
  const validator = new HtmlValidate({
    extends: ['html-validate:recommended'],
    rules: {
      // A fixed public fixture is validated against the exact selected rules.
      'prefer-button': 'off'
    }
  });
  const result = await validator.validateString(html, fixtureHtml);
  if (!result.valid) {
    const messages = result.results.flatMap(item => item.messages)
      .slice(0, 20).map(({ ruleId, message, line }) => ({ ruleId, message, line }));
    throw new Error('HTML-Validate rejected synthetic fixture: ' + JSON.stringify(messages));
  }
  return { valid: true, validatorResults: result.results.length };
});

await check('prettier', async () => {
  const formatted = await prettier.format(html, { parser: 'html', printWidth: 100 });
  if (!formatted.includes('Validation open source')) throw new Error('Formatter lost fixture text');
  return { formattedBytes: Buffer.byteLength(formatted), originalSha256: sha256(html) };
});

await check('svgo', async () => {
  const cleaned = optimize(originalSvg.toString('utf8'), { multipass: true });
  if (typeof cleaned.data !== 'string' || !cleaned.data.includes('<svg')) {
    throw new Error('SVGO did not return a vector');
  }
  return { beforeBytes: originalSvg.length, afterBytes: Buffer.byteLength(cleaned.data),
           originalSha256: sha256(originalSvg), originalsModified: false };
});

await check('sharp', async () => {
  const meta = await sharp(originalSvg, { limitInputPixels: 25000000 }).metadata();
  if (meta.width !== 480 || meta.height !== 320) throw new Error('Unexpected vector dimensions');
  const png = await sharp(originalSvg, { limitInputPixels: 25000000 }).resize(480, 320).png().toBuffer();
  if (png.length < 100) throw new Error('Raster preview is unexpectedly small');
  return { nativeWidth: meta.width, nativeHeight: meta.height,
           temporaryPreviewBytes: png.length, originalSha256: sha256(originalSvg),
           originalsModified: false };
});

const result = {
  project: 'MNIN Bridge Pro',
  version: '0.8.0',
  source: 'SYNTHETIC_PUBLIC_FIXTURE_ONLY',
  checks,
  passed: checks.filter(x => x.status === 'PASS').length,
  failed: checks.filter(x => x.status === 'FAIL').length,
  disclaimer: 'Does not attest production quality, security, WCAG compliance or live WordPress.'
};
fs.writeFileSync(path.join(output, 'oss-tools-report.json'), JSON.stringify(result, null, 2));
console.log(JSON.stringify({ passed: result.passed, failed: result.failed, checks: checks.map(x => ({ id: x.id, status: x.status })) }));
if (result.failed) process.exitCode = 1;
