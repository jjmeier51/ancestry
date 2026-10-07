(function () {
  'use strict';
  var F = window.Family, U = window.UI, el = U.el;

  document.addEventListener('DOMContentLoaded', function () {
    var id = U.param('id');
    var focus = id ? F.get(id) : null;
    var box = document.getElementById('gallery');
    var intro = document.getElementById('gallery-intro');
    var lb = document.getElementById('lightbox');

    var photos = F.photos.slice();
    // Also include people's portrait photos
    F.all().forEach(function (p) {
      if (p.photo) photos.push({ src: p.photo, caption: 'Portrait of ' + F.fullName(p), people: [p.id], portrait: true });
    });
    if (focus) {
      photos = photos.filter(function (ph) { return (ph.people || []).indexOf(focus.id) >= 0; });
      intro.innerHTML = '';
      intro.appendChild(el('span', {}, ['Photos of ', el('a', { href: U.personUrl(focus), text: F.fullName(focus) }), '. ', el('a', { href: 'gallery.html', text: 'Show all photos' })]));
    } else {
      intro.textContent = photos.length ? photos.length + ' photographs. Add more to the "photos" list in data/family.js and drop the files in the images/ folder.'
        : 'Add photos to the "photos" list in data/family.js and drop the files in the images/ folder.';
    }
    photos.sort(function (a, b) { return F.sortKey(a.date) - F.sortKey(b.date); });
    if (!photos.length) { box.appendChild(el('div', { class: 'empty-state', text: 'No photos yet.' })); return; }

    photos.forEach(function (ph) {
      var people = (ph.people || []).map(F.get).filter(Boolean);
      var img = el('img', { src: ph.src, alt: ph.caption || '', loading: 'lazy' });
      img.addEventListener('click', function () {
        lb.querySelector('img').src = ph.src; lb.querySelector('p').textContent = ph.caption || ''; lb.hidden = false;
      });
      box.appendChild(el('figure', {}, [img, el('figcaption', {}, [
        ph.date ? el('span', { class: 'date', text: F.formatDate(ph.date) }) : null,
        ph.caption || '',
        people.length ? el('div', { class: 'people' }, [el('span', { class: 'muted', text: 'Pictured: ' })].concat(people.map(function (p, i) {
          return el('span', {}, [i ? ', ' : '', el('a', { href: U.personUrl(p), text: F.shortName(p) })]);
        }))) : null
      ])]));
    });
    lb.addEventListener('click', function () { lb.hidden = true; });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') lb.hidden = true; });
  });
})();
