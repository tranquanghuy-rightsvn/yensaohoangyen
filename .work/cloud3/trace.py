"""Trace 6 đám mây từ 7e938263...jpg -> các lớp: outline(viền đậm), body(thân), shade(bóng đậm), hi(highlight trắng)."""
import cv2, numpy as np, json
img = cv2.imread('../../images/7e938263ddf1aa79ec1438041c2b562f.jpg')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV); H, S, V = cv2.split(hsv)
dark = ((V < 90)).astype(np.uint8) * 255                      # viền xanh đen
cloud = ((S > 40) | (V < 90)).astype(np.uint8) * 255          # toàn bộ đám mây (không phải nền trắng)
cloud = cv2.morphologyEx(cloud, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
filled = np.zeros_like(cloud)
cnts, _ = cv2.findContours(cloud, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cnts = sorted([c for c in cnts if cv2.contourArea(c) > 5000], key=lambda c: cv2.boundingRect(c)[1])
inner_body = ((S > 40) & (V >= 90)).astype(np.uint8) * 255    # vùng màu bên trong viền
# bóng = các vùng tối hơn trong thân (V thấp hơn trung vị của đám)
hi = ((S < 40) & (V > 225)).astype(np.uint8) * 255            # vệt trắng bên trong mây

def path(c, eps=1.6):
    c = cv2.approxPolyDP(c, eps, True)[:, 0, :].astype(float); n = len(c)
    if n < 3: return ''
    d = f'M{c[0][0]:.1f},{c[0][1]:.1f}'
    for i in range(n):
        p0, p1, p2, p3 = c[i-1], c[i], c[(i+1) % n], c[(i+2) % n]; t = .17
        c1 = p1 + (p2 - p0) * t; c2 = p2 - (p3 - p1) * t
        d += f'C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}'
    return d + 'Z'

out = []
for c in cnts:
    x, y, w, h = cv2.boundingRect(c)
    m = np.zeros_like(cloud); cv2.drawContours(m, [c], -1, 255, -1)
    body = cv2.bitwise_and(inner_body, m); body = cv2.morphologyEx(body, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    vals = V[body > 0]; thr = np.percentile(vals, 45)
    shade = ((V < thr) & (body > 0)).astype(np.uint8) * 255
    shade = cv2.GaussianBlur(shade, (0, 0), 4); _, shade = cv2.threshold(shade, 127, 255, cv2.THRESH_BINARY)
    shade = cv2.morphologyEx(shade, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))
    hm = cv2.bitwise_and(hi, cv2.erode(m, np.ones((9, 9), np.uint8))); hm = cv2.morphologyEx(hm, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    def paths(mask, mina):
        cs, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        return ''.join(path(k) for k in cs if cv2.contourArea(k) > mina)
    bc, _ = cv2.findContours(body, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    out.append(dict(box=[x, y, w, h], outline=path(c), body=''.join(path(k) for k in bc if cv2.contourArea(k) > 400),
                    shade=paths(shade, 250), hi=paths(hm, 30)))
json.dump(out, open('clouds.json', 'w'))
print([o['box'] for o in out], [len(o['outline']) + len(o['body']) + len(o['shade']) + len(o['hi']) for o in out])
