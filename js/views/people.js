(function () {
  'use strict';
  const F = window.Family, A = window.App, el = A.el, icon = A.icon;
  A.views.people = {
    title: () => 'People',
    render(container, r) {
      const q = el('input', { type: 'search', placeholder: 'Filter by name, place, year or tag', 'aria-label': 'Filter people', value: r.params.q || '' });
      const surname = el('select', { 'aria-label': 'Surname' }, [el('option', { value: '', text: 'All surnames' })].concat(F.surnames().map(s => el('option', { value: s.name, text: `${s.name} (${s.count})` }))));
      const conf = el('select', { 'aria-label': 'Confidence' }, [el('option', { value: '', text: 'Any confidence' })].concat(Object.keys(F.confidenceLevels).map(k => el('option', { value: k, text: F.confidenceLabel(k) }))));
      const sort = el('select', { 'aria-label': 'Sort' }, [['surname', 'By surname'], ['given', 'By first name'], ['birth', 'By birth year'], ['confidence', 'By confidence']].map(o => el('option', { value: o[0], text: o[1] })));
      surname.value = r.params.surname || ''; conf.value = r.params.conf || ''; sort.value = r.params.sort || 'surname';
      const tagRow = el('div', { class: 'chip-row' });
      let activeTag = r.params.tag || '';
      const tags = F.allTags();
      tags.forEach(t => tagRow.appendChild(el('button', { class: 'chip' + (activeTag === t.name ? ' active' : ''), 'data-tag': t.name, html: icon(A.tagIcon(t.name)) + A.esc(A.tagLabel(t.name)) + ` <small>${t.count}</small>`, onclick: () => { activeTag = activeTag === t.name ? '' : t.name; tagRow.querySelectorAll('.chip').forEach(c => c.classList.toggle('active', c.dataset.tag === activeTag)); render(); } })));
      const count = el('span', { class: 'count' });
      const list = el('div', { class: 'people-list' });
      container.appendChild(el('div', { class: 'wrap' }, [
        el('h1', { text: 'People' }),
        el('div', { class: 'toolbar' }, [el('div', { class: 'input-wrap', html: icon('search') }, [q]), surname, conf, sort, count]),
        tags.length ? tagRow : null, list
      ]));
      const CONF_ORDER = { confirmed: 0, probable: 1, possible: 2, unverified: 3 };
      function render() {
        let people = q.value.trim() ? F.search(q.value) : F.all();
        if (surname.value) people = people.filter(p => (p.surname || '(unknown)') === surname.value);
        if (conf.value) people = people.filter(p => F.confidence(p) === conf.value);
        if (activeTag) people = people.filter(p => F.tags(p).includes(activeTag));
        const mode = sort.value;
        people.sort((a, b) => mode === 'birth' ? F.sortKey(a.birth && a.birth.date) - F.sortKey(b.birth && b.birth.date)
          : mode === 'given' ? (a.given || '').localeCompare(b.given || '') || (a.surname || '').localeCompare(b.surname || '')
          : mode === 'confidence' ? CONF_ORDER[F.confidence(a)] - CONF_ORDER[F.confidence(b)] || F.fullName(a).localeCompare(F.fullName(b))
          : (a.surname || '').localeCompare(b.surname || '') || (a.given || '').localeCompare(b.given || ''));
        count.textContent = `${people.length} of ${F.all().length}`;
        list.innerHTML = '';
        if (!people.length) { list.appendChild(el('div', { class: 'empty', text: 'No one matches that filter.' })); return; }
        const groups = {}, order = [];
        people.forEach(p => {
          const key = mode === 'birth' ? (F.birthYear(p) === null ? 'Unknown' : Math.floor(F.birthYear(p) / 10) * 10 + 's')
            : mode === 'confidence' ? F.confidenceLabel(F.confidence(p))
            : ((mode === 'given' ? p.given : p.surname) || '?')[0].toUpperCase();
          if (!groups[key]) { groups[key] = []; order.push(key); }
          groups[key].push(p);
        });
        order.forEach(k => {
          list.appendChild(el('h2', { class: 'group-head', text: k }));
          const g = el('div', { class: 'row-list' });
          groups[k].forEach(p => g.appendChild(A.personRow(p)));
          list.appendChild(g);
        });
        const params = [];
        if (q.value) params.push('q=' + encodeURIComponent(q.value));
        if (surname.value) params.push('surname=' + encodeURIComponent(surname.value));
        if (conf.value) params.push('conf=' + conf.value);
        if (activeTag) params.push('tag=' + encodeURIComponent(activeTag));
        if (mode !== 'surname') params.push('sort=' + mode);
        history.replaceState(null, '', '#/people' + (params.length ? '?' + params.join('&') : ''));
      }
      [q, surname, conf, sort].forEach(x => x.addEventListener('input', render));
      render();
      return { update: nr => nr.name === 'people' && nr.hash === location.hash };
    }
  };
})();
