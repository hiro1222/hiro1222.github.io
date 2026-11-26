# -*- coding: utf-8 -*-
# 作品の中身（tools/works.json）から、確認用の
#   1) トップの作品一覧（dev/index.html の <!-- WORKS:BEGIN --> 〜 <!-- WORKS:END --> の間）
#   2) 作品ごとのページ（dev/works/<slug>.html）
# を作る。作品の文を直す時は works.json を直してから
#   python tools/make_works.py
# 中身が「準備中」の所は null にしておく（ページには「準備中」と出る）。devOnly の作品は確認用だけ（公開用へ写す時に消える）
import html
import io
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEV = os.path.join(ROOT, 'dev')
WORKS = json.load(io.open(os.path.join(ROOT, 'tools', 'works.json'), encoding='utf-8'))
TODO = '<span class="todo">準備中</span>'
IMG_V = '4'
SPEAKER = ('<svg class="sfx-ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z" fill="currentColor"/>'
           '<path class="sfx-w" d="M15.5 9a4 4 0 0 1 0 6M18 6.5a7.5 7.5 0 0 1 0 11" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
           '<path class="sfx-x" d="M16 9.5l5 5M21 9.5l-5 5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>')
SFX_BTN = '<button type="button" class="sfx" aria-pressed="false" aria-label="操作の音">' + SPEAKER + '<span class="sfx-l">SOUND OFF</span></button>'


def t(v):
    return v if v else TODO


def a(v):
    return html.escape(v or '', quote=True)


def genre_tag(g):
    # 表の「—（音響エンジン）」は一覧の札では「音響エンジン」
    if not g:
        return None
    m = re.match(r'^—（(.*)）$', g)
    return m.group(1) if m else g


def dev_wrap(w, s, what):
    return ('<!-- DEV-ONLY: %s（確認用だけ） -->\n' % what) + s + '\n<!-- /DEV-ONLY -->' if w.get('devOnly') else s


def img_tag(w, prefix, cls, lazy=True, alt=None):
    im = w.get('image')
    if not im:
        return '<span class="%s-noimg">IMAGE<br>準備中</span>' % cls
    return ('<img src="%s%s?v=%s" width="%d" height="%d" alt="%s"%s decoding="async" style="view-transition-name:jk-%s">'
            % (prefix, im['src'], IMG_V, im['w'], im['h'], a(im['alt'] if alt is None else alt), ' loading="lazy"' if lazy else '', w['slug']))


# ---------- 1) トップの作品一覧 ----------
def list_block():
    rows = []
    for i, w in enumerate(WORKS):
        tags = ['<span>%s</span>' % w['year']] if w.get('year') else []
        g = genre_tag(w.get('genre'))
        if g:
            tags.append('<span>%s</span>' % g)
        if w.get('wip'):
            tags.append('<span class="wl-wip">制作中</span>')
        row = ('    <li class="wl-i" style="--wa:%s">\n'
               '      <a class="wl-a" href="works/%s.html" data-i="%d">\n'
               '        <span class="wl-no" aria-hidden="true"><i class="wl-cur"></i>%02d</span>\n'
               '        <span class="wl-jk"><span class="wl-disc" aria-hidden="true"></span>%s</span>\n'
               '        <span class="wl-body">\n'
               '          <span class="wl-tags">%s</span>\n'
               '          <span class="wl-t">%s</span>\n'
               '          <span class="wl-k">%s</span>\n'
               '        </span>\n'
               '        <span class="wl-side" aria-hidden="true"><span class="wl-eq"><i></i><i></i><i></i><i></i><i></i></span></span>\n'
               '      </a>\n'
               '    </li>') % (w['color'], w['slug'], i, i + 1, img_tag(w, '', 'wl', alt=''), ''.join(tags), w['title'], t(w.get('kodawari')))
        rows.append(dev_wrap(w, row, w['title']))
    return ('<!-- WORKS:BEGIN（tools/make_works.py が tools/works.json から作る。ここは手で直さない） -->\n'
            '  <!-- 03 作品：トラックリストの形の一覧。押すと作品ごとのページ（works/〇〇.html）へ -->\n'
            '  <section class="panel dark p-works" id="works" aria-labelledby="h-works">\n'
            '    <div class="wrap">\n'
            '      <div class="wl-head">\n'
            '        <div class="head">\n'
            '          <p class="eyebrow"><span class="no">02</span>Works</p>\n'
            '          <h2 id="h-works">作品</h2>\n'
            '        </div>\n'
            '      </div>\n'
            '      <ol class="wl">\n' + '\n'.join(rows) + '\n      </ol>\n'
            '    </div>\n'
            '  </section>\n'
            '  <!-- WORKS:END -->')


