(function () {
  'use strict';
  const F = window.Family, A = window.App, el = A.el, icon = A.icon;
  const isImg = m => m.file && /\.(jpe?g|png|gif|webp|svg)$/i.test(m.file);
  A.views.media = {
    title: () => 'Media',
    render(container, r) {
      const all = F.allMedia();
      const types = {}; all.forEach(m => { types[m.type || 'other'] = (types[m.type || 'other'] || 0) + 1; });
      let active = r.params.type || '';
      const chips = el('div', { class: 'chip-row' }, Object.keys(types).sort().map(t => el('button', { class: 'chip' + (active === t ? ' active' : ''), 'data-t': t, html: `${A.tagLabel(t)} <small>${types[t]}</small>`, onclick: () => { active = active === t ? '' : t; chips.querySelectorAll('.chip').forEach(c => c.classList.toggle('active', c.dataset.t === active)); render(); } })));
      const grid = el('div', { class: 'media-grid large' });
      container.appendChild(el('div', { class: 'wrap' }, [
        el('h1', { text: 'Media & documents' }),
        el('p', { class: 'muted', text: all.length ? `${all.length} items across the family. Photos open in a viewer; documents open in a new tab.` : 'Nothing attached yet. Use scripts/attach_media.py to add photos and documents.' }),
        chips, grid
      ]));
      function render() {
        const items = all.filter(m => !active || (m.type || 'other') === active);
        const images = items.filter(isImg);
        grid.innerHTML = '';
        if (!items.length) { grid.appendChild(el('div', { class: 'empty', text: 'Nothing here yet.' })); return; }
        items.forEach((m, i) => {
          const card = el('a', { class: 'media-card type-' + (m.type || 'other'), href: m.url || m.file || '#', target: m.url || !isImg(m) ? '_blank' : null, rel: 'noopener', style: { '--i': Math.min(i, 24) } }, [
            isImg(m) ? el('img', { src: m.file, alt: m.title || '', loading: 'lazy' }) : el('div', { class: 'media-icon', html: icon(m.type === 'link' ? 'link' : 'doc') }),
            el('div', { class: 'media-cap' }, [
              el('b', { text: m.title || 'Untitled' }),
              el('span', { text: [m.date ? F.formatDate(m.date) : '', m.source].filter(Boolean).join(' · ') }),
              el('a', { class: 'media-owner', href: `#/person/${encodeURIComponent(m.owner.id)}` }, [A.avatar(m.owner, 'xs'), F.fullName(m.owner)])
            ])
          ]);
          if (isImg(m)) card.addEventListener('click', e => { if (e.target.closest('.media-owner')) return; e.preventDefault(); A.lightbox(images, images.indexOf(m)); });
          grid.appendChild(card);
        });
      }
      render();
    }
  };
})();
