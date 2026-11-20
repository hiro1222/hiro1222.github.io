# -*- coding: utf-8 -*-
# 公開用（/）と調整確認用（/dev/）を行き来させる
#   python tools/site.py publish     … dev/ の中身を公開用へ写す（確認用だけの部分は消す）
#   python tools/site.py reset-dev   … 公開用の中身で dev/ を作り直す（確認用の帯を足す）
# dev/ は index.html・img/・audio/ を全部持つ写し。直すのはいつも dev/ の方
import io
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEV = os.path.join(ROOT, 'dev')
ASSETS = ['img', 'audio']
TITLE_DEV = '【確認用】'
DEV_BLOCK = '''<!-- DEV-ONLY: 調整確認用のページだけに出す（tools/site.py publish で消える） -->
<style>
.devbar{position:fixed; left:12px; bottom:12px; z-index:60; display:flex; flex-wrap:wrap; align-items:center; gap:6px 8px; max-width:calc(100% - 24px); padding:6px 10px; border-radius:8px; background:#D9774C; color:#0D1620; font:600 12px/1.4 var(--f-body); box-shadow:0 6px 20px rgba(0,0,0,.35)}
.devbar b{letter-spacing:.06em}
.devbar button{padding:3px 8px; border:1px solid rgba(13,22,32,.45); border-radius:5px; background:rgba(255,255,255,.35); color:inherit; font:inherit; cursor:pointer}
.devbar button[aria-pressed="true"]{background:#0D1620; color:#FFFFFF}
</style>
<div class="devbar" role="region" aria-label="調整確認用"><b>調整確認用</b><span>ミニマップの足音:</span><button type="button" data-snd="synth">合成</button><button type="button" data-snd="idreal">IdReal</button></div>
<script>
// 確認用：ミニマップの足音を 合成／IdReal で焼いた音 で切り替える（この端末で覚える）
(function(){
  var sm = document.getElementById('smap'), bs = document.querySelectorAll('.devbar [data-snd]');
  if (!sm) return;
  function set(v){
    sm.setAttribute('data-sound', v);
    bs.forEach(function(b){ b.setAttribute('aria-pressed', b.getAttribute('data-snd') === v ? 'true' : 'false'); });
    try{ localStorage.setItem('dev-snd', v); }catch(e){}
  }
  bs.forEach(function(b){ b.addEventListener('click', function(){ set(b.getAttribute('data-snd')); }); });
  var v = sm.getAttribute('data-sound') || 'synth';
  try{ v = localStorage.getItem('dev-snd') || v; }catch(e){}
  set(v);
})();
</script>
<!-- /DEV-ONLY -->
'''


def read(p):
    return io.open(p, encoding='utf-8', newline='').read()


def write(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


def mirror(src, dst):
    # src と同じ中身に（無い物は足す・違う物は上書き・src に無い物は消す）
    added = changed = removed = 0
    for base, dirs, files in os.walk(src):
        rel = os.path.relpath(base, src)
        os.makedirs(os.path.join(dst, rel), exist_ok=True)
        for f in files:
            a, b = os.path.join(base, f), os.path.join(dst, rel, f)
            if not os.path.exists(b):
                added += 1
            elif open(a, 'rb').read() != open(b, 'rb').read():
                changed += 1
            else:
                continue
            shutil.copy2(a, b)
    for base, dirs, files in os.walk(dst, topdown=False):
        rel = os.path.relpath(base, dst)
        for f in files:
            if not os.path.exists(os.path.join(src, rel, f)):
                os.remove(os.path.join(base, f))
                removed += 1
        if not os.listdir(base) and not os.path.exists(os.path.join(src, rel)):
            os.rmdir(base)
    return added, changed, removed


# 確認用だけの部分の印。HTML は <!-- DEV-ONLY: … --> 〜 <!-- /DEV-ONLY -->、CSS・JS は /* DEV-ONLY: … */ 〜 /* /DEV-ONLY */
DEV_ONLY = re.compile(r'[ \t]*(?:<!--|/\*) DEV-ONLY.*?(?:<!--|/\*) /DEV-ONLY (?:-->|\*/)[ \t]*\r?\n?', re.S)


def publish():
    s = read(os.path.join(DEV, 'index.html'))
    n = len(DEV_ONLY.findall(s))
    s = DEV_ONLY.sub('', s)
    assert 'DEV-ONLY' not in s and 'devbar' not in s
    s = s.replace('<title>' + TITLE_DEV, '<title>')
    write(os.path.join(ROOT, 'index.html'), s)
    print('index.html: 確認用の部分 %d か所を消して写した' % n)
    for a in ASSETS:
        if os.path.isdir(os.path.join(DEV, a)):
            print('%s/: 足した %d・変えた %d・消した %d' % ((a,) + mirror(os.path.join(DEV, a), os.path.join(ROOT, a))))


def reset_dev():
    s = read(os.path.join(ROOT, 'index.html'))
    nl = '\r\n' if '\r\n' in s else '\n'
    assert s.count('</body>') == 1 and s.count('<title>') == 1
    s = s.replace('<title>', '<title>' + TITLE_DEV)
    s = s.replace('</body>', DEV_BLOCK.replace('\n', nl) + '</body>')
    os.makedirs(DEV, exist_ok=True)
    write(os.path.join(DEV, 'index.html'), s)
    print('dev/index.html を公開用から作り直した')
    for a in ASSETS:
        if os.path.isdir(os.path.join(ROOT, a)):
            print('dev/%s/: 足した %d・変えた %d・消した %d' % ((a,) + mirror(os.path.join(ROOT, a), os.path.join(DEV, a))))


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'publish':
        publish()
    elif cmd == 'reset-dev':
        reset_dev()
    else:
        print(__doc__ or '使い方: python tools/site.py publish | reset-dev')
        print('使い方: python tools/site.py publish | reset-dev')
        sys.exit(1)
