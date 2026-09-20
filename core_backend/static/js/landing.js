/* ── Hamburger ── */
  const ham = document.getElementById('hamburger');
  const mob = document.getElementById('mobile-menu');
  ham.addEventListener('click', () => {
    const open = mob.classList.toggle('open');
    ham.classList.toggle('open', open);
    ham.setAttribute('aria-expanded', String(open));
  });
  mob.querySelectorAll('[data-close]').forEach(el => {
    el.addEventListener('click', () => {
      mob.classList.remove('open');
      ham.classList.remove('open');
      ham.setAttribute('aria-expanded', 'false');
    });
  });

  /* ── Counter animation ── */
  function animateCounter(el) {
    const target = +el.dataset.target;
    const isPercent = target <= 100 && !!el.closest('.stat-cell');
    const dur = 1800, t0 = performance.now();
    const tick = now => {
      const p = Math.min((now - t0) / dur, 1);
      const e = 1 - Math.pow(1 - p, 3);
      const v = Math.floor(e * target);
      el.textContent = v.toLocaleString('en-IN') + (p >= 1 ? (target > 100 ? '+' : isPercent ? '%' : '') : '');
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }
  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting && !e.target.dataset.animated) {
        e.target.dataset.animated = '1';
        animateCounter(e.target);
      }
    });
  }, { threshold: 0.3 });
  document.querySelectorAll('[data-target]').forEach(el => obs.observe(el));

  /* ── FAQ Accordion ── */
  document.querySelectorAll('.faq-item').forEach(item => {
    item.querySelector('.faq-q').addEventListener('click', () => {
      const wasOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(o => {
        o.classList.remove('open');
        o.querySelector('.faq-q').setAttribute('aria-expanded', 'false');
      });
      if (!wasOpen) {
        item.classList.add('open');
        item.querySelector('.faq-q').setAttribute('aria-expanded', 'true');
      }
    });
  });

  /* ── Smooth scroll ── */
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const t = document.querySelector(a.getAttribute('href'));
      if (t) { e.preventDefault(); t.scrollIntoView({ behavior:'smooth', block:'start' }); }
    });
  });