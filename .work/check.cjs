const {chromium}=require('playwright');
const EXE=process.env.HOME+'/Library/Caches/ms-playwright/chromium_headless_shell-1223/chrome-headless-shell-mac-arm64/chrome-headless-shell';
(async()=>{const b=await chromium.launch({executablePath:EXE});const r=[],errs=[];
for(const w of [375,768,1366,1920]){const p=await b.newPage({viewport:{width:w,height:900}});p.on('pageerror',e=>errs.push(w+' '+e.message));p.on('requestfailed',q=>errs.push('FAIL '+q.url()));
await p.goto('http://127.0.0.1:8934/',{waitUntil:'networkidle'});
const o=await p.evaluate(()=>{const W=innerWidth;const bad=[];document.querySelectorAll('body *').forEach(e=>{const r=e.getBoundingClientRect();if(r.width&&(r.right>W+1||r.left<-1)){let q=e.parentElement,clip=false;while(q&&q!==document.body){if(getComputedStyle(q).overflowX!=='visible'){clip=true;break}q=q.parentElement}if(!clip)bad.push(e.tagName+'.'+(e.className+'').slice(0,30))}});
// text clipping inside buttons
const clipped=[...document.querySelectorAll('.btn,.tab,.card-title,h1,h2,h3')].filter(e=>e.scrollWidth>e.clientWidth+2&&getComputedStyle(e).overflow!=='visible').map(e=>e.className+':'+e.textContent.trim().slice(0,30));
return {sw:document.documentElement.scrollWidth,bad:bad.slice(0,6),clipped:clipped.slice(0,6),broken:[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src)}});
r.push(w+' '+JSON.stringify(o));
if(w===375){await p.click('.menu-btn');await p.waitForTimeout(400);r.push('drawer '+await p.$eval('#drawer',e=>e.className));await p.click('.drawer-head button');await p.waitForTimeout(400);}
if(w===1366){await p.click('.tab[data-tab=yen-to]');r.push('tab panel on: '+await p.$eval('.panel.on',e=>e.dataset.panel));
await p.click('.panel.on .card .add');await p.waitForTimeout(300);r.push('cart '+await p.$eval('[data-cart-count]',e=>e.textContent)+' toast '+await p.$eval('.toast',e=>e.className));
await p.click('[data-search-open]');await p.waitForTimeout(300);r.push('search '+await p.$eval('#search',e=>e.className));await p.keyboard.press('Escape');
await p.hover('.nav-drop>button');await p.waitForTimeout(400);r.push('mega '+await p.$eval('.mega',e=>getComputedStyle(e).visibility));
await p.$eval('#qua-bieu',e=>e.scrollIntoView());await p.click('#qua-bieu [data-next]');await p.waitForTimeout(800);r.push('gift slider '+await p.$eval('#qua-bieu .track',e=>e.scrollLeft));
r.push('header '+await p.$eval('.header',e=>e.className));}
await p.close()}
console.log(r.join('\n'));console.log('errs',errs);await b.close()})();