# ---------- 2) 作品ごとのページ ----------
def facts(w):
    items = [('ゲームジャンル', w.get('genre')), ('制作規模', w.get('scale')), ('担当範囲', w.get('role')),
             ('制作期間', w.get('period')), ('制作環境', w.get('env'))]
    return ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (k, t(v)) for k, v in items)


def points(w):
    out = []
    for k, p in enumerate(w.get('points') or [], 1):
        out.append('<li class="wp-pt"><h3><span class="wp-pt-no">%02d</span>%s</h3><p>%s</p></li>'
                   % (k, p.get('h') or '<span class="todo">こだわり（準備中）</span>', t(p.get('p'))))
    return '<ol class="wp-pts">' + ''.join(out) + '</ol>' if out else ''


def strip_items(cur):
    out = []
    for i, w in enumerate(WORKS):
        im = w.get('image')
        th = ('<img src="../%s?v=%s" width="%d" height="%d" alt="" loading="lazy" decoding="async">' % (im['src'], IMG_V, im['w'], im['h'])
              if im else '<span class="ws-noimg">IMAGE 準備中</span>')
        li = ('<li class="ws-i%s" style="--wa:%s"><a href="%s.html" data-i="%d" data-t="%s"%s><span class="ws-th">%s</span>'
              '<span class="ws-cap"><span class="ws-no">%02d</span>%s</span>%s</a></li>'
              % (' is-cur' if w is cur else '', w['color'], w['slug'], i, a(w['title']), ' aria-current="page"' if w is cur else '',
                 th, i + 1, w['title'], ''))
        out.append(dev_wrap(w, li, w['title']))
    return '\n'.join(out)


def neighbors(w):
    # 公開用でも切れないよう、静的な前後は公開する作品だけで決める（確認用は work.js が一覧の並びで差し替える）
    pub = [x for x in WORKS if not x.get('devOnly')] if not w.get('devOnly') else WORKS
    k = pub.index(w)
    return pub[(k - 1) % len(pub)], pub[(k + 1) % len(pub)]


