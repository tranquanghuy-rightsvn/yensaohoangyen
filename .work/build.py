#!/usr/bin/env python3
"""Sinh hoangyen/index.html từ data.py (chạy: python3 .work/build.py)."""
import os, re, sys, html
W = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(os.path.dirname(W), 'html')  # trang web nằm trong hoangyen/html/
sys.path.insert(0, W)
from data import TABS, SPECIAL, GIFTS, CUSTOMERS, CERTS, POSTS

E = html.escape
def slug(f): return re.sub(r'\.(png|jpe?g|webp)$', '', f).lower()[:40]
def im(prefix, f): return f'images/{prefix}-{slug(f)}.jpg'

# ---------- Icon set (stroke, 24px) ----------
P = {
 'phone': '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/>',
 'search': '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
 'cart': '<path d="M3 4h2l2.2 10.4a2 2 0 0 0 2 1.6h7.6a2 2 0 0 0 2-1.5L21 8H6.2"/><circle cx="9.5" cy="20" r="1.4"/><circle cx="17" cy="20" r="1.4"/>',
 'cartplus': '<path d="M2.5 3.5h2.2l2.4 11.2a1.6 1.6 0 0 0 1.6 1.3h8.4a1.6 1.6 0 0 0 1.6-1.2l1.6-6.8H6.2"/><circle cx="9.4" cy="20" r="1.35"/><circle cx="17" cy="20" r="1.35"/><path class="plus" d="M13 8.2v5M10.5 10.7h5"/><path class="tick" d="m10.4 10.9 2 2 3.4-3.6"/>',
 'bag': '<path d="M6 7h12l1 13H5L6 7Z"/><path d="M9 7a3 3 0 0 1 6 0"/>',
 'menu': '<path d="M4 7h16M4 12h16M4 17h10"/>',
 'down': '<path d="m6 9 6 6 6-6"/>',
 'left': '<path d="m15 18-6-6 6-6"/>',
 'right': '<path d="m9 18 6-6-6-6"/>',
 'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
 'up': '<path d="m18 15-6-6-6 6"/>',
 'check': '<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>',
 'shield': '<path d="M12 3 4 6v6c0 5 3.4 8.4 8 9 4.6-.6 8-4 8-9V6l-8-3Z"/><path d="m9 12 2 2 4-4"/>',
 'leaf': '<path d="M5 19c0-8 5-14 15-15-1 10-7 15-15 15Z"/><path d="M5 19 13 11"/>',
 'award': '<circle cx="12" cy="9" r="6"/><path d="m8.5 14-1.5 7 5-3 5 3-1.5-7"/>',
 'truck': '<path d="M3 6h11v10H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17.5" cy="17.5" r="1.8"/>',
 'gift': '<rect x="3" y="8" width="18" height="13" rx="1.5"/><path d="M12 8v13M3 12h18M12 8S9 3 6.5 4.5 8 8 12 8Zm0 0s3-5 5.5-3.5S16 8 12 8Z"/>',
 'crown': '<path d="m3 8 4.5 4L12 5l4.5 7L21 8l-2 11H5L3 8Z"/>',
 'sparkle': '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
 'flask': '<path d="M9 3h6M10 3v6L4.5 18.5A2 2 0 0 0 6.2 21h11.6a2 2 0 0 0 1.7-2.5L14 9V3"/><path d="M7 15h10"/>',
 'tag': '<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8Z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
 'card': '<rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="M2.5 10h19M6 15h4"/>',
 'pin': '<path d="M12 21s-7-6.2-7-12a7 7 0 0 1 14 0c0 5.8-7 12-7 12Z"/><circle cx="12" cy="9" r="2.5"/>',
 'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
 'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3Z"/>',
 'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'home': '<path d="m3 11 9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1v-9Z"/>',
 'grid': '<rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/>',
 'chat': '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12Z"/>',
 'fb': '<path d="M15 3h-2.5A3.5 3.5 0 0 0 9 6.5V9H6.5v3.5H9V21h3.5v-8.5H15l.5-3.5h-3V7a1 1 0 0 1 1-1H15V3Z"/>',
 'yt': '<rect x="2.5" y="5.5" width="19" height="13" rx="3.5"/><path d="m10 9.5 5 2.5-5 2.5v-5Z"/>',
 'user': '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4.4 3.6-7 8-7s8 2.6 8 7"/>',
 'tiktok': '<path d="M14 3v11.5a3.5 3.5 0 1 1-3.5-3.5"/><path d="M14 3c.5 2.6 2.4 4.5 5 5"/>',
}
def ic(name, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{P[name]}</svg>'
STAR = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="m12 2.8 2.8 5.8 6.3.9-4.6 4.4 1.1 6.3L12 17.2l-5.6 3 1.1-6.3-4.6-4.4 6.3-.9L12 2.8Z"/></svg>'

def price_html(p):
    if p.startswith('Từ '):
        return f'<span class="price"><small>Từ</small>{E(p[3:])}₫</span>'
    return f'<span class="price">{E(p)}₫</span>'

def card(name, f, price, badge, cat, eager=False, sub=''):
    b = ''
    if badge:
        b = f'<span class="badge{" hot" if badge in ("Bán chạy", "Quà Tết") else ""}">{E(badge)}</span>'
    lz = '' if eager else ' loading="lazy" decoding="async"'
    ds = f' data-sub="{sub}"' if sub else ''
    return f'''<article class="card"{ds}>{b}
<a class="card-img" href="#" aria-label="{E(name)}"><img src="{im('p', f)}" alt="{E(name)}" width="560" height="560"{lz}></a>
<div class="card-body"><span class="card-cat">{E(cat)}</span><h3 class="card-title"><a href="#">{E(name)}</a></h3>
<div class="stars" aria-label="5 sao">{STAR*5}<span>(5.0)</span></div>
<div class="card-foot">{price_html(price)}<button class="add" type="button" data-add="{E(name)}" aria-label="Thêm {E(name)} vào giỏ">{ic('cartplus')}</button></div></div></article>'''

def head(eyebrow, title, desc=''):
    d = f'<p class="sec-desc">{desc}</p>' if desc else ''
    return f'<div class="sec-head reveal"><span class="eyebrow">{eyebrow}</span><h2 class="sec-title">{title}</h2><div class="ornament" aria-hidden="true"></div>{d}</div>'

def slider(items, label):
    return f'''<div class="slider" data-slider><div class="track" aria-label="{label}">{''.join(items)}</div>
<div class="s-nav"><button class="s-btn" data-prev aria-label="Trước">{ic('left')}</button><button class="s-btn" data-next aria-label="Sau">{ic('right')}</button></div></div>'''

# ---------- Header ----------
SUB = ['Yến tổ', 'Yến chưng tươi', 'Nước yến chưng sẵn', 'Quà tặng', 'Đông trùng hạ thảo']
MENU_CATS = [('menu-yen-to.jpg', 'Yến tổ', 'Tinh chế · Thô · Rút lông'), ('menu-yen-chung-tuoi.jpg', 'Yến chưng tươi', 'Chưng mới mỗi ngày'),
             ('menu-yen-chung-san.jpg', 'Nước yến chưng sẵn', 'Tiện lợi, dùng ngay'), ('menu-set-qua.jpg', 'Quà tặng', 'Hộp quà sang trọng'),
             ('menu-dong-trung.jpg', 'Đông trùng hạ thảo', 'Bồi bổ chuyên sâu')]
def mega_shop():
    tiles = ''.join(f'<a class="m-tile" href="#"><span class="m-img"><img src="images/{f}" alt="{t}" width="320" height="288" loading="lazy"></span><b>{t}</b><small>{d}</small></a>' for f, t, d in MENU_CATS)
    promo = (f'<a class="m-promo" href="#qua-bieu"><img src="images/menu-promo.jpg" alt="Hộp quà Cung Đình" width="520" height="520" loading="lazy">'
             f'<span><small>Bộ sưu tập Tết</small><b>Hộp quà Cung Đình</b><em>Xem ngay {ic("arrow")}</em></span></a>')
    return f'<div class="mega"><div class="m-grid">{tiles}</div>{promo}</div>'
def mega_gift():
    tiles = ''.join(f'<a class="m-tile" href="#"><span class="m-img"><img src="{im("g", f)}" alt="{E(n)}" width="320" height="320" loading="lazy"></span><b>{E(n.replace("Hoàng Yến Hộp Quà Cung Đình – ", ""))}</b><small>{price_html(p)}</small></a>' for n, f, p in GIFTS[:4])
    return f'<div class="mega mega-4"><div class="m-grid">{tiles}</div></div>'
def drawer_tiles():
    return '<div class="d-tiles">' + ''.join(f'<a href="#"><img src="images/{f}" alt="{t}" width="320" height="288" loading="lazy"><span>{t}</span></a>' for f, t, d in MENU_CATS) + '</div>' 
header = f'''<div class="topbar"><div class="container">
<div class="topbar-l"><span>{ic('crown')}Thượng phẩm Hoàng gia – Yến Tiến Vua</span></div>
<div class="topbar-r"><a href="#">Hệ thống cửa hàng</a><a href="#">Tuyển dụng</a><span class="flags"><a href="#" aria-label="Tiếng Việt" class="on"><img src="images/flag-vi.svg" alt="VI" width="20" height="14">VI</a><a href="#" aria-label="中文"><img src="images/flag-zh.svg" alt="中文" width="20" height="14">中文</a></span></div>
</div></div>
<header class="header" id="top"><div class="container">
<div class="nav nav-l">
<a class="hotline" href="tel:0938699797"><i>{ic('phone')}</i><span><small>Tư vấn 24/7</small><b>0938.699.797</b></span></a>
<nav class="nav-links" aria-label="Menu chính trái"><a class="active" href="index.html">Trang chủ</a><a href="#">Về Hoàng Yến</a>
<div class="nav-drop mega-host"><button type="button" aria-haspopup="true">Cửa hàng {ic('down')}</button>{mega_shop()}</div></nav>
</div>
<button class="icon-btn menu-btn" type="button" aria-label="Mở menu" data-drawer-open>{ic('menu')}</button>
<a class="logo" href="index.html" aria-label="Yến Sào Hoàng Yến – Trang chủ"><img src="images/logo.png" alt="Yến Sào Hoàng Yến" width="240" height="240"></a>
<div class="nav nav-r">
<nav class="nav-links" aria-label="Menu chính phải"><div class="nav-drop mega-host"><button type="button" aria-haspopup="true">Quà biếu Tết {ic('down')}</button>{mega_gift()}</div><a href="#">Vùng nguyên liệu</a><a href="#tin-tuc">Tin tức</a><a href="#lien-he">Liên hệ</a></nav>
<div class="tools"><button class="icon-btn" type="button" aria-label="Tìm kiếm" data-search-open>{ic('search')}</button><a class="icon-btn" href="#" aria-label="Giỏ hàng">{ic('cart')}<span class="cart-count" data-cart-count>0</span></a><a class="icon-btn" href="#" aria-label="Đăng nhập">{ic('user')}</a></div>
</div>
</div></header>
<div class="search" id="search" role="dialog" aria-label="Tìm kiếm"><form action="#" role="search"><input type="search" placeholder="Bạn đang tìm yến chưng, yến tổ hay quà biếu…" aria-label="Từ khóa"><button class="btn btn-red" type="submit">{ic('search')}Tìm</button></form></div>
<div class="drawer" id="drawer" aria-hidden="true"><div class="drawer-bg" data-drawer-close></div><div class="drawer-panel">
<div class="drawer-head"><img src="images/logo.png" alt="Hoàng Yến" width="52" height="52"><button type="button" data-drawer-close aria-label="Đóng">&times;</button></div>
<nav aria-label="Menu di động"><a href="index.html">Trang chủ</a><a href="#">Về Hoàng Yến</a><details open><summary>Cửa hàng</summary>{drawer_tiles()}</details><a href="#qua-bieu">Quà biếu Tết</a><a href="#">Vùng nguyên liệu</a><a href="#tin-tuc">Tin tức</a><a href="#lien-he">Liên hệ</a></nav>
<div class="drawer-foot"><a class="btn btn-red" href="tel:0938699797">{ic('phone')}0938.699.797</a><a class="btn btn-line" href="https://zalo.me/0938699797"><img class="zalo-ic" src="images/zalo.webp" alt="" width="20" height="20">Chat Zalo</a></div>
</div></div>'''

# ---------- Hero ----------
BANNERS_D = [('banner-1.jpg', 'Bộ quà Trung Thu Tuyết Lam An'), ('banner-2.jpg', 'Món quà đổi thay – Tấm lòng vẫn vẹn nguyên'), ('banner-3.jpg', 'Quà đoàn viên – Tấm lòng vẫn vẹn nguyên')]
BANNERS_M = [('banner-m1.jpg', 'Món quà đổi thay – Tấm lòng vẫn vẹn nguyên'), ('banner-m2.jpg', 'Quà đoàn viên – Tấm lòng vẫn vẹn nguyên')]
def banner_slides(items, w, h):
    out = []
    for k, (f, a) in enumerate(items):
        attr = ' fetchpriority="high"' if k == 0 else ' loading="lazy"'
        out.append(f'<a class="hb-slide" href="#qua-bieu"><img src="images/{f}" alt="Yến Sào Hoàng Yến – {E(a)}" width="{w}" height="{h}"{attr}></a>')
    return ''.join(out)
def banner(cls, items, w, h):
    return f'''<div class="hb {cls}" data-hero aria-roledescription="carousel" aria-label="Banner"><div class="hb-track">{banner_slides(items, w, h)}</div>
<button class="hb-arrow prev" type="button" aria-label="Banner trước">{ic('left')}</button><button class="hb-arrow next" type="button" aria-label="Banner sau">{ic('right')}</button></div>'''
hero = f'''<section class="hero-banner">
{banner('hb-d', BANNERS_D, 1920, 731)}
{banner('hb-m', BANNERS_M, 900, 900)}
<svg class="hero-waves" viewBox="0 0 1440 205" preserveAspectRatio="none" aria-hidden="true"><path class="hw-back" d="M0,4 C40,22 140,13 260,20 C440,30 500,90 660,110 C820,130 900,80 1040,70 C1180,60 1300,120 1440,100 L1440,175 L0,175 Z"/><path class="hw-front" d="M0,15 C60,48 110,36 220,45 C400,60 460,113 620,130 C760,145 820,110 980,100 C1140,90 1280,140 1440,120 L1440,210 L0,210 Z"/></svg>
</section>'''

# Icon cam kết vẽ riêng (48x48, nét vàng đồng). Hàng thật = chim hoàng yến.
PI = {
 'bird': '<defs><linearGradient id="hyG" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2c48a"/><stop offset=".5" stop-color="#b48a45"/><stop offset="1" stop-color="#7f5c24"/></linearGradient></defs><path fill="url(#hyG)" fill-rule="evenodd" d="M43.28,38.12C43.2,38.2 43.1,38.2 43.1,38.3C43.0,38.4 43.0,38.4 43.0,38.4C43.0,38.5 43.0,38.7 43.0,38.8C43.0,38.8 43.0,38.8 43.1,38.9C43.1,39.0 43.2,39.0 43.3,39.1C43.4,39.1 43.5,39.1 43.7,39.1C43.8,39.0 43.9,38.9 43.9,38.8C44.0,38.7 44.0,38.5 43.9,38.4C43.9,38.3 43.8,38.2 43.7,38.1C43.5,38.1 43.4,38.1 43.3,38.1ZM26.58,1.77C26.5,1.9 26.4,2.0 26.4,2.5C26.4,3.0 26.3,3.3 26.3,4.6C26.4,5.9 26.4,8.1 26.7,10.5C27.0,13.0 27.7,18.0 28.0,19.9C28.2,21.7 28.3,21.6 28.4,22.0C28.4,22.4 28.3,22.3 28.3,22.4C28.3,22.4 28.4,23.3 28.2,22.2C28.1,21.2 27.3,16.9 27.1,15.9C26.9,14.8 27.1,15.6 27.1,15.9C27.1,16.1 27.1,17.2 27.1,17.5C27.1,17.9 27.1,17.8 27.0,17.9C26.9,18.1 26.4,17.8 26.6,18.7C26.7,19.6 27.8,22.5 28.0,23.3C28.2,24.0 28.2,24.0 27.9,23.3C27.6,22.6 26.7,19.6 26.3,18.9C25.9,18.3 25.6,19.3 25.5,19.4C25.4,19.4 25.4,19.4 25.4,19.4C25.4,19.4 25.0,18.9 25.4,19.5C25.7,20.1 27.1,22.7 27.4,23.4C27.7,24.0 27.7,24.1 27.4,23.5C27.0,22.9 25.5,20.2 25.0,19.5C24.5,18.9 24.2,19.5 24.1,19.5C23.9,19.5 23.6,18.9 24.1,19.6C24.5,20.3 26.4,23.2 26.9,23.9C27.3,24.6 26.9,24.0 26.8,24.0C26.8,23.9 26.9,24.2 26.4,23.5C25.9,22.8 24.1,20.3 23.7,19.6C23.2,19.0 23.6,19.5 23.5,19.5C23.3,19.5 22.9,19.5 22.6,19.4C22.3,19.3 21.3,18.3 21.9,19.0C22.4,19.7 25.3,23.1 26.0,23.9C26.6,24.7 26.9,25.1 26.0,24.1C25.1,23.1 21.8,19.3 20.5,17.9C19.2,16.4 18.9,16.3 17.9,15.3C16.9,14.2 15.3,12.5 14.2,11.2C13.0,9.9 11.1,7.7 10.5,7.0C9.9,6.4 10.4,7.0 10.4,7.0C10.4,7.0 10.4,7.0 10.4,7.1C10.5,7.3 10.5,7.4 10.8,7.8C11.1,8.3 10.7,7.8 12.3,10.1C13.9,12.3 19.1,19.3 21.0,21.9C22.9,24.4 23.3,25.0 23.9,26.1C24.6,27.2 24.7,27.6 25.2,28.7C25.7,29.8 26.5,31.9 26.9,32.8C27.2,33.8 27.5,34.1 27.7,34.4C27.9,34.6 27.8,34.5 27.8,34.5C27.9,34.5 27.9,34.5 28.1,34.5C28.2,34.5 28.6,34.4 28.8,34.3C29.0,34.2 29.2,34.1 29.4,34.0C29.6,33.8 30.0,33.5 30.1,33.4C30.3,33.2 30.4,33.1 30.4,32.9C30.5,32.8 30.5,32.7 30.5,32.7C30.5,32.6 30.6,32.6 30.6,32.7C30.6,32.7 30.6,32.8 30.6,32.9C30.6,33.1 30.5,33.4 30.5,33.5C30.4,33.7 30.4,33.7 30.3,33.8C30.2,33.9 30.1,34.1 29.9,34.2C29.7,34.4 29.4,34.6 29.2,34.7C28.9,34.8 28.1,34.6 28.3,34.9C28.4,35.3 29.9,36.7 30.1,37.0C30.4,37.4 30.5,37.4 30.1,37.1C29.7,36.7 27.9,35.2 27.4,34.8C26.9,34.5 27.1,34.9 27.0,34.9C26.9,34.9 26.8,35.0 26.8,35.0C26.8,35.0 26.5,34.8 26.8,35.1C27.1,35.4 28.4,36.8 28.7,37.1C29.0,37.5 29.2,37.7 28.8,37.4C28.4,37.0 26.5,35.6 26.1,35.2C25.7,34.8 26.2,35.0 26.1,35.0C26.1,35.0 25.8,35.0 25.7,35.0C25.6,35.0 25.6,35.0 25.5,35.0C25.5,35.1 25.2,34.9 25.4,35.2C25.7,35.5 26.9,36.8 27.2,37.1C27.5,37.4 27.6,37.5 27.2,37.2C26.8,36.9 25.0,35.3 24.5,35.0C24.0,34.6 24.1,35.0 24.1,35.0C24.0,35.1 23.7,34.8 24.0,35.1C24.3,35.5 25.6,36.8 25.9,37.2C26.2,37.5 26.3,37.6 25.9,37.2C25.4,36.9 23.6,35.3 23.1,35.0C22.6,34.6 22.7,35.0 22.6,35.0C22.5,35.0 22.3,34.7 22.6,35.0C22.8,35.4 24.0,36.6 24.2,36.9C24.5,37.2 24.6,37.3 24.2,36.9C23.8,36.6 22.0,35.1 21.5,34.8C21.0,34.4 21.0,34.8 20.9,34.8C20.8,34.9 20.6,34.7 20.9,34.9C21.1,35.2 22.2,36.3 22.5,36.6C22.7,36.9 22.9,37.1 22.5,36.8C22.0,36.4 20.3,34.9 19.8,34.5C19.2,34.2 19.2,34.5 19.1,34.5C19.0,34.5 18.8,34.3 19.1,34.6C19.3,34.9 20.4,36.0 20.6,36.3C20.9,36.6 21.0,36.7 20.6,36.4C20.2,36.1 18.4,34.5 17.9,34.1C17.4,33.8 17.5,34.1 17.3,34.1C17.2,34.1 17.1,34.1 17.0,34.1C17.0,34.2 16.8,34.0 17.0,34.2C17.3,34.5 18.4,35.7 18.6,36.0C18.9,36.3 19.0,36.4 18.6,36.0C18.2,35.7 16.4,34.2 16.0,33.9C15.5,33.5 15.9,33.8 15.7,33.8C15.6,33.8 15.1,33.7 15.0,33.8C14.9,33.8 14.7,33.5 14.9,33.8C15.2,34.2 16.5,35.5 16.8,35.8C17.1,36.2 17.2,36.2 16.8,35.9C16.3,35.5 14.8,34.1 14.1,33.7C13.5,33.3 13.3,33.5 12.7,33.4C12.1,33.3 10.9,33.2 10.2,33.2C9.6,33.2 9.1,33.2 8.5,33.2C7.9,33.2 7.2,33.3 6.7,33.3C6.2,33.4 5.6,33.5 5.1,33.5C4.6,33.6 4.0,33.8 3.5,33.9C3.0,34.1 2.4,34.3 2.1,34.4C1.7,34.6 1.5,34.8 1.2,34.9C1.0,35.0 0.9,35.2 0.7,35.3C0.5,35.4 0.4,35.6 0.3,35.7C0.2,35.8 -0.0,36.1 0.0,36.1C0.0,36.2 0.3,35.9 0.5,35.8C0.7,35.8 0.9,35.6 1.3,35.5C1.6,35.5 2.2,35.4 2.6,35.3C2.9,35.3 3.1,35.3 3.5,35.3C3.8,35.4 4.3,35.4 4.7,35.5C5.1,35.5 5.4,35.6 5.8,35.7C6.2,35.8 6.5,35.8 7.2,36.1C7.9,36.3 9.3,36.8 10.2,37.2C11.2,37.6 12.1,38.0 13.2,38.5C14.3,39.1 15.7,39.8 17.2,40.6C18.7,41.3 21.2,42.8 22.4,43.4C23.5,44.0 23.7,44.0 24.3,44.3C25.0,44.6 26.0,45.1 26.5,45.3C27.1,45.5 27.4,45.6 27.8,45.8C28.2,45.9 28.6,46.0 29.1,46.0C29.5,46.1 30.1,46.2 30.5,46.2C30.9,46.2 31.4,46.2 31.7,46.1C32.1,46.1 32.4,46.0 32.8,45.9C33.2,45.8 33.6,45.6 34.0,45.4C34.3,45.3 34.6,45.1 35.0,44.9C35.3,44.6 35.7,44.3 36.0,44.0C36.3,43.7 36.6,43.4 36.8,43.1C37.0,42.8 37.2,42.5 37.5,42.2C37.7,41.9 38.0,41.4 38.2,41.0C38.5,40.6 38.9,39.7 39.1,39.4C39.2,39.2 39.1,39.5 39.1,39.5C39.1,39.6 39.1,39.6 39.0,39.9C38.9,40.2 38.6,40.9 38.4,41.3C38.2,41.7 38.0,42.0 37.9,42.2C37.7,42.5 37.4,42.7 37.4,42.9C37.3,43.0 37.1,42.9 37.4,42.9C37.7,42.9 38.6,43.0 39.2,42.9C39.8,42.8 40.6,42.6 41.0,42.5C41.5,42.4 41.7,42.3 42.1,42.1C42.4,42.0 42.7,41.9 43.1,41.7C43.4,41.5 44.0,41.1 44.3,40.9C44.6,40.8 44.3,40.5 44.9,40.4C45.5,40.4 47.5,40.4 48.0,40.4C48.5,40.3 48.3,40.5 47.9,40.2C47.5,40.0 46.0,39.2 45.6,38.8C45.2,38.3 45.7,37.6 45.7,37.3C45.6,37.0 45.6,36.8 45.5,36.6C45.4,36.4 45.3,36.2 45.2,36.0C45.2,35.8 45.0,35.6 44.9,35.5C44.8,35.3 44.6,35.1 44.4,35.0C44.3,34.9 44.0,34.7 43.8,34.6C43.6,34.5 43.2,34.5 43.2,34.3C43.3,34.1 43.9,33.5 44.2,33.2C44.4,32.9 44.5,32.7 44.8,32.3C45.0,31.9 45.3,31.3 45.5,30.9C45.7,30.5 45.8,30.2 46.0,29.8C46.1,29.5 46.2,29.2 46.2,28.9C46.3,28.5 46.4,28.0 46.5,27.7C46.5,27.4 46.6,27.2 46.6,26.9C46.6,26.5 46.5,25.8 46.5,25.3C46.4,24.9 46.4,24.6 46.2,24.0C46.0,23.5 45.6,22.4 45.3,21.8C45.1,21.2 45.2,21.4 44.6,20.2C44.0,19.1 42.3,15.7 41.6,14.4C40.9,13.0 40.7,12.4 40.4,11.6C40.1,10.9 39.9,10.2 39.8,9.7C39.7,9.2 39.7,8.9 39.7,8.6C39.7,8.4 39.8,8.3 39.8,8.2C39.8,8.2 39.9,8.1 39.9,8.0C39.9,8.0 40.0,7.9 39.9,8.0C39.7,8.1 39.4,8.4 39.2,8.6C39.1,8.7 39.0,8.9 38.9,9.1C38.9,9.3 38.8,9.4 38.8,9.6C38.7,9.8 38.6,9.9 38.6,10.5C38.6,11.0 38.6,12.0 38.6,12.9C38.7,13.9 38.8,15.0 39.0,16.3C39.2,17.5 39.5,19.8 39.7,20.9C39.8,21.9 39.6,22.5 39.8,23.1C40.1,23.7 40.9,24.3 41.1,24.5C41.3,24.7 41.3,24.7 41.1,24.5C40.9,24.4 40.1,23.7 39.9,23.5C39.6,23.3 39.8,23.5 39.8,23.6C39.7,23.6 39.7,23.9 39.7,24.0C39.7,24.1 39.5,23.9 39.8,24.1C40.0,24.4 40.8,25.3 41.0,25.5C41.2,25.7 41.0,25.6 40.8,25.4C40.6,25.3 39.9,24.7 39.8,24.5C39.6,24.4 39.7,24.5 39.7,24.6C39.7,24.6 39.4,24.6 39.6,24.9C39.8,25.2 40.8,26.2 41.0,26.5C41.2,26.7 41.2,26.7 41.0,26.5C40.7,26.3 40.0,25.6 39.8,25.5C39.5,25.3 39.6,25.4 39.6,25.4C39.5,25.5 39.3,25.6 39.5,25.9C39.6,26.2 40.6,27.2 40.8,27.4C41.0,27.7 41.0,27.6 40.7,27.4C40.5,27.3 39.6,26.4 39.4,26.3C39.1,26.1 39.2,26.4 39.2,26.4C39.1,26.5 38.9,26.5 39.1,26.8C39.3,27.1 40.2,28.0 40.4,28.2C40.6,28.5 40.6,28.5 40.4,28.3C40.1,28.1 39.1,27.2 38.9,27.0C38.6,26.8 38.8,27.0 38.8,27.1C38.7,27.1 38.6,27.2 38.6,27.3C38.5,27.4 38.3,27.2 38.6,27.5C38.8,27.7 39.7,28.7 39.9,28.9C40.1,29.2 40.1,29.2 39.9,29.0C39.6,28.8 38.5,27.8 38.2,27.6C37.9,27.4 38.1,27.7 38.0,27.8C38.0,27.8 37.9,27.9 37.9,28.0C37.9,28.1 37.7,27.9 38.0,28.2C38.2,28.4 39.1,29.3 39.3,29.6C39.5,29.8 39.5,29.9 39.2,29.7C39.0,29.5 37.9,28.5 37.6,28.3C37.3,28.1 37.5,28.4 37.4,28.4C37.3,28.4 37.2,28.6 37.2,28.6C37.1,28.7 36.9,28.6 37.1,28.9C37.3,29.2 38.4,30.2 38.6,30.5C38.9,30.8 38.9,30.8 38.6,30.6C38.3,30.3 37.0,29.2 36.7,29.0C36.4,28.8 36.6,29.0 36.6,29.1C36.5,29.1 36.4,29.2 36.4,29.2C36.3,29.3 36.1,29.2 36.3,29.5C36.5,29.8 37.6,30.8 37.8,31.1C38.0,31.4 38.2,31.5 37.9,31.3C37.5,31.0 36.2,29.8 35.8,29.6C35.4,29.3 35.5,29.7 35.4,29.7C35.2,29.8 35.2,29.9 35.1,29.9C35.1,30.0 35.1,30.0 35.1,30.1C35.2,30.2 35.4,30.5 35.6,30.7C35.8,30.9 36.0,31.1 36.3,31.3C36.6,31.6 37.1,31.9 37.5,32.2C37.9,32.4 38.5,32.8 38.8,32.9C39.2,33.1 39.5,33.2 39.7,33.2C39.9,33.3 39.9,33.3 40.1,33.3C40.3,33.3 40.9,33.3 41.1,33.3C41.2,33.3 41.2,33.3 41.3,33.4C41.5,33.4 41.8,33.6 42.0,33.7C42.2,33.8 42.7,34.1 42.4,34.1C42.1,34.1 40.5,33.9 40.0,33.8C39.5,33.8 39.5,33.7 39.2,33.6C38.9,33.5 38.4,33.3 38.1,33.2C37.8,33.0 37.6,32.9 37.3,32.7C37.0,32.5 36.5,32.2 36.2,31.9C35.8,31.6 35.5,31.3 35.2,31.0C34.9,30.7 34.6,30.4 34.2,30.0C33.9,29.6 33.5,29.0 33.2,28.6C32.9,28.1 32.7,27.7 32.5,27.2C32.2,26.8 32.1,26.4 31.9,25.6C31.6,24.8 31.3,23.8 30.9,22.2C30.5,20.7 29.8,17.9 29.3,15.9C28.8,13.9 28.3,11.5 28.0,9.8C27.6,8.2 27.3,6.8 27.1,5.6C26.9,4.5 26.8,3.3 26.7,2.7C26.6,2.1 26.6,1.9 26.6,1.8C26.6,1.6 26.6,1.7 26.6,1.8ZM37.95,38.60C37.8,39.0 37.0,40.5 36.7,41.1C36.4,41.6 36.2,41.8 36.0,42.0C35.8,42.3 35.5,42.7 35.2,42.9C34.9,43.2 34.6,43.4 34.4,43.6C34.1,43.8 33.9,43.9 33.6,44.0C33.3,44.2 33.0,44.3 32.6,44.4C32.3,44.5 31.9,44.6 31.5,44.6C31.1,44.7 30.5,44.7 30.1,44.7C29.6,44.7 29.4,44.6 29.0,44.6C28.6,44.5 27.9,44.4 27.4,44.3C26.9,44.2 26.5,44.0 25.9,43.8C25.3,43.6 24.7,43.4 23.7,42.9C22.7,42.4 20.6,41.2 19.8,40.8C19.0,40.3 18.8,40.3 18.7,40.2C18.5,40.2 18.7,40.2 18.8,40.2C19.0,40.2 18.6,40.0 19.5,40.4C20.3,40.8 22.9,42.1 24.1,42.6C25.3,43.1 26.2,43.4 26.9,43.6C27.5,43.8 27.7,43.8 28.2,43.9C28.6,44.0 29.3,44.1 29.7,44.1C30.1,44.1 30.4,44.1 30.8,44.1C31.1,44.1 31.3,44.1 31.6,44.1C31.9,44.1 32.4,43.9 32.7,43.9C33.0,43.8 33.1,43.8 33.3,43.6C33.5,43.5 33.9,43.4 34.1,43.2C34.4,43.0 34.7,42.9 35.0,42.5C35.4,42.2 35.9,41.6 36.2,41.1C36.6,40.7 36.9,40.2 37.2,39.8C37.4,39.4 37.8,38.8 37.9,38.6C38.0,38.4 38.1,38.2 38.0,38.6ZM44.48,38.15C44.6,38.3 44.6,38.4 44.6,38.5C44.6,38.7 44.6,39.0 44.6,39.2C44.6,39.4 44.5,39.5 44.5,39.6C44.4,39.8 44.4,39.9 44.2,40.1C44.0,40.3 43.7,40.5 43.4,40.8C43.1,41.0 42.7,41.2 42.2,41.4C41.8,41.5 41.1,41.8 40.6,41.9C40.1,42.1 39.5,42.2 39.2,42.2C38.8,42.3 38.6,42.3 38.4,42.3C38.2,42.3 37.9,42.3 38.0,42.3C38.0,42.2 38.5,42.1 38.8,41.9C39.1,41.8 39.4,41.5 39.7,41.2C39.9,40.9 40.3,40.5 40.6,40.1C40.9,39.7 41.3,38.9 41.5,38.6C41.8,38.3 41.9,38.2 42.1,38.0C42.2,37.9 42.2,37.9 42.4,37.8C42.5,37.7 42.9,37.6 43.1,37.6C43.3,37.5 43.4,37.6 43.6,37.6C43.8,37.6 43.9,37.6 44.1,37.7C44.2,37.8 44.4,38.0 44.5,38.1ZM24.15,25.57C24.2,25.6 24.5,25.8 24.7,25.9C24.8,26.0 24.9,26.0 25.2,26.2C25.5,26.5 26.1,27.2 26.6,27.7C27.0,28.2 27.1,28.3 27.7,29.1C28.2,29.8 29.6,31.7 29.9,32.2C30.3,32.8 29.9,32.5 29.9,32.6C29.8,32.7 29.8,32.7 29.7,32.8C29.6,32.9 29.4,33.2 29.2,33.3C29.0,33.5 28.8,33.6 28.6,33.6C28.4,33.7 28.3,33.7 28.2,33.8C28.0,33.8 27.9,33.8 27.9,33.7C27.8,33.7 27.8,33.8 27.7,33.5C27.5,33.2 27.2,32.6 26.8,31.7C26.4,30.8 25.6,28.7 25.2,27.8C24.9,26.9 24.7,26.7 24.6,26.4C24.4,26.0 24.2,25.8 24.1,25.7C24.1,25.6 24.1,25.5 24.2,25.6ZM45.62,24.85C45.6,25.0 45.7,25.4 45.7,25.8C45.7,26.1 45.7,26.7 45.6,27.2C45.5,27.6 45.4,28.2 45.3,28.6C45.2,28.9 45.1,29.2 44.9,29.6C44.8,30.0 44.5,30.6 44.2,31.0C44.0,31.4 43.8,31.7 43.6,32.0C43.4,32.3 43.1,32.6 42.9,32.8C42.6,33.0 42.2,33.4 42.1,33.4C41.9,33.4 41.8,33.1 41.8,32.9C41.9,32.8 42.2,32.7 42.5,32.5C42.8,32.2 43.3,31.7 43.6,31.3C43.8,31.0 44.1,30.5 44.3,30.2C44.5,29.8 44.7,29.4 44.9,28.9C45.1,28.4 45.3,27.5 45.4,27.1C45.5,26.7 45.5,26.6 45.6,26.3C45.6,25.9 45.6,25.2 45.6,24.9C45.6,24.7 45.6,24.7 45.6,24.9Z"/>',
 'shield': '<path class="ln" d="M24 5 9 10.5v11.2c0 9.6 6.3 17 15 20.3 8.7-3.3 15-10.7 15-20.3V10.5L24 5Z"/><path class="fill soft" d="M24 9.5 13 13.6v8.1c0 7.3 4.6 12.8 11 15.4 6.4-2.6 11-8.1 11-15.4v-8.1L24 9.5Z"/><path class="ln" d="M19 18.5c0 5.5 3.2 8.6 9 8.4.2-5.8-3-8.8-9-8.4ZM20.5 20c2.3 1.8 4.2 4 5.6 6.6"/><path class="ln" d="m17.5 30.5 3.3 3 6.8-7"/>',
 'medal': '<path class="fill soft" d="m15 26-5 15 6.2-1.6L19.5 45l4.5-12M33 26l5 15-6.2-1.6L28.5 45 24 33"/><circle class="ln" cx="24" cy="18.5" r="13"/><circle class="ln" cx="24" cy="18.5" r="9"/><path class="fill" d="m24 12.3 1.9 3.9 4.3.6-3.1 3 .7 4.3-3.8-2-3.8 2 .7-4.3-3.1-3 4.3-.6L24 12.3Z"/>',
 'truck': '<path class="ln" d="M14 13h18v19H14zM32 19.5h6.8l4.2 6v6.5H32"/><path class="fill soft" d="M33.5 21h4.6l2.9 4.2h-7.5z"/><circle class="ln" cx="20" cy="33.5" r="3.8"/><circle class="ln" cx="37" cy="33.5" r="3.8"/><path class="ln" d="M3 17h7M5 22h5M7 27h3"/><path class="ln" d="m19.5 22 3 3 5.5-6"/>',
}
def picon(k):
    return f'<svg viewBox="0 0 48 48" aria-hidden="true">{PI[k]}</svg>'
PROMISE = [('bird', 'Hàng thật 100%', 'Bồi hoàn 10 lần giá trị nếu phát hiện hàng giả.'),
           ('shield', 'Đảm bảo VSATTP', 'Nhà máy khép kín, đạt chuẩn ISO 22000:2018.'),
           ('medal', 'Cam kết chất lượng', 'Kiểm nghiệm từng lô, công bố minh bạch.'),
           ('truck', 'Giao hàng toàn quốc', 'Hỏa tốc 24h nội thành, thanh toán COD.')]
promise = '<section class="promise"><div class="container promise-grid">' + ''.join(
    f'<div class="pm"><span class="pm-ic">{picon(k)}</span><div class="pm-txt"><h3>{t}</h3><p>{d}</p></div></div>' for k, t, d in PROMISE) + '</div></section>'

CATS = [('cat-yen-to.jpg', 'Yến tổ', 'Tinh chế · Thô · Rút lông'), ('cat-yen-chung-tuoi.jpg', 'Yến chưng tươi', 'Chưng mới mỗi ngày'),
        ('cat-yen-chung-san.jpg', 'Yến chưng sẵn', 'Tiện lợi, dùng ngay'), ('cat-set-qua.jpg', 'Set quà biếu', 'Sang trọng, ý nghĩa'),
        ('cat-dong-trung.jpg', 'Đông trùng hạ thảo', 'Bồi bổ chuyên sâu')]
cats = f'''<section class="sec cloud-art" id="danh-muc">
<svg class="deco-bird" viewBox="0 0 48 48" aria-hidden="true">{PI["bird"].replace("hyG","hyG2")}</svg><div class="container">
{head('Khám phá nhanh', 'Danh mục sản phẩm')}
<div class="cats">{''.join(f'<a class="cat reveal" href="#"><span class="cat-img"><img src="images/{f}" alt="{n}" width="640" height="576" loading="lazy"></span><h3>{n}</h3><span>{d}</span></a>' for f, n, d in CATS)}</div>
</div></section>'''

NEEDS = [('need-hang-ngay.jpg', 'Dùng hằng ngày', 'Cả gia đình'), ('need-tre-em.jpg', 'Dành cho trẻ em', 'Ít ngọt · dễ uống'),
         ('need-cao-tuoi.jpg', 'Người cao tuổi', 'Đường kiêng · bồi bổ'), ('need-bieu-tang.jpg', 'Mua biếu tặng', 'Hộp quà cao cấp')]
needs = f'''<section class="sec bg-sand has-swallow"><div class="container">
{head('Chọn theo nhu cầu', 'Bạn mua yến dành cho ai?', 'Chọn nhóm phù hợp – chúng tôi gợi ý sản phẩm và liều dùng đúng cho từng người.')}
<div class="needs">{''.join(f'<a class="need reveal" href="#"><img src="images/{f}" alt="{t}" width="640" height="427" loading="lazy"><div class="need-body"><small>{s}</small><h3>{t}</h3><span>Xem gợi ý {ic("arrow")}</span></div></a>' for f, t, s in NEEDS)}</div>
</div></section>'''

# ---------- Tabs sản phẩm ----------
tab_btns, panels = [], []
for i, (key, (label, subs, items)) in enumerate(TABS.items()):
    on = ' on' if i == 0 else ''
    tab_btns.append(f'<button class="tab{on}" type="button" role="tab" aria-selected="{str(i == 0).lower()}" data-tab="{key}">{label}</button>')
    chips = ''
    if subs:
        chips = '<div class="chips" role="group" aria-label="Lọc ' + label + '"><button class="chip on" type="button" data-sub="all">Tất cả</button>' + ''.join(f'<button class="chip" type="button" data-sub="{k}">{t}</button>' for k, t in subs) + '</div>'
    panels.append(f'<div class="panel{on}" role="tabpanel" data-panel="{key}">{chips}<div class="grid-4">' + ''.join(card(n, f, p, bd, label, sub=g) for n, f, p, bd, g in items) + '</div></div>')
special_cards = [card(n, f, p, 'Tháng này', 'Yến chưng sẵn') for n, f, p in SPECIAL]
special = f'''<section class="sec bg-ivory" id="dac-biet"><div class="container">
{head('Bộ sưu tập theo mùa', 'Sản phẩm đặc biệt tháng này', 'Những hũ yến chưng được chọn riêng cho tháng này – ưu đãi có hạn.')}
<div class="special">{slider(special_cards, 'Sản phẩm đặc biệt tháng này')}</div>
</div></section>'''

products = f'''<section class="sec bg-ivory has-deco" id="san-pham">
<img class="deco deco-tl" src="images/deco-yen.webp" alt="" width="172" height="147" loading="lazy" aria-hidden="true"><img class="deco deco-br" src="images/deco-yen.webp" alt="" width="172" height="147" loading="lazy" aria-hidden="true">
<div class="container">
{head('Được yêu thích nhất', 'Sản phẩm nổi bật')}
<div class="tabs-wrap"><div class="tabs" role="tablist">{''.join(tab_btns)}</div></div>
{''.join(panels)}
<div class="sec-more"><a class="btn btn-line" href="#">Xem tất cả sản phẩm {ic('arrow')}</a></div>
</div></section>'''

# ---------- Câu chuyện ----------
story = f'''<section class="sec bg-sand has-swallow story"><div class="container">
<div class="collage reveal"><div class="big"><img src="images/story-to-yen.jpg" alt="Tổ yến tinh chế Hoàng Yến" width="1024" height="922" loading="lazy"></div>
<div class="small"><img src="images/story-gift.jpg" alt="Hộp quà Cung Đình Hoàng Yến" width="900" height="900" loading="lazy"></div>
<div class="year"><b>10+</b><span>năm<br>kinh nghiệm</span></div></div>
<div class="story-text reveal"><span class="eyebrow">Về Hoàng Yến</span>
<h2 class="sec-title">Yến Tiến Vua – tâm huyết trong từng tổ yến</h2><div class="ornament" aria-hidden="true"></div>
<p>Hoàng Yến là đơn vị tiên phong tạo dấu ấn riêng trong ngành yến sào với dòng sản phẩm “Yến Tiến Vua”. Mọi sản phẩm đều được kiểm nghiệm và công bố chất lượng, tối ưu sự tiện lợi nhưng vẫn giữ trọn giá trị dinh dưỡng quý giá của tổ yến.</p>
<ul class="checks"><li>{ic('check')}<span>Tổ yến tuyển chọn từ vùng nguyên liệu, tinh chế thủ công bởi thợ lành nghề</span></li><li>{ic('check')}<span>Nhà máy khép kín, đạt chuẩn ISO 22000:2018 và FDA Hoa Kỳ</span></li><li>{ic('check')}<span>Mỗi hộp có mã QR truy xuất nguồn gốc</span></li></ul>
<div class="stats"><div class="stat"><b>10+</b><span>năm kinh nghiệm</span></div><div class="stat"><b>ISO</b><span>22000:2018</span></div><div class="stat"><b>100%</b><span>không chất bảo quản</span></div></div>
<a class="btn btn-red" href="#">Tìm hiểu về doanh nghiệp {ic('arrow')}</a></div>
</div></section>'''

WHY_L = [('crown', 'Yến sào thượng hạng', 'Tinh chế thủ công bởi những người thợ lành nghề.'),
         ('leaf', 'Chất lượng tuyệt đối', '100% tự nhiên, khai thác và chế biến khép kín.'),
         ('flask', 'Tiêu chuẩn sản phẩm', 'Đạt chuẩn ATVSTP, ISO 22000, FDA Hoa Kỳ.')]
WHY_R = [('tag', 'Giá cả hợp lý', 'Không qua trung gian, trực tiếp từ nhà phân phối chính thức.'),
         ('truck', 'Giao hàng siêu tốc', 'Trong 24h, giao tận tay, kiểm hàng rồi thanh toán.'),
         ('card', 'Thanh toán an toàn', 'Đa dạng phương thức, bảo mật thông tin khách hàng.')]
def why_col(items, side):
    return f'<div class="why-col {side}">' + ''.join(f'<div class="why-item reveal"><span class="why-ico">{ic(a)}</span><div><h3>{b}</h3><p>{c}</p></div></div>' for a, b, c in items) + '</div>'
why = f'''<section class="sec bg-ivory"><div class="container">
{head('Trân quý món quà', 'Nâng niu sức khỏe người thương')}
<div class="why">{why_col(WHY_L, 'l')}<div class="why-center"><img src="images/logo-lg.png" alt="Logo Yến Sào Hoàng Yến" width="520" height="520" loading="lazy"></div>{why_col(WHY_R, 'r')}</div>
</div></section>'''

gift_cards = [f'''<article class="card"><span class="badge hot">Quà Tết</span><a class="card-img" href="#"><img src="{im('g', f)}" alt="{E(n)}" width="760" height="760" loading="lazy"></a>
<div class="card-body"><span class="card-cat">Hộp quà Cung Đình</span><h3 class="card-title"><a href="#">{E(n)}</a></h3>
<div class="card-foot">{price_html(p)}<button class="add" type="button" data-add="{E(n)}" aria-label="Thêm vào giỏ">{ic('cartplus')}</button></div></div></article>''' for n, f, p in GIFTS]
gift = f'''<section class="sec bg-sand has-swallow" id="qua-bieu"><div class="container gift">
<div class="gift-intro reveal"><span class="eyebrow">Quà biếu tặng</span><h2>Trao <em>tâm ý</em>,<br>gửi an khang</h2>
<p>Bộ sưu tập hộp quà Cung Đình – sang trọng cho đối tác, ấm áp cho gia đình.</p>
<ul><li>{ic('gift')}Đóng hộp sang trọng, kèm túi xách</li><li>{ic('sparkle')}In thiệp &amp; logo theo yêu cầu doanh nghiệp</li><li>{ic('truck')}Giao hỏa tốc trong ngày tại nội thành</li></ul>
<a class="btn btn-gold" href="tel:0938699797">{ic('phone')}Báo giá quà doanh nghiệp</a></div>
{slider(gift_cards, 'Hộp quà biếu')}
</div></section>'''

mosaic = ''.join(f'<a href="#" aria-label="Ảnh khách hàng {i+1}"><img src="{im("kh", f)}" alt="Khách hàng Yến Sào Hoàng Yến {i+1}" width="640" height="427" loading="lazy"></a>' for i, f in enumerate(CUSTOMERS))
cust = f'''<section class="cust"><div class="container">
{head('Được tin yêu', '+50.000 khách hàng yêu quý', 'Những khoảnh khắc thật của khách hàng, đối tác và đại lý cùng Yến Sào Hoàng Yến.')}
<div class="counter reveal"><div><b data-count="50000">50.000</b><span>khách hàng</span></div><div><b data-count="10">10</b><span>năm kinh nghiệm</span></div><div><b data-count="40">40</b><span>sản phẩm</span></div><div><b data-count="63">63</b><span>tỉnh thành giao tới</span></div></div>
<div class="mosaic reveal">{mosaic}</div>
</div></section>'''

cert_items = [f'<a class="cert" href="{im("cn", f)}" target="_blank" rel="noopener"><img src="{im("cn", f)}" alt="Chứng nhận và kết quả kiểm nghiệm {i+1}" width="560" height="760" loading="lazy"></a>' for i, f in enumerate(CERTS)]
certs = f'''<section class="sec bg-ivory certs"><div class="container">
{head('Chất lượng được công nhận', 'Chứng nhận &amp; kiểm nghiệm', 'Minh bạch kết quả kiểm nghiệm cho từng dòng sản phẩm.')}
{slider(cert_items, 'Chứng nhận')}
</div></section>'''

post_items = ''.join(f'''<article class="post reveal"><a class="post-img" href="#"><img src="{im('post', f)}" alt="{E(t)}" width="760" height="475" loading="lazy"></a>
<div class="post-body"><span class="post-tag">{tag}</span><h3><a href="#">{E(t)}</a></h3><p>{E(d)}</p><a class="read" href="#">Đọc tiếp {ic('arrow')}</a></div></article>''' for t, f, d, tag in POSTS)
posts = f'''<section class="sec bg-sand has-swallow" id="tin-tuc"><div class="container">
{head('Cẩm nang yến sào', 'Hiểu hơn về chúng tôi')}
<div class="posts">{post_items}</div>
<div class="sec-more"><a class="btn btn-line" href="#">Xem tất cả bài viết {ic('arrow')}</a></div>
</div></section>'''

consult = f'''<section class="sec bg-ivory" id="lien-he" style="padding-bottom:0"><div class="consult"><div class="consult-box reveal">
<div><span class="eyebrow">Tư vấn miễn phí</span><h2 style="margin-top:14px">Chưa biết chọn yến nào?<br><em>Để chúng tôi giúp bạn.</em></h2>
<p>Chuyên viên Hoàng Yến tư vấn loại yến, liều dùng và hộp quà phù hợp ngân sách – hoàn toàn miễn phí.</p></div>
<div class="consult-bowl" aria-hidden="true"><img src="images/deco-dia.webp" alt="" width="341" height="400" loading="lazy"></div>
<div class="consult-actions"><a class="btn btn-red" href="tel:0938699797">{ic('phone')}Gọi 0938.699.797<small>8h – 21h hằng ngày</small></a>
<a class="btn btn-gold" href="https://zalo.me/0938699797"><img class="zalo-ic" src="images/zalo.webp" alt="" width="20" height="20">Chat Zalo<small>Phản hồi trong 5 phút</small></a>
<a class="btn btn-line" href="https://m.me/111315987862501">{ic('chat')}Nhắn Messenger</a></div>
</div></div></section>'''

PAYS = ['asset-39-4x', 'asset-42-4x', 'asset-37-4x', 'asset-41-4x', 'asset-38-4x', 'asset-40-4x']
CERT_F = ['asset-45-4x', 'asset-44-4x', 'asset-43-4x']
footer = f'''<footer class="footer">
<svg class="footer-wave" viewBox="0 0 1440 70" preserveAspectRatio="none" aria-hidden="true"><path d="M0 0h1440v20c-180 30-360 44-540 34S540 8 360 10 90 40 0 46Z" fill="currentColor"/><path d="M0 46c90-6 180-34 360-36s360 34 540 44 360-4 540-34" fill="none" stroke="#c9a35f" stroke-width="1.4" opacity=".7"/></svg>
<div class="container"><div class="footer-main">
<div class="f-brand"><img src="images/logo.png" alt="Yến Sào Hoàng Yến" width="88" height="88" loading="lazy"><h3>Công ty Cổ phần Yến Sào Hoàng Yến</h3>
<ul><li>{ic('pin')}<span>Trụ sở &amp; văn phòng: 391 Cát Bi, Hải An, Hải Phòng</span></li><li>{ic('phone')}<a href="tel:0938699797">0938.699.797</a></li><li>{ic('mail')}<a href="mailto:yensaohoangyenvietnam@gmail.com">yensaohoangyenvietnam@gmail.com</a></li><li>{ic('globe')}<span>yensaohoangyenvietnam.com</span></li></ul></div>
<div><h4>Chính sách</h4><ul class="f-links"><li><a href="#">Tuyển đại lý, NPP, nhượng quyền</a></li><li><a href="#">Chiết khấu đối tác doanh nghiệp</a></li><li><a href="#">Chính sách vận chuyển</a></li><li><a href="#">Chính sách đổi trả</a></li><li><a href="#">Chính sách bảo mật</a></li><li><a href="#">Quy định sử dụng</a></li></ul></div>
<div><h4>Hướng dẫn</h4><ul class="f-links"><li><a href="#">Hướng dẫn mua hàng</a></li><li><a href="#">Hướng dẫn thanh toán</a></li><li><a href="#">Hướng dẫn giao nhận</a></li><li><a href="#">Điều khoản dịch vụ</a></li></ul></div>
<div class="f-pay"><h4>Thanh toán</h4><div class="pays">{''.join(f'<span><img src="images/pay-{p}.png" alt="Phương thức thanh toán" loading="lazy"></span>' for p in PAYS)}</div>
<h4>Chứng nhận</h4><div class="pays">{''.join(f'<span><img src="images/pay-{p}.png" alt="Chứng nhận website" loading="lazy"></span>' for p in CERT_F)}</div>
<div class="socials"><a href="https://www.facebook.com/yensaohoangyenvietnam" aria-label="Facebook">{ic('fb')}</a><a href="#" aria-label="YouTube">{ic('yt')}</a><a href="https://www.tiktok.com/@yensaohoangyen_vn" aria-label="TikTok">{ic('tiktok')}</a></div></div>
</div>
<div class="copy"><span>© 2021 – 2027 Yến Sào Hoàng Yến · Công ty Cổ phần Yến Sào Hoàng Yến</span><span>Yến Tiến Vua – Trao trọn tâm ý</span></div></div>
</footer>
<div class="fab"><a class="zalo" href="https://zalo.me/0938699797" target="_blank" rel="noopener" aria-label="Chat qua Zalo"></a><a class="call" href="tel:0938699797" aria-label="Gọi hotline">{ic('phone')}</a><button class="top" type="button" aria-label="Lên đầu trang" data-top>{ic('up')}</button></div>
<nav class="mbar" aria-label="Thanh tác vụ"><a href="index.html">{ic('home')}Trang chủ</a><a href="#danh-muc">{ic('grid')}Danh mục</a><a class="main" href="tel:0938699797"><span class="ic">{ic('phone')}</span><em>Gọi ngay</em></a><a href="https://zalo.me/0938699797"><img class="zalo-ic" src="images/zalo.webp" alt="" width="20" height="20">Zalo</a><a href="#">{ic('cart')}Giỏ hàng<span class="cart-count" data-cart-count>0</span></a></nav>
<div class="toast" role="status" aria-live="polite">{ic('check')}<span data-toast-text>Đã thêm vào giỏ</span></div>'''

page = f'''<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Yến Sào Hoàng Yến – Yến Tiến Vua · Tinh hoa yến sào cao cấp</title>
<meta name="description" content="Yến Sào Hoàng Yến – Yến Tiến Vua. Yến tổ tinh chế, yến chưng sẵn, yến chưng tươi và hộp quà biếu cao cấp. Đạt chuẩn ISO 22000 &amp; FDA, giao hỏa tốc 24h.">
<meta name="theme-color" content="#2e0b0e">
<link rel="icon" href="images/logo.png">
<link rel="preload" href="fonts/PlayfairDisplay-700-vietnamese.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="images/banner-1.jpg" as="image" media="(min-width:641px)">
<link rel="preload" href="images/banner-m1.jpg" as="image" media="(max-width:640px)">
<link rel="stylesheet" href="css/main.css">
</head>
<body>
{header}
<main>
{hero}
{promise}
{cats}
{products}
{needs}
{special}
{story}
{gift}
{why}
{cust}
{certs}
{posts}
{consult}
</main>
{footer}
<script src="js/main.js" defer></script>
</body>
</html>
'''
open(f'{ROOT}/index.html', 'w').write(page)
print('ok', len(page))
