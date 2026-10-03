// usage: node shot.cjs <url> <out-prefix> <width> [--sections]
const {chromium}=require('playwright');
const fs=require('fs');
const EXE=process.env.HOME+'/Library/Caches/ms-playwright/chromium_headless_shell-1223/chrome-headless-shell-mac-arm64/chrome-headless-shell';
(async()=>{
  const [url,out,w]=process.argv.slice(2);
  const b=await chromium.launch({executablePath:EXE});
  const p=await b.newPage({viewport:{width:+w,height:900},deviceScaleFactor:1});
  await p.goto(url,{waitUntil:'networkidle',timeout:90000}).catch(()=>{});
  // kill popups/floating widgets for stable diffs
  await p.addStyleTag({content:'.popup-coupon,.chat-social-button,.pv-contact-box,.pv-mobile-toggle,#phongvt-contact-footer-outer,.backdrop__body-backdrop___1rvky,.dt-popup-main,.mfp-wrap,.mfp-bg,.fixed-widgets,.float-contact,.back-top,.fab,.mbar,.toast{display:none!important} *{animation-duration:0s!important;transition:none!important} iframe{visibility:hidden!important} [data-animate]{opacity:1!important;transform:none!important;filter:none!important}'});
  const H=await p.evaluate(()=>document.documentElement.scrollHeight);
  for(let y=0;y<H;y+=300){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(250);}
  await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(2500);
  const boxes=await p.evaluate(()=>{
    const out=[];const hd=document.querySelector('.site-header')||document.querySelector('header');if(hd)out.push({n:'header',y:hd.getBoundingClientRect().top+scrollY,h:hd.offsetHeight});
    let root=document.querySelector('#content')||document.querySelector('main'); while(root&&root.id==='content'&&root.children.length===1) root=root.children[0]; if(root&&root.id==='content'){} 
    if(root)[...root.children].forEach((e,i)=>{if(e.offsetHeight>30)out.push({n:'s'+String(i).padStart(2,'0'),y:e.getBoundingClientRect().top+scrollY,h:e.offsetHeight})});
    const f=document.querySelector('.site-footer')||document.querySelector('footer');if(f)out.push({n:'footer',y:f.getBoundingClientRect().top+scrollY,h:f.offsetHeight});
    return out;});
  await p.screenshot({path:out+'-full.png',fullPage:true});
  fs.writeFileSync(out+'-boxes.json',JSON.stringify(boxes,null,1));
  console.log(H, JSON.stringify(boxes));
  await b.close();
})();
