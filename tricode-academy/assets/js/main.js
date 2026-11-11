(function () {
  'use strict';
  var header = document.getElementById('site-header');
  var btn = document.getElementById('menu-btn');
  var menu = document.getElementById('mobile-menu');

  function onScroll() { if (header) header.classList.toggle('scrolled', window.scrollY > 8); }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  function setMenu(open) {
    menu.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', open);
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  if (btn && menu) {
    btn.addEventListener('click', function () { setMenu(btn.getAttribute('aria-expanded') !== 'true'); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('click', function (e) { if (!e.target.closest('.nav-shell')) setMenu(false); });
    window.matchMedia('(min-width:1080px)').addEventListener('change', function () { setMenu(false); });
  }

  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else { items.forEach(function (el) { el.classList.add('in'); }); }

  // Gallery lightbox (opens only for tiles that have a real photo)
  var lb = document.getElementById('lightbox');
  if (lb) {
    var lbImg = document.getElementById('lightbox-img');
    var lastFocus = null;
    var close = function () { lb.hidden = true; document.body.style.overflow = ''; if (lastFocus) lastFocus.focus(); };
    document.querySelectorAll('.gallery-btn').forEach(function (b) {
      b.addEventListener('click', function () {
        var img = b.querySelector('img');
        if (!img || !img.naturalWidth) return;
        lastFocus = b; lbImg.src = img.currentSrc || img.src; lbImg.alt = img.alt;
        lb.hidden = false; document.body.style.overflow = 'hidden';
        lb.querySelector('.lightbox-close').focus();
      });
    });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target.closest('.lightbox-close')) close(); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !lb.hidden) close(); });
  }

  // Apply form
  var form = document.getElementById('apply-form');
  if (form) {
    var status = document.getElementById('form-status');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (form.website && form.website.value) return; // honeypot
      var bad = null;
      form.querySelectorAll('[required]').forEach(function (f) {
        var ok = f.value.trim() !== '';
        f.setAttribute('aria-invalid', ok ? 'false' : 'true');
        if (!ok && !bad) bad = f;
      });
      if (bad) { status.textContent = 'Please complete the highlighted fields.'; status.className = 'text-sm font-semibold text-red-600'; bad.focus(); return; }
      var endpoint = form.getAttribute('data-endpoint');
      if (!endpoint) {
        status.textContent = 'Thank you! Online submission is being connected. Please contact the academy to confirm your application.';
        status.className = 'text-sm font-semibold text-brand-mid';
        return;
      }
      status.textContent = 'Sending...'; status.className = 'text-sm font-semibold text-slate-600';
      fetch(endpoint, { method: 'POST', body: new FormData(form), mode: 'no-cors' })
        .then(function () { form.reset(); status.textContent = 'Application sent. We will contact you soon.'; status.className = 'text-sm font-semibold text-green-700'; })
        .catch(function () { status.textContent = 'Could not send. Please try again or contact us.'; status.className = 'text-sm font-semibold text-red-600'; });
    });
  }
})();
