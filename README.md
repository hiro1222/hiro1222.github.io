# ポートフォリオ

ゲームのサウンドプログラマーを目指す学生のポートフォリオサイト。

- 公開用: https://hiro1222.github.io/ （`index.html`・`img/`・`audio/`）
- 調整確認用: https://hiro1222.github.io/dev/ （`dev/` の中に同じ物を全部持つ写し。左下に「調整確認用」の帯）
- 直すのはいつも `dev/` の方。確かめてから公開用へ写す:
  - `python tools/site.py publish` … `dev/` → 公開用（確認用の帯 `<!-- DEV-ONLY -->〜<!-- /DEV-ONLY -->` とタイトルの【確認用】は消える。`img/`・`audio/` は `dev/` と同じ中身にそろう）
  - `python tools/site.py reset-dev` … 公開用の中身で `dev/` を作り直す
- 外部の読み込みは Google Fonts だけ。どちらも検索に出さない（noindex）
