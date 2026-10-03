"""Mây cát tường (tường vân) – họa tiết mây cuộn cung đình, nét vàng đồng mảnh. Sinh images/bg-clouds.svg"""
import math
GOLD, BODY = '#c9a35f', '#fffaf0'

def spiral(cx, cy, r0, r1, turns, start, cw=True, n=60):
    """Xoắn ốc log từ bán kính r0 (ngoài) vào r1 (trong)."""
    pts = []
    for i in range(n + 1):
        t = i / n
        a = start + (1 if cw else -1) * t * turns * 2 * math.pi
        r = r0 * (r1 / r0) ** t
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts

def smooth(pts):
    d = f'M{pts[0][0]:.1f},{pts[0][1]:.1f}'
    for i in range(1, len(pts) - 1):
        mx, my = (pts[i][0] + pts[i+1][0]) / 2, (pts[i][1] + pts[i+1][1]) / 2
        d += f'Q{pts[i][0]:.1f},{pts[i][1]:.1f} {mx:.1f},{my:.1f}'
    return d + f'L{pts[-1][0]:.1f},{pts[-1][1]:.1f}'

# Mỗi thùy mây: (cx, cy, r, chiều xoắn). Viền ngoài = cung trên của các thùy; mỗi thùy cuộn xoắn vào trong.
MOTIFS = {
 'a': [(-46, 4, 16, False), (-16, -14, 24, True), (20, -6, 19, True), (48, 8, 13, True)],
 'b': [(-30, 2, 18, False), (0, -16, 22, True), (30, 0, 17, True)],
 'c': [(-18, 0, 14, False), (12, -6, 17, True)],
 'd': [(-60, 8, 12, False), (-36, -6, 17, False), (-6, -20, 23, True), (26, -10, 19, True), (54, 4, 14, True), (78, 12, 9, True)],
}

def motif(lobes):
    paths, body = [], []
    for cx, cy, r, cw in lobes:
        # xoắn bắt đầu từ phía dưới thùy, cuộn ~1.35 vòng vào tâm
        start = math.pi / 2 + (0.9 if cw else -0.9)
        paths.append(smooth(spiral(cx, cy, r, r * 0.16, 1.5, start, cw)))
        body.append(f'<circle cx="{cx}" cy="{cy}" r="{r}"/>')
    lo = lobes[0]; hi = lobes[-1]
    base_y = max(cy + r for cx, cy, r, _ in lobes) - 2
    # đường đáy uốn nhẹ, kéo dài thành đuôi mây mảnh
    x0, x1 = lo[0] - lo[2] * .2, hi[0] + hi[2] + 34
    tail = (f'M{x0:.1f},{lo[1] + lo[2]:.1f} C{x0 + 30:.1f},{base_y + 6:.1f} {hi[0] - 10:.1f},{base_y + 4:.1f} {hi[0] + hi[2] * .6:.1f},{base_y:.1f}'
            f' S{x1 - 12:.1f},{base_y - 6:.1f} {x1:.1f},{base_y - 2:.1f}')
    return ''.join(body), paths + [tail]

W, H = 1440, 620
PLACE = [  # (motif, x, y, scale, opacity, flip)
 ('a', 220, 125, 1.6, .9, 0), ('c', 520, 62, 1.2, .6, 1), ('b', 1170, 95, 1.45, .85, 1), ('c', 1010, 250, 1.0, .45, 0),
 ('d', 1280, 330, 1.25, .7, 0), ('b', 85, 360, 1.15, .6, 0),
 ('a', 270, 610, 1.4, .8, 1), ('d', 1080, 615, 1.4, .8, 1), ('c', 1400, 525, 1.1, .5, 0), ('b', 720, 625, 1.1, .5, 0),
]
out = []
for m, x, y, s, op, fl in PLACE:
    body, paths = motif(MOTIFS[m])
    sw = 1.2 / s
    ring = body.replace('/>', '/>').replace('r="', 'r="')
    big = ''.join(f'<circle cx="{cx}" cy="{cy}" r="{r + sw:.2f}"/>' for cx, cy, r, _ in MOTIFS[m])
    out.append(f'<g transform="translate({x} {y}) scale({-s if fl else s} {s})" opacity="{op}">'
               f'<g fill="{GOLD}">{big}</g><g fill="{BODY}">{body}</g>'
               f'<g fill="none" stroke="{GOLD}" stroke-width="{sw:.2f}" stroke-linecap="round" stroke-linejoin="round">'
               + ''.join(f'<path d="{d}"/>' for d in paths) + '</g></g>')
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice">' + ''.join(out) + '</svg>'
open('../../images/bg-clouds.svg', 'w').write(svg)
open('preview.html', 'w').write(f'<body style="margin:0;background:#f8eedd">{svg.replace("<svg ", "<svg width=1440 height=620 ")}</body>')
print(len(svg))
