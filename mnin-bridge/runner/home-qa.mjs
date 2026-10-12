// QA on a locally served checkout, not on WordPress production.
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

const entry = process.env.MNIN_HOME_PATH || '';
if (!/^(site|home|preview)\/[A-Za-z0-9._/-]+\.html$/.test(entry) || entry.includes('..')) {
  throw new Error('Expected approved, repository-relative Home HTML path');
}
if (!fs.existsSync(entry)) {
  throw new Error('BLOQUE: Home HTML not present in the checked-out branch: ' + entry);
}
const output = path.resolve('mnin-bridge-qa-results');
fs.mkdirSync(output, {recursive: true});
const viewports = [
  {name:'desktop-xl', width:1920,height:1080},
  {name:'laptop-compact',width:1280,height:800},
  {name:'tablet-11',width:834,height:1194},
  {name:'mobile-medium',width:390,height:844},
  {name:'mobile-small',width:320,height:568}
];
const browser = await chromium.launch({headless:true});
let problems = 0;
const cases = [];
try {
  for (const size of viewports) {
    const page = await browser.newPage({viewport:{width:size.width,height:size.height},deviceScaleFactor:1});
    const errors = [];
    page.on('pageerror',error => errors.push(error.message));
    const route = entry.split('/').map(encodeURIComponent).join('/');
    await page.goto('http://127.0.0.1:8765/' + route,{waitUntil:'networkidle',timeout:30000});
    await page.screenshot({path:path.join(output,size.name+'-'+size.width+'x'+size.height+'.png')});
    await page.screenshot({path:path.join(output,size.name+'-'+size.width+'-full.png'),fullPage:true});
    const metrics=await page.evaluate(()=>({
      scrollWidth:document.documentElement.scrollWidth,
      viewportWidth:window.innerWidth,
      scrollHeight:document.documentElement.scrollHeight,
      brokenImages:Array.from(document.images).filter(img=>!img.complete||!img.naturalWidth).length,
      mainHeading:document.querySelector('h1')?.textContent?.trim() || ''
    }));
    const overflow=metrics.scrollWidth>metrics.viewportWidth+1;
    const passed=errors.length===0 && !overflow && metrics.brokenImages===0;
    if(!passed) problems++;
    cases.push({size,passed,overflow,errors,...metrics});
    await page.close();
  }
} finally {
  await browser.close();
}
fs.writeFileSync(path.join(output,'qa-report.json'),JSON.stringify({
  generator:'MNIN Bridge 0.1',
  source:entry,
  status:problems===0?'PASS':'FAIL',
  caveat:'No claim of pixel-perfect similarity, physical-device coverage or WCAG certification',
  cases
},null,2));
if(problems) process.exitCode=1;
