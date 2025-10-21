// /src/js/work.js

/**
 * Portfolio grid + slider + Masonry layout
 * - Renders project cards from /projects/index.json
 * - Wires image sliders with autoplay + hover pause
 * - Filters by tag
 * - Lays out with Masonry after images load
 */

/* ---------------- DOM ---------------- */

const GRID   = document.getElementById('project-grid');
const EMPTY  = document.getElementById('no-results');
const FILTERS = Array.from(document.querySelectorAll('.filter'));

/* ---------------- Slider / Motion ---------------- */

const AUTOPLAY_MS   = 8000; // time between slides
const IDLE_PAUSE_MS = 5000; // pause after manual interaction
const RESPECTS_RM   = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches === true;

/* ---------------- Masonry ---------------- */

let msnry = null;
let layoutQueued = false;

/**
 * Initialize Masonry once all images inside GRID are fully loaded.
 * Uses a column sizer (.masonry-sizer) + percentPosition for responsive columns.
 */
function initMasonryAfterImages() {
  if (!window.imagesLoaded || !window.Masonry || !GRID) return;

  imagesLoaded(GRID, { background: true }, () => {
    if (msnry) msnry.destroy();

    msnry = new Masonry(GRID, {
      itemSelector: '.project',
      columnWidth:  '.masonry-sizer',
      gutter: 24,
      percentPosition: true,
      transitionDuration: '0.5s',
      // NOTE: Let Masonry handle window resizes (no custom resizing needed).
      // resize: false
    });

    msnry.layout();
  });
}

/**
 * Request a single Masonry layout on the next animation frame.
 * Safe to call frequently—coalesces multiple calls into one.
 */
function relayoutMasonrySoon() {
  if (!msnry || layoutQueued) return;
  layoutQueued = true;
  requestAnimationFrame(() => {
    layoutQueued = false;
    msnry.layout();
  });
}

/* ---------------- App Bootstrap ---------------- */

main().catch(err => {
  console.error('[work.js] init failed:', err);
  if (EMPTY) {
    EMPTY.hidden = false;
    EMPTY.textContent = 'Failed to load projects.';
  }
});

/**
 * App entrypoint
 */
async function main() {
  if (!GRID) {
    console.warn('[work.js] #project-grid not found; aborting.');
    return;
  }

  const slugs = await fetchJSON('/projects/index.json'); // [{slug}]
  if (!Array.isArray(slugs)) throw new Error('index.json must be an array');

  const projects = (await Promise.all(slugs.map(loadProjectSafely))).filter(Boolean);
  projects.sort((a, b) => new Date(b.date || 0) - new Date(a.date || 0));

  // Inject a Masonry sizer + cards
  GRID.innerHTML = `<div class="masonry-sizer"></div>` + projects.map(renderProjectCard).join('');

  // Wire sliders per card
  GRID.querySelectorAll('.project').forEach(wireSlider);

  // Init Masonry after images finish loading
  initMasonryAfterImages();

  // Filters
  FILTERS.forEach(btn => {
    btn.addEventListener('click', () => {
      FILTERS.forEach(b => {
        const active = b === btn;
        b.classList.toggle('active', active);
        b.setAttribute('aria-selected', String(active));
      });
      applyFilter(btn.dataset.filter || 'all');
    });
  });

  applyFilter('all');
}

/* ---------------- Data / Rendering ---------------- */

/**
 * Load and validate a single project safely.
 * @param {{slug:string}} item
 * @returns {Promise<null|object>}
 */
async function loadProjectSafely(item) {
  try {
    if (!item || !item.slug) return null;
    const base = `/projects/${item.slug}`;
    const meta = await fetchJSON(`${base}/meta.json`);
    if (!meta || !meta.title) return null;

    return {
      slug: item.slug,
      base,
      title: meta.title,
      summary: meta.summary || '',
      tags: (meta.tags || []).map(t => String(t).toLowerCase()),
      date: meta.date || '',
      size: meta.size || null,              // "small" | "wide" (optional)
      links: meta.links || {},
      images: Array.isArray(meta.images) ? meta.images : [],
      files: Array.isArray(meta.files) ? meta.files : []
    };
  } catch (e) {
    console.warn(`[work.js] skipping ${item?.slug}:`, e);
    return null;
  }
}

