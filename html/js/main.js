(function () {
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  // Header thu gọn khi cuộn + nút lên đầu trang
  var header = $('.header'), topBtn = $('[data-top]');
  function onScroll() {
    var y = window.scrollY;
    header.classList.toggle('scrolled', y > 40);
    if (topBtn) topBtn.classList.toggle('show', y > 700);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  if (topBtn) topBtn.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });

  // Menu mobile
  var drawer = $('#drawer');
  function setDrawer(open) {
    drawer.classList.toggle('open', open);
    drawer.setAttribute('aria-hidden', String(!open));
    document.body.style.overflow = open ? 'hidden' : '';
  }
  $$('[data-drawer-open]').forEach(function (b) { b.addEventListener('click', function () { setDrawer(true); }); });
  $$('[data-drawer-close]').forEach(function (b) { b.addEventListener('click', function () { setDrawer(false); }); });
  $$('#drawer nav > a').forEach(function (a) { a.addEventListener('click', function () { setDrawer(false); }); });

  // Tìm kiếm
  var search = $('#search');
  $$('[data-search-open]').forEach(function (b) {
    b.addEventListener('click', function () { search.classList.add('open'); setTimeout(function () { $('input', search).focus(); }, 50); });
  });
  search.addEventListener('click', function (e) { if (e.target === search) search.classList.remove('open'); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { search.classList.remove('open'); setDrawer(false); }
  });


  // Hero banner: mũi tên + tự chạy 5s (dừng khi rê chuột/chạm)
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  $$('[data-hero]').forEach(function (root) {
    var track = $('.hb-track', root), n = track.children.length, paused = false;
    function cur() { return Math.round(track.scrollLeft / (track.clientWidth || 1)); }
    function go(i) {
      if (!track.offsetParent) return; // slider đang ẩn ở breakpoint này
      track.scrollTo({ left: ((i + n) % n) * track.clientWidth, behavior: 'smooth' });
    }
    $('.prev', root).addEventListener('click', function () { go(cur() - 1); });
    $('.next', root).addEventListener('click', function () { go(cur() + 1); });
    ['mouseenter', 'touchstart', 'focusin'].forEach(function (ev) { root.addEventListener(ev, function () { paused = true; }, { passive: true }); });
    ['mouseleave', 'touchend', 'focusout'].forEach(function (ev) { root.addEventListener(ev, function () { paused = false; }, { passive: true }); });
    if (!reduce && n > 1) setInterval(function () { if (!paused && !document.hidden) go(cur() + 1); }, 5000);
  });

  // Tabs sản phẩm
  $$('.tab').forEach(function (t) {
    t.addEventListener('click', function () {
      var key = t.getAttribute('data-tab');
      $$('.tab').forEach(function (x) { x.classList.toggle('on', x === t); x.setAttribute('aria-selected', String(x === t)); });
      $$('.panel').forEach(function (p) { p.classList.toggle('on', p.getAttribute('data-panel') === key); });
    });
  });

  // Bộ lọc con (Tất cả / Trẻ em / Người lớn …)
  $$('.chips').forEach(function (box) {
    var panel = box.closest('.panel');
    $$('.chip', box).forEach(function (c) {
      c.addEventListener('click', function () {
        var sub = c.getAttribute('data-sub');
        $$('.chip', box).forEach(function (x) { x.classList.toggle('on', x === c); });
        $$('.card', panel).forEach(function (card) {
          card.classList.toggle('is-hidden', sub !== 'all' && card.getAttribute('data-sub') !== sub);
        });
      });
    });
  });

  // Slider (CSS scroll-snap + nút trước/sau)
  $$('[data-slider]').forEach(function (s) {
    var track = $('.track', s), prev = $('[data-prev]', s), next = $('[data-next]', s);
    function step() { var first = track.children[0]; return first ? first.getBoundingClientRect().width + 22 : track.clientWidth; }
    function update() {
      prev.disabled = track.scrollLeft < 4;
      next.disabled = track.scrollLeft > track.scrollWidth - track.clientWidth - 4;
    }
    prev.addEventListener('click', function () { track.scrollBy({ left: -step(), behavior: 'smooth' }); });
    next.addEventListener('click', function () { track.scrollBy({ left: step(), behavior: 'smooth' }); });
    track.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  });

  // Giỏ hàng (mô phỏng phía giao diện)
  var count = 0, toast = $('.toast'), toastTimer;
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-add]');
    if (!btn) return;
    count++;
    btn.classList.add('added');
    clearTimeout(btn._t);
    btn._t = setTimeout(function () { btn.classList.remove('added'); }, 1600);
    $$('[data-cart-count]').forEach(function (c) {
      c.textContent = count;
      c.classList.add('bump');
      setTimeout(function () { c.classList.remove('bump'); }, 300);
    });
    $('[data-toast-text]').textContent = 'Đã thêm “' + btn.getAttribute('data-add') + '” vào giỏ';
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.classList.remove('show'); }, 2200);
  });

  // Hiệu ứng xuất hiện + đếm số
  var nf = new Intl.NumberFormat('vi-VN');
  function countUp(el) {
    var end = +el.getAttribute('data-count'), t0 = null;
    function tick(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / 1400, 1);
      el.textContent = nf.format(Math.round(end * (1 - Math.pow(1 - p, 3))));
      if (p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('in');
        $$('[data-count]', en.target).forEach(countUp);
        io.unobserve(en.target);
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    $$('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    $$('.reveal').forEach(function (el) { el.classList.add('in'); });
  }
})();
