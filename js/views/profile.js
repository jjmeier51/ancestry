/* Person profile view. */
(function () {
  'use strict';
  const F = window.Family, A = window.App, el = A.el, icon = A.icon, esc = A.esc;

  const eventLine = ev => ev ? [ev.date ? F.formatDate(ev.date) : '', ev.place || ''].filter(Boolean).join(' · ') : '';
  const paragraphs = text => String(text || '').split(/\n+/).map(t => t.trim()).filter(Boolean).map(t => el('p', { text: t }));
  const personLink = p => `#/person/${encodeURIComponent(p.id)}`;
  const section = (title, iconName, children, cls) => el('section', { class: 'card ' + (cls || '') }, [el('h2', { html: icon(iconName) + esc(title) })].concat(children));
  const relLabel = (q, kind) => q.sex === 'M' ? kind[0] : q.sex === 'F' ? kind[1] : kind[2];

  function mediaCard(m, allImages) {
    const isImg = m.type === 'photo' || (m.file && /\.(jpe?g|png|gif|webp|svg)$/i.test(m.file));
    const href = m.url || m.file || '#';
    const card = el('a', { class: 'media-card type-' + (m.type || 'other'), href, target: m.url || !isImg ? '_blank' : null, rel: 'noopener' }, [
      isImg && m.file ? el('img', { src: m.file, alt: m.title || '', loading: 'lazy' }) : el('div', { class: 'media-icon', html: icon(m.type === 'link' ? 'link' : m.type === 'audio' || m.type === 'video' ? 'sparkle' : 'doc') }),
      el('div', { class: 'media-cap' }, [
        el('b', { text: m.title || (m.type === 'link' ? m.url : 'Untitled') }),
        el('span', { text: [m.date ? F.formatDate(m.date) : '', m.source].filter(Boolean).join(' · ') })
      ])
    ]);
    if (isImg && m.file) card.addEventListener('click', e => { e.preventDefault(); A.lightbox(allImages, allImages.indexOf(m)); });
    return card;
  }

  A.views.person = {
    title: r => { const p = F.get(r.id); return p ? F.fullName(p) : 'Person'; },
    render(container, r) {
      const p = F.get(r.id);
      if (!p) { container.appendChild(el('div', { class: 'wrap empty' }, [el('h1', { text: 'Person not found' }), el('a', { class: 'btn primary', href: '#/people', text: 'Browse people' })])); return; }
      const me = F.owner();
      const conf = F.confidence(p);
      const photo = F.photo(p);
      const a = F.age(p);
      const tags = F.tags(p);

      /* Hero */
      const hero = el('header', { class: 'hero' }, [
        photo ? el('div', { class: 'hero-bg', style: { backgroundImage: `url("${photo}")` } }) : null,
        el('div', { class: 'hero-inner' }, [
          A.avatar(p, 'xl'),
          el('div', { class: 'hero-text' }, [
            el('h1', { text: F.fullName(p) }),
            p.nickname ? el('div', { class: 'nick', text: '“' + p.nickname + '”' }) : null,
            el('div', { class: 'hero-meta', text: [F.lifespan(p), a !== null ? (F.isDeceased(p) ? `died aged ${a}` : `age ${a}`) : '', p.occupation].filter(Boolean).join(' · ') }),
            el('div', { class: 'hero-badges' }, [A.confBadge(p, true)].concat(tags.map(t => el('span', { class: 'tag', html: icon(A.tagIcon(t)) + esc(A.tagLabel(t)) })))),
            me ? el('p', { class: 'hero-rel', html: icon('heart') + esc(F.relationshipSentence(me.id, p.id)) }) : null,
            el('div', { class: 'hero-actions' }, [
              el('a', { class: 'btn primary', href: `#/tree/${encodeURIComponent(p.id)}`, html: icon('tree') + 'View tree' }),
              el('a', { class: 'btn', href: `#/timeline/${encodeURIComponent(p.id)}`, html: icon('clock') + 'Timeline' }),
              navigator.share ? el('button', { class: 'btn', html: icon('share') + 'Share', onclick: () => navigator.share({ title: F.fullName(p), url: location.href }).catch(() => {}) }) : null
            ])
          ])
        ])
      ]);
      container.appendChild(hero);

      const grid = el('div', { class: 'wrap profile-grid' });
      const main = el('div', { class: 'col-main' }), side = el('div', { class: 'col-side' });
      grid.appendChild(main); grid.appendChild(side);
      container.appendChild(grid);

      /* Summary / bio */
      if (p.summary || p.bio || p.notes) {
        main.appendChild(section('About', 'book', [
          p.summary ? el('p', { class: 'lead', text: p.summary }) : null
        ].concat(paragraphs(p.bio), p.notes && p.notes !== p.bio ? [el('details', {}, [el('summary', { text: 'Notes from the family tree file' })].concat(paragraphs(p.notes)))] : [])));
      }

      /* Key facts */
      const facts = [];
      const fact = (label, value) => { if (value) facts.push(el('div', { class: 'fact' }, [el('dt', { text: label }), el('dd', { text: value })])); };
      fact('Born', eventLine(p.birth)); fact('Died', eventLine(p.death)); fact('Buried', eventLine(p.burial));
      fact('Occupation', p.occupation); fact('Religion', p.religion); fact('Education', p.education);
      (p.facts || []).forEach(f => fact(f.label, f.value));
      (p.events || []).forEach(e => fact(e.title || 'Event', [e.date ? F.formatDate(e.date) : '', e.place, e.description].filter(Boolean).join(' · ')));
      if (facts.length) main.appendChild(section('Life', 'info', [el('dl', { class: 'facts' }, facts)]));

      /* Places lived */
      const places = [];
      if (p.birth && p.birth.place) places.push({ date: p.birth.date, place: p.birth.place, what: 'Born' });
      (p.residences || []).forEach(rs => places.push({ date: rs.date, place: rs.place, what: rs.note || 'Lived' }));
      if (p.death && p.death.place) places.push({ date: p.death.date, place: p.death.place, what: 'Died' });
      if (places.length) main.appendChild(section('Places', 'pin', [el('ol', { class: 'places' }, places.map(pl => el('li', {}, [
        el('span', { class: 'place-when', text: pl.date ? (pl.date.includes('–') ? pl.date : F.formatDate(pl.date, true)) : '' }),
        el('span', { class: 'place-what', text: pl.what }),
        el('a', { class: 'place-where', href: 'https://www.google.com/maps/search/' + encodeURIComponent(pl.place), target: '_blank', rel: 'noopener', text: pl.place })
      ])))]));

      /* Military */
      if (p.military && p.military.length) main.appendChild(section('Military service', 'military', p.military.map(m => el('div', { class: 'military' }, [
        el('b', { text: [m.branch, m.service].filter(Boolean).join(' · ') }),
        el('div', { class: 'muted', text: [m.rank, m.unit, m.theatre].filter(Boolean).join(' · ') }),
        m.note ? el('p', { text: m.note }) : null
      ]))));

      /* Notable & fun facts */
      if (p.notable) main.appendChild(section('Noteworthy', 'star', paragraphs(p.notable)));
      if (p.funFacts && p.funFacts.length) main.appendChild(section('Fun facts', 'sparkle', [el('ul', { class: 'fun' }, p.funFacts.map(f => el('li', { text: f })))]));

      /* Stories */
      const stories = F.storiesFor(p.id);
      if (stories.length) main.appendChild(section('Stories', 'book', stories.map(s => el('a', { class: 'story-teaser', href: `#/stories/${encodeURIComponent(s.id)}` }, [
        el('span', { class: 'story-date', text: s.date || '' }), el('b', { text: s.title }),
        el('span', { class: 'muted', text: (s.body || '').slice(0, 160).replace(/\s+\S*$/, '') + '…' })
      ]))));

      /* Media */
      const media = F.mediaFor(p.id);
      if (media.length) {
        const images = media.filter(m => m.file && /\.(jpe?g|png|gif|webp|svg)$/i.test(m.file));
        main.appendChild(section(`Media & documents (${media.length})`, 'image', [el('div', { class: 'media-grid' }, media.map(m => mediaCard(m, images)))]));
      }

      /* Sources & research */
      const log = p.researchLog || [];
      side.appendChild(el('section', { class: 'card research conf-' + conf }, [
        el('h2', { html: icon('check') + 'Research status' }),
        el('div', { class: 'research-conf' }, [A.confBadge(p, true), el('span', { class: 'muted', text: F.confidenceDescription(conf) })]),
        p.link && p.link.note ? el('p', { text: p.link.note }) : null,
        p.sources && p.sources.length ? el('div', {}, [el('h3', { text: 'Sources' }), el('ul', { class: 'sources' }, p.sources.map(s => el('li', { html: /^https?:/.test(s) ? `<a href="${esc(s)}" target="_blank" rel="noopener">${esc(s)}</a>` : esc(s) })))]) : null,
        log.length ? el('div', {}, [el('h3', { text: 'Research log' }), el('ul', { class: 'log' }, log.slice().reverse().map(e => el('li', {}, [el('time', { text: e.date || '' }), ' ', e.note || ''])))]) : null,
        !log.length && !(p.sources && p.sources.length) ? el('p', { class: 'muted', text: 'No research recorded yet.' }) : null
      ]));

      /* Family */
      const fam = el('section', { class: 'card' }, [el('h2', { html: icon('people') + 'Family' })]);
      const group = (title, items, labelFn) => {
        if (!items.length) return;
        fam.appendChild(el('h3', { text: title }));
        items.forEach(q => fam.appendChild(A.personRow(q, { compact: true, label: labelFn ? labelFn(q) : null })));
      };
      const parents = F.parents(p.id);
      group('Parents', parents, q => relLabel(q, ['Father', 'Mother', 'Parent']));
      const pf = F.parentsFamily(p.id);
      if (pf && pf.marriage && (pf.marriage.date || pf.marriage.place)) fam.appendChild(el('p', { class: 'muted small', text: 'Married ' + eventLine(pf.marriage) }));
      group('Siblings', F.siblings(p.id), q => {
        const mine = F.birthYear(p), theirs = F.birthYear(q), kind = relLabel(q, ['brother', 'sister', 'sibling']);
        if (mine === null || theirs === null) return kind[0].toUpperCase() + kind.slice(1);
        return (theirs < mine ? 'Older ' : theirs > mine ? 'Younger ' : 'Twin ') + kind;
      });
      F.spouseFamilies(p.id).forEach(f => {
        const sp = F.get(f.husband === p.id ? f.wife : f.husband);
        fam.appendChild(el('h3', { text: sp ? relLabel(sp, ['Husband', 'Wife', 'Spouse']) : 'Partner' }));
        if (sp) fam.appendChild(A.personRow(sp, { compact: true }));
        const ml = eventLine(f.marriage); if (ml) fam.appendChild(el('p', { class: 'muted small', text: 'Married ' + ml }));
        const dl = eventLine(f.divorce); if (dl) fam.appendChild(el('p', { class: 'muted small', text: 'Divorced ' + dl }));
        const kids = F.sortByBirth(f.children.map(F.get).filter(Boolean));
        if (kids.length) { fam.appendChild(el('h3', { text: 'Children' + (sp ? ' with ' + F.firstName(sp) : '') })); kids.forEach(k => fam.appendChild(A.personRow(k, { compact: true, label: relLabel(k, ['Son', 'Daughter', 'Child']) }))); }
      });
      const gps = []; parents.forEach(q => F.parents(q.id).forEach(g => gps.push(g)));
      group('Grandparents', gps, q => relLabel(q, ['Grandfather', 'Grandmother', 'Grandparent']));
      if (fam.children.length === 1) fam.appendChild(el('p', { class: 'muted', text: 'No relatives recorded yet.' }));
      side.appendChild(fam);

      /* Relationship calculator */
      if (F.all().length > 1) {
        const sel = el('select', { 'aria-label': 'Compare with' });
        F.all().sort((x, y) => F.fullName(x).localeCompare(F.fullName(y))).forEach(q => { if (q.id !== p.id) sel.appendChild(el('option', { value: q.id, text: F.fullName(q) + (F.lifespan(q) ? ` (${F.lifespan(q)})` : '') })); });
        if (me && me.id !== p.id) sel.value = me.id;
        const out = el('p', { class: 'rel-out' });
        const upd = () => { out.textContent = F.relationshipSentence(sel.value, p.id); };
        sel.addEventListener('change', upd); upd();
        side.appendChild(el('section', { class: 'card' }, [el('h2', { html: icon('heart') + 'Relationship to…' }), sel, out]));
      }
    }
  };
})();
