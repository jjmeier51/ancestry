(function () {
  'use strict';
  const F = window.Family, A = window.App, el = A.el, icon = A.icon;
  A.views.stories = {
    title: () => 'Stories',
    render(container, r) {
      const wrap = el('div', { class: 'wrap narrow' }, [el('h1', { text: 'Family stories' })]);
      container.appendChild(wrap);
      if (!F.stories.length) { wrap.appendChild(el('div', { class: 'empty', text: 'No stories yet. Add them to data/stories.json.' })); return; }
      F.stories.forEach(s => {
        const people = (s.people || []).map(F.get).filter(Boolean);
        wrap.appendChild(el('article', { class: 'card story', id: 'story-' + s.id }, [
          el('h2', { text: s.title }),
          s.date ? el('p', { class: s.date.length > 40 ? 'story-when muted small' : 'story-date', html: (s.date.length > 40 ? 'When: ' : '') + A.md(s.date) }) : null,
          el('div', { class: 'story-body' }, String(s.body || '').split(/\n+/).filter(Boolean).map(t => el('p', { html: A.md(t.trim()) }))),
          s.image ? el('img', { src: s.image, alt: s.title, class: 'story-img' }) : null,
          s.source ? el('p', { class: 'muted small story-source', html: 'Source: ' + A.md(s.source) }) : null,
          people.length ? el('div', { class: 'chip-row' }, people.map(p => el('a', { class: 'chip', href: `#/person/${encodeURIComponent(p.id)}` }, [A.avatar(p, 'xs'), el('b', { text: F.shortName(p) })]))) : null
        ]));
      });
      if (r.id) { const t = document.getElementById('story-' + r.id); if (t) { setTimeout(() => t.scrollIntoView({ behavior: 'smooth', block: 'start' }), 50); t.classList.add('highlight'); } }
    }
  };
})();