/**
 * Render a project card (HTML string).
 */
function renderProjectCard(p) {
  const sizeClass = p.size ? ` ${p.size}` : '';
  const tagAttr = p.tags.join(' ');
  const humanDate = formatDate(p.date);

  const slides = (p.images.length ? p.images : [{ src: '', alt: '' }])
    .map(img => renderSlide(p.base, img, p.title))
    .join('');

  const filesList = (p.files && p.files.length)
    ? `<div class="project-files">
         <ul>
           ${p.files.map(f => {
             const label = escapeHtml(f.label || f.src || 'Download');
             const href  = `${p.base}/${escapeHtml(f.src || '')}`;
             const icon  = pickFileEmoji(f.src);
             return `<li><a href="${href}" target="_blank" rel="noopener">${icon} ${label}</a></li>`;
           }).join('')}
         </ul>
       </div>`
    : '';

  const linksBlock = (p.links && (p.links.live || p.links.repo))
    ? `<div class="project-links">
         ${p.links.live ? `<a href="${escapeHtml(p.links.live)}" target="_blank" rel="noopener">Visit ↗</a>` : ''}
         ${p.links.repo ? `<a href="${escapeHtml(p.links.repo)}" target="_blank" rel="noopener">GitHub ↗</a>` : ''}
       </div>`
    : '';

  return `
  <article class="project ${sizeClass}" data-tags="${escapeHtml(tagAttr)}">
    <div class="project-hero">
      <div class="hero-slider">
        <div class="slider-track">
          ${slides}
        </div>
      </div>
    </div>

    <div class="slider-nav" aria-label="Project images">
      <button class="slider-arrow prev" aria-label="Previous slide">←</button>
      <div class="slider-dots"></div>
      <button class="slider-arrow next" aria-label="Next slide">→</button>
    </div>

    <div class="project-description">
      ${linksBlock}
      <h2>${escapeHtml(p.title)}</h2>
      <p>${escapeHtml(p.summary)}</p>
      ${humanDate ? `<div class="project-meta"><time class="project-date" datetime="${escapeHtml(p.date)}">${humanDate}</time></div>` : ''}
      ${filesList}
    </div>
  </article>`;
}

/**
 * Render a single slider slide.
 */
function renderSlide(base, img, fallbackAlt) {
  const src = String(img?.src || '').trim();
  const alt = escapeHtml(img?.alt || fallbackAlt || '');

  if (!src) {
    return `
      <div class="slide">
        <div class="slide-fallback" aria-hidden="true" style="width:90%;height:90%;"></div>
      </div>
    `;
  }

  return `
    <div class="slide">
      <img src="${base}/${escapeHtml(src)}" alt="${alt}" loading="lazy" decoding="async">
    </div>
  `;
}

/* ---------------- Slider Wiring ---------------- */

/**
 * Wire a slider inside a project card.
 */
