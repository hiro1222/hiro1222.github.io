/* 操作の音（サイト全体で 1 つのスイッチ）
 * 既定は OFF。.sfx のボタンで切り替えて、その端末に覚える（作品のページへ移っても同じ）
 * 音は Web Audio でその場で作る（音のファイルは使わない） */
(function(){
  var KEY = 'pf-sfx', on = false, ctx = null, subs = [];
  try{ on = localStorage.getItem(KEY) === '1'; }catch(e){}
  //作品一覧の行ごとに 1 音（A の短調の 5 音音階。上から順になぞるとメロディになる）
  var SCALE = [440, 523.25, 587.33, 659.25, 783.99, 880, 1046.5, 1174.66];
  function ac(){
    if (!ctx){
      var C = window.AudioContext || window.webkitAudioContext;
      if (!C) return null;
      ctx = new C();
    }
    if (ctx.state === 'suspended'){ try{ ctx.resume(); }catch(e){} }
    return ctx;
  }
  //短い音を 1 つ（立ち上がり 5 ms、あとは減っていく）
  function tone(f, at, dur, vol, type){
    var c = ac();
    if (!c || c.state !== 'running') return;
    var o = c.createOscillator(), g = c.createGain(), t = c.currentTime + (at || 0);
    o.type = type || 'triangle';
    o.frequency.value = f;
    g.gain.setValueAtTime(0, t);
    g.gain.linearRampToValueAtTime(vol, t + .005);
    g.gain.exponentialRampToValueAtTime(.0001, t + dur);
    o.connect(g); g.connect(c.destination);
    o.start(t); o.stop(t + dur + .03);
  }
  function paint(){
    document.querySelectorAll('.sfx').forEach(function(b){
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      var l = b.querySelector('.sfx-l');
      if (l) l.textContent = on ? 'SOUND ON' : 'SOUND OFF';
    });
  }
  var api = {
    isOn: function(){ return on; },
    set: function(v){
      on = !!v;
      try{ localStorage.setItem(KEY, on ? '1' : '0'); }catch(e){}
      paint();
      subs.forEach(function(f){ f(on); });
      if (on){ ac(); setTimeout(api.confirm, 30); }
    },
    sub: function(f){ subs.push(f); },
    note: function(i){
      if (!on) return;
      var f = SCALE[((i % SCALE.length) + SCALE.length) % SCALE.length];
      tone(f, 0, .26, .05, 'triangle');
      tone(f * 2, 0, .09, .012, 'sine');
    },
    confirm: function(){ if (!on) return; tone(659.25, 0, .12, .06); tone(880, .07, .22, .06); },
    back: function(){ if (!on) return; tone(880, 0, .1, .05); tone(659.25, .06, .18, .05); },
    tick: function(){ if (!on) return; tone(1975.5, 0, .035, .018, 'square'); },
    //針を落とす音：低い「プツッ」と、盤のまばらな「ジリッ」
    drop: function(){
      if (!on) return;
      var c = ac();
      if (!c || c.state !== 'running') return;
      tone(68, 0, .1, .09, 'sine');
      var sr = c.sampleRate, len = Math.floor(sr * .45), buf = c.createBuffer(1, len, sr), d = buf.getChannelData(0), i, k;
      for (i = 0; i < len; i++){
        k = 1 - i / len;
        d[i] = (Math.random() < .003 ? (Math.random() * 2 - 1) : 0) * Math.pow(k, 1.4) + (Math.random() * 2 - 1) * .012 * k;
      }
      var s = c.createBufferSource(), hp = c.createBiquadFilter(), g = c.createGain();
      s.buffer = buf; hp.type = 'highpass'; hp.frequency.value = 1400; g.gain.value = .4;
      s.connect(hp); hp.connect(g); g.connect(c.destination);
      s.start(c.currentTime + .015);
    }
  };
  window.SFX = api;
  //押したら切り替え（どの .sfx でも同じ）
  document.addEventListener('click', function(e){
    var b = e.target.closest && e.target.closest('.sfx');
    if (b){ e.preventDefault(); api.set(!on); }
  });
  //ON のまま開いた時は、最初に触った時に音の準備（ブラウザは触るまで鳴らさない）
  ['pointerdown', 'keydown'].forEach(function(t){
    window.addEventListener(t, function(){ if (on) ac(); }, {passive: true, capture: true});
  });
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', paint); else paint();
})();
