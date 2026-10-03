const {chromium}=require('playwright');
(async()=>{const [w,out]=process.argv.slice(2);const b=await chromium.launch({executablePath:process.env.HOME+'/Library/Caches/ms-playwright/chromium_headless_shell-1223/chrome-headless-shell-mac-arm64/chrome-headless-shell'});
const p=await b.newPage({viewport:{width:+w,height:1200}});await p.goto('http://localhost:8008/?v='+Date.now(),{waitUntil:'networkidle'});
await p.addStyleTag({content:'html{scroll-behavior:auto!important}.reveal{opacity:1!important;transform:none!important}*{animation:none!important;transition:none!important}.fab,.mbar{display:none!important}'});
await p.evaluate(()=>document.querySelectorAll('[data-hero] .hb-track').forEach(t=>t.scrollLeft=0));
const H=await p.evaluate(()=>document.documentElement.scrollHeight);for(let y=0;y<H;y+=900){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(60)}await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(800);
await p.screenshot({path:out,fullPage:true});console.log(w,'H',H,'sw',await p.evaluate(()=>document.documentElement.scrollWidth));await b.close()})();
