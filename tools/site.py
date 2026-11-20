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
ASSETS = ['img', 'audio', 'video', 'docs']
TITLE_DEV = '【確認用】'
# 確認用だけに足す帯（2026-11-20 本人「確認用の下のタブ消して」で無しに。確認用だと分かるのはタイトルの【確認用】だけ）
DEV_BLOCK = ''


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
    # 印の入れ子は消し方がずれるので止める（始まりと終わりが交互になっているか）
    seq = ['E' if m.group(1) else 'S' for m in re.finditer(r'(?:<!--|/\*) (/)?DEV-ONLY', s)]
    bad = [i for i in range(len(seq) - 1) if seq[i] == seq[i + 1]]
    assert not bad and (not seq or (seq[0] == 'S' and seq[-1] == 'E')), '確認用だけの印が入れ子か、閉じていない所がある（%d 番目あたり）' % (bad[0] + 1 if bad else 0)
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
    if DEV_BLOCK:
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
