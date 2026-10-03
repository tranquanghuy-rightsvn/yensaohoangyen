const {chromium}=require('playwright');
const EXE=process.env.HOME+'/Library/Caches/ms-playwright/chromium_headless_shell-1223/chrome-headless-shell-mac-arm64/chrome-headless-shell';
(async()=>{const b=await chromium.launch({executablePath:EXE});
for(const w of [1366,1920]){const p=await b.newPage({viewport:{width:w,height:900}});await p.goto('http://127.0.0.1:8934/',{waitUntil:'networkidle'});
await p.hover('.nav-l .mega-host>button');await p.waitForTimeout(500);await p.screenshot({path:`shots/mega-shop-${w}.png`,clip:{x:0,y:0,width:w,height:560}});
// move mouse down into mega to test hover bridge
const box=await p.$eval('.nav-l .mega',e=>{const r=e.getBoundingClientRect();return [r.x+r.width/2,r.y+60]});await p.mouse.move(box[0],box[1],{steps:8});await p.waitForTimeout(300);
console.log(w,'still open after move:',await p.$eval('.nav-l .mega',e=>getComputedStyle(e).visibility));
await p.hover('.nav-r .mega-host>button');await p.waitForTimeout(500);await p.screenshot({path:`shots/mega-gift-${w}.png`,clip:{x:0,y:0,width:w,height:520}});await p.close()}
const m=await b.newPage({viewport:{width:375,height:800}});await m.goto('http://127.0.0.1:8934/',{waitUntil:'networkidle'});await m.click('.menu-btn');await m.waitForTimeout(500);await m.screenshot({path:'shots/drawer-375.png'});
console.log('sw',await m.evaluate(()=>document.documentElement.scrollWidth));await b.close()})();
