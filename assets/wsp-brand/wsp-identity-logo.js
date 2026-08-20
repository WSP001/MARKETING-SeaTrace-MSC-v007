(function () {
  const canvases = document.querySelectorAll('[data-wsp-identity-globe]');
  if (!canvases.length) return;

  const reduceMotion = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function setup(canvas) {
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let frame = 0;

    function resize() {
      const rect = canvas.getBoundingClientRect();
      const ratio = Math.min(window.devicePixelRatio || 1, 2);
      canvas.width = Math.max(48, Math.round(rect.width * ratio));
      canvas.height = Math.max(48, Math.round(rect.height * ratio));
      ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
    }

    function draw() {
      const size = canvas.getBoundingClientRect().width;
      const center = size / 2;
      const radius = size * 0.43;
      const rotation = reduceMotion ? 0 : frame * 0.03;

      ctx.clearRect(0, 0, size, size);
      ctx.fillStyle = '#063d4d';
      ctx.beginPath();
      ctx.arc(center, center, radius, 0, Math.PI * 2);
      ctx.fill();

      ctx.strokeStyle = 'rgba(245, 251, 255, 0.24)';
      ctx.lineWidth = 0.8;
      for (let i = -2; i <= 2; i += 1) {
        ctx.beginPath();
        ctx.ellipse(center, center, radius * (0.25 + Math.abs(i) * 0.16), radius, rotation + i * 0.32, 0, Math.PI * 2);
        ctx.stroke();
      }

      ctx.strokeStyle = 'rgba(0, 229, 255, 0.38)';
      for (let y = -0.5; y <= 0.5; y += 0.25) {
        ctx.beginPath();
        ctx.ellipse(center, center + y * radius, radius * Math.cos(y), radius * 0.18, 0, 0, Math.PI * 2);
        ctx.stroke();
      }

      ctx.fillStyle = '#d4af37';
      ctx.beginPath();
      ctx.arc(center + Math.sin(rotation * 6) * radius * 0.55, center - radius * 0.2, 2, 0, Math.PI * 2);
      ctx.fill();

      frame += 1;
      if (!reduceMotion) requestAnimationFrame(draw);
    }

    resize();
    draw();
    window.addEventListener('resize', () => { resize(); draw(); }, { passive: true });
  }

  canvases.forEach(setup);
})();
