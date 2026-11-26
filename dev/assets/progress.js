/* 上のアドレス欄に、どこまで読んだかを出す（?progress=-----O-----） */
(function(){
  if (!window.history || !history.replaceState) return;
  var N = 40, last = '', at = 0, wait = false;
  function bar(){
    var max = document.documentElement.scrollHeight - window.innerHeight;
    var r = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
    var k = Math.round(r * (N - 1));
    return new Array(k + 1).join('-') + 'O' + new Array(N - k).join('-');
  }
  function write(){
    wait = false; at = Date.now();
    var b = bar();
    if (b === last) return;
    last = b;
    //Safari は書き換えの回数に上限があるので、0.25 秒に 1 回まで
    try{ history.replaceState(history.state, '', location.pathname + '?progress=' + b + location.hash); }catch(e){}
  }
  window.addEventListener('scroll', function(){
    if (wait) return;
    wait = true;
    setTimeout(write, Math.max(0, 250 - (Date.now() - at)));
  }, {passive: true});
  window.addEventListener('load', write);
})();
