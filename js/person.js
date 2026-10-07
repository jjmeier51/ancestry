(function () {
  'use strict';
  var F = window.Family, U = window.UI, el = U.el;

  function paragraphs(text) {
    return String(text || '').split(/\n+/).map(function (t) { return el('p', { text: t.trim() }); });
  }
  function eventLine(ev) {
    if (!ev) return null;
    var bits = [];
    if (ev.date) bits.push(F.formatDate(ev.date));
    if (ev.place) bits.push(ev.place);
    return bits.join(' · ') || null;
  }

  document.addEventListener('DOMContentLoaded', function () {
    var page = document.getElementById('person-page');
    var id = U.param('id');
    var p = id ? F.get(id) : null;
    if (!p) {
      document.title = 'Person not found';
      page.appendChild(el('div', { class: 'empty-state', style: 'margin-top:40px' }, [
        el('h1', { text: 'Person not found' }),
        el('p', {}, ['No one with that id is in the family file. ', el('a', { href: 'people.html', text: 'Browse all people' }), '.'])
      ]));
      return;
    }
    document.title = F.fullName(p);

    /* ---- Hero ---- */
    var tags = [];
    if (p.occupation) tags.push(p.occupation);
    if (p.nickname) tags.push('“' + p.nickname + '”');
    var a = F.age(p);
    if (a !== null) tags.push(F.isDeceased(p) ? 'Died aged ' + a : 'Age ' + a);
    var hero = el('section', { class: 'person-hero' }, [
      U.avatar(p, 'xl'),
      el('div', {}, [
        el('p', { class: 'eyebrow', text: p.surname ? p.surname + ' family' : 'Family member' }),
        el('h1', { text: F.fullName(p) }),
        el('div', { class: 'life', text: F.lifespan(p) }),
        el('div', { class: 'tags' }, tags.map(function (t) { return el('span', { class: 'chip', text: t }); })),
        el('div', { style: 'margin-top:14px;display:flex;gap:8px;flex-wrap:wrap' }, [
          el('a', { class: 'btn small', href: 'tree.html?id=' + encodeURIComponent(p.id) + '&view=ancestors', text: 'Ancestors chart' }),
          el('a', { class: 'btn small ghost', href: 'tree.html?id=' + encodeURIComponent(p.id) + '&view=descendants', text: 'Descendants chart' }),
          el('a', { class: 'btn small ghost', href: 'timeline.html?id=' + encodeURIComponent(p.id), text: 'Timeline' })
        ])
      ])
    ]);
    page.appendChild(hero);

    var layout = el('div', { class: 'person-layout' });
    var mainCol = el('div'), side = el('div');
    layout.appendChild(mainCol); layout.appendChild(side);
    page.appendChild(layout);

    /* ---- Relationship to home person ---- */
    var root = F.rootPerson();
    if (root && root.id !== p.id) {
      var relText = el('strong');
      var sel = el('select', { 'aria-label': 'Compare with' });
      F.all().sort(function (x, y) { return F.fullName(x).localeCompare(F.fullName(y)); }).forEach(function (q) {
        if (q.id !== p.id) sel.appendChild(el('option', { value: q.id, text: F.fullName(q) + (F.lifespan(q) ? ' (' + F.lifespan(q) + ')' : '') }));
      });
      sel.value = root.id;
      function updateRel() {
        var other = F.get(sel.value);
        var r = F.relationship(other.id, p.id);
        relText.textContent = F.shortName(p) + ' is ' + (r === 'no known blood relation' ? 'of ' + r + ' to' : (/^(\d|[aeiou])/i.test(r) ? 'the ' : 'the ') + r + ' of') + ' ' + F.shortName(other) + '.';
      }
      sel.addEventListener('change', updateRel);
      updateRel();
      mainCol.appendChild(el('div', { class: 'relationship-box' }, [
        el('div', { style: 'display:flex;gap:10px;align-items:center;flex-wrap:wrap' }, ['Relationship to ', sel]),
        el('div', { style: 'margin-top:6px' }, [relText])
      ]));
    }

    /* ---- Facts ---- */
    var facts = el('dl', { class: 'facts' });
    function fact(label, value) { if (value) { facts.appendChild(el('dt', { text: label })); facts.appendChild(el('dd', { text: value })); } }
    fact('Born', eventLine(p.birth));
    fact('Died', eventLine(p.death));
    if (p.burial) fact('Buried', eventLine(p.burial));
    fact('Occupation', p.occupation);
    fact('Religion', p.religion);
    fact('Education', p.education);
    (p.facts || []).forEach(function (f) { fact(f.label, f.value); });
    if (p.sources && p.sources.length) fact('Sources', p.sources.join('; '));
    if (facts.children.length) mainCol.appendChild(el('div', { class: 'panel' }, [el('h2', { text: 'Life' }), facts]));

    if (p.bio) mainCol.appendChild(el('div', { class: 'panel bio' }, [el('h2', { text: 'About' })].concat(paragraphs(p.bio))));

    /* ---- Timeline of own events ---- */
    var evs = F.events().filter(function (e) { return e.people.some(function (q) { return q.id === p.id; }); });
    if (evs.length > 1) {
      var ul = el('div', { class: 'timeline', style: 'margin:10px 0 0' });
      evs.forEach(function (e) {
        var who = e.people.filter(function (q) { return q.id !== p.id; }).map(F.shortName).join(' & ');
        var label = e.type === 'birth' ? 'Born' : e.type === 'death' ? 'Died' : e.type === 'marriage' ? 'Married ' + who : e.title || e.type;
        ul.appendChild(el('div', { class: 'tl-event tl-' + e.type }, [
          el('div', { class: 'tl-date', text: F.formatDate(e.date) }),
          el('div', { class: 'tl-body' }, [
            el('div', {}, [e.story ? el('a', { href: 'stories.html#' + encodeURIComponent(e.story.id), text: label }) : label]),
            e.place ? el('div', { class: 'tl-place', text: e.place }) : null
          ])
        ]));
      });
      mainCol.appendChild(el('div', { class: 'panel' }, [el('h2', { text: 'Events' }), ul]));
    }

    /* ---- Stories & photos ---- */
    var stories = F.storiesFor(p.id);
    if (stories.length) {
      mainCol.appendChild(el('div', { class: 'panel' }, [el('h2', { text: 'Stories' })].concat(stories.map(function (s) {
        return el('article', { class: 'story-teaser' }, [
          el('div', { class: 'date', text: s.date || '' }),
          el('h3', {}, [el('a', { href: 'stories.html#' + encodeURIComponent(s.id), text: s.title })]),
          el('p', { class: 'muted', text: (s.body || '').slice(0, 220).replace(/\s+\S*$/, '') + '…' })
        ]);
      }))));
    }
    var photos = F.photosFor(p.id);
    if (photos.length) {
      mainCol.appendChild(el('div', { class: 'panel' }, [el('h2', { text: 'Photos' }), el('div', { class: 'photo-strip' }, photos.map(function (ph) {
        return el('figure', {}, [
          el('a', { href: 'gallery.html?id=' + encodeURIComponent(p.id) }, [el('img', { src: ph.src, alt: ph.caption || '', loading: 'lazy' })]),
          el('figcaption', { text: ph.caption || '' })
        ]);
      }))]));
    }

    /* ---- Family sidebar ---- */
    var fam = el('div', { class: 'panel' }, [el('h2', { text: 'Family' })]);
    function group(title, items, labelFn) {
      if (!items.length) return;
      var g = el('div', { class: 'rel-group' }, [el('h3', { text: title })]);
      var list = el('div', { class: 'rel-list' });
      items.forEach(function (q, i) { list.appendChild(U.personCard(q, { compact: true, label: labelFn ? labelFn(q, i) : null })); });
      g.appendChild(list);
      fam.appendChild(g);
    }
    var parents = F.parents(p.id);
    group('Parents', parents, function (q) { return q.sex === 'M' ? 'Father' : q.sex === 'F' ? 'Mother' : 'Parent'; });
    var pf = F.parentsFamily(p.id);
    if (pf && pf.marriage && (pf.marriage.date || pf.marriage.place)) {
      fam.appendChild(el('p', { class: 'marriage-note', style: 'margin-left:0;margin-top:-10px', text: 'Married ' + eventLine(pf.marriage) }));
    }
    group('Siblings', F.siblings(p.id), function (q) {
      var mine = F.birthYear(p), theirs = F.birthYear(q);
      var kind = q.sex === 'M' ? 'brother' : q.sex === 'F' ? 'sister' : 'sibling';
      if (mine === null || theirs === null) return kind.charAt(0).toUpperCase() + kind.slice(1);
      return (theirs < mine ? 'Older ' : theirs > mine ? 'Younger ' : 'Twin ') + kind;
    });

    var spouseFams = F.spouseFamilies(p.id);
    if (spouseFams.length) {
      var g = el('div', { class: 'rel-group' }, [el('h3', { text: spouseFams.length > 1 ? 'Marriages & children' : 'Spouse & children' })]);
      spouseFams.forEach(function (f) {
        var sp = F.get(f.husband === p.id ? f.wife : f.husband);
        var list = el('div', { class: 'rel-list' });
        if (sp) list.appendChild(U.personCard(sp, { compact: true, label: sp.sex === 'M' ? 'Husband' : sp.sex === 'F' ? 'Wife' : 'Spouse' }));
        g.appendChild(list);
        var ml = eventLine(f.marriage);
        if (ml) g.appendChild(el('p', { class: 'marriage-note', text: 'Married ' + ml }));
        var kids = F.sortByBirth(f.children.map(F.get).filter(Boolean));
        if (kids.length) {
          var kl = el('div', { class: 'rel-list', style: 'margin:4px 0 14px 24px' });
          kids.forEach(function (k) { kl.appendChild(U.personCard(k, { compact: true, label: k.sex === 'M' ? 'Son' : k.sex === 'F' ? 'Daughter' : 'Child' })); });
          g.appendChild(kl);
        }
      });
      fam.appendChild(g);
    }
    if (fam.children.length === 1) fam.appendChild(el('p', { class: 'muted', text: 'No relatives recorded yet.' }));
    side.appendChild(fam);

    // Grandparents quick view
    var gps = [];
    parents.forEach(function (q) { F.parents(q.id).forEach(function (g) { gps.push(g); }); });
    if (gps.length) {
      var gp = el('div', { class: 'panel' }, [el('h2', { text: 'Grandparents' })]);
      var gl = el('div', { class: 'rel-list' });
      gps.forEach(function (g) { gl.appendChild(U.personCard(g, { compact: true })); });
      gp.appendChild(gl);
      side.appendChild(gp);
    }
  });
})();