def page(w):
    i = WORKS.index(w)
    pv, nx = neighbors(w)
    g = genre_tag(w.get('genre'))
    im = w.get('image')
    pdf = ('<button type="button" class="wp-doc" data-pdf="../%s" disabled><span class="wp-doc-t">作品資料（PDF）</span><small>準備中</small></button>' % w['pdf']) if w.get('pdf') else ''
    cap = ('<figcaption>%s</figcaption>' % html.escape(im['alt'])) if im else ''
    eb = ['<span class="wp-track">TRACK <b>%02d</b><span class="wp-total"></span></span>' % (i + 1)]
    if w.get('year'):
        eb.append('<span class="wp-year">%s</span>' % w['year'])
    if w.get('wip'):
        eb.append('<span class="wp-wip">制作中</span>')
    s = '''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="竹内寛登のポートフォリオ：%(title_a)s">
<meta name="robots" content="noindex">
<meta name="format-detection" content="telephone=no, email=no, address=no, date=no">
<title>【確認用】%(title_a)s｜ポートフォリオ 竹内寛登</title>
%(devpage)s<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans+JP:wght@400;500;600&family=Shippori+Mincho+B1:wght@600;800&display=swap">
<link rel="stylesheet" href="work.css?v=%(v)s">
</head>
<!-- tools/make_works.py が tools/works.json から作ったページ。ここは手で直さない -->
<body class="wpage" style="--wa:%(color)s" data-slug="%(slug)s" data-video="../%(video)s">
<header class="wb">
  <div class="wb-in">
    <a class="logo" href="../" aria-label="Hiroto Takeuchi Portfolio（トップへ）"><span class="logo-disc" aria-hidden="true"></span><span class="logo-t"><span class="who">HIROTO TAKEUCHI</span><span class="mark">Portfolio</span></span></a>
    <a class="wb-back" href="../#works" data-back><span class="wb-back-ic" aria-hidden="true"></span><span class="wb-back-t">作品一覧<span class="wb-pc">へ</span></span></a>
    %(sfx)s
  </div>
  <div class="wb-prog" aria-hidden="true"><canvas></canvas></div>
</header>
<main class="wp">
  <section class="wp-hero">
    <div class="wp-in wp-hero-in">
      <div class="wp-ttl">
        <p class="wp-eb">%(eb)s</p>
        <h1>%(title)s</h1>
        %(genre)s
      </div>
      <figure class="wp-media">
        <div class="wp-jk"><span class="wp-disc" aria-hidden="true"></span><div class="wp-shot">%(img)s</div></div>
        <div class="wp-player"><button type="button" class="wp-play" disabled aria-label="%(title_a)s の動画（準備中）"><i class="wp-play-ic" aria-hidden="true"></i><span class="wp-play-t"><small>準備中</small><b>動画</b></span></button><canvas class="wp-wave"></canvas></div>
      </figure>
    </div>
  </section>
  <div class="wp-sheet">
    <div class="wp-in wp-sheet-in">
      <article class="wp-main">
        <section class="wp-sec" data-mark="概要">
          <h2 class="wp-h">概要</h2>
          <p class="wp-txt">%(summary)s</p>
        </section>
        <section class="wp-sec" data-mark="こだわり">
          <h2 class="wp-h">こだわり</h2>
          <p class="wp-txt wp-lead">%(kodawari)s</p>
          %(points)s
        </section>
      </article>
      <aside class="wp-credits" data-mark="制作情報">
        <h2 class="wp-cr-h">制作情報</h2>
        <dl class="wp-facts">%(facts)s</dl>
        %(pdf)s
      </aside>
    </div>
  </div>
  <nav class="wp-nav wp-in" aria-label="前後の作品">
    <a class="wp-prev" href="%(pv)s.html" rel="prev"><small>前の作品</small><b>%(pv_t)s</b></a>
    <a class="wp-list" href="../#works" data-back>一覧へ</a>
    <a class="wp-next" href="%(nx)s.html" rel="next"><small>次の作品</small><b>%(nx_t)s</b></a>
  </nav>
  <section class="wp-other" aria-labelledby="h-other">
    <div class="wp-in">
      <h2 class="wp-other-h" id="h-other">ほかの作品</h2>
    </div>
    <div class="ws">
      <button type="button" class="ws-arr prev" aria-label="前へ流す"></button>
      <ol class="ws-list">
%(strip)s
      </ol>
      <button type="button" class="ws-arr next" aria-label="次へ流す"></button>
    </div>
  </section>
</main>
<footer class="wf"><div class="wp-in wf-in"><span>© Hiroto Takeuchi</span><a href="../">ポートフォリオのトップへ</a></div></footer>
<dialog class="wp-dlg" id="pdf-dlg" aria-label="作品資料"><div class="wp-dlg-bar"><a id="pdf-open" href="#" target="_blank" rel="noopener">新しいタブで開く</a><button type="button" data-close>閉じる ×</button></div><iframe id="pdf-frame" title="作品資料（PDF）"></iframe></dialog>
<script src="../assets/sfx.js?v=%(v)s"></script>
<script src="../assets/progress.js?v=%(v)s"></script>
<script src="work.js?v=%(v)s"></script>
</body>
</html>
''' % {
        'title': w['title'], 'title_a': a(w['title']), 'color': w['color'], 'slug': w['slug'], 'video': w.get('video', ''),
        'devpage': '<meta name="pf-dev-only" content="1">\n' if w.get('devOnly') else '',  # 公開用へは写さない（tools/site.py が見る）
        'sfx': SFX_BTN, 'eb': ''.join(eb), 'genre': ('<p class="wp-genre">%s</p>' % g) if g else '',
        'img': img_tag(w, '../', 'wp', lazy=False), 'cap': cap,
        'summary': t(w.get('summary')), 'kodawari': t(w.get('kodawari')), 'points': points(w),
        'facts': facts(w), 'pdf': pdf,
        'pv': pv['slug'], 'pv_t': '%02d %s' % (WORKS.index(pv) + 1, pv['title']),
        'nx': nx['slug'], 'nx_t': '%02d %s' % (WORKS.index(nx) + 1, nx['title']),
        'strip': strip_items(w), 'v': '5',
    }
    return s


def main():
    os.makedirs(os.path.join(DEV, 'works'), exist_ok=True)
    for w in WORKS:
        io.open(os.path.join(DEV, 'works', w['slug'] + '.html'), 'w', encoding='utf-8', newline='\n').write(page(w))
    p = os.path.join(DEV, 'index.html')
    s = io.open(p, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    blk = list_block().replace('\n', nl)
    m = re.search(r'<!-- WORKS:BEGIN.*?<!-- WORKS:END -->', s, re.S)
    assert m, 'dev/index.html に <!-- WORKS:BEGIN --> 〜 <!-- WORKS:END --> が無い'
    s = s[:m.start()] + blk + s[m.end():]
    io.open(p, 'w', encoding='utf-8', newline='').write(s)
    print('作品ページ %d 枚と、トップの一覧を作った' % len(WORKS))


if __name__ == '__main__':
    main()
