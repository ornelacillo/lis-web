/**
 * LIS. Creative Studio — Shared Navigation
 * Injects a unified pill nav into every page.
 *
 * Usage: add <script src="/nav.js"></script> inside <head> or before </body>
 *
 * Per-page config via data attributes on the <body>:
 *   data-nav-page="home|branding|web|identidad|curaduria|asesoria|shop|freebies|masterclass"
 *   data-nav-lang="es|en"  (default: es)
 *
 * Automatic theme switching:
 *   The nav pill switches between "light" (white text on dark) and "dark"
 *   (dark text on light) based on what section is currently visible.
 *   Mark dark-background sections with  data-nav-theme="light"
 *   Mark light-background sections with data-nav-theme="dark"
 *   If none observed → defaults to "light" (pill on dark bg).
 */

(function () {
  'use strict';

  /* ─── CSS ─────────────────────────────────────────────────── */
  const CSS = `
    #lis-nav {
      position: fixed; top: 0; left: 0; right: 0; z-index: 900;
      display: flex; align-items: center; justify-content: center;
      padding: 14px 24px;
      pointer-events: none;
      gap: 0;
    }

    /* ── pill ── */
    #lis-nav-pill {
      display: flex; align-items: center; gap: 2px;
      padding: 4px 6px;
      border-radius: 12px;
      pointer-events: all;
      transition:
        background 0.35s ease,
        border-color 0.35s ease,
        box-shadow 0.35s ease;
      backdrop-filter: blur(18px);
      -webkit-backdrop-filter: blur(18px);
    }

    /* LIGHT mode: white text, semi-transparent dark pill */
    #lis-nav.nav-light #lis-nav-pill {
      background: rgba(15, 15, 15, 0.55);
      border: 0.5px solid rgba(255, 255, 255, 0.12);
      box-shadow: 0 2px 20px rgba(0,0,0,0.35);
    }

    /* DARK mode: dark text, semi-transparent white pill */
    #lis-nav.nav-dark #lis-nav-pill {
      background: rgba(255, 255, 255, 0.72);
      border: 0.5px solid rgba(0, 0, 0, 0.08);
      box-shadow: 0 2px 20px rgba(0,0,0,0.10);
    }

    /* ── nav links ── */
    #lis-nav-pill a,
    #lis-nav-pill button.nav-link-btn {
      text-decoration: none;
      font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
      font-size: 13px;
      letter-spacing: 0.04em;
      padding: 6px 12px;
      border-radius: 8px;
      white-space: nowrap;
      border: none; background: none; cursor: pointer;
      transition: background 0.15s, opacity 0.15s, color 0.35s;
      display: inline-flex; align-items: center; gap: 4px;
    }

    #lis-nav.nav-light #lis-nav-pill a,
    #lis-nav.nav-light #lis-nav-pill button.nav-link-btn {
      color: rgba(255, 255, 255, 0.90);
    }
    #lis-nav.nav-dark #lis-nav-pill a,
    #lis-nav.nav-dark #lis-nav-pill button.nav-link-btn {
      color: rgba(17, 17, 17, 0.88);
    }

    #lis-nav.nav-light #lis-nav-pill a:hover,
    #lis-nav.nav-light #lis-nav-pill button.nav-link-btn:hover {
      background: rgba(255, 255, 255, 0.12);
      opacity: 1;
    }
    #lis-nav.nav-dark #lis-nav-pill a:hover,
    #lis-nav.nav-dark #lis-nav-pill button.nav-link-btn:hover {
      background: rgba(0, 0, 0, 0.07);
    }

    /* active page highlight */
    #lis-nav.nav-light #lis-nav-pill a.nav-active {
      background: rgba(255,255,255,0.15);
    }
    #lis-nav.nav-dark #lis-nav-pill a.nav-active {
      background: rgba(0,0,0,0.09);
    }

    /* ── separator ── */
    .nav-sep {
      width: 1px; height: 14px; flex-shrink: 0; margin: 0 2px;
      transition: background 0.35s;
    }
    #lis-nav.nav-light .nav-sep { background: rgba(255,255,255,0.18); }
    #lis-nav.nav-dark  .nav-sep { background: rgba(0,0,0,0.12); }

    /* ── lang switcher ── */
    .nav-lang {
      display: flex; align-items: center; gap: 2px;
      margin-left: 4px;
    }
    .nav-lang a {
      font-size: 11px !important;
      letter-spacing: 0.08em !important;
      padding: 4px 7px !important;
      opacity: 0.5;
    }
    .nav-lang a.lang-active { opacity: 1 !important; font-weight: 500; }
    .nav-lang-sep {
      font-size: 10px; opacity: 0.3;
      transition: color 0.35s;
    }
    #lis-nav.nav-light .nav-lang-sep { color: #fff; }
    #lis-nav.nav-dark  .nav-lang-sep { color: #111; }

    /* ── dropdown ── */
    .nav-dropdown { position: relative; }
    .nav-dropdown-menu {
      display: none;
      position: absolute; top: 100%;
      padding-top: 10px; left: 50%;
      transform: translateX(-50%);
      z-index: 1000;
      min-width: 210px;
    }
    .nav-dropdown-inner {
      background: #111;
      border: 0.5px solid rgba(255,255,255,0.08);
      border-radius: 10px;
      padding: 6px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }
    .nav-dropdown-menu a {
      display: flex !important;
      padding: 9px 14px !important;
      color: rgba(255,255,255,0.80) !important;
      font-size: 13px !important;
      border-radius: 6px !important;
      border-bottom: none !important;
      transition: background 0.15s !important;
    }
    .nav-dropdown-menu a:hover {
      background: rgba(255,255,255,0.08) !important;
      opacity: 1 !important;
    }
    .nav-dropdown-menu.dd-open { display: block; }
    .nav-dropdown:focus-within .nav-dropdown-menu { display: block; }

    /* chevron */
    .nav-chevron {
      width: 10px; height: 10px; flex-shrink: 0;
      transition: transform 0.2s, opacity 0.35s;
      opacity: 0.5;
    }
    #lis-nav.nav-light .nav-chevron { stroke: #fff; }
    #lis-nav.nav-dark  .nav-chevron { stroke: #111; }
    .nav-dropdown:hover .nav-chevron { transform: rotate(180deg); opacity: 1; }

    /* ── hamburger button (mobile) ── */
    #lis-nav-hamburger {
      display: none;
      background: none; border: none;
      cursor: pointer; padding: 6px;
      width: 40px; height: 40px;
      align-items: center; justify-content: center;
      pointer-events: all;
      border-radius: 8px;
      transition: background 0.15s;
      position: fixed; top: 14px; right: 20px; z-index: 910;
    }
    #lis-nav-hamburger:hover { background: rgba(128,128,128,0.12); }
    #lis-nav-hamburger svg {
      width: 22px; height: 22px;
      transition: stroke 0.35s;
    }
    .hamburger-light svg { stroke: rgba(255,255,255,0.9); }
    .hamburger-dark  svg { stroke: rgba(17,17,17,0.88); }

    /* ── mobile logo (left side) ── */
    #lis-nav-mobile-logo {
      display: none;
      position: fixed; top: 0; left: 0; right: 0; z-index: 905;
      padding: 18px 24px;
      pointer-events: none;
    }
    #lis-nav-mobile-logo a {
      pointer-events: all;
      text-decoration: none;
      font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
      font-size: 15px; font-weight: 600; letter-spacing: 0.02em;
      transition: color 0.35s;
    }
    .mobile-logo-light a { color: rgba(255,255,255,0.9); }
    .mobile-logo-dark  a { color: rgba(17,17,17,0.9); }

    /* ── mobile overlay ── */
    #lis-nav-overlay {
      display: none;
      position: fixed; inset: 0; z-index: 950;
      background: #09090b;
      flex-direction: column;
      align-items: center; justify-content: center;
      gap: 8px;
    }
    #lis-nav-overlay.open { display: flex; }

    #lis-nav-overlay-close {
      position: absolute; top: 20px; right: 20px;
      background: none; border: none; cursor: pointer;
      width: 44px; height: 44px;
      display: flex; align-items: center; justify-content: center;
    }
    #lis-nav-overlay-close svg {
      width: 22px; height: 22px;
      stroke: rgba(255,255,255,0.6); stroke-width: 2; stroke-linecap: round;
    }

    #lis-nav-overlay a {
      text-decoration: none;
      color: rgba(255,255,255,0.88);
      font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
      font-size: 24px; font-weight: 400; letter-spacing: -0.01em;
      padding: 10px 0;
      transition: opacity 0.2s;
    }
    #lis-nav-overlay a:hover { opacity: 0.55; }

    /* services sub-group in overlay */
    #lis-nav-overlay .overlay-services-toggle {
      background: none; border: none; cursor: pointer;
      color: rgba(255,255,255,0.88);
      font-family: 'Inter', 'Helvetica Neue', Helvetica, Arial, sans-serif;
      font-size: 24px; font-weight: 400; letter-spacing: -0.01em;
      padding: 10px 0;
      display: flex; align-items: center; gap: 8px;
    }
    #lis-nav-overlay .overlay-services-toggle svg {
      width: 16px; height: 16px; stroke: rgba(255,255,255,0.5);
      transition: transform 0.3s;
    }
    #lis-nav-overlay .overlay-services-toggle.open svg {
      transform: rotate(180deg);
    }
    #lis-nav-overlay .overlay-sub {
      display: none;
      flex-direction: column; align-items: center;
      gap: 0; padding: 4px 0 8px;
      border-top: 1px solid rgba(255,255,255,0.07);
      width: 240px;
    }
    #lis-nav-overlay .overlay-sub.open { display: flex; }
    #lis-nav-overlay .overlay-sub a {
      font-size: 15px !important;
      color: rgba(255,255,255,0.45) !important;
      padding: 7px 0 !important;
    }
    #lis-nav-overlay .overlay-sub a:hover {
      color: rgba(255,255,255,0.80) !important;
    }

    /* lang in overlay */
    #lis-nav-overlay .overlay-lang {
      display: flex; gap: 16px; margin-top: 16px;
      border-top: 1px solid rgba(255,255,255,0.07);
      padding-top: 20px; width: 240px; justify-content: center;
    }
    #lis-nav-overlay .overlay-lang a {
      font-size: 13px !important; letter-spacing: 0.08em !important;
      color: rgba(255,255,255,0.35) !important;
      padding: 4px 8px !important;
    }
    #lis-nav-overlay .overlay-lang a.lang-active {
      color: rgba(255,255,255,0.88) !important;
      font-weight: 500;
    }

    /* ── Responsive breakpoints ── */
    @media (max-width: 768px) {
      #lis-nav { display: none; }
      #lis-nav-hamburger { display: flex; }
      #lis-nav-mobile-logo { display: block; }
    }
    @media (min-width: 769px) {
      #lis-nav-hamburger { display: none; }
      #lis-nav-mobile-logo { display: none; }
    }
  `;

  /* ─── Helpers ─────────────────────────────────────────────── */
  function injectStyles() {
    const style = document.createElement('style');
    style.id = 'lis-nav-styles';
    style.textContent = CSS;
    document.head.appendChild(style);
  }

  function svgChevron() {
    return `<svg class="nav-chevron" viewBox="0 0 10 10" fill="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3.5l3 3 3-3"/></svg>`;
  }

  /* Determine base path prefix depending on current location */
  function getBase() {
    const path = window.location.pathname;
    // If inside /en/ subfolder
    if(path==='/en'||path.startsWith('/en/')) return '/en/';
    return '/';
  }

  function isEn() {
    var _p2=window.location.pathname; return _p2==='/en'||_p2.startsWith('/en/');
  }

  /* Mark active link */
  function markActive(pill) {
    const path = window.location.pathname.replace(/\/$/, '') || '/';
    pill.querySelectorAll('a').forEach(a => {
      const href = a.getAttribute('href') || '';
      // exact match or hash-less match
      const aPath = href.split('#')[0].replace(/\/$/, '') || '/';
      if (aPath && aPath !== '/' && path.endsWith(aPath)) {
        a.classList.add('nav-active');
      } else if ((aPath === '/' || aPath === '/en/') && (path === '/' || path === '/en/')) {
        a.classList.add('nav-active');
      }
    });
  }

  /* ─── Build pill HTML ─────────────────────────────────────── */
  function buildPill() {
    const base = getBase();
    const en = isEn();

    const links = en ? [
      { label: 'home',      href: '/en' },
      { label: 'about',     href: '/en/#about' },
      { label: 'services',  href: '/en/#services', dropdown: true },
      { label: 'portfolio', href: '/en/#portfolio' },
      { label: 'shop',      href: '/en/shop' },
      { label: 'freebies',  href: '/en/freebies' },
      { label: 'contact',   href: '/en/#contact', cta: true },
    ] : [
      { label: 'home',      href: '/' },
      { label: 'about',     href: '/#about' },
      { label: 'services',  href: '/#services', dropdown: true },
      { label: 'portfolio', href: '/#portfolio' },
      { label: 'shop',      href: '/shop' },
      { label: 'freebies',  href: '/freebies' },
      { label: 'contact',   href: '/#contact', cta: true },
    ];

    const serviceLinks = en ? [
      { label: 'Complete Branding', href: '/en/branding' },
      { label: 'Visual Identity',   href: '/en/identity' },
      { label: 'Web Design',        href: '/en/web' },
      { label: 'Visual Curation',   href: '/en/curation' },
      { label: 'Advisory 1:1',      href: '/en/advisory' },
    ] : [
      { label: 'Branding Completo',  href: '/branding' },
      { label: 'Identidad Visual',   href: '/identidad-visual' },
      { label: 'Diseño Web',         href: '/web' },
      { label: 'Curaduría Visual',   href: '/curaduria' },
      { label: 'Asesoría 1:1',       href: '/asesoria' },
    ];

    let html = '';

    links.forEach((link, i) => {
      // Add sep before shop
      if (link.label === 'shop') {
        html += `<span class="nav-sep"></span>`;
      }
      // Add sep before contact
      if (link.label === 'contact') {
        html += `<span class="nav-sep"></span>`;
      }

      if (link.dropdown) {
        // Services dropdown
        const ddItems = serviceLinks.map(s =>
          `<a href="${s.href}">${s.label}</a>`
        ).join('');

        html += `
          <div class="nav-dropdown">
            <a href="${link.href}" style="display:inline-flex;align-items:center;gap:4px;">
              ${link.label}
              ${svgChevron()}
            </a>
            <div class="nav-dropdown-menu">
              <div class="nav-dropdown-inner">
                ${ddItems}
              </div>
            </div>
          </div>`;
      } else {
        const ctaStyle = link.cta ? ' style="background:rgba(255,255,255,0.12);"' : '';
        html += `<a href="${link.href}"${ctaStyle}>${link.label}</a>`;
      }
    });

    // Lang switcher
    const esPath = window.location.pathname.replace(/^\/en\//, '/');
    const enPath = '/en' + (window.location.pathname === '/' ? '/index.html' : window.location.pathname);
    html += `
      <span class="nav-sep"></span>
      <div class="nav-lang">
        <a href="${esPath}" class="lang-btn${!en ? ' lang-active' : ''}">ES</a>
        <span class="nav-lang-sep">·</span>
        <a href="${enPath}" class="lang-btn${en ? ' lang-active' : ''}">EN</a>
      </div>`;

    return html;
  }

  /* ─── Build mobile overlay ────────────────────────────────── */
  function buildOverlay() {
    const base = getBase();
    const en = isEn();
    const esPath = window.location.pathname.replace(/^\/en\//, '/');
    const enPath = '/en' + (window.location.pathname === '/' ? '/index.html' : window.location.pathname);

    const serviceLinks = en ? [
      { label: 'Complete Branding', href: '/en/branding' },
      { label: 'Visual Identity',   href: '/en/identity' },
      { label: 'Web Design',        href: '/en/web' },
      { label: 'Visual Curation',   href: '/en/curation' },
      { label: 'Advisory 1:1',      href: '/en/advisory' },
    ] : [
      { label: 'Branding Completo',  href: '/branding' },
      { label: 'Identidad Visual',   href: '/identidad-visual' },
      { label: 'Diseño Web',         href: '/web' },
      { label: 'Curaduría Visual',   href: '/curaduria' },
      { label: 'Asesoría 1:1',       href: '/asesoria' },
    ];

    const subItems = serviceLinks.map(s => `<a href="${s.href}">${s.label}</a>`).join('');

    return `
      <button id="lis-nav-overlay-close" aria-label="Cerrar menú">
        <svg viewBox="0 0 24 24" fill="none">
          <path d="M18 6L6 18M6 6l12 12"/>
        </svg>
      </button>
      <a href="${en ? base + 'index.html' : '/'}">home</a>
      <a href="${en ? base + 'index.html#about' : '/#about'}">about</a>
      <button class="overlay-services-toggle" id="overlay-services-btn">
        services
        <svg viewBox="0 0 16 16" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
          <path d="M4 6l4 4 4-4"/>
        </svg>
      </button>
      <div class="overlay-sub" id="overlay-sub">
        ${subItems}
      </div>
      <a href="${en ? base + 'index.html#portfolio' : '/#portfolio'}">portfolio</a>
      <a href="${en ? base + 'shop.html' : '/shop'}">shop</a>
      <a href="${en ? base + 'freebies.html' : '/freebies'}">freebies</a>
      <a href="${en ? base + 'index.html#contact' : '/#contact'}">contact</a>
      <div class="overlay-lang">
        <a href="${esPath}" class="lang-btn${!en ? ' lang-active' : ''}">ES</a>
        <a href="${enPath}" class="lang-btn${en ? ' lang-active' : ''}">EN</a>
      </div>
    `;
  }

  /* ─── Theme switching logic ───────────────────────────────── */
  function setupThemeObserver(navEl, hamburgerEl, mobileLogoEl) {
    // Default theme: light (white text on dark bg)
    // This is set on page load and refined by observers

    // Check body data attribute for forced override
    const bodyTheme = document.body.getAttribute('data-nav-theme');

    // Find all elements with data-nav-theme
    const themedSections = document.querySelectorAll('[data-nav-theme]');

    if (themedSections.length === 0 && !bodyTheme) {
      // No sections defined — use body attribute or default light
      setTheme(navEl, hamburgerEl, mobileLogoEl, bodyTheme || 'light');
      return;
    }

    if (bodyTheme) {
      setTheme(navEl, hamburgerEl, mobileLogoEl, bodyTheme);
    }

    // Map to track which sections are intersecting
    const intersecting = new Map();

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const theme = entry.target.getAttribute('data-nav-theme');
        intersecting.set(entry.target, entry.isIntersecting ? theme : null);
      });

      // Find topmost visible themed section
      // Sort by their position on page (top to bottom)
      let activeTheme = bodyTheme || 'light';

      // Get all sections sorted by how close their top is to viewport top
      const visible = [];
      intersecting.forEach((theme, el) => {
        if (theme) {
          const rect = el.getBoundingClientRect();
          visible.push({ theme, top: rect.top });
        }
      });

      if (visible.length > 0) {
        // Use the section whose top is closest to (or just above) the top of viewport
        visible.sort((a, b) => a.top - b.top);
        // Find the last section that started above mid-screen
        const midScreen = window.innerHeight * 0.3;
        const above = visible.filter(v => v.top <= midScreen);
        if (above.length > 0) {
          activeTheme = above[above.length - 1].theme;
        } else {
          activeTheme = visible[0].theme;
        }
      }

      setTheme(navEl, hamburgerEl, mobileLogoEl, activeTheme);
    }, {
      threshold: [0, 0.1, 0.3, 0.5],
      rootMargin: '0px 0px -40% 0px'
    });

    themedSections.forEach(el => {
      intersecting.set(el, null);
      observer.observe(el);
    });
  }

  function setTheme(navEl, hamburgerEl, mobileLogoEl, theme) {
    if (!navEl || !hamburgerEl || !mobileLogoEl) return;
    navEl.classList.toggle('nav-light', theme === 'light');
    navEl.classList.toggle('nav-dark',  theme === 'dark');
    hamburgerEl.classList.toggle('hamburger-light', theme === 'light');
    hamburgerEl.classList.toggle('hamburger-dark',  theme === 'dark');
    mobileLogoEl.classList.toggle('mobile-logo-light', theme === 'light');
    mobileLogoEl.classList.toggle('mobile-logo-dark',  theme === 'dark');
  }


  function setupDropdowns() {
    document.querySelectorAll('.nav-dropdown').forEach(function(dd) {
      var menu = dd.querySelector('.nav-dropdown-menu');
      if (!menu) return;
      var timer;
      function openMenu() { clearTimeout(timer); menu.classList.add('dd-open'); }
      function closeMenu() { timer = setTimeout(function() { if(menu) menu.classList.remove('dd-open'); }, 120); }
      dd.addEventListener('mouseenter', openMenu);
      dd.addEventListener('mouseleave', closeMenu);
      menu.addEventListener('mouseenter', function() { clearTimeout(timer); });
      menu.addEventListener('mouseleave', closeMenu);
    });
  }

  /* ─── Init ────────────────────────────────────────────────── */
  function init() {
    injectStyles();

    // ── Nav pill wrapper ──
    const nav = document.createElement('nav');
    nav.id = 'lis-nav';
    nav.setAttribute('role', 'navigation');
    nav.setAttribute('aria-label', 'Menú principal');

    const pill = document.createElement('div');
    pill.id = 'lis-nav-pill';
    pill.innerHTML = buildPill();
    nav.appendChild(pill);
    document.body.insertBefore(nav, document.body.firstChild);

    markActive(pill);
    setupDropdowns();

    // ── Mobile logo ──
    const mobileLogo = document.createElement('div');
    mobileLogo.id = 'lis-nav-mobile-logo';
    var _mhref = (window.location.pathname==='/en'||window.location.pathname.startsWith('/en/')) ? '/en' : '/';
    mobileLogo.innerHTML = '<a href="'+_mhref+'"><img src="/Branding_2026_logo_blanco_sin_fondo.png" alt="LIS." style="height:26px;width:auto;display:block;filter:brightness(0) invert(1);opacity:0.9;"></a>';
    document.body.insertBefore(mobileLogo, document.body.firstChild);

    // ── Hamburger button ──
    const hamburger = document.createElement('button');
    hamburger.id = 'lis-nav-hamburger';
    hamburger.setAttribute('aria-label', 'Abrir menú');
    hamburger.innerHTML = `
      <svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round">
        <path d="M4 6h16M4 12h16M4 18h16"/>
      </svg>`;
    document.body.insertBefore(hamburger, document.body.firstChild);

    // ── Mobile overlay ──
    const overlay = document.createElement('div');
    overlay.id = 'lis-nav-overlay';
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('role', 'dialog');
    overlay.innerHTML = buildOverlay();
    document.body.appendChild(overlay);

    // ── Theme observer ──
    setupThemeObserver(nav, hamburger, mobileLogo);

    // ── Hamburger toggle ──
    hamburger.addEventListener('click', () => {
      overlay.classList.toggle('open');
      document.body.style.overflow = overlay.classList.contains('open') ? 'hidden' : '';
    });

    // ── Overlay close button ──
    overlay.querySelector('#lis-nav-overlay-close').addEventListener('click', () => {
      overlay.classList.remove('open');
      document.body.style.overflow = '';
    });

    // ── Services toggle in overlay ──
    const serviceBtn = overlay.querySelector('#overlay-services-btn');
    const serviceSub = overlay.querySelector('#overlay-sub');
    if (serviceBtn && serviceSub) {
      serviceBtn.addEventListener('click', () => {
        serviceBtn.classList.toggle('open');
        serviceSub.classList.toggle('open');
      });
    }

    // ── Close overlay on link click ──
    overlay.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        overlay.classList.remove('open');
        document.body.style.overflow = '';
      });
    });

    // ── Close overlay on Escape ──
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && overlay.classList.contains('open')) {
        overlay.classList.remove('open');
        document.body.style.overflow = '';
      }
    });

    // ── Scroll: add subtle shadow after scrolling ──
    window.addEventListener('scroll', () => {
      const scrolled = window.scrollY > 40;
      pill.style.boxShadow = scrolled
        ? (nav.classList.contains('nav-dark')
            ? '0 2px 24px rgba(0,0,0,0.13)'
            : '0 2px 24px rgba(0,0,0,0.45)')
        : '';
    }, { passive: true });
  }

  /* ─── Run when DOM ready ──────────────────────────────────── */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
