(function () {
  'use strict';
  var F = window.Family, U = window.UI, el = U.el;

  document.addEventListener('DOMContentLoaded', function () {
    var id = U.param('id');
    var focus = id ? F.get(id) : null;
    var box = document.getElementById('timeline');
    var intro = document.getElementById('timeline-intro');
    var filters = document.getElementById('timeline-filters');

    if (focus) {
      intro.innerHTML = '';
      intro.appendChild(el('span', {}, ['Events in the life of ', el('a', { href: U.personUrl(focus), text: F.fullName(focus) }), ' and their immediate family. ', el('a', { href: 'timeline.html', text: 'Show everyone' })]));
    } else {
      intro.textContent = 'Every dated event in the family record, from the earliest birth to the present day.';
    }

    function relevant(e) {
      if (!focus) return true;
      var ids = [focus.id].concat(F.parents(focus.id), F.siblings(focus.id), F.spouses(focus.id), F.children(focus.id)).map(function (x) { return typeof x === 'string' ? x : x.id; });
      return e.people.some(function (p) { return ids.indexOf(p.id) >= 0; });
    }

    function render() {
      var on = {};
      filters.querySelectorAll('input').forEach(function (i) { on[i.value] = i.checked; });
      var evs = F.events().filter(function (e) { return (on[e.type] !== undefined ? on[e.type] : on.event) && relevant(e); });
      box.innerHTML = '';
      if (!evs.length) { box.appendChild(el('div', { class: 'empty-state', text: 'No events to show.' })); return; }
      var lastDecade = null;
      evs.forEach(function (e) {
        var y = F.year(e.date);
        var decade = Math.floor(y / 10) * 10;
        if (decade !== lastDecade) { box.appendChild(el('h2', { class: 'decade', text: decade + 's' })); lastDecade = decade; }
        var names = e.people.map(function (p) { return el('a', { href: U.personUrl(p), text: F.fullName(p) }); });
        var title;
        if (e.type === 'birth') title = [names[0], ' is born'];
        else if (e.type === 'death') { var a = F.age(e.people[0]); title = [names[0], ' dies' + (a !== null ? ', aged ' + a : '')]; }
        else if (e.type === 'marriage') title = names.length === 2 ? [names[0], ' marries ', names[1]] : [names[0], ' marries'];
        else if (e.type === 'story') title = [el('a', { href: 'stories.html#' + encodeURIComponent(e.story.id), text: e.title })];
        else title = [e.title || e.type, names.length ? ' — ' : '', names[0]];
        box.appendChild(el('div', { class: 'tl-event tl-' + e.type }, [
          el('div', { class: 'tl-date', text: F.formatDate(e.date) }),
          el('div', { class: 'tl-body' }, [
            el('div', { class: 'tl-type', text: e.type }),
            el('div', {}, title),
            e.place ? el('div', { class: 'tl-place', text: e.place }) : null,
            e.description ? el('div', { class: 'muted', text: e.description }) : null
          ])
        ]));
      });
    }
    filters.addEventListener('change', render);
    render();
  });
})();
