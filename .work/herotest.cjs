const {chromium}=require('playwright');
const EXE=process.env.HOME+'/Library/Caches/ms-playwright/chromium_headless_shell-1223/chrome-headless-shell-mac-arm64/chrome-headless-shell';
(async()=>{const b=await chromium.launch({executablePath:EXE});
for(const w of [1366,1920,768,375]){const p=await b.newPage({viewport:{width:w,height:900}});await p.goto('http://127.0.0.1:8934/',{waitUntil:'networkidle'});
await p.screenshot({path:`shots/hero-${w}.png`,clip:{x:0,y:0,width:w,height:Math.min(900,w<641?720:w*0.62)}});
const vis=w<641?'.hb-m':'.hb-d';await p.click(vis+' .hb-dots button:nth-child(2)');await p.waitForTimeout(900);
console.log(w,'slide after dot2:',await p.$eval(vis+' .hb-track',e=>Math.round(e.scrollLeft/e.clientWidth)),'sw',await p.evaluate(()=>document.documentElement.scrollWidth));await p.close()}
await b.close()})();
