// node crop.cjs in.png out.png y h [x w]
const {PNG}=require('pngjs');const fs=require('fs');
const [i,o,y,h,x=0,w]=process.argv.slice(2);const src=PNG.sync.read(fs.readFileSync(i));
const W=w?+w:src.width-+x;const Y=Math.round(+y);const Hh=Math.min(Math.round(+h),src.height-Y);
const d=new PNG({width:W,height:Hh});PNG.bitblt(src,d,+x,Y,W,Hh,0,0);fs.writeFileSync(o,PNG.sync.write(d));
