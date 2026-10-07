/* Shared UI: header/navigation, global search, person cards, helpers. */
(function () {
  'use strict';
  var F = window.Family;

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function el(tag, attrs, children) {
    var e = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === 'class') e.className = attrs[k];
      else if (k === 'html') e.innerHTML = attrs[k];
      else if (k === 'text') e.textContent = attrs[k];
      else if (k.indexOf('on') === 0) e.addEventListener(k.slice(2), attrs[k]);
      else e.setAttribute(k, attrs[k]);
    });
    (children || []).forEach(function (c) { if (c) e.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return e;
  }
  function param(name) {
    var m = new RegExp('[?&]' + name + '=([^&]*)').exec(location.search);
    return m ? decodeURIComponent(m[1].replace(/\+/g, ' ')) : null;
  }
  function personUrl(p) { return 'person.html?id=' + encodeURIComponent(typeof p === 'string' ? p : p.id); }

  var NAV = [
    ['index.html', 'Home'], ['tree.html', 'Family Tree'], ['people.html', 'People'],
    ['timeline.html', 'Timeline'], ['stories.html', 'Stories'], ['gallery.html', 'Gallery']
  ];

  function renderHeader() {
    var here = location.pathname.split('/').pop() || 'index.html';
    var header = document.querySelector('header.site-header');
    if (!header) return;
    header.innerHTML =
      '<div class="wrap header-inner">' +
      '  <a class="brand" href="index.html"><span class="brand-mark" aria-hidden="true">&#x2767;</span><span>' + esc(F.title) + '</span></a>' +
      '  <button class="nav-toggle" aria-label="Menu" aria-expanded="false">&#9776;</button>' +
      '  <nav class="site-nav" aria-label="Main">' +
      NAV.map(function (n) {
        return '<a href="' + n[0] + '"' + (n[0] === here ? ' class="active" aria-current="page"' : '') + '>' + n[1] + '</a>';
      }).join('') +
      '  </nav>' +
      '  <form class="search" role="search" autocomplete="off">' +
      '    <input type="search" name="q" placeholder="Search people…" aria-label="Search people" />' +
      '    <ul class="search-results" hidden></ul>' +
      '  </form>' +
      '</div>';
    document.title = (document.title ? document.title + ' · ' : '') + F.title;

    var toggle = header.querySelector('.nav-toggle');
    toggle.addEventListener('click', function () {
      var open = header.classList.toggle('nav-open');
      toggle.setAttribute('aria-expanded', open);
    });

    var form = header.querySelector('.search');
    var input = form.querySelector('input');
    var list = form.querySelector('.search-results');
    function update() {
      var res = F.search(input.value).slice(0, 8);
      list.innerHTML = '';
      if (!res.length) { list.hidden = true; return; }
      res.forEach(function (p) {
        list.appendChild(el('li', {}, [el('a', { href: personUrl(p) }, [
          avatar(p, 'xs'),
          el('span', {}, [el('strong', { text: F.fullName(p) }), ' ', el('small', { text: F.lifespan(p) })])
        ])]));
      });
      list.hidden = false;
    }
    input.addEventListener('input', update);
    input.addEventListener('focus', update);
    document.addEventListener('click', function (e) { if (!form.contains(e.target)) list.hidden = true; });
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var res = F.search(input.value);
      if (res.length === 1) location.href = personUrl(res[0]);
      else location.href = 'people.html?q=' + encodeURIComponent(input.value);
    });
  }

  function renderFooter() {
    var f = document.querySelector('footer.site-footer');
    if (!f) return;
    var people = F.all();
    f.innerHTML = '<div class="wrap">' +
      '<p>' + esc(F.title) + ' · ' + people.length + ' people · ' + F.families.length + ' families · ' +
      'generated from <code>data/family.js</code></p></div>';
  }

  function avatar(p, size) {
    var cls = 'avatar' + (size ? ' avatar-' + size : '') + ' sex-' + (p && p.sex ? p.sex.toLowerCase() : 'u');
    if (p && p.photo) return el('img', { class: cls, src: p.photo, alt: F.fullName(p), loading: 'lazy' });
    return el('span', { class: cls, 'aria-hidden': 'true', text: F.initials(p) });
  }

  function personCard(p, opts) {
    opts = opts || {};
    var meta = [];
    var life = F.lifespan(p); if (life) meta.push(life);
    if (p.birth && p.birth.place && !opts.compact) meta.push(p.birth.place.split(',')[0]);
    var card = el('a', { class: 'person-card' + (opts.compact ? ' compact' : ''), href: personUrl(p) }, [
      avatar(p, opts.compact ? 'sm' : 'md'),
      el('span', { class: 'person-card-body' }, [
        opts.label ? el('span', { class: 'person-card-label', text: opts.label }) : null,
        el('span', { class: 'person-card-name', text: F.fullName(p) }),
        el('span', { class: 'person-card-meta', text: meta.join(' · ') })
      ])
    ]);
    return card;
  }

  function init() {
    renderHeader();
    renderFooter();
    if (!F.all().length) {
      var main = document.querySelector('main');
      if (main) main.insertBefore(el('div', { class: 'wrap notice' }, [
        el('strong', { text: 'No family data found. ' }),
        'Edit data/family.js or import a GEDCOM file with scripts/gedcom_to_data.py.'
      ]), main.firstChild);
    }
  }

  window.UI = { esc: esc, el: el, param: param, personUrl: personUrl, avatar: avatar, personCard: personCard, init: init };
  document.addEventListener('DOMContentLoaded', init);
})();
