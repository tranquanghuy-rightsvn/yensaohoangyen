const {chromium}=require('playwright');
const EXE=process.env.HOME+'/Library/Caches/ms-playwright/chromium_headless_shell-1223/chrome-headless-shell-mac-arm64/chrome-headless-shell';
(async()=>{const b=await chromium.launch({executablePath:EXE});const p=await b.newPage({viewport:{width:+(process.env.W||1366),height:900}});
await p.goto(process.argv[2],{waitUntil:'networkidle',timeout:90000}).catch(()=>{});
const r=await p.evaluate(process.argv[3]);console.log(typeof r==='string'?r:JSON.stringify(r,null,1));await b.close()})();
