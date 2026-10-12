// Pixelmatch compare TWO existing PNG screenshots of exactly the SAME width/height.
// Usage: node compare-captures.mjs <baseline.png> <candidate.png> <output-diff.png>
// Local QA only. Never edits, deletes or upscales the official MNIN reference.
import fs from 'node:fs';
import path from 'node:path';
import { PNG } from 'pngjs';
import pixelmatch from 'pixelmatch';

const args=process.argv.slice(2);
if(args.length!==3)throw new Error('Need baseline, candidate and output path');
const safeInput=p=>{
  const absolute=path.resolve(p);
  if (!absolute.endsWith('.png') || !fs.existsSync(absolute)) throw new Error('Input must be an existing PNG');
  if(fs.statSync(absolute).size > 100*1024*1024)throw new Error('Input exceeds safe size');
  return absolute;
};
const [baselinePath,candidatePath]=args.slice(0,2).map(safeInput);
const out=path.resolve(args[2]);
if(!out.endsWith('.png')||out===baselinePath||out===candidatePath)throw new Error('Unsafe output filename');
const baseline=PNG.sync.read(fs.readFileSync(baselinePath));
const candidate=PNG.sync.read(fs.readFileSync(candidatePath));
if(baseline.width!==candidate.width||baseline.height!==candidate.height){
  throw new Error('BLOQUE: screenshots must have identical dimensions; never stretch the official baseline');
}
const diff=new PNG({width:baseline.width,height:baseline.height});
const changed=pixelmatch(baseline.data,candidate.data,diff.data,baseline.width,baseline.height,
  {threshold:0.1,includeAA:true});
const denominator=baseline.width*baseline.height;
fs.mkdirSync(path.dirname(out),{recursive:true});
fs.writeFileSync(out,PNG.sync.write(diff));
const record={baseline:path.basename(baselinePath),candidate:path.basename(candidatePath),
  output:path.basename(out),size:[baseline.width,baseline.height],
  changedPixels:changed,changedPercent:Number((100*changed/denominator).toFixed(4)),
  note:'Approximate raster comparison, not approval of pixel-perfect responsive reconstruction'};
process.stdout.write(JSON.stringify(record,null,2)+'\n');