function wireSlider(projectEl) {
  const track = projectEl.querySelector('.slider-track');
  if (!track) return;

  const slides = Array.from(track.children);
  const dots   = projectEl.querySelector('.slider-dots');
  const prev   = projectEl.querySelector('.slider-arrow.prev');
  const next   = projectEl.querySelector('.slider-arrow.next');
  const hero   = projectEl.querySelector('.hero-slider');
  const nav    = projectEl.querySelector('.slider-nav');

  // If only one slide, hide nav and bail.
  if (slides.length <= 1) {
    if (nav) nav.style.display = 'none';
    return;
  }

  let current = 0;
  let timer = null;
  let idlePauseTimer = null;
  let isHovering = false;

  // (Re)build dots
  if (dots) {
    dots.innerHTML = '';
    slides.forEach((_, i) => {
      const dot = document.createElement('button');
      dot.type = 'button';
      dot.className = 'slider-dot';
      dot.setAttribute('aria-label', `Show slide ${i + 1}`);
      dot.setAttribute('role', 'tab');
      dot.addEventListener('click', () => { show(i); userInteracted(); });
      dots.appendChild(dot);
    });
  }

  function show(i) {
    if (!slides.length) return;
    current = (i + slides.length) % slides.length;
    track.style.transform = `translateX(-${current * 100}%)`;

    if (dots) {
      Array.from(dots.children).forEach((d, j) => {
        const active = j === current;
        d.classList.toggle('active', active);
        d.setAttribute('aria-selected', String(active));
      });
    }

    slides.forEach((s, j) => s.classList.toggle('active', j === current));
    relayoutMasonrySoon();
  }

  function start() {
    if (RESPECTS_RM || document.hidden || slides.length <= 1 || isHovering) return;
    stop();

    timer = setInterval(() => {
      show(current + 1);
    }, AUTOPLAY_MS);
  }

  function stop() {
    clearInterval(timer);
    timer = null;
  }

  function userInteracted() {
    stop();
    clearTimeout(idlePauseTimer);
    idlePauseTimer = setTimeout(start, IDLE_PAUSE_MS);
  }

  // Mouse controls
  // Mouse controls
  prev?.addEventListener('click', () => { show(current - 1); userInteracted(); });
  next?.addEventListener('click', () => { show(current + 1); userInteracted(); });

  // Hover pause/resume (works on arrows, dots, and hero)
  [hero, dots, prev, next].filter(Boolean).forEach(el => {
    el.addEventListener('mouseenter', () => { 
      isHovering = true; 
      stop(); 
    });
    el.addEventListener('mouseleave', () => { 
      isHovering = false; 
      userInteracted(); 
    });
  });

  // Tab visibility pause
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) stop(); 
    else userInteracted();
  });

  // Init
  show(0);
  start();
}

/* ---------------- Filtering ---------------- */

/**
 * Show only cards that contain the tag `key` (case-insensitive).
 * Use 'all' to show everything.
 */
function applyFilter(key) {
  const k = (key || 'all').toLowerCase();
  const cards = Array.from(GRID.querySelectorAll('.project'));
  let shown = 0;

  for (const card of cards) {
    const tags = (card.getAttribute('data-tags') || '').toLowerCase();
    const match = k === 'all' || tags.includes(k);
    card.hidden = !match;
    card.setAttribute('aria-hidden', String(!match));
    if (match) shown++;
  }

  if (EMPTY) EMPTY.hidden = shown !== 0;

  // Tighten layout after visibility changes
  relayoutMasonrySoon();
}

/* ---------------- Utilities ---------------- */

/**
 * Fetch JSON with basic error handling.
 */
async function fetchJSON(url) {
  const res = await fetch(url, { headers: { 'Accept': 'application/json' } });
  if (!res.ok) throw new Error(`${url} -> ${res.status}`);
  return res.json();
}

/**
 * Escape HTML entities.
 */
function escapeHtml(s) {
  return String(s ?? '')
    .replace(/&/g,'&amp;')
    .replace(/</g,'&lt;')
    .replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;')
    .replace(/'/g,'&#039;');
}

/**
 * Format ISO date to a localized long date, or '' if invalid.
 */
function formatDate(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  if (isNaN(d)) return '';
  return d.toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' });
}

/**
 * Pick an icon based on file extension.
 */
function pickFileEmoji(path = '') {
  const lower = String(path).toLowerCase();
  if (lower.endsWith('.pdf')) return '📄';
  if (lower.endsWith('.zip') || lower.endsWith('.rar') || lower.endsWith('.7z')) return '📦';
  if (lower.endsWith('.mov') || lower.endsWith('.mp4') || lower.endsWith('.webm')) return '🎬';
  if (lower.endsWith('.png') || lower.endsWith('.jpg') || lower.endsWith('.jpeg') || lower.endsWith('.gif') || lower.endsWith('.webp')) return '🖼️';
  return '⬇️';
}
