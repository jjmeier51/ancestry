(function () {
  'use strict';
  var F = window.Family, U = window.UI, el = U.el;

  document.addEventListener('DOMContentLoaded', function () {
    var q = document.getElementById('people-q');
    var sel = document.getElementById('people-surname');
    var sort = document.getElementById('people-sort');
    var list = document.getElementById('people-list');
    var count = document.getElementById('people-count');

    F.surnames().forEach(function (s) { sel.appendChild(el('option', { value: s.name, text: s.name + ' (' + s.count + ')' })); });
    q.value = U.param('q') || '';
    sel.value = U.param('surname') || '';
    sort.value = U.param('sort') || 'surname';

    function render() {
      var people = q.value.trim() ? F.search(q.value) : F.all();
      if (sel.value) people = people.filter(function (p) { return (p.surname || '(unknown)') === sel.value; });
      var mode = sort.value;
      people.sort(function (a, b) {
        if (mode === 'birth') return F.sortKey(a.birth && a.birth.date) - F.sortKey(b.birth && b.birth.date);
        if (mode === 'given') return (a.given || '').localeCompare(b.given || '') || (a.surname || '').localeCompare(b.surname || '');
        return (a.surname || '').localeCompare(b.surname || '') || (a.given || '').localeCompare(b.given || '');
      });
      count.textContent = people.length + ' of ' + F.all().length + ' people';
      list.innerHTML = '';
      if (!people.length) { list.appendChild(el('div', { class: 'empty-state', text: 'No one matches that filter.' })); return; }

      var groups = {}, order = [];
      people.forEach(function (p) {
        var key = mode === 'birth' ? (F.birthYear(p) === null ? 'Unknown' : Math.floor(F.birthYear(p) / 10) * 10 + 's')
          : ((mode === 'given' ? p.given : p.surname) || '?')[0].toUpperCase();
        if (!groups[key]) { groups[key] = []; order.push(key); }
        groups[key].push(p);
      });
      order.forEach(function (k) {
        list.appendChild(el('h2', { class: 'letter-head', text: k }));
        var grid = el('div', { class: 'card-grid' });
        groups[k].forEach(function (p) { grid.appendChild(U.personCard(p)); });
        list.appendChild(grid);
      });
      var params = [];
      if (q.value) params.push('q=' + encodeURIComponent(q.value));
      if (sel.value) params.push('surname=' + encodeURIComponent(sel.value));
      if (mode !== 'surname') params.push('sort=' + mode);
      history.replaceState(null, '', 'people.html' + (params.length ? '?' + params.join('&') : ''));
    }
    q.addEventListener('input', render);
    sel.addEventListener('change', render);
    sort.addEventListener('change', render);
    render();
  });
})();
