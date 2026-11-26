/* 選んでいる作品の画像を、ぼかして後ろに出す（<i> を 2 枚重ねて、新しい方を上に入れ替える）
 * 画像が無い作品は、その作品の色のにじみ */
window.ShotBg = function(box){
  var L = box ? [].slice.call(box.querySelectorAll('i')) : [], front = 0, key = null;
  return function(src, color){
    if (L.length < 2) return;
    var k = (src || '') + '|' + (color || '');
    if (k === key) return;
    key = k;
    var n = L[1 - front];
    n.style.backgroundImage = src ? 'url("' + src + '")' : 'radial-gradient(60% 70% at 40% 45%, ' + (color || '#7DB8D1') + ', transparent 75%)';
    n.classList.add('on');
    L[front].classList.remove('on');
    front = 1 - front;
  };
};
