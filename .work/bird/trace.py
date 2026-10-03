import cv2, numpy as np
img=cv2.imread('../../images/chim-yen-vector-03.jpg',cv2.IMREAD_GRAYSCALE)
img=cv2.resize(img,None,fx=3,fy=3,interpolation=cv2.INTER_CUBIC)   # trace ở độ phân giải cao cho mượt
_,bw=cv2.threshold(img,110,255,cv2.THRESH_BINARY_INV)
bw=cv2.morphologyEx(bw,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
cnts,hier=cv2.findContours(bw,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)
x,y,w,h=cv2.boundingRect(max(cnts,key=cv2.contourArea))
S=48/max(w,h); ox=(48-w*S)/2-x*S; oy=(48-h*S)/2-y*S
def path(c):
    c=cv2.approxPolyDP(c,1.8,True)[:,0,:].astype(float)
    if len(c)<3: return ''
    p=[(px*S+ox,py*S+oy) for px,py in c]; n=len(p)
    d=f'M{p[0][0]:.2f},{p[0][1]:.2f}'
    for i in range(n):   # Catmull-Rom -> cubic Bezier
        p0,p1,p2,p3=p[i-1],p[i],p[(i+1)%n],p[(i+2)%n]
        t=0.16
        c1=(p1[0]+(p2[0]-p0[0])*t,p1[1]+(p2[1]-p0[1])*t); c2=(p2[0]-(p3[0]-p1[0])*t,p2[1]-(p3[1]-p1[1])*t)
        d+=f'C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}'
    return d+'Z'
ds=[path(c) for c in cnts if cv2.contourArea(c)>40]
d=''.join(ds)
open('swallow.d','w').write(d)
print(len(ds),'subpaths',len(d),'chars')
open('trace.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="480" height="480"><rect width="48" height="48" fill="#fbf3e4"/><path fill="#b48a45" fill-rule="evenodd" d="{d}"/></svg>')
