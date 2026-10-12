(() => {
  'use strict';
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const canvas = document.createElement('canvas');
  canvas.id = 'zenith-binary-rain';
  Object.assign(canvas.style, {
    position: 'fixed', inset: '0', width: '100%', height: '100%',
    pointerEvents: 'none', zIndex: '1', opacity: '0.42',
    mixBlendMode: 'screen'
  });
  canvas.setAttribute('aria-hidden', 'true');
  document.addEventListener('DOMContentLoaded', () => {
    if (!document.body) return;
    document.body.appendChild(canvas);
    const ctx = canvas.getContext('2d', { alpha: true });
    if (!ctx) return;

    const colors = ['#00f5ff', '#a855f7', '#39ff88', '#ff4fa3', '#4287ff', '#ffd166'];
    const words = ['ZENITH', 'ZENITH', 'ZENITH'];
    let w = 0, h = 0, streams = [], raf = 0, last = 0;
    const rand = (a, b) => Math.random() * (b - a) + a;

    function resize() {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = window.innerWidth; h = window.innerHeight;
      canvas.width = Math.floor(w * dpr);
      canvas.height = Math.floor(h * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const count = Math.max(24, Math.min(100, Math.floor(w / 15)));
      streams = Array.from({ length: count }, () => makeStream(true));
    }
    function makeStream(initial = false) {
      const angle = rand(-Math.PI * 0.82, Math.PI * 0.82);
      const speed = rand(35, 190);
      const length = Math.floor(rand(7, 27));
      return {
        x: rand(0, w), y: initial ? rand(-h, h) : rand(-h * .25, -20),
        angle, speed, length, size: rand(10, 19),
        color: colors[Math.floor(rand(0, colors.length))],
        alpha: rand(.35, .95), word: Math.random() < .12 ? words[0] : '',
        drift: rand(-13, 13), phase: rand(0, 10), fast: speed > 125
      };
    }
    function draw(now) {
      if (now - last < 28) { raf = requestAnimationFrame(draw); return; }
      const dt = Math.min((now - (last || now)) / 1000, .05);
      last = now;
      ctx.clearRect(0, 0, w, h);
      ctx.textBaseline = 'top';
      for (let i = 0; i < streams.length; i++) {
        const s = streams[i];
        const dx = Math.cos(s.angle), dy = Math.sin(s.angle);
        const step = s.size * .92;
        ctx.font = '700 ' + s.size + 'px ui-monospace, SFMono-Regular, Menlo, monospace';
        for (let j = 0; j < s.length; j++) {
          const x = s.x - dx * j * step;
          const y = s.y - dy * j * step;
          if (x < -30 || x > w + 30 || y < -30 || y > h + 30) continue;
          ctx.globalAlpha = s.alpha * (1 - j / s.length) * (j === 0 ? 1 : .82);
          ctx.fillStyle = j === 0 ? '#ffffff' : s.color;
          const glyph = Math.random() < .5 ? '0' : '1';
          ctx.fillText(glyph, x, y);
        }
        if (s.word) {
          ctx.globalAlpha = Math.min(.95, s.alpha + .15);
          ctx.fillStyle = s.color;
          ctx.font = '900 ' + Math.max(11, s.size) + 'px ui-monospace, monospace';
          ctx.fillText('ZENITH', s.x, s.y);
        }
        s.x += (dx * s.speed + s.drift) * dt;
        s.y += dy * s.speed * dt;
        s.phase += dt;
        if (s.x < -w * .25 || s.x > w * 1.25 || s.y < -h * .3 || s.y > h * 1.3) {
          streams[i] = makeStream(false);
        }
      }
      ctx.globalAlpha = 1;
      raf = requestAnimationFrame(draw);
    }
    resize();
    window.addEventListener('resize', resize, { passive: true });
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) cancelAnimationFrame(raf);
      else { last = 0; raf = requestAnimationFrame(draw); }
    });
    raf = requestAnimationFrame(draw);
  });
})();
