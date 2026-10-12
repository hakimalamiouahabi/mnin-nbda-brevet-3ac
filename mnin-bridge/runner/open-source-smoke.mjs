// Check ACTUAL installed npm components. No network access in this script.
import { chromium } from 'playwright';
import axe from 'axe-core';
import pixelmatch from 'pixelmatch';
import { PNG } from 'pngjs';
import sharp from 'sharp';
import { optimize } from 'svgo';

function assert(b, message) { if (!b) throw new Error(message); }
assert(typeof chromium.launch==='function','Playwright browser driver missing');
assert(typeof axe.source==='string' && axe.source.length>1000,'axe-core missing');
assert(typeof pixelmatch==='function','Pixelmatch missing');
assert(typeof PNG.sync.write==='function','PNGJS missing');
assert(typeof sharp==='function','Sharp missing');
const rgba=new PNG({width:2,height:2});
rgba.data.fill(255);
const original=PNG.sync.write(rgba);
const pixels=PNG.sync.read(original);
assert(pixels.width===2&&pixels.height===2,'PNGJS decode mismatch');
const diff=new PNG({width:2,height:2});
assert(pixelmatch(pixels.data,pixels.data,diff.data,2,2,{threshold:0.1})===0,'pixelmatch identity mismatch');
const meta=await sharp(original).metadata();
assert(meta.width===2&&meta.height===2,'Sharp metadata mismatch');
const svg=optimize('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"><rect x="0" y="0" width="10" height="10"/></svg>');
assert(typeof svg.data==='string'&&svg.data.includes('<svg'),'SVGO basic optimize failed');
console.log(JSON.stringify({
  status:'PASS',components:['playwright','axe-core','pixelmatch','pngjs','sharp','svgo'],
  checks:['APIs importable','pixelmatch identical PNG zero difference','sharp PNG metadata','SVGO derivative'],
  assurance:'Only npm modules tested, NOT an authenticated ChatGPT plugin or live WordPress connection'
},null,2));
