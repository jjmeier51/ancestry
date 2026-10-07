(function () {
  'use strict';
  var F = window.Family, U = window.UI, el = U.el;

  document.addEventListener('DOMContentLoaded', function () {
    var box = document.getElementById('stories');
    document.getElementById('stories-intro').textContent = F.stories.length
      ? F.stories.length + ' stories passed down through the family.'
      : 'Add stories to the "stories" list in data/family.js to see them here.';
    if (!F.stories.length) { box.appendChild(el('div', { class: 'empty-state', text: 'No stories yet.' })); return; }
    F.stories.forEach(function (s) {
      var people = (s.people || []).map(F.get).filter(Boolean);
      var body = el('div', { class: 'body' });
      String(s.body || '').split(/\n+/).forEach(function (t) { body.appendChild(el('p', { text: t.trim() })); });
      box.appendChild(el('article', { class: 'story', id: s.id }, [
        el('h2', { text: s.title }),
        s.date ? el('span', { class: 'date', text: s.date }) : null,
        body,
        s.image ? el('img', { src: s.image, alt: s.title, style: 'border-radius:8px;margin-top:12px' }) : null,
        people.length ? el('div', { class: 'people' }, [el('span', { class: 'muted', text: 'People: ' })].concat(people.map(function (p) {
          return el('a', { href: U.personUrl(p) }, [U.avatar(p, 'xs'), F.fullName(p)]);
        }))) : null
      ]));
    });
    if (location.hash) {
      var t = document.getElementById(decodeURIComponent(location.hash.slice(1)));
      if (t) { t.scrollIntoView(); t.style.borderColor = 'var(--gold)'; }
    }
  });
})();
