// MNIN Bridge BrowserLab v0.2: QA of checked-out HTML only; no live WordPress access.
import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

const entry = process.env.MNIN_HOME_PATH || '';
if (!/^(site|home|preview)\/[A-Za-z0-9._/-]+\.html$/.test(entry) || entry.includes('..') || entry.includes('//')) {
  throw new Error('BLOQUE: unapproved HTML path');
}
if (!fs.existsSync(entry)) throw new Error('BLOQUE: HTML missing in checkout: '+entry);
const mode=process.env.MNIN_QA_MATRIX || 'smoke';
if (!['smoke','full'].includes(mode)) throw new Error('Invalid matrix mode');
const matrix=[
['desktop-4k',3840,2160],['desktop-xl',1920,1080],['desktop-large',1600,900],
['laptop-large',1536,864],['laptop-15-16',1440,900],['laptop-standard',1366,768],
['laptop-compact',1280,800],['laptop-small',1280,720],
['tablet-13',1032,1376],['tablet-129',1024,1366],
['tablet-11',834,1194],['tablet-10-11',820,1180],
['tablet-classic',768,1024],['tablet-small',600,960],
['mobile-xl',430,932],['mobile-large',412,915],
['mobile-intermediate',393,852],['mobile-medium',390,844],
['mobile-standard',375,812],['mobile-compact',360,800],['mobile-small',320,568]
];
const smoke=new Set(['desktop-xl','laptop-compact','tablet-11','mobile-medium','mobile-small']);
const cases=mode==='full'?matrix:matrix.filter(x=>smoke.has(x[0]));
const folder=path.resolve('mnin-bridge-qa-results');
fs.mkdirSync(folder,{recursive:true});
const route=entry.split('/').map(encodeURIComponent).join('/');
const browser=await chromium.launch({headless:true});
const tests=[];
let failures=0;
try {
 for(const [name,width,height] of cases){
  const page=await browser.newPage({viewport:{width,height},deviceScaleFactor:1,reducedMotion:'reduce'});
  const errors=[];
  page.on('pageerror',e=>errors.push(String(e.message)));
  const start=Date.now();
  try{
   await page.goto('http://127.0.0.1:8765/'+route,{waitUntil:'networkidle',timeout:30000});
   await page.evaluate(async()=>{if(document.fonts)await document.fonts.ready;});
   const metrics=await page.evaluate(()=>{
     const images=[...document.images].map(img=>({
       file:img.currentSrc.split('/').pop()?.split('?')[0]||'',
       loaded:img.complete&&img.naturalWidth>0,
       nativeWidth:img.naturalWidth,
       renderedWidth:img.getBoundingClientRect().width,
       raster:/\.(png|jpe?g|webp)(?:\?|$)/i.test(img.currentSrc)
     }));
     return {
       contentWidth:document.documentElement.scrollWidth,
       viewportWidth:innerWidth,
       pageHeight:document.documentElement.scrollHeight,
       h1:document.querySelector('h1')?.textContent?.trim()||'',
       imageCount:images.length,
       brokenImages:images.filter(i=>!i.loaded).map(i=>i.file),
       densityWarnings:images.filter(i=>i.loaded&&i.raster&&i.renderedWidth>24&&i.nativeWidth<i.renderedWidth*2)
         .map(i=>({file:i.file,nativeWidth:i.nativeWidth,displayWidth:Math.round(i.renderedWidth)}))
     };
   });
   const overflow=metrics.contentWidth>metrics.viewportWidth+1;
   const pass=!overflow&&!metrics.brokenImages.length&&!errors.length&&!!metrics.h1;
   if(!pass)failures++;
   await page.screenshot({path:path.join(folder,name+'-'+width+'x'+height+'-viewport.png')});
   await page.screenshot({path:path.join(folder,name+'-'+width+'-full-page.png'),fullPage:true});
   tests.push({name,width,height,status:pass?'PASS':'FAIL',overflow,errors,...metrics,durationMs:Date.now()-start});
  }catch(e){failures++;tests.push({name,width,height,status:'FAIL',error:String(e.message)});}
  finally{await page.close();}
 }
}finally{await browser.close();}
fs.writeFileSync(path.join(folder,'report.json'),JSON.stringify({
 version:'0.2.0',mode,total:tests.length,failures,status:failures?'FAIL':'PASS',
 source:entry,tests,
 disclaimer:'Structural QA only; does not certify visual fidelity, accessibility or Core Web Vitals.'
},null,2));
if(failures)process.exitCode=1;
