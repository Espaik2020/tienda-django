// ===== Cards Tilt / Shine =====
(function(){
  const cards = document.querySelectorAll('.tilt');
  if(!cards.length) return;

  const bounds = el => el.getBoundingClientRect();
  cards.forEach(card => {
    const shine = card.querySelector('.shine');
    card.addEventListener('pointermove', (e) => {
      const b = bounds(card);
      const px = (e.clientX - b.left) / b.width;
      const py = (e.clientY - b.top) / b.height;
      const rx = (py - 0.5) * -10; // inclinación X
      const ry = (px - 0.5) * 10;  // inclinación Y
      card.style.setProperty('--rx', rx + 'deg');
      card.style.setProperty('--ry', ry + 'deg');
      card.style.setProperty('--mx', (px * 100) + '%');
      card.style.setProperty('--my', (py * 100) + '%');
    });
    card.addEventListener('pointerleave', () => {
      card.style.setProperty('--rx', '0deg');
      card.style.setProperty('--ry', '0deg');
      card.style.setProperty('--mx', '50%');
      card.style.setProperty('--my', '50%');
    });
  });
})();

// ===== Showcase: pausa auto-scroll si el usuario hace scroll horizontal (mobile) =====
(function(){
  const track = document.querySelector('.showcase-track');
  if(!track) return;

  let touching = false, startX = 0, scrollX = 0;

  const stopAnim = () => track.style.animationPlayState = 'paused';
  const resumeAnim = () => track.style.animationPlayState = '';

  track.addEventListener('pointerdown', (e) => {
    touching = true;
    startX = e.clientX;
    stopAnim();
  });
  window.addEventListener('pointermove', (e) => {
    if(!touching) return;
    const dx = e.clientX - startX;
    startX = e.clientX;
    scrollX += dx;
    track.style.transform = `translateX(${scrollX}px)`;
  });
  window.addEventListener('pointerup', () => {
    touching = false;
    // Suaviza regreso al ciclo automático
    track.style.transform = '';
    scrollX = 0;
    resumeAnim();
  });
})();

// ===== Galería: detalle de producto (imagen grande + miniaturas + zoom) =====
document.addEventListener('DOMContentLoaded', () => {
  const main = document.querySelector('#mainImg');          // img grande (detalle)
  const zoomImg = document.querySelector('#zoomImg');       // img dentro del modal
  const zoomModalEl = document.getElementById('zoomModal'); // modal Bootstrap
  const zoomModal = zoomModalEl ? new bootstrap.Modal(zoomModalEl) : null;

  if (main) {
    const thumbs = Array.from(document.querySelectorAll('.product-gallery-thumbs .thumb'));

    const setMain = (src, alt, activeEl) => {
      if (!src) return;
      main.src = src;
      if (alt) main.alt = alt;
      if (zoomImg) { zoomImg.src = src; zoomImg.alt = main.alt || alt || ''; }
      thumbs.forEach(t => t.classList.remove('active'));
      if (activeEl) activeEl.classList.add('active');
    };

    // Preload para que no “parpadeen”
    thumbs.forEach(t => { const img = new Image(); img.src = t.dataset.src || t.src; });

    // Eventos de miniaturas
    thumbs.forEach(t => {
      const src = t.dataset.src || t.src;
      const alt = t.dataset.alt || t.alt;
      t.addEventListener('click', () => setMain(src, alt, t));
      t.addEventListener('mouseenter', () => setMain(src, alt, t));
    });

    // Estado inicial
    if (thumbs.length) {
      const first = thumbs[0];
      setMain(first.dataset.src || first.src, first.dataset.alt || first.alt, first);
    }

    // Click en imagen principal = abrir zoom
    main.addEventListener('click', () => { if (zoomModal) zoomModal.show(); });

    // Navegación con flechas en el modal (← →)
    document.addEventListener('keydown', (e) => {
      if (!zoomModalEl || !zoomModalEl.classList.contains('show') || thumbs.length < 2) return;
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      const idx = thumbs.findIndex(t => t.classList.contains('active'));
      if (idx < 0) return;
      const nextIdx = e.key === 'ArrowRight' ? (idx + 1) % thumbs.length : (idx - 1 + thumbs.length) % thumbs.length;
      const next = thumbs[nextIdx];
      setMain(next.dataset.src || next.src, next.dataset.alt || next.alt, next);
    });
  }

  // ===== Lista de productos: miniaturas bajo cada card (cambian la imagen principal de la card) =====
  document.querySelectorAll('[data-main-target]').forEach(thumb => {
    const targetSel = thumb.getAttribute('data-main-target'); // ej. "#main-5"
    const targetImg = document.querySelector(targetSel);
    if (!targetImg) return;

    const swap = () => {
      const src = thumb.dataset.src || thumb.src;
      const alt = thumb.dataset.alt || targetImg.alt;
      if (src) { targetImg.src = src; targetImg.alt = alt; }
    };

    // Preload
    const preload = new Image();
    preload.src = thumb.dataset.src || thumb.src;

    // Interacciones
    thumb.addEventListener('mouseenter', swap);
    thumb.addEventListener('focus', swap);
    thumb.addEventListener('click', (e) => { e.preventDefault(); swap(); });
  });
});
