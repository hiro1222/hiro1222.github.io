# ポートフォリオ

ゲームのサウンドプログラマーを目指す学生のポートフォリオサイト。

- 公開用: https://hiro1222.github.io/ （`index.html`・`img/`・`audio/`）
- 調整確認用: https://hiro1222.github.io/dev/ （`dev/` の中に同じ物を全部持つ写し。タイトルに【確認用】）
- 直すのはいつも `dev/` の方。確かめてから公開用へ写す:
  - `python tools/site.py publish` … `dev/` → 公開用（確認用だけの部分 `<!-- DEV-ONLY: … -->`〜`<!-- /DEV-ONLY -->`（CSS・JS は `/* DEV-ONLY: … */`〜`/* /DEV-ONLY */`）とタイトルの【確認用】は消える。`img/`・`audio/` は `dev/` と同じ中身にそろう）
  - `python tools/site.py reset-dev` … 公開用の中身で `dev/` を作り直す
- 作品の動画（確認用で仕組みだけ）: `dev/video/<名前>.mp4` を置くと、その作品の ▶ が押せるようになる。名前は `idreal`・`horror`・`osumitsuki`・`ribbond`・`soundmarker`・`friend-a`・`friend-b`。1 本 5〜10 MB くらいの H.264 の mp4 が目安（publish で `video/` も公開用へそろう）
- 作品資料（確認用で、今は IdReal だけ）: `dev/docs/idreal.pdf` を置くと、MORE の横の「作品資料」が押せるようになる（PC は窓の中、スマホは新しいタブで PDF を開く）。publish で `docs/` も公開用へそろう
- ホームのミニゲーム（確認用）の音: `dev/audio/idreal-steps/`（足音）・`dev/audio/idreal-claps/`（手拍子）は、マスごとに Idreal で焼いた「素の音＋響き」の mp3。耳の向き 4 つ（`u` 地図の上・`r` 右・`d` 下・`l` 左）のフォルダに分けてあり、ミニゲームは三角の向きに一番近い物を鳴らす（Idreal の道具 portfolio_bake の bake_footmap → encode_footmap、向き 4 つは同じ倍率で焼く）。`#smap` の `data-sound="synth"` で前の合成の音に戻せる
- 外部の読み込みは Google Fonts だけ。どちらも検索に出さない（noindex）
