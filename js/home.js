(function () {
  'use strict';
  var F = window.Family, U = window.UI, el = U.el;

  document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('home-title').textContent = F.title;
    document.getElementById('home-subtitle').textContent = F.subtitle;
    document.title = 'Home';

    var people = F.all();
    var years = people.map(F.birthYear).filter(function (y) { return y !== null; });
    var places = {};
    people.forEach(function (p) {
      ['birth', 'death'].forEach(function (k) {
        if (p[k] && p[k].place) places[p[k].place.split(',').pop().trim()] = true;
      });
    });
    var root = F.rootPerson();
    var gens = 0;
    if (root) {
      var anc = F.ancestorMap(root.id), desc = F.descendantMap(root.id);
      var up = Object.keys(anc).reduce(function (m, k) { return Math.max(m, anc[k]); }, 0);
      var down = Object.keys(desc).reduce(function (m, k) { return Math.max(m, desc[k]); }, 0);
      gens = up + down + 1;
    }
    var stats = [
      [people.length, 'People'], [F.families.length, 'Families'], [gens, 'Generations'],
      [F.surnames().length, 'Surnames'],
      [years.length ? Math.min.apply(null, years) + '–' + Math.max.apply(null, years) : '—', 'Years spanned'],
      [Object.keys(places).length, 'Countries / regions']
    ];
    var statsEl = document.getElementById('stats');
    stats.forEach(function (s) { statsEl.appendChild(el('div', { class: 'stat' }, [el('b', { class: String(s[0]).length > 5 ? 'long' : '', text: s[0] }), el('span', { text: s[1] })])); });

    // Start-here mini pedigree: root, parents, grandparents
    var sh = document.getElementById('start-here');
    if (root) {
      var col1 = el('div', { class: 'col' }, [U.personCard(root, { label: 'Home person' })]);
      var par = [F.father(root.id), F.mother(root.id)];
      var col2 = el('div', { class: 'col' }, par.map(function (p, i) {
        return p ? U.personCard(p, { label: i === 0 ? 'Father' : 'Mother' }) : el('div', { class: 'empty', text: 'Unknown' });
      }));
      var col3 = el('div', { class: 'col' }, []);
      par.forEach(function (p) {
        if (!p) { col3.appendChild(el('div', { class: 'empty', text: 'Unknown' })); col3.appendChild(el('div', { class: 'empty', text: 'Unknown' })); return; }
        [F.father(p.id), F.mother(p.id)].forEach(function (g, i) {
          col3.appendChild(g ? U.personCard(g, { label: 'Grand' + (i === 0 ? 'father' : 'mother'), compact: true }) : el('div', { class: 'empty', text: 'Unknown' }));
        });
      });
      sh.appendChild(col1); sh.appendChild(col2); sh.appendChild(col3);
    } else {
      sh.appendChild(el('div', { class: 'empty-state', text: 'Add people to data/family.js to get started.' }));
    }

    // Stories
    var st = document.getElementById('home-stories');
    if (!F.stories.length) st.appendChild(el('p', { class: 'muted', text: 'No stories yet.' }));
    F.stories.slice(0, 3).forEach(function (s) {
      st.appendChild(el('article', { class: 'story-teaser' }, [
        el('div', { class: 'date', text: s.date || '' }),
        el('h3', {}, [el('a', { href: 'stories.html#' + encodeURIComponent(s.id), text: s.title })]),
        el('p', { class: 'muted', text: (s.body || '').slice(0, 180).replace(/\s+\S*$/, '') + '…' })
      ]));
    });

    // Earliest ancestors: people with no recorded parents, oldest first
    var earliest = people.filter(function (p) { return !F.parents(p.id).length && F.birthYear(p) !== null; });
    earliest = F.sortByBirth(earliest).slice(0, 5);
    var ea = document.getElementById('earliest');
    earliest.forEach(function (p) { ea.appendChild(U.personCard(p, { compact: true })); });

    // Surnames
    var sn = document.getElementById('surnames');
    F.surnames().forEach(function (s) {
      sn.appendChild(el('a', { class: 'chip', href: 'people.html?surname=' + encodeURIComponent(s.name), text: s.name + ' (' + s.count + ')' }));
    });
  });
})();
