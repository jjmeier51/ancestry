/* Person profile view. */
(function () {
  'use strict';
  const F = window.Family, A = window.App, el = A.el, icon = A.icon, esc = A.esc;

  const eventLine = ev => ev ? [ev.date ? F.formatDate(ev.date) : '', ev.place || ''].filter(Boolean).join(' · ') : '';
  const eventNode = ev => { const out = []; if (ev && ev.date) out.push(F.formatDate(ev.date)); if (ev && ev.place) { if (out.length) out.push(' · '); out.push(A.placeLink(ev.place)); } return out; };
  const paragraphs = text => String(text || '').split(/\n+/).map(t => t.trim()).filter(Boolean).map(t => el('p', { html: A.md(t) }));
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
      const a = (F.isDeceased(p) || (p.birth && F.parseDate(p.birth.date) && F.parseDate(p.birth.date).month)) ? F.age(p) : null;
      const tags = F.tags(p);

      /* Hero */
      const hero = el('header', { class: 'hero' }, [
        photo ? el('div', { class: 'hero-bg', style: { backgroundImage: `url("${photo}")` } }) : null,
        el('div', { class: 'hero-inner' }, [
          A.avatar(p, 'xl'),
          el('div', { class: 'hero-text' }, [
            el('h1', { text: F.fullName(p) }),
            p.nickname ? el('div', { class: 'nick', text: '“' + p.nickname + '”' }) : null,
            p.aka && p.aka.length ? el('div', { class: 'nick', text: 'Also recorded as ' + p.aka.join(', ') }) : null,
            el('div', { class: 'hero-meta', text: [F.lifespan(p), a !== null ? (F.isDeceased(p) ? `died aged ${a}` : `age ${a}`) : '', p.occupation].filter(Boolean).join(' · ') }),
            el('div', { class: 'hero-badges' }, [A.confBadge(p, true)].concat(tags.map(t => el('span', { class: 'tag', html: icon(A.tagIcon(t)) + esc(A.tagLabel(t)) })))),
            me ? el('p', { class: 'hero-rel', html: icon('heart') + esc(F.relationshipSentence(me.id, p.id)) }) : null,
            el('div', { class: 'hero-actions' }, [
              el('a', { class: 'btn primary', href: `#/tree/${encodeURIComponent(p.id)}`, html: icon('tree') + 'View tree' }),
              el('a', { class: 'btn', href: `#/timeline/${encodeURIComponent(p.id)}`, html: icon('clock') + 'Timeline' }),
              el('button', { class: 'btn', html: icon('share') + 'Share', onclick: () => {
                /* share the preview page, which carries the person's name, dates and card for Messages etc. */
                const url = `${location.origin}/p/${encodeURIComponent(p.id)}`;
                if (navigator.share) navigator.share({ title: F.fullName(p), text: p.summary || '', url }).catch(() => {});
                else if (navigator.clipboard) navigator.clipboard.writeText(url).then(() => A.toast('Link copied'), () => prompt('Copy this link', url));
                else prompt('Copy this link', url);
              } })
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
          p.summary ? el('p', { class: 'lead', html: A.md(p.summary) }) : null
        ].concat(paragraphs(p.bio), p.notes && p.notes !== p.bio ? [el('details', {}, [el('summary', { text: 'Notes from the family tree file' })].concat(paragraphs(p.notes)))] : [])));
      }

      /* Key facts */
      const facts = [];
      const fact = (label, value) => { if (value) facts.push(el('div', { class: 'fact' }, [el('dt', { text: label }), Array.isArray(value) ? el('dd', {}, value) : el('dd', { html: A.md(value) })])); };
      if (p.birth && (p.birth.date || p.birth.place)) fact('Born', eventNode(p.birth).concat(p.birthDateReduced ? [' (full date withheld for a living person)'] : [])); if (p.death && (p.death.date || p.death.place)) fact('Died', eventNode(p.death)); if (p.burial && (p.burial.date || p.burial.place)) fact('Buried', eventNode(p.burial));
      fact('Occupation', p.occupation); fact('Religion', p.religion); fact('Education', p.education);
      (p.facts || []).forEach(f => fact(f.label, f.value));
      (p.events || []).forEach(e => { const parts = []; if (e.date) parts.push(F.formatDate(e.date)); if (e.place) { if (parts.length) parts.push(' · '); parts.push(A.placeLink(e.place)); } if (e.description) { if (parts.length) parts.push(' · '); parts.push(el('span', { html: A.md(e.description) })); } fact(e.title || 'Event', parts); });
      if (facts.length) main.appendChild(section('Life', 'info', [el('dl', { class: 'facts' }, facts)]));

      /* Places lived */
      const places = [];
      if (p.birth && p.birth.place) places.push({ date: p.birth.date, place: p.birth.place, what: 'Born' });
      (p.residences || []).forEach(rs => places.push({ date: rs.date, place: rs.place, what: rs.note || 'Lived' }));
      if (p.death && p.death.place) places.push({ date: p.death.date, place: p.death.place, what: 'Died' });
      if (places.length) main.appendChild(section('Places', 'pin', [el('ol', { class: 'places' }, places.map(pl => el('li', {}, [
        el('span', { class: 'place-when', text: pl.date ? F.formatDate(pl.date, true) : '' }),
        el('span', { class: 'place-what', text: pl.what }),
        el('span', { class: 'place-where' }, [A.placeLink(pl.place)])
      ])))]));

      /* Military */
      if (p.military && p.military.length) main.appendChild(section('Military service', 'military', p.military.map(m => el('div', { class: 'military' }, [
        el('b', { text: [m.branch, m.service].filter(Boolean).join(' · ') }),
        el('div', { class: 'muted', text: [m.rank, m.unit, m.theatre].filter(Boolean).join(' · ') }),
        m.note ? el('p', { html: A.md(m.note) }) : null
      ]))));

      /* Notable & fun facts */
      if (p.notable) main.appendChild(section('Noteworthy', 'star', paragraphs(p.notable)));
      if (p.funFacts && p.funFacts.length) main.appendChild(section('Fun facts', 'sparkle', [el('ul', { class: 'fun' }, p.funFacts.map(f => el('li', { html: A.md(f) })))]));

      /* Stories */
      const stories = F.storiesFor(p.id);
      if (stories.length) main.appendChild(section('Stories', 'book', stories.map(s => el('a', { class: 'story-teaser', href: `#/stories/${encodeURIComponent(s.id)}` }, [
        el('span', { class: 'story-date', text: s.date || '' }), el('b', { text: s.title }),
        el('span', { class: 'muted', text: (s.body || '').replace(/\*\*/g, '').slice(0, 160).replace(/\s+\S*$/, '') + '…' })
      ]))));

      /* Media */
      const media = F.mediaFor(p.id);
      if (media.length) {
        const images = media.filter(m => m.file && /\.(jpe?g|png|gif|webp|svg)$/i.test(m.file));
        main.appendChild(section(`Media & documents (${media.length})`, 'image', [el('div', { class: 'media-grid' }, media.map(m => mediaCard(m, images)))]));
      }

      /* Records on Ancestry (citations from the GEDCOM) and media not yet downloaded */
      const cites = p.citations || [];
      if (cites.length) {
        const groups = {};
        cites.forEach(c => { (groups[c.source] = groups[c.source] || []).push(c); });
        main.appendChild(section(`Records (${cites.length})`, 'doc', [el('ul', { class: 'records' }, Object.keys(groups).map(src => el('li', {}, [
          el('b', { text: src }),
          el('ul', {}, groups[src].filter(c => c.page).map(c => el('li', { class: 'muted small', text: c.page })))
        ])))], 'records-card'));
      }
      const am = p.ancestryMedia || [];
      if (am.length) {
        main.appendChild(section(`On Ancestry, not yet downloaded (${am.length})`, 'image', [
          el('p', { class: 'muted small', text: 'These items are attached to this person in the Ancestry tree. The export does not include the files; once they are copied into the media folder they will appear in Media & documents.' }),
          el('ul', { class: 'fun' }, am.map(m => el('li', { text: [m.title || 'Untitled', m.kind, m.form].filter(Boolean).join(' · ') + (m.primary ? ' (profile photo)' : '') })))
        ]));
      }

      /* Sources & research */
      const log = p.researchLog || [];
      const researchCard = el('section', { class: 'card research conf-' + conf }, [
        el('h2', { html: icon('check') + 'Research status' }),
        el('div', { class: 'research-conf' }, [A.confBadge(p, true), el('span', { class: 'muted', text: F.confidenceDescription(conf) })]),
        p.link && p.link.note ? el('p', { html: A.md(p.link.note) }) : null,
        p.corrections && p.corrections.length ? el('div', { class: 'correction' }, [el('h3', { text: 'Corrected from the Ancestry tree' })].concat(p.corrections.map(c => el('p', { class: 'small', html: (c.what === 'parents' ? 'Parents changed. ' : '') + A.md(c.reason || '') })))) : null,
        p.source === 'research' ? el('p', { class: 'muted small', text: 'Added by research; this person is not in the Ancestry GEDCOM.' }) : null,
        p.mergedFrom && p.mergedFrom.length ? el('div', { class: 'correction' }, [el('h3', { text: 'Merged duplicate records' })].concat(p.mergedFrom.map(m => el('p', { class: 'small', html: A.md(`The separate record "${m.name}" was the same person. ${m.reason || ''}`) })))) : null,
        p.conflicts && p.conflicts.length ? el('div', {}, [el('h3', { text: 'Conflicting evidence' }), el('ul', { class: 'sources' }, p.conflicts.map(c => el('li', { html: A.md(`**${c.field}**: tree says “${c.site || '—'}”, records say “${c.found || '—'}”. ${c.assessment || ''}`) })))]) : null,
        p.researchNotes ? el('details', { class: 'research-notes' }, [el('summary', { text: 'Evidence notes (research detail)' })].concat(p.researchNotes.split(/\n\s*\n/).map(t => el('p', { class: 'small', html: A.md(t) })))) : null,
        p.openQuestions && p.openQuestions.length ? el('div', {}, [el('h3', { text: 'Open questions' }), el('ul', { class: 'sources' }, p.openQuestions.map(q => el('li', { html: A.md(q) })))]) : null,
        p.mediaKnown && p.mediaKnown.length ? el('div', {}, [el('h3', { text: 'Known media not yet attached' }), el('ul', { class: 'sources' }, p.mediaKnown.map(q => el('li', { html: A.md(q) })))]) : null,
        p.sources && p.sources.length ? el('div', {}, [el('h3', { text: 'Sources' }), el('ul', { class: 'sources' }, p.sources.map(s => el('li', { html: A.md(s) })))]) : null,
        log.length ? el('div', {}, [el('h3', { text: 'Research log' }), el('ul', { class: 'log' }, log.slice().reverse().map(e => el('li', {}, [el('time', { text: e.date || '' }), ' ', el('span', { html: A.md(e.note || '') })])))]) : null,
        !log.length && !(p.sources && p.sources.length) ? el('p', { class: 'muted', text: 'No research recorded yet.' }) : null
      ]);

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
      if (pf && pf.marriage && (pf.marriage.date || pf.marriage.place)) fam.appendChild(el('p', { class: 'muted small' }, ['Married '].concat(eventNode(pf.marriage))));
      group('Siblings', F.siblings(p.id), q => {
        const mine = F.birthYear(p), theirs = F.birthYear(q), kind = relLabel(q, ['brother', 'sister', 'sibling']);
        if (mine === null || theirs === null) return kind[0].toUpperCase() + kind.slice(1);
        return (theirs < mine ? 'Older ' : theirs > mine ? 'Younger ' : 'Twin ') + kind;
      });
      F.spouseFamilies(p.id).forEach(f => {
        const sp = F.get(f.husband === p.id ? f.wife : f.husband);
        fam.appendChild(el('h3', { text: sp ? (f.status === 'engaged' ? relLabel(sp, ['Fiancé', 'Fiancée', 'Fiancé(e)']) : f.status === 'partner' ? 'Partner' : f.status === 'divorced' ? relLabel(sp, ['Former husband', 'Former wife', 'Former spouse']) : relLabel(sp, ['Husband', 'Wife', 'Spouse'])) : 'Partner' }));
        if (sp) fam.appendChild(A.personRow(sp, { compact: true }));
        if (f.marriage && (f.marriage.date || f.marriage.place)) fam.appendChild(el('p', { class: 'muted small' }, ['Married '].concat(eventNode(f.marriage))));
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

      /* Research status: the last thing on the page */
      container.appendChild(el('div', { class: 'wrap profile-foot' }, [researchCard]));
    }
  };
})();
