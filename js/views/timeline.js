(function () {
  'use strict';
  const F = window.Family, A = window.App, el = A.el, icon = A.icon;
  const TYPES = [['birth', 'Births', 'baby'], ['marriage', 'Marriages', 'rings'], ['death', 'Deaths', 'cross'], ['residence', 'Moves', 'pin'], ['military', 'Military', 'military'], ['story', 'Stories', 'book'], ['event', 'Other', 'sparkle']];
  A.views.timeline = {
    title: () => 'Timeline',
    render(container, r) {
      const focus = r.id ? F.get(r.id) : null;
      const on = {}; TYPES.forEach(t => { on[t[0]] = true; });
      const filters = el('div', { class: 'chip-row' }, TYPES.map(t => el('button', { class: 'chip active', html: icon(t[2]) + t[1], onclick: e => { on[t[0]] = !on[t[0]]; e.currentTarget.classList.toggle('active', on[t[0]]); render(); } })));
      const box = el('div', { class: 'timeline' });
      container.appendChild(el('div', { class: 'wrap' }, [
        el('h1', { text: focus ? 'Timeline of ' + F.shortName(focus) : 'Timeline' }),
        focus ? el('p', { class: 'muted' }, [`Events in the life of ${F.fullName(focus)} and their immediate family. `, el('a', { href: '#/timeline', text: 'Show everyone' })]) : el('p', { class: 'muted', text: 'Every dated event in the family record, earliest first.' }),
        filters, box
      ]));
      const relevant = e => {
        if (!focus) return true;
        const ids = [focus.id].concat(F.parents(focus.id), F.siblings(focus.id), F.spouses(focus.id), F.children(focus.id)).map(x => typeof x === 'string' ? x : x.id);
        return e.people.some(p => ids.includes(p.id));
      };
      function render() {
        const evs = F.events().filter(e => on[e.type] && relevant(e));
        box.innerHTML = '';
        if (!evs.length) { box.appendChild(el('div', { class: 'empty', text: 'No events to show.' })); return; }
        let lastDecade = null;
        evs.forEach((e, i) => {
          const decade = Math.floor(F.year(e.date) / 10) * 10;
          if (decade !== lastDecade) { box.appendChild(el('h2', { class: 'decade', text: decade + 's' })); lastDecade = decade; }
          const names = e.people.map(p => el('a', { href: `#/person/${encodeURIComponent(p.id)}`, text: F.fullName(p) }));
          let title;
          if (e.type === 'birth') title = [names[0], ' is born'];
          else if (e.type === 'death') { const a = F.age(e.people[0]); title = [names[0], ' dies' + (a !== null ? `, aged ${a}` : '')]; }
          else if (e.type === 'marriage') title = names.length === 2 ? [names[0], ' marries ', names[1]] : [names[0], ' marries'];
          else if (e.type === 'story') title = [el('a', { href: `#/stories/${encodeURIComponent(e.story.id)}`, text: e.title })];
          else title = [e.title || e.type, names.length ? ': ' : '', names[0]];
          const t = TYPES.find(x => x[0] === e.type) || TYPES[6];
          box.appendChild(el('div', { class: 'tl-event tl-' + e.type, style: { '--i': Math.min(i, 20) } }, [
            el('div', { class: 'tl-dot', html: icon(t[2]) }),
            el('div', { class: 'tl-body' }, [
              el('div', { class: 'tl-date', text: F.formatDate(e.date) }),
              el('div', { class: 'tl-title' }, title),
              e.place ? el('div', { class: 'muted small', text: e.place }) : null,
              e.description ? el('div', { class: 'muted small', text: e.description }) : null
            ])
          ]));
        });
      }
      render();
    }
  };
})();
