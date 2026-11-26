# ポートフォリオ

ゲームのサウンドプログラマーを目指す学生のポートフォリオサイト。

- 公開用: https://hiro1222.github.io/ （`index.html`・`img/`・`audio/`）
- 調整確認用: https://hiro1222.github.io/dev/ （`dev/` の中に同じ物を全部持つ写し。タイトルに【確認用】）
- 直すのはいつも `dev/` の方。確かめてから公開用へ写す:
  - `python tools/site.py publish` … `dev/` → 公開用（確認用だけの部分 `<!-- DEV-ONLY: … -->`〜`<!-- /DEV-ONLY -->`（CSS・JS は `/* DEV-ONLY: … */`〜`/* /DEV-ONLY */`）とタイトルの【確認用】は消える。`img/`・`audio/` は `dev/` と同じ中身にそろう）
  - `python tools/site.py reset-dev` … 公開用の中身で `dev/` を作り直す
- 作品の動画（確認用で仕組みだけ）: `dev/video/<名前>.mp4` を置くと、その作品の ▶ が押せるようになる。名前は `idreal`・`horror`・`osumitsuki`・`ribbond`・`soundmarker`・`friend-a`・`friend-b`。1 本 5〜10 MB くらいの H.264 の mp4 が目安（publish で `video/` も公開用へそろう）
- 作品資料（確認用で、今は IdReal だけ）: `dev/docs/idreal.pdf` を置くと、MORE の横の「作品資料」が押せるようになる（PC は窓の中、スマホは新しいタブで PDF を開く）。publish で `docs/` も公開用へそろう
- ホームのミニゲーム（確認用）の音: `dev/audio/idreal-steps/`（足音）・`dev/audio/idreal-claps/`（手拍子）は、マスごとに Idreal で焼いた響きの mp3（響きだけ、素の音は各フォルダの `dry.mp3` をページが鳴らす）。Unreal と同じ作りで、3 部屋を戸口でつないで焼いてある（戸口のマス・外の口のそばのマスにも音がある）。耳の向き 4 つ（`u` 地図の上・`r` 右・`d` 下・`l` 左）のフォルダに分けてあり、ミニゲームは三角の向きに一番近い物を鳴らす。焼く道具は Idreal の portfolio_bake の bake_footmap2 → encode_footmap（向き 4 つは同じ倍率、響きの量は 11-21 から全部の部屋で −3 dB、壁までの距離の曲線は Unreal の今の値の 2.5 倍。11-21 に 1.5 倍 → 本人「もう少し大げさに」で 2.5 倍、3 倍にしても大きくならない）。`#smap` の `data-sound="synth"` で前の合成の音に戻せる。足音の元の音は本人が渡した素材のコンクリート 9 本（swuing の footstep-concrete.wav https://freesound.org/people/swuing/sounds/38873/ から作られた物、CC BY 3.0）で、`idreal-steps/u/dry0〜8.mp3` が素の音・響きは 0 番で焼いた。CC BY なのでミニゲームの下（枠の外）にクレジットを出している（消さない）。大広間と小部屋の間に扉（扉の方を向いて 3 マス以内の A で開け閉め、閉じると通れない・見通せない）と、小部屋にオルゴール（`dev/audio/musicbox.mp3`、Idreal の portfolio_bake の musicbox_synth.py で作った曲と音、借り物ではない。0.5 秒から 1 周 15.652 秒をループ）。扉越しの聞こえ方（11-24 夜から）: 直接の音は Unreal と同じくゲームの側が決める形をページに写した（扉の角度の音量 DoorVolume・こもり DoorMuffle の曲線、耳→音源の 5 本のレイで隠れている割合でこもり +14 dB・音量 −1 dB、距離の減衰は Wwise の IDR_Distance、こもりの鳴らし方は Wwise の IDR_Eq と同じ 3 帯域＋低域通過）。響きは Idreal で焼いたインパルス応答（`dev/audio/idreal-musicbox/<向き>/c|o<列><行>.mp3`、閉と開、24 kHz）を畳み込み、扉が動く間は自由端と枠の弦で混ぜる。焼く道具は Idreal の portfolio_bake の bake_musicbox（版 26 のエンジン）→ encode_musicbox。閉じた扉の向こうへは響きが抜けない（エンジンの決まり）。音量 MB.vol は仮。最初はスタート画面（SOUND MAP・PRESS A）で、A（キーボードは Z・Space・Enter）を押すまで歩かず鳴らない。見た目は 11-24 から携帯ゲーム機の形で、色はサイトの紙の色と青（案C。本物っぽすぎたので緑の画面・赤紫のボタンなどはやめた。青みの灰色の画面・十字キー・丸いボタン 1 つで手をたたく（走るのはキーボードの X）・スマホの指で地図を触っても歩かない（PC のマウスでなぞるのは残す）・上の切り替えで音の ON/OFF）
- 作品の束（確認用、11-26 から）: 作品の節は 1 画面ぶんで、縦のスクロールはそのまま上下の節へ流れる（前は作品の数だけスクロールを止めて、ホイール 1 目盛りで 1 作品ずつ送っていた）。作品を替えるのは横の操作だけ: 一覧の両わきの ‹ ›・一覧の札・← → キー・スマホの横スワイプ・タッチパッドの横の動き。7 の次は 1、1 の前は 7 にループし、下からのぞくカードもいつも次の作品
- 広い PC の拡大（確認用、11-25 から）: 幅 1600・高さ 860 以上で 1.15 倍、1900・980 以上で 1.25 倍、2300・1200 以上で 1.5 倍に、ページ全体を CSS の `zoom` で拡大する（`:root` の `--z`）。拡大すると vh・vw も一緒に大きくなるので、CSS の vh・vw は全部 `calc(… / var(--z,1))` で割り戻してある。JS で見た目の大きさ（getBoundingClientRect・clientX）から CSS の px を作る所も `--z` で割る（舞台の高さ `--sh`・ミニゲームのつまみ・波形のなぞり）。`zoom` が使えないブラウザは `@supports` で 1 倍のまま
- 外部の読み込みは Google Fonts だけ。どちらも検索に出さない（noindex）
