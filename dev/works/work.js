/* 作品ごとのページの動き
 * ・バーの下の波形＝ページのどこまで読んだか（再生位置）。節の頭に印、押すとそこへ。節をまたぐとカチッと鳴る（音が ON の時）
 * ・下の帯（ほかの作品）は、なぞると作品ごとの音・押すと決定の音で移る。← → キーでも前後の作品へ（7 の次は 1）
 * ・画像の下の ▶ は動画（dev/video/<slug>.mp4 を置くと押せる）。作品資料の PDF も置くと押せる */
(function(){
  var reduce = false;
  try{ reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches; }catch(e){}
  var body = document.body, slug = body.getAttribute('data-slug') || '';
  var S = window.SFX || {isOn: function(){ return false; }, note: function(){}, confirm: function(){}, back: function(){}, tick: function(){}};
  function zoom(){ return parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--z')) || 1; }
  function col(){ return getComputedStyle(body).getPropertyValue('--wa').trim() || '#7DB8D1'; }

  //音を鳴らしてから移る（鳴っている途中で切れないよう、ON の時だけ少し待つ）
  function go(href, kind){
    if (kind === 'back') S.back(); else S.confirm();
    if (S.isOn()) setTimeout(function(){ location.href = href; }, 150); else location.href = href;
  }

  // ---------- ほかの作品の帯・前後の作品 ----------
  var items = [].slice.call(document.querySelectorAll('.ws-i a')), list = document.querySelector('.ws-list'), cur = -1;
  items.forEach(function(a, k){ if (a.getAttribute('aria-current') === 'page') cur = k; });
  var N = items.length;
  var tot = document.querySelector('.wp-total');
  if (tot) tot.textContent = ' / ' + String(N).padStart(2, '0');
  //前後は帯の並びで決める（確認用だけの作品も入る。公開用ではそこが無い並びになる）
  function setNav(sel, k){
    var el = document.querySelector(sel), a = items[k];
    if (!el || !a) return;
    el.href = a.getAttribute('href');
    var no = a.querySelector('.ws-no');
    el.querySelector('b').textContent = (no ? no.textContent + ' ' : '') + a.getAttribute('data-t');
  }
  if (cur >= 0 && N > 1){ setNav('.wp-prev', (cur - 1 + N) % N); setNav('.wp-next', (cur + 1) % N); }
  //帯はループ：同じ並びを前後にもう 1 周ずつ写して、真ん中の周を見せる。端の周へ寄ったら 1 周ぶん戻す（同じ並びなので継ぎ目は見えない）
  var curI = cur >= 0 ? items[cur].getAttribute('data-i') : null, orig = list ? [].slice.call(list.children) : [], loop = !!list && N > 1;
  if (loop){
    var pre = document.createDocumentFragment(), post = document.createDocumentFragment();
    orig.forEach(function(li){
      [pre, post].forEach(function(f){
        var c = li.cloneNode(true);
        c.setAttribute('aria-hidden', 'true');
        c.classList.add('ws-clone');
        c.querySelectorAll('a').forEach(function(x){ x.tabIndex = -1; x.removeAttribute('aria-current'); });
        f.appendChild(c);
      });
    });
    list.insertBefore(pre, list.firstChild);
    list.appendChild(post);
  }
  function period(){ return loop ? list.children[2 * N].offsetLeft - list.children[N].offsetLeft : 0; }
  function jump(dx){ list.style.scrollBehavior = 'auto'; list.scrollLeft += dx; list.style.scrollBehavior = ''; }
  //真ん中の周から外れていたら、見た目はそのまま 1 周ぶん戻す
  function wrap(){
    if (!loop) return;
    var P = period(), base = list.children[N].offsetLeft - list.children[0].offsetLeft;
    if (!P) return;
    if (list.scrollLeft < base - P * .5) jump(P);
    else if (list.scrollLeft > base + P * .5) jump(-P);
  }
  //今の作品を帯の真ん中へ（真ん中の周の物）
  if (list && cur >= 0){
    var li = orig[cur];
    list.style.scrollBehavior = 'auto';
    list.scrollLeft = li.offsetLeft - list.children[0].offsetLeft - (list.clientWidth - li.offsetWidth) / 2;
    list.style.scrollBehavior = '';
  }
  if (loop){
    var endT = 0;
    list.addEventListener('scroll', function(){ clearTimeout(endT); endT = setTimeout(wrap, 140); }, {passive: true});
    window.addEventListener('resize', wrap);
  }
  [].slice.call(document.querySelectorAll('.ws-i a')).forEach(function(a){
    a.addEventListener('pointerenter', function(e){ if (e.pointerType === 'mouse') S.note(+a.getAttribute('data-i')); });
    a.addEventListener('focus', function(){ S.note(+a.getAttribute('data-i')); });
    a.addEventListener('click', function(e){
      if (e.metaKey || e.ctrlKey || e.shiftKey || e.button) return;
      e.preventDefault();
      if (a.getAttribute('data-i') === curI){ S.tick(); return; }
      go(a.getAttribute('href'));
    });
  });
  //矢印は 1 作品ずつ。押す前に端の周に寄っていたら戻しておく
  document.querySelectorAll('.ws-arr').forEach(function(b){
    b.addEventListener('click', function(){
      if (!list) return;
      S.tick();
      wrap();
      var step = orig.length > 1 ? orig[1].offsetLeft - orig[0].offsetLeft : list.clientWidth * .8;
      list.scrollBy({left: (b.classList.contains('next') ? 1 : -1) * step, behavior: reduce ? 'auto' : 'smooth'});
    });
  });
  document.querySelectorAll('.wp-prev, .wp-next').forEach(function(a){
    a.addEventListener('click', function(e){ if (e.metaKey || e.ctrlKey || e.shiftKey || e.button) return; e.preventDefault(); go(a.href); });
  });
  document.querySelectorAll('[data-back]').forEach(function(a){
    a.addEventListener('click', function(e){ if (e.metaKey || e.ctrlKey || e.shiftKey || e.button) return; e.preventDefault(); go(a.href, 'back'); });
  });
  window.addEventListener('keydown', function(e){
    if (e.ctrlKey || e.metaKey || e.altKey || (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight')) return;
    var t = e.target;
    if (t && t.closest && t.closest('input, textarea, select, [contenteditable], video, dialog')) return;
    var el = document.querySelector(e.key === 'ArrowRight' ? '.wp-next' : '.wp-prev');
    if (!el) return;
    e.preventDefault();
    go(el.href);
  });

  // ---------- 読んだ所までの波形（バーの下） ----------
  var pcv = document.querySelector('.wb-prog canvas'), marks = [], lastSec = -1;
  //形は作品の名前から決まる（開くたびに同じ。ときどき大きく立ち上がって、だんだん減る）
  function shape(seedStr, n){
    var seed = 7, i, env = .3, out = [];
    for (i = 0; i < seedStr.length; i++) seed = (seed * 31 + seedStr.charCodeAt(i)) >>> 0;
    function rnd(){ seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; }
    for (i = 0; i < n; i++){
      if (rnd() < .11) env = .6 + rnd() * .4;
      env = Math.max(.18 + rnd() * .12, env * .9);
      out.push(Math.min(1, env * (.62 + rnd() * .45)));
    }
    return out;
  }
  var pbase = shape(slug + ':page', 220);
  function maxScroll(){ return Math.max(1, document.documentElement.scrollHeight - window.innerHeight); }
  function measureMarks(){
    marks = [].slice.call(document.querySelectorAll('[data-mark]')).map(function(el){
      var y = el.getBoundingClientRect().top + window.scrollY - window.innerHeight * .35;
      return {y: Math.max(0, y), r: Math.min(1, Math.max(0, y / maxScroll())), label: el.getAttribute('data-mark')};
    });
  }
  function drawProg(){
    if (!pcv) return;
    var w = pcv.clientWidth, h = pcv.clientHeight, dpr = Math.min(2, window.devicePixelRatio || 1) * zoom();
    if (!w || !h) return;
    if (pcv.width !== Math.round(w * dpr) || pcv.height !== Math.round(h * dpr)){ pcv.width = Math.round(w * dpr); pcv.height = Math.round(h * dpr); }
    var g = pcv.getContext('2d'), r = Math.min(1, window.scrollY / maxScroll()), bw = 2, gap = 2, n = Math.floor((w + gap) / (bw + gap)), k, f, a, v, x, bh, c = col();
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.clearRect(0, 0, w, h);
    for (k = 0; k < n; k++){
      f = k / Math.max(1, n - 1) * (pbase.length - 1); a = Math.floor(f);
      v = pbase[a] + (pbase[Math.min(pbase.length - 1, a + 1)] - pbase[a]) * (f - a);
      x = k * (bw + gap);
      bh = Math.max(2, v * (h - 6));
      g.fillStyle = x <= r * w ? c : 'rgba(227,233,238,.2)';
      g.fillRect(x, (h - bh) / 2, bw, bh);
    }
    //節の頭の印
    g.fillStyle = '#E3E9EE';
    marks.forEach(function(m){ var mx = Math.round(m.r * (w - 2)); g.fillRect(mx, 0, 2, 4); g.fillRect(mx, h - 4, 2, 4); });
    //再生位置の線
    g.fillStyle = '#FFFFFF';
    g.fillRect(Math.round(r * (w - 2)), 0, 2, h);
  }
  function onScroll(){
    drawProg();
    var y = window.scrollY + 2, s = -1;
    marks.forEach(function(m, k){ if (y >= m.y) s = k; });
    if (s !== lastSec){ if (lastSec !== -2) S.tick(); lastSec = s; }
  }
  if (pcv){
    pcv.parentNode.addEventListener('click', function(e){
      var rect = pcv.getBoundingClientRect(), r = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
      window.scrollTo({top: r * maxScroll(), behavior: reduce ? 'auto' : 'smooth'});
    });
  }
  var ticking = false;
  window.addEventListener('scroll', function(){ if (ticking) return; ticking = true; requestAnimationFrame(function(){ ticking = false; onScroll(); }); }, {passive: true});
  window.addEventListener('resize', function(){ measureMarks(); drawProg(); drawWave(); });
  window.addEventListener('load', function(){ measureMarks(); drawProg(); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function(){ measureMarks(); drawProg(); });
  lastSec = -2; measureMarks(); onScroll();

  // ---------- 画像の下の波形と動画 ----------
  var wcv = document.querySelector('.wp-wave'), wbase = shape(slug, 96), play = reduce ? 1 : 0, hover = -1, run = 0;
  function drawWave(){
    if (!wcv) return;
    var w = wcv.clientWidth, h = wcv.clientHeight, dpr = Math.min(2, window.devicePixelRatio || 1) * zoom();
    if (!w || !h) return;
    if (wcv.width !== Math.round(w * dpr) || wcv.height !== Math.round(h * dpr)){ wcv.width = Math.round(w * dpr); wcv.height = Math.round(h * dpr); }
    var g = wcv.getContext('2d'), bw = 3, gap = 2, n = Math.max(8, Math.floor((w + gap) / (bw + gap))), upto = hover >= 0 ? hover : play * w, k, f, a, v, x, d, bh;
    g.setTransform(dpr, 0, 0, dpr, 0, 0);
    g.clearRect(0, 0, w, h);
    g.fillStyle = col();
    for (k = 0; k < n; k++){
      f = k / (n - 1) * (wbase.length - 1); a = Math.floor(f);
      v = wbase[a] + (wbase[Math.min(wbase.length - 1, a + 1)] - wbase[a]) * (f - a);
      x = k * (bw + gap);
      if (hover >= 0){ d = (x - hover) / 34; v = Math.min(1, v * (1 + .75 * Math.exp(-d * d))); }
      bh = Math.max(2, v * (h - 2));
      g.globalAlpha = x + bw <= upto ? 1 : .26;
      g.fillRect(x, (h - bh) / 2, bw, bh);
    }
    g.globalAlpha = 1;
    if (hover >= 0){ g.fillStyle = '#E3E9EE'; g.fillRect(Math.round(hover), 0, 1, h); }
  }
  //開いた時に左から右へ色が付く（再生の見立て）
  if (!reduce){
    var t0 = performance.now(), my = ++run;
    (function f(now){
      if (run !== my) return;
      var q = Math.min(1, Math.max(0, (now - t0 - 500) / 2600));
      play = 1 - Math.pow(1 - q, 3);
      drawWave();
      if (q < 1) requestAnimationFrame(f);
    })(t0);
  }
  var btn = document.querySelector('.wp-play'), shot = document.querySelector('.wp-shot'), video = null, raf = 0, url = body.getAttribute('data-video') || '';
  var title = (document.querySelector('h1') || {}).textContent || '';
  function progress(){
    cancelAnimationFrame(raf);
    if (!video) return;
    if (video.duration){ run++; play = video.currentTime / video.duration; drawWave(); }
    if (!video.paused && !video.ended) raf = requestAnimationFrame(progress);
  }
  function state(){
    var on = !!video && !video.paused && !video.ended;
    btn.classList.toggle('is-playing', on);
    body.classList.toggle('is-playing', on);
    btn.setAttribute('aria-label', title + (on ? ' の動画を止める' : ' の動画を再生'));
  }
  function ensure(){
    if (video) return video;
    video = document.createElement('video');
    video.preload = 'auto';
    video.playsInline = true;
    video.setAttribute('playsinline', '');
    video.src = url;
    shot.appendChild(video);
    video.addEventListener('play', function(){ state(); progress(); });
    video.addEventListener('pause', state);
    video.addEventListener('ended', function(){ state(); progress(); });
    video.addEventListener('click', toggle);
    return video;
  }
  function toggle(){
    if (!btn || btn.disabled) return;
    var v = ensure();
    if (v.paused || v.ended){ if (v.ended) v.currentTime = 0; var pr = v.play(); if (pr && pr['catch']) pr['catch'](function(){}); }
    else v.pause();
  }
  if (wcv){
    var at = function(e){ var r = wcv.getBoundingClientRect(); hover = r.width ? Math.max(0, Math.min(1, (e.clientX - r.left) / r.width)) * wcv.clientWidth : 0; drawWave(); };
    var off = function(){ hover = -1; drawWave(); };
    wcv.addEventListener('pointermove', at);
    wcv.addEventListener('pointerdown', at);
    wcv.addEventListener('pointerleave', off);
    wcv.addEventListener('pointercancel', off);
    wcv.addEventListener('pointerup', function(e){ if (e.pointerType !== 'mouse') off(); });
    wcv.addEventListener('click', function(e){
      if (!btn || btn.disabled) return;
      var r = wcv.getBoundingClientRect(), q = Math.max(0, Math.min(1, (e.clientX - r.left) / r.width));
      var v = ensure(), seek = function(){ v.currentTime = q * v.duration; if (v.paused){ var pr = v.play(); if (pr && pr['catch']) pr['catch'](function(){}); } progress(); };
      if (v.readyState >= 1) seek(); else v.addEventListener('loadedmetadata', seek, {once: true});
    });
  }
  if (btn){
    btn.addEventListener('click', toggle);
    var enable = function(){ btn.disabled = false; btn.querySelector('small').textContent = 'PLAY'; state(); };
    if (url && window.fetch) fetch(url, {method: 'HEAD', cache: 'no-store'}).then(function(r){ if (r.ok) enable(); }, function(){});
  }
  drawWave();

  // ---------- 作品資料（PDF） ----------
  var doc = document.querySelector('.wp-doc[data-pdf]'), dlg = document.getElementById('pdf-dlg'), frame = document.getElementById('pdf-frame');
  if (doc && dlg){
    var purl = doc.getAttribute('data-pdf'), phone = window.matchMedia ? window.matchMedia('(max-width: 860px), (pointer: coarse)') : null;
    doc.addEventListener('click', function(){
      if (navigator.pdfViewerEnabled === false || (phone && phone.matches) || !dlg.showModal){ window.open(purl, '_blank', 'noopener'); return; }
      document.getElementById('pdf-open').href = purl;
      frame.src = purl;
      dlg.showModal();
    });
    dlg.addEventListener('close', function(){ frame.removeAttribute('src'); });
    dlg.addEventListener('click', function(e){ if (e.target === dlg || e.target.closest('[data-close]')) dlg.close(); });
    if (window.fetch) fetch(purl, {method: 'HEAD', cache: 'no-store'}).then(function(r){ if (r.ok){ doc.disabled = false; doc.querySelector('small').textContent = 'OPEN'; } }, function(){});
  }
})();
