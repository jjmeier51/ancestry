/* Tree view: hourglass / ancestor / descendant chart with pan, pinch-zoom and inertia. */
(function () {
  'use strict';
  const F = window.Family, A = window.App, el = A.el, icon = A.icon;
  const NW = 200, NH = 60, HG = 20, VG = 76, CG = 22, ROWH = NH + VG;

  /* Contour-based pedigree layout: each subtree keeps per-depth extents so
   * branches pack tightly without overlapping. All x are relative to root = 0. */
  function layoutAncestors(rootId, gens, expanded) {
    const links = [];
    function build(id, gen, limit) {
      const p = F.get(id); if (!p) return null;
      const node = { p, gen, x: 0, y: -gen * ROWH, more: {} };
      const par = [F.father(id), F.mother(id)].filter(Boolean);
      if (expanded[id]) limit = Math.max(limit, gen + gens);
      let nodes = [node], ext = [{ min: -NW / 2, max: NW / 2 }];
      if (par.length && gen < limit) {
        const subs = par.map(q => build(q.id, gen + 1, limit)).filter(Boolean);
        subs.forEach(s => links.push({ type: 'parent', from: node, to: s.node }));
        if (subs.length === 1) {
          nodes = nodes.concat(subs[0].nodes);
          ext = ext.concat(subs[0].ext);
        } else if (subs.length === 2) {
          const [L, R] = subs;
          let shift = 0;
          for (let d = 0; d < Math.min(L.ext.length, R.ext.length); d++) shift = Math.max(shift, L.ext[d].max - R.ext[d].min + HG);
          const c = shift / 2; // node sits midway between the two parents
          L.nodes.forEach(n => { n.x -= c; }); R.nodes.forEach(n => { n.x += shift - c; });
          nodes = nodes.concat(L.nodes, R.nodes);
          for (let d = 0; d < Math.max(L.ext.length, R.ext.length); d++) {
            const a = L.ext[d], b = R.ext[d];
            ext.push({ min: Math.min(a ? a.min - c : Infinity, b ? b.min + shift - c : Infinity), max: Math.max(a ? a.max - c : -Infinity, b ? b.max + shift - c : -Infinity) });
          }
        }
      } else if (par.length) node.more.up = true;
      return { node, nodes, ext };
    }
    const r = build(rootId, 0, gens);
    return { nodes: r.nodes, links, root: r.node };
  }

  function layoutDescendants(rootId, gens, expanded) {
    const nodes = [], links = [], seen = { [rootId]: true };
    function build(id, gen, limit) {
      const p = F.get(id);
      const unit = { p, gen, fams: [], coupleW: NW, kidsW: 0, more: false };
      if (expanded[id]) limit = Math.max(limit, gen + gens);
      F.spouseFamilies(id).forEach(f => {
        const spouse = F.get(f.husband === id ? f.wife : f.husband);
        const fam = { f, spouse, kids: [], kidsW: 0 };
        if (spouse) unit.coupleW += CG + NW;
        const kids = F.sortByBirth(f.children.map(F.get).filter(Boolean));
        if (kids.length && gen >= limit) unit.more = true;
        if (gen < limit) kids.forEach(c => {
          if (seen[c.id]) return; seen[c.id] = true;
          const u = build(c.id, gen + 1, limit); fam.kids.push(u); fam.kidsW += u.width + HG;
        });
        if (fam.kids.length) { fam.kidsW -= HG; unit.kidsW += fam.kidsW + HG * 2; }
        unit.fams.push(fam);
      });
      if (unit.kidsW) unit.kidsW -= HG * 2;
      unit.width = Math.max(unit.coupleW, unit.kidsW);
      return unit;
    }
    function place(unit, x0, y) {
      let kx = x0 + (unit.width - unit.kidsW) / 2;
      let cx = x0 + (unit.width - unit.coupleW) / 2 + NW / 2;
      const node = { p: unit.p, gen: unit.gen, x: cx, y, more: { down: unit.more } };
      nodes.push(node);
      cx += NW + CG;
      let prev = node;
      unit.fams.forEach(fam => {
        let sNode = null;
        if (fam.spouse) {
          sNode = { p: fam.spouse, gen: unit.gen, x: cx, y, spouse: true, more: {} };
          nodes.push(sNode); links.push({ type: 'marriage', from: prev, to: sNode }); prev = sNode; cx += NW + CG;
        }
        if (fam.kids.length) {
          const dropX = sNode ? sNode.x - NW / 2 - CG / 2 : node.x;
          const dropY = sNode ? y : y + NH / 2;
          const kidNodes = fam.kids.map(k => { const kn = place(k, kx, y + ROWH); kx += k.width + HG; return kn; });
          kx += HG;
          links.push({ type: 'children', dropX, dropY, busY: y + NH / 2 + VG / 2, kids: kidNodes });
        }
      });
      return node;
    }
    const root = place(build(rootId, 0, gens), 0, 0);
    const dx = root.x; nodes.forEach(n => { n.x -= dx; }); links.forEach(l => { if (l.dropX !== undefined) l.dropX -= dx; });
    return { nodes, links, root };
  }

  function layout(rootId, mode, gens, expanded) {
    if (mode === 'ancestors') return layoutAncestors(rootId, gens, expanded);
    if (mode === 'descendants') return layoutDescendants(rootId, gens, expanded);
    const a = layoutAncestors(rootId, gens, expanded), d = layoutDescendants(rootId, gens, expanded);
    d.root.more.up = a.root.more.up;
    a.links.forEach(l => { if (l.from === a.root) l.from = d.root; });
    return { nodes: d.nodes.concat(a.nodes.filter(n => n !== a.root)), links: d.links.concat(a.links), root: d.root };
  }

  const genLabel = (gen, up) => {
    const g = Math.abs(gen);
    if (g === 0) return '';
    if (up) return g === 1 ? 'Parents' : g === 2 ? 'Grandparents' : (g === 3 ? '' : ordinal(g - 2) + ' ') + 'great-grandparents';
    return g === 1 ? 'Children' : g === 2 ? 'Grandchildren' : (g === 3 ? '' : ordinal(g - 2) + ' ') + 'great-grandchildren';
  };
  const ordinal = n => { const s = ['th', 'st', 'nd', 'rd'], v = n % 100; return n + (s[(v - 20) % 10] || s[v] || s[0]); };

  const view = {
    title: () => F.shortTitle,
    render(container, r) {
      const state = { rootId: null, mode: 'both', gens: F.config.defaultGenerations || 4, expanded: {}, k: 1, tx: 0, ty: 0 };
      const stage = el('div', { class: 'stage', role: 'application', 'aria-label': 'Family tree chart' });
      const layer = el('div', { class: 'layer' });
      const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('class', 'links'); svg.setAttribute('width', '1'); svg.setAttribute('height', '1');
      layer.appendChild(svg);
      stage.appendChild(layer);

      const rootChip = el('button', { class: 'glass root-chip', 'aria-label': 'Current person' });
      const modeSeg = el('div', { class: 'glass seg', role: 'group', 'aria-label': 'View' }, [
        ['both', 'Both', 'layers'], ['ancestors', 'Ancestors', 'up'], ['descendants', 'Descendants', 'down']
      ].map(m => el('button', { 'data-mode': m[0], html: icon(m[2]) + '<span>' + m[1] + '</span>', onclick: () => { state.mode = m[0]; state.expanded = {}; sync(); draw(); } })));
      const genSel = el('select', { class: 'glass gen-sel', 'aria-label': 'Generations' }, [2, 3, 4, 5, 6, 8].map(n => el('option', { value: n, text: n + ' gen' })));
      genSel.appendChild(el('option', { value: 99, text: 'All' }));
      genSel.addEventListener('change', () => { state.gens = +genSel.value; state.expanded = {}; sync(); draw(); });
      const zoomBox = el('div', { class: 'glass zoom-box' }, [
        el('button', { 'aria-label': 'Zoom in', html: icon('plus'), onclick: () => zoomAt(1.3, cx(), cy()) }),
        el('button', { 'aria-label': 'Zoom out', html: icon('minus'), onclick: () => zoomAt(1 / 1.3, cx(), cy()) }),
        el('button', { 'aria-label': 'Fit to screen', html: icon('fit'), onclick: () => fit(true) })
      ]);
      const homeBtn = el('a', { class: 'glass icon-btn home-btn', href: '#/', 'aria-label': 'Back to me', html: icon('home') });
      const legend = el('div', { class: 'glass legend' }, Object.keys(F.confidenceLevels).map(k => el('span', { class: 'conf conf-' + k, title: F.confidenceDescription(k) }, [el('i'), F.confidenceLabel(k)])));
      container.appendChild(stage);
      container.appendChild(el('div', { class: 'hud hud-top' }, [rootChip, homeBtn]));
      container.appendChild(el('div', { class: 'hud hud-bottom' }, [modeSeg, genSel, legend]));
      container.appendChild(zoomBox);

      const cx = () => stage.clientWidth / 2, cy = () => stage.clientHeight / 2;
      const apply = () => { layer.style.transform = `translate3d(${state.tx}px, ${state.ty}px, 0) scale(${state.k})`; };
      function zoomAt(factor, px, py, animate) {
        const nk = Math.min(2.5, Math.max(0.12, state.k * factor));
        state.tx = px - (px - state.tx) * (nk / state.k);
        state.ty = py - (py - state.ty) * (nk / state.k);
        state.k = nk;
        if (animate !== false) { layer.classList.add('animate'); setTimeout(() => layer.classList.remove('animate'), 260); }
        apply();
      }
      let bbox = null;
      function fit(animate) {
        if (!bbox) return;
        const W = stage.clientWidth, H = stage.clientHeight;
        const bw = bbox.maxX - bbox.minX, bh = bbox.maxY - bbox.minY;
        let k = Math.min(W / bw, H / bh, 1);
        const minK = W < 700 ? 0.62 : 0.45;
        if (k < minK) {
          k = minK;
          state.k = k;
          // Root is at (0,0): centre it horizontally, and vertically in proportion to how much tree lies above vs below it.
          const frac = Math.min(0.78, Math.max(0.22, (0 - bbox.minY) / (bbox.maxY - bbox.minY)));
          state.tx = W / 2; state.ty = H * frac;
        } else {
          state.k = k;
          state.tx = (W - bw * k) / 2 - bbox.minX * k;
          state.ty = (H - bh * k) / 2 - bbox.minY * k;
        }
        if (animate) { layer.classList.add('animate'); setTimeout(() => layer.classList.remove('animate'), 320); }
        apply();
      }

      function draw() {
        const L = layout(state.rootId, state.mode, state.gens, state.expanded);
        layer.querySelectorAll('.node, .expander, .gen-label').forEach(n => n.remove());
        while (svg.firstChild) svg.removeChild(svg.firstChild);
        let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
        L.nodes.forEach(n => { minX = Math.min(minX, n.x - NW / 2); maxX = Math.max(maxX, n.x + NW / 2); minY = Math.min(minY, n.y - NH / 2); maxY = Math.max(maxY, n.y + NH / 2); });

        const ns = 'http://www.w3.org/2000/svg';
        L.links.forEach(l => {
          const path = document.createElementNS(ns, 'path');
          let d = '';
          if (l.type === 'parent') {
            const x1 = l.from.x, y1 = l.from.y - NH / 2, x2 = l.to.x, y2 = l.to.y + NH / 2, my = (y1 + y2) / 2;
            d = `M${x1},${y1} V${my} H${x2} V${y2}`;
          } else if (l.type === 'marriage') {
            d = `M${l.from.x + NW / 2},${l.from.y} H${l.to.x - NW / 2}`;
            path.setAttribute('class', 'marriage');
          } else {
            d = `M${l.dropX},${l.dropY} V${l.busY}`;
            const xs = l.kids.map(k => k.x);
            d += ` M${Math.min(l.dropX, ...xs)},${l.busY} H${Math.max(l.dropX, ...xs)}`;
            l.kids.forEach(k => { d += ` M${k.x},${l.busY} V${k.y - NH / 2}`; });
          }
          path.setAttribute('d', d);
          svg.appendChild(path);
        });

        const gens = {};
        L.nodes.forEach((n, i) => {
          const p = n.p;
          const node = el('div', {
            class: `node sex-${(p.sex || 'U').toLowerCase()} conf-${F.confidence(p)}${n === L.root ? ' root' : ''}${n.spouse ? ' spouse' : ''}`,
            style: { left: (n.x - NW / 2) + 'px', top: (n.y - NH / 2) + 'px', '--i': Math.min(i, 24) },
            role: 'button', tabindex: '0', 'data-id': p.id
          }, [
            A.avatar(p, 'node-avatar'),
            el('div', { class: 'node-text' }, [
              el('div', { class: 'node-name', text: F.fullName(p) }),
              el('div', { class: 'node-sub', text: [F.lifespan(p), p.birth && p.birth.place ? p.birth.place.split(',')[0] : ''].filter(Boolean).join(' · ') })
            ]),
            el('span', { class: 'node-conf', title: F.confidenceLabel(F.confidence(p)) }),
            F.tags(p).length ? el('span', { class: 'node-tag', html: icon(A.tagIcon(F.tags(p)[0])) }) : null
          ]);
          node.addEventListener('click', e => { e.stopPropagation(); A.personSheet(p, { treeLinks: true }); });
          node.addEventListener('keydown', e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); A.personSheet(p, { treeLinks: true }); } });
          layer.appendChild(node);
          if (n.more.up) layer.appendChild(expander(p, n.x, n.y - NH / 2 - 16, 'Show earlier generations'));
          if (n.more.down) layer.appendChild(expander(p, n.x, n.y + NH / 2 + 16, 'Show later generations'));
          if (n.gen !== 0 && !gens[n.y]) gens[n.y] = genLabel(n.gen, n.y < 0);
        });
        Object.keys(gens).forEach(y => {
          layer.appendChild(el('div', { class: 'gen-label', text: gens[y], style: { left: (minX - 16) + 'px', top: (+y - 10) + 'px' } }));
        });
        bbox = { minX: minX - 250, minY: minY - 40, maxX: maxX + 40, maxY: maxY + 50 };
        fit(false);
        requestAnimationFrame(() => layer.classList.add('in'));
      }
      function expander(p, x, y, label) {
        return el('button', { class: 'expander', style: { left: (x - 14) + 'px', top: (y - 14) + 'px' }, 'aria-label': label, title: label, html: icon('plus'),
          onclick: e => { e.stopPropagation(); state.expanded[p.id] = true; layer.classList.remove('in'); draw(); } });
      }

      function sync() {
        modeSeg.querySelectorAll('button').forEach(b => b.classList.toggle('active', b.dataset.mode === state.mode));
        genSel.value = String(state.gens);
        const p = F.get(state.rootId);
        rootChip.innerHTML = '';
        rootChip.appendChild(A.avatar(p, 'sm'));
        rootChip.appendChild(el('span', {}, [el('small', { text: state.mode === 'both' ? 'Tree of' : state.mode === 'ancestors' ? 'Ancestors of' : 'Descendants of' }), el('b', { text: F.fullName(p) })]));
        rootChip.onclick = () => A.personSheet(p, { treeLinks: true });
        const me = F.rootPerson();
        homeBtn.style.display = me && me.id === state.rootId && state.mode === 'both' ? 'none' : '';
        const q = `?mode=${state.mode}&gen=${state.gens}`;
        const want = state.rootId === (me && me.id) && state.mode === 'both' && state.gens === (F.config.defaultGenerations || 4) ? '#/' : `#/tree/${encodeURIComponent(state.rootId)}${q}`;
        if (location.hash !== want && !(want === '#/' && (location.hash === '' || location.hash === '#'))) history.replaceState(null, '', want);
      }
      function load(r) {
        const p = (r.id && F.get(r.id)) || F.rootPerson();
        if (!p) { stage.innerHTML = '<div class="empty"><h2>No people yet</h2><p>Import a GEDCOM file to begin.</p></div>'; return; }
        state.rootId = p.id;
        if (r.params.mode) state.mode = r.params.mode;
        if (r.params.gen) state.gens = +r.params.gen || state.gens;
        state.expanded = {};
        layer.classList.remove('in');
        sync();
        draw();
      }

      /* ---- Pointer handling: pan, pinch, double-tap, inertia ---- */
      const pts = new Map();
      let moved = false, pinch = null, vel = { x: 0, y: 0 }, lastMove = null, raf = null, lastTap = null;
      const stopInertia = () => { if (raf) { cancelAnimationFrame(raf); raf = null; } };
      stage.addEventListener('pointerdown', e => {
        if (e.target.closest('.expander')) return;
        stopInertia();
        pts.set(e.pointerId, { x: e.clientX, y: e.clientY, sx: e.clientX, sy: e.clientY, t: performance.now() });
        if (pts.size === 2) { const [a, b] = [...pts.values()]; pinch = { d: Math.hypot(a.x - b.x, a.y - b.y), mx: (a.x + b.x) / 2, my: (a.y + b.y) / 2 }; }
        if (pts.size === 1) { vel = { x: 0, y: 0 }; lastMove = { t: performance.now(), x: e.clientX, y: e.clientY }; }
      });
      const move = e => {
        const pt = pts.get(e.pointerId); if (!pt) return;
        pt.x = e.clientX; pt.y = e.clientY;
        if (pts.size === 1) {
          const dx = e.clientX - lastMove.x, dy = e.clientY - lastMove.y;
          if (!moved && Math.hypot(e.clientX - pt.sx, e.clientY - pt.sy) > 5) { moved = true; stage.classList.add('dragging'); }
          if (moved) {
            state.tx += dx; state.ty += dy; apply();
            const now = performance.now(), dt = Math.max(1, now - lastMove.t);
            vel = { x: dx / dt, y: dy / dt };
            lastMove = { t: now, x: e.clientX, y: e.clientY };
          }
        } else if (pts.size === 2 && pinch) {
          const [a, b] = [...pts.values()];
          const d = Math.hypot(a.x - b.x, a.y - b.y), mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2;
          const rect = stage.getBoundingClientRect();
          moved = true;
          zoomAt(d / pinch.d, pinch.mx - rect.left, pinch.my - rect.top, false);
          state.tx += mx - pinch.mx; state.ty += my - pinch.my; apply();
          pinch = { d, mx, my };
        }
      };
      window.addEventListener('pointermove', move);
      const up = e => {
        if (!pts.has(e.pointerId)) return;
        pts.delete(e.pointerId);
        if (pts.size === 1) { pinch = null; const [a] = [...pts.values()]; lastMove = { t: performance.now(), x: a.x, y: a.y }; vel = { x: 0, y: 0 }; }
        if (pts.size === 0) {
          stage.classList.remove('dragging');
          if (moved && Math.hypot(vel.x, vel.y) > 0.15) inertia();
          if (!moved && !e.target.closest('.node, .expander, .hud, .zoom-box')) {
            const now = performance.now();
            if (lastTap && now - lastTap.t < 320 && Math.hypot(e.clientX - lastTap.x, e.clientY - lastTap.y) < 30) {
              const rect = stage.getBoundingClientRect(); zoomAt(1.7, e.clientX - rect.left, e.clientY - rect.top); lastTap = null;
            } else lastTap = { t: now, x: e.clientX, y: e.clientY };
          }
          setTimeout(() => { moved = false; }, 0);
        }
      };
      window.addEventListener('pointerup', up); window.addEventListener('pointercancel', up);
      stage.addEventListener('click', e => { if (moved) { e.stopPropagation(); e.preventDefault(); } }, true);
      function inertia() {
        let v = { x: vel.x * 16, y: vel.y * 16 };
        const step = () => { v.x *= 0.92; v.y *= 0.92; state.tx += v.x; state.ty += v.y; apply(); if (Math.abs(v.x) + Math.abs(v.y) > 0.3) raf = requestAnimationFrame(step); else raf = null; };
        raf = requestAnimationFrame(step);
      }
      stage.addEventListener('wheel', e => {
        e.preventDefault();
        const rect = stage.getBoundingClientRect();
        if (e.ctrlKey || Math.abs(e.deltaY) > Math.abs(e.deltaX)) zoomAt(Math.exp(-e.deltaY * (e.ctrlKey ? 0.01 : 0.0018)), e.clientX - rect.left, e.clientY - rect.top, false);
        else { state.tx -= e.deltaX; apply(); }
      }, { passive: false });
      ['gesturestart', 'gesturechange', 'gestureend'].forEach(t => stage.addEventListener(t, e => e.preventDefault()));
      const onResize = () => fit(false);
      window.addEventListener('resize', onResize);

      load(r);
      return {
        update(nr) { if (nr.name !== 'tree') return false; load(nr); return true; },
        destroy() { window.removeEventListener('resize', onResize); window.removeEventListener('pointermove', move); window.removeEventListener('pointerup', up); window.removeEventListener('pointercancel', up); stopInertia(); }
      };
    }
  };
  A.views.tree = view;
})();
