/* App shell: routing, navigation chrome, search overlay, bottom sheet, helpers. */
(function () {
  'use strict';
  const F = window.Family;

  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  function el(tag, attrs, children) {
    const e = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(k => {
      const v = attrs[k];
      if (v === null || v === undefined || v === false) return;
      if (k === 'class') e.className = v;
      else if (k === 'html') e.innerHTML = v;
      else if (k === 'text') e.textContent = v;
      else if (k.startsWith('on')) e.addEventListener(k.slice(2), v);
      else if (k === 'style' && typeof v === 'object') Object.assign(e.style, v);
      else e.setAttribute(k, v === true ? '' : v);
    });
    (children || []).forEach(c => { if (c !== null && c !== undefined && c !== false) e.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return e;
  }

  const ICONS = {
    tree: '<path d="M12 3v4M12 7a3 3 0 0 1 3 3v1H9v-1a3 3 0 0 1 3-3zM5 15h14M5 15v-3h14v3M5 15v4M19 15v4M12 15v4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    people: '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0" stroke-linecap="round"/><circle cx="17" cy="9" r="2.5"/><path d="M15.5 14.5a5 5 0 0 1 6 5" stroke-linecap="round"/>',
    clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2" stroke-linecap="round" stroke-linejoin="round"/>',
    book: '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 21V5M8 7h7" stroke-linecap="round"/>',
    image: '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="M21 16l-5-5-8 8" stroke-linecap="round" stroke-linejoin="round"/>',
    search: '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5" stroke-linecap="round"/>',
    back: '<path d="M15 5l-7 7 7 7" stroke-linecap="round" stroke-linejoin="round"/>',
    close: '<path d="M6 6l12 12M18 6L6 18" stroke-linecap="round"/>',
    plus: '<path d="M12 5v14M5 12h14" stroke-linecap="round"/>',
    minus: '<path d="M5 12h14" stroke-linecap="round"/>',
    fit: '<path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" stroke-linecap="round" stroke-linejoin="round"/>',
    person: '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0" stroke-linecap="round"/>',
    military: '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z" stroke-linejoin="round"/><path d="M9 12l2 2 4-4" stroke-linecap="round" stroke-linejoin="round"/>',
    star: '<path d="M12 3l2.7 5.8 6.3.7-4.7 4.3 1.3 6.2L12 17l-5.6 3 1.3-6.2L3 9.5l6.3-.7z" stroke-linejoin="round"/>',
    pin: '<path d="M12 21s-6-5.5-6-11a6 6 0 0 1 12 0c0 5.5-6 11-6 11z"/><circle cx="12" cy="10" r="2"/>',
    doc: '<path d="M6 3h8l5 5v13H6z" stroke-linejoin="round"/><path d="M14 3v5h5M9 13h6M9 17h6" stroke-linecap="round"/>',
    link: '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1" stroke-linecap="round"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1" stroke-linecap="round"/>',
    external: '<path d="M14 4h6v6M20 4l-9 9" stroke-linecap="round" stroke-linejoin="round"/><path d="M19 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h5" stroke-linecap="round"/>',
    heart: '<path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.5A4 4 0 0 1 19 10c0 5.5-7 10-7 10z" stroke-linejoin="round"/>',
    rings: '<circle cx="9" cy="13" r="5"/><circle cx="15" cy="13" r="5"/>',
    baby: '<circle cx="12" cy="12" r="8"/><path d="M9 10h.01M15 10h.01M9 14.5a4 4 0 0 0 6 0" stroke-linecap="round"/>',
    cross: '<path d="M12 4v16M7 9h10" stroke-linecap="round"/>',
    check: '<path d="M5 12l4 4 10-10" stroke-linecap="round" stroke-linejoin="round"/>',
    info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8h.01" stroke-linecap="round"/>',
    sparkle: '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z" stroke-linejoin="round"/><path d="M19 17l.7 1.8 1.8.7-1.8.7L19 22l-.7-1.8-1.8-.7 1.8-.7z" stroke-linejoin="round"/>',
    chevron: '<path d="M9 6l6 6-6 6" stroke-linecap="round" stroke-linejoin="round"/>',
    layers: '<path d="M12 3l9 5-9 5-9-5z" stroke-linejoin="round"/><path d="M3 13l9 5 9-5M3 17l9 5 9-5" stroke-linejoin="round"/>',
    up: '<path d="M12 19V5M5 12l7-7 7 7" stroke-linecap="round" stroke-linejoin="round"/>',
    down: '<path d="M12 5v14M5 12l7 7 7-7" stroke-linecap="round" stroke-linejoin="round"/>',
    home: '<path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z" stroke-linejoin="round"/>',
    share: '<circle cx="18" cy="5" r="2.5"/><circle cx="6" cy="12" r="2.5"/><circle cx="18" cy="19" r="2.5"/><path d="M8.2 10.8l7.6-4.6M8.2 13.2l7.6 4.6" stroke-linecap="round"/>'
  };
  const icon = (name, cls) => `<svg class="icon${cls ? ' ' + cls : ''}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">${ICONS[name] || ''}</svg>`;
  const iconEl = (name, cls) => { const t = document.createElement('span'); t.innerHTML = icon(name, cls); return t.firstChild; };

  const TAG_ICONS = { military: 'military', veteran: 'military', notable: 'star', famous: 'star', artist: 'sparkle', athlete: 'star', immigrant: 'pin', historian: 'book', clergy: 'book', politician: 'star', musician: 'sparkle', author: 'book', inventor: 'sparkle', pioneer: 'pin' };
  const tagIcon = t => TAG_ICONS[t] || 'sparkle';
  const tagLabel = t => t.charAt(0).toUpperCase() + t.slice(1).replace(/[-_]/g, ' ');

  /* ---------- Reusable components ---------- */
  function avatar(p, size) {
    const cls = `avatar ${size || ''} sex-${(p && p.sex || 'U').toLowerCase()}`;
    const src = F.photo(p);
    if (src) return el('img', { class: cls, src, alt: F.fullName(p), loading: 'lazy' });
    return el('span', { class: cls, 'aria-hidden': 'true', text: F.initials(p) });
  }
  function confBadge(p, withLabel) {
    const c = F.confidence(p);
    return el('span', { class: `conf conf-${c}`, title: F.confidenceLabel(c) + ': ' + F.confidenceDescription(c) }, [
      el('i'), withLabel ? F.confidenceLabel(c) : null
    ]);
  }
  function personRow(p, opts) {
    opts = opts || {};
    const meta = [F.lifespan(p), opts.meta !== undefined ? opts.meta : (p.birth && p.birth.place ? p.birth.place.split(',')[0] : '')].filter(Boolean).join(' · ');
    return el('a', { class: 'row' + (opts.compact ? ' compact' : ''), href: opts.href || `#/person/${encodeURIComponent(p.id)}` }, [
      avatar(p, opts.compact ? 'sm' : 'md'),
      el('span', { class: 'row-body' }, [
        opts.label ? el('span', { class: 'row-label', text: opts.label }) : null,
        el('span', { class: 'row-name', text: F.fullName(p) }),
        el('span', { class: 'row-meta', text: meta })
      ]),
      el('span', { class: 'row-end' }, [confBadge(p), iconEl('chevron', 'chev')])
    ]);
  }

  /* ---------- Router ---------- */
  const views = {};
  let current = null, currentName = null;
  const TABS = [
    { route: 'tree', label: 'Tree', icon: 'tree', hash: '#/' },
    { route: 'people', label: 'People', icon: 'people', hash: '#/people' },
    { route: 'timeline', label: 'Timeline', icon: 'clock', hash: '#/timeline' },
    { route: 'stories', label: 'Stories', icon: 'book', hash: '#/stories' },
    { route: 'media', label: 'Media', icon: 'image', hash: '#/media' }
  ];
  function parseHash() {
    const h = (location.hash || '#/').replace(/^#\/?/, '');
    const [path, qs] = h.split('?');
    const parts = path.split('/').filter(Boolean);
    const params = {};
    (qs || '').split('&').forEach(kv => { if (!kv) return; const [k, v] = kv.split('='); params[decodeURIComponent(k)] = decodeURIComponent(v || ''); });
    const name = parts[0] || 'tree';
    return { name: views[name] ? name : (parts[0] ? '404' : 'tree'), id: parts[1] ? decodeURIComponent(parts[1]) : null, params, hash: location.hash };
  }
  function route() {
    const r = parseHash();
    hideSheet();
    const main = document.getElementById('view');
    const sameView = currentName === r.name && current && current.update && current.update(r) !== false;
    if (sameView) { updateChrome(r); return; }
    if (current && current.destroy) current.destroy();
    const container = el('section', { class: 'view view-' + r.name, 'data-view': r.name });
    const render = () => {
      main.innerHTML = '';
      main.appendChild(container);
      main.scrollTop = 0; window.scrollTo(0, 0);
      const v = views[r.name] || views['404'];
      current = v.render(container, r) || {};
      currentName = r.name;
      updateChrome(r);
    };
    if (document.startViewTransition && currentName) document.startViewTransition(render);
    else render();
  }
  function updateChrome(r) {
    document.querySelectorAll('.tabbar a').forEach(a => a.classList.toggle('active', a.dataset.route === r.name || (r.name === 'person' && a.dataset.route === 'people' && false)));
    const top = document.querySelector('.topbar');
    const isSub = r.name === 'person' || (r.name !== 'tree' && r.id);
    top.classList.toggle('sub', !!isSub);
    const titleEl = top.querySelector('.topbar-title');
    const v = views[r.name];
    const t = v && v.title ? v.title(r) : F.shortTitle;
    titleEl.textContent = t;
    document.title = (t === F.shortTitle ? F.title : t + ' · ' + F.shortTitle);
  }
  function navigate(hash) { if (location.hash === hash) route(); else location.hash = hash; }
  function back() { if (history.length > 1) history.back(); else navigate('#/'); }

  /* ---------- Bottom sheet ---------- */
  let sheetEl = null;
  function showSheet(content, opts) {
    hideSheet(true);
    opts = opts || {};
    const backdrop = el('div', { class: 'sheet-backdrop', onclick: () => hideSheet() });
    const sheet = el('div', { class: 'sheet' + (opts.cls ? ' ' + opts.cls : ''), role: 'dialog', 'aria-modal': 'true' }, [
      el('div', { class: 'sheet-handle' }),
      el('button', { class: 'sheet-close', 'aria-label': 'Close', onclick: () => hideSheet(), html: icon('close') }),
      content
    ]);
    sheetEl = el('div', { class: 'sheet-host' }, [backdrop, sheet]);
    document.body.appendChild(sheetEl);
    // swipe down to dismiss
    let startY = null;
    sheet.addEventListener('touchstart', e => { startY = e.touches[0].clientY; }, { passive: true });
    sheet.addEventListener('touchmove', e => {
      if (startY === null) return;
      const dy = e.touches[0].clientY - startY;
      if (dy > 0 && sheet.scrollTop <= 0) sheet.style.transform = `translateY(${dy}px)`;
    }, { passive: true });
    sheet.addEventListener('touchend', e => {
      const dy = e.changedTouches[0].clientY - (startY || 0);
      startY = null;
      if (dy > 90) hideSheet(); else sheet.style.transform = '';
    });
    requestAnimationFrame(() => sheetEl.classList.add('open'));
    return sheet;
  }
  function hideSheet(immediate) {
    if (!sheetEl) return;
    const s = sheetEl; sheetEl = null;
    if (immediate) { s.remove(); return; }
    s.classList.remove('open');
    setTimeout(() => s.remove(), 260);
  }
  function personSheet(p, opts) {
    opts = opts || {};
    const me = F.owner();
    const rel = me ? F.relationshipSentence(me.id, p.id) : '';
    const relatives = [];
    F.parents(p.id).forEach(q => relatives.push([q, q.sex === 'M' ? 'Father' : q.sex === 'F' ? 'Mother' : 'Parent']));
    F.spouses(p.id).forEach(q => relatives.push([q, q.sex === 'M' ? 'Husband' : q.sex === 'F' ? 'Wife' : 'Spouse']));
    F.children(p.id).forEach(q => relatives.push([q, q.sex === 'M' ? 'Son' : q.sex === 'F' ? 'Daughter' : 'Child']));
    const content = el('div', { class: 'person-sheet' }, [
      el('div', { class: 'ps-head' }, [
        avatar(p, 'lg'),
        el('div', { class: 'ps-text' }, [
          el('h2', { text: F.fullName(p) }),
          el('div', { class: 'ps-meta', text: [F.lifespan(p), p.birth && p.birth.place ? p.birth.place.split(',')[0] : ''].filter(Boolean).join(' · ') }),
          el('div', { class: 'ps-badges' }, [confBadge(p, true)].concat(F.tags(p).slice(0, 3).map(t => el('span', { class: 'tag', html: icon(tagIcon(t)) + esc(tagLabel(t)) }))))
        ])
      ]),
      rel ? el('p', { class: 'ps-rel', html: icon('heart') + esc(rel) }) : null,
      el('div', { class: 'ps-actions' }, [
        el('a', { class: 'btn primary', href: `#/person/${encodeURIComponent(p.id)}`, html: icon('person') + 'View profile' }),
        el('a', { class: 'btn', href: `#/tree/${encodeURIComponent(p.id)}`, html: icon('tree') + 'View tree', onclick: () => { hideSheet(); } })
      ]),
      relatives.length ? el('div', { class: 'ps-relatives' }, [
        el('div', { class: 'ps-label', text: 'Jump to' }),
        el('div', { class: 'chip-row' }, relatives.map(([q, label]) => el('a', { class: 'chip', href: opts.treeLinks ? `#/tree/${encodeURIComponent(q.id)}` : `#/person/${encodeURIComponent(q.id)}`, onclick: () => hideSheet(true) }, [
          avatar(q, 'xs'), el('span', {}, [el('small', { text: label }), el('b', { text: F.shortName(q) })])
        ])))
      ]) : null
    ]);
    return showSheet(content);
  }

  /* ---------- Search overlay ---------- */
  let searchHost = null;
  function openSearch() {
    if (searchHost) return;
    const input = el('input', { type: 'search', placeholder: 'Search people, places, years…', autocomplete: 'off', autocorrect: 'off', 'aria-label': 'Search' });
    const results = el('div', { class: 'search-results' });
    const close = () => { searchHost.classList.remove('open'); setTimeout(() => { if (searchHost) { searchHost.remove(); searchHost = null; } }, 200); };
    function update() {
      results.innerHTML = '';
      const q = input.value.trim();
      const res = q ? F.search(q).slice(0, 30) : [];
      if (!q) { results.appendChild(el('p', { class: 'hint', text: 'Try a name, a town, a year or a tag like “military”.' })); return; }
      if (!res.length) { results.appendChild(el('p', { class: 'hint', text: 'No one matches “' + q + '”.' })); return; }
      res.forEach(p => { const r = personRow(p, { compact: true }); r.addEventListener('click', close); results.appendChild(r); });
    }
    searchHost = el('div', { class: 'search-host' }, [
      el('div', { class: 'search-bar' }, [iconEl('search'), input, el('button', { class: 'link-btn', text: 'Cancel', onclick: close })]),
      results
    ]);
    document.body.appendChild(searchHost);
    input.addEventListener('input', update);
    input.addEventListener('keydown', e => { if (e.key === 'Escape') close(); if (e.key === 'Enter') { const first = results.querySelector('a'); if (first) first.click(); } });
    update();
    requestAnimationFrame(() => { searchHost.classList.add('open'); input.focus(); });
  }

  /* ---------- Lightbox ---------- */
  function lightbox(items, index) {
    let i = index || 0;
    const img = el('img', { alt: '' });
    const cap = el('p');
    const host = el('div', { class: 'lightbox', onclick: e => { if (e.target === host || e.target === img) host.remove(); } }, [
      el('button', { class: 'lb-close', 'aria-label': 'Close', html: icon('close'), onclick: () => host.remove() }),
      items.length > 1 ? el('button', { class: 'lb-prev', 'aria-label': 'Previous', html: icon('back'), onclick: e => { e.stopPropagation(); show(i - 1); } }) : null,
      img, cap,
      items.length > 1 ? el('button', { class: 'lb-next', 'aria-label': 'Next', html: icon('chevron'), onclick: e => { e.stopPropagation(); show(i + 1); } }) : null
    ]);
    function show(n) { i = (n + items.length) % items.length; img.src = items[i].file; cap.textContent = [items[i].title, items[i].date ? F.formatDate(items[i].date) : ''].filter(Boolean).join(' · '); }
    show(i);
    const key = e => { if (e.key === 'Escape') host.remove(); if (e.key === 'ArrowRight') show(i + 1); if (e.key === 'ArrowLeft') show(i - 1); };
    document.addEventListener('keydown', key);
    host.addEventListener('DOMNodeRemoved', () => document.removeEventListener('keydown', key));
    document.body.appendChild(host);
  }

  function toast(msg) {
    const t = el('div', { class: 'toast', text: msg });
    document.body.appendChild(t);
    requestAnimationFrame(() => t.classList.add('show'));
    setTimeout(() => { t.classList.remove('show'); setTimeout(() => t.remove(), 300); }, 2600);
  }

  /* ---------- Boot ---------- */
  function buildChrome() {
    const top = document.querySelector('.topbar');
    top.innerHTML = '';
    top.appendChild(el('button', { class: 'tb-btn tb-back', 'aria-label': 'Back', html: icon('back'), onclick: back }));
    top.appendChild(el('a', { class: 'tb-brand', href: '#/' }, [el('span', { class: 'brand-mark', html: icon('tree') }), el('span', { class: 'topbar-title', text: F.shortTitle })]));
    top.appendChild(el('nav', { class: 'topnav' }, TABS.map(t => el('a', { href: t.hash, 'data-route': t.route, html: icon(t.icon) + esc(t.label) }))));
    top.appendChild(el('button', { class: 'tb-btn tb-search', 'aria-label': 'Search', html: icon('search'), onclick: openSearch }));
    const tabs = document.querySelector('.tabbar');
    tabs.innerHTML = '';
    TABS.forEach(t => tabs.appendChild(el('a', { href: t.hash, 'data-route': t.route, html: icon(t.icon) + '<span>' + esc(t.label) + '</span>' })));
    document.querySelectorAll('.tabbar a, .topnav a').forEach(a => a.addEventListener('click', e => {
      // tapping the active tab returns to that section's root
      if (a.classList.contains('active') && location.hash === a.getAttribute('href')) { e.preventDefault(); route(); }
    }));
    let dismissed = false; try { dismissed = sessionStorage.getItem('bannerDismissed') === '1'; } catch (e) { /* ignore */ }
    if (F.raw.sample && !dismissed) {
      const b = el('div', { class: 'banner', html: icon('info') + '<span><b>Sample data.</b> Import your GEDCOM to see your own family.</span>' }, [
        el('button', { 'aria-label': 'Dismiss', html: icon('close'), onclick: () => { b.remove(); try { sessionStorage.setItem('bannerDismissed', '1'); } catch (e) { /* ignore */ } } })
      ]);
      document.body.appendChild(b); document.body.classList.add('has-banner');
      b.querySelector('button').addEventListener('click', () => document.body.classList.remove('has-banner'));
    }
  }

  window.App = { esc, el, icon, iconEl, avatar, confBadge, personRow, tagIcon, tagLabel, views, navigate, back, route, parseHash, showSheet, hideSheet, personSheet, openSearch, lightbox, toast, TABS };

  views['404'] = { title: () => 'Not found', render(c) { c.appendChild(el('div', { class: 'wrap empty' }, [el('h1', { text: 'Page not found' }), el('a', { class: 'btn primary', href: '#/', text: 'Back to the tree' })])); } };

  document.addEventListener('DOMContentLoaded', () => {
    buildChrome();
    window.addEventListener('hashchange', route);
    document.addEventListener('keydown', e => { if ((e.metaKey || e.ctrlKey) && e.key === 'k') { e.preventDefault(); openSearch(); } if (e.key === '/' && !/input|textarea|select/i.test(document.activeElement.tagName)) { e.preventDefault(); openSearch(); } });
    route();
    document.body.classList.add('ready');
  });
})();
