"""Ghép 6 đám mây đã trace thành nền rải rác, tông vàng kem nhạt. Sinh images/bg-clouds.svg"""
import json
C = json.load(open('clouds.json'))
LINE, BODY, SHADE, HI = '#dcc08a', '#fdf6e8', '#f3e3c3', '#ffffff'
defs = ''.join(
    f'<symbol id="c{i}" viewBox="{c["box"][0]-6} {c["box"][1]-6} {c["box"][2]+12} {c["box"][3]+12}">'
    f'<path fill="{LINE}" d="{c["outline"]}"/><path fill="{BODY}" d="{c["body"]}"/>'
    f'<path fill="{SHADE}" d="{c["shade"]}"/><path fill="{HI}" opacity=".9" d="{c["hi"]}"/></symbol>'
    for i, c in enumerate(C))
W, H = 1440, 760
# (đám, x, y, rộng, opacity, lật)
PLACE = [(0, 40, 30, 280, .8, 0), (3, 430, 15, 110, .5, 1), (1, 880, 25, 150, .6, 0),
         (4, 1260, 290, 160, .5, 0), (5, 10, 300, 120, .5, 0), (2, 1130, 580, 260, .7, 1), (4, 110, 590, 230, .65, 0),
         (1, 640, 610, 140, .45, 1), (3, 880, 225, 90, .35, 0)]
use = []
for i, x, y, w, op, fl in PLACE:
    bw, bh = C[i]['box'][2] + 12, C[i]['box'][3] + 12; h = w * bh / bw
    tf = f' transform="translate({2*x+w} 0) scale(-1 1)"' if fl else ''
    use.append(f'<use href="#c{i}" x="{x}" y="{y}" width="{w}" height="{h:.0f}" opacity="{op}"{tf}/>')
svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid slice"><defs>{defs}</defs>{"".join(use)}</svg>'
open('../../images/bg-clouds.svg', 'w').write(svg)
open('preview.html', 'w').write(f'<body style="margin:0;background:#f8eedd">{svg.replace("<svg ", "<svg width=1440 height=640 ")}</body>')
print(len(svg))
