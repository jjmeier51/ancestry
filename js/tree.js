/* Interactive family tree: ancestor (pedigree) and descendant charts rendered
 * as SVG with pan/zoom. Pure DOM, no libraries. */
(function () {
  'use strict';
  var F = window.Family, U = window.UI, el = U.el;
  var SVG_NS = 'http://www.w3.org/2000/svg';

  var W = 180, H = 50;           // node size
  var COL = 240, ROW = 64;       // ancestor chart spacing
  var HGAP = 18, VGAP = 90, COUPLE_GAP = 30; // descendant chart spacing

  var state = { rootId: null, view: 'ancestors', gens: 4, expanded: {}, k: 1, tx: 0, ty: 0 };
  var stage, svg, layer, popover;

  function svgEl(tag, attrs) {
    var e = document.createElementNS(SVG_NS, tag);
    if (attrs) Object.keys(attrs).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    return e;
  }
  function trunc(s, n) { return s.length > n ? s.slice(0, n - 1) + '…' : s; }

  /* ---------------- Ancestor layout ---------------- */
  function layoutAncestors(rootId, maxGen) {
    var nodes = [], links = [], slot = 0, maxGenSeen = 0;
    function build(id, gen, limit, viaChild) {
      var p = F.get(id);
      if (!p) return null;
      var node = { p: p, gen: gen, x: gen * COL, y: 0 };
      nodes.push(node);
      maxGenSeen = Math.max(maxGenSeen, gen);
      var parents = [F.father(id), F.mother(id)];
      var hasParents = parents.some(Boolean);
      if (state.expanded[id]) limit = Math.max(limit, gen + state.gens);
      if (hasParents && gen < limit) {
        var ys = [];
        parents.forEach(function (par) {
          if (!par) return;
          var n = build(par.id, gen + 1, limit);
          if (n) { ys.push(n.y); links.push({ from: node, to: n }); }
        });
        node.y = ys.reduce(function (a, b) { return a + b; }, 0) / ys.length;
        if (parents[0] && !parents[1] || !parents[0] && parents[1]) {
          // Single known parent: leave a gap for the unknown one to keep alignment
          slot += 0.5;
        }
      } else {
        node.y = slot * ROW; slot += 1;
        if (hasParents) node.more = true;
      }
      return node;
    }
    var root = build(rootId, 0, maxGen);
    if (root) root.focus = true;
    return { nodes: nodes, links: links, gens: maxGenSeen, orientation: 'h' };
  }

  /* ---------------- Descendant layout ---------------- */
  function layoutDescendants(rootId, maxGen) {
    var nodes = [], links = [], seen = {}, maxGenSeen = 0;
    function build(id, gen, limit) {
      var p = F.get(id);
      if (!p) return null;
      var unit = { p: p, gen: gen, fams: [], width: W };
      maxGenSeen = Math.max(maxGenSeen, gen);
      if (state.expanded[id]) limit = Math.max(limit, gen + state.gens);
      var sf = F.spouseFamilies(id);
      var coupleW = W, kidsW = 0, anyKids = false;
      sf.forEach(function (f) {
        var spouse = F.get(f.husband === id ? f.wife : f.husband);
        var fam = { f: f, spouse: spouse, kids: [], kidsW: 0 };
        if (spouse) coupleW += COUPLE_GAP + W;
        if (f.children.length) anyKids = true;
        if (gen < limit) {
          F.sortByBirth(f.children.map(F.get).filter(Boolean)).forEach(function (c) {
            if (seen[c.id]) return; seen[c.id] = true;
            var u = build(c.id, gen + 1, limit);
            if (u) { fam.kids.push(u); fam.kidsW += u.width + HGAP; }
          });
          if (fam.kids.length) { fam.kidsW -= HGAP; kidsW += fam.kidsW + HGAP * 2; }
        }
        unit.fams.push(fam);
      });
      if (kidsW) kidsW -= HGAP * 2;
      unit.coupleW = coupleW;
      unit.width = Math.max(coupleW, kidsW);
      unit.more = anyKids && gen >= limit;
      return unit;
    }
    function place(unit, x0, y) {
      var kidsTotal = unit.fams.reduce(function (s, f) { return s + (f.kids.length ? f.kidsW + HGAP * 2 : 0); }, 0);
      if (kidsTotal) kidsTotal -= HGAP * 2;
      var kx = x0 + (unit.width - kidsTotal) / 2;
      var cx = x0 + (unit.width - unit.coupleW) / 2;
      var node = { p: unit.p, gen: unit.gen, x: cx, y: y, more: unit.more };
      nodes.push(node);
      cx += W + COUPLE_GAP;
      unit.fams.forEach(function (fam) {
        var sNode = null;
        if (fam.spouse) {
          sNode = { p: fam.spouse, gen: unit.gen, x: cx, y: y, spouse: true };
          nodes.push(sNode);
          links.push({ marriage: true, from: node, to: sNode });
          cx += W + COUPLE_GAP;
        }
        if (fam.kids.length) {
          var dropX = sNode ? (sNode.x + node.x + W) / 2 : node.x + W / 2;
          // Marriage link mid point: between left neighbour and this spouse
          if (sNode) dropX = sNode.x - COUPLE_GAP / 2;
          var kidNodes = [];
          fam.kids.forEach(function (k) {
            var kn = place(k, kx, y + H + VGAP);
            kidNodes.push(kn);
            kx += k.width + HGAP;
          });
          kx += HGAP;
          links.push({ family: true, dropX: dropX, dropY: y + H / 2, fromSpouse: !!sNode, parentBottom: y + H, kids: kidNodes, busY: y + H + VGAP / 2 });
        }
      });
      return node;
    }
    var rootUnit = build(rootId, 0, maxGen);
    if (!rootUnit) return { nodes: [], links: [], gens: 0, orientation: 'v' };
    var rootNode = place(rootUnit, 0, 0);
    rootNode.focus = true;
    return { nodes: nodes, links: links, gens: maxGenSeen, orientation: 'v' };
  }

  /* ---------------- Rendering ---------------- */
  function genLabel(view, gen) {
    if (gen === 0) return view === 'ancestors' ? 'Self' : 'Root';
    if (view === 'ancestors') {
      if (gen === 1) return 'Parents';
      if (gen === 2) return 'Grandparents';
      return (gen === 3 ? '' : ordinal(gen - 2) + ' ') + 'great-grandparents';
    }
    if (gen === 1) return 'Children';
    if (gen === 2) return 'Grandchildren';
    return (gen === 3 ? '' : ordinal(gen - 2) + ' ') + 'great-grandchildren';
  }
  function ordinal(n) { var s = ['th', 'st', 'nd', 'rd'], v = n % 100; return n + (s[(v - 20) % 10] || s[v] || s[0]); }

  function draw() {
    var layout = state.view === 'ancestors' ? layoutAncestors(state.rootId, state.gens) : layoutDescendants(state.rootId, state.gens);
    while (layer.firstChild) layer.removeChild(layer.firstChild);
    hidePopover();
    if (!layout.nodes.length) return;

    // Generation labels
    var minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    layout.nodes.forEach(function (n) {
      minX = Math.min(minX, n.x); minY = Math.min(minY, n.y); maxX = Math.max(maxX, n.x + W); maxY = Math.max(maxY, n.y + H);
    });
    for (var g = 0; g <= layout.gens; g++) {
      var t = svgEl('text', { class: 'gen-label' });
      t.textContent = genLabel(state.view, g);
      if (layout.orientation === 'h') { t.setAttribute('x', g * COL); t.setAttribute('y', minY - 18); }
      else { t.setAttribute('x', minX - 10); t.setAttribute('y', g * (H + VGAP) + H / 2 + 4); t.setAttribute('text-anchor', 'end'); }
      layer.appendChild(t);
    }

    // Links
    layout.links.forEach(function (l) {
      var d;
      if (l.marriage) {
        d = 'M' + (l.from.x + W) + ',' + (l.from.y + H / 2) + 'H' + l.to.x;
        layer.appendChild(svgEl('path', { class: 'link marriage', d: d }));
      } else if (l.family) {
        var start = l.fromSpouse ? 'M' + l.dropX + ',' + l.dropY : 'M' + l.dropX + ',' + l.parentBottom;
        d = start + 'V' + l.busY;
        var xs = l.kids.map(function (k) { return k.x + W / 2; });
        d += 'M' + Math.min(Math.min.apply(null, xs), l.dropX) + ',' + l.busY + 'H' + Math.max(Math.max.apply(null, xs), l.dropX);
        l.kids.forEach(function (k) { d += 'M' + (k.x + W / 2) + ',' + l.busY + 'V' + k.y; });
        layer.appendChild(svgEl('path', { class: 'link', d: d }));
      } else {
        var x1 = l.from.x + W, y1 = l.from.y + H / 2, x2 = l.to.x, y2 = l.to.y + H / 2, mx = (x1 + x2) / 2;
        d = 'M' + x1 + ',' + y1 + 'H' + mx + 'V' + y2 + 'H' + x2;
        layer.appendChild(svgEl('path', { class: 'link', d: d }));
      }
    });

    // Nodes
    layout.nodes.forEach(function (n) {
      var p = n.p;
      var g = svgEl('g', { class: 'node sex-' + (p.sex || 'U').toLowerCase() + (n.focus ? ' focus' : ''), transform: 'translate(' + n.x + ',' + n.y + ')', tabindex: '0', role: 'button' });
      g.appendChild(svgEl('rect', { width: W, height: H }));
      g.appendChild(svgEl('rect', { class: 'bar', x: 0, y: 8, width: 5, height: H - 16, rx: 2 }));
      var name = svgEl('text', { class: 'name', x: 16, y: 21 });
      name.textContent = trunc(F.fullName(p), 24);
      g.appendChild(name);
      var dates = svgEl('text', { class: 'dates', x: 16, y: 38 });
      var place = p.birth && p.birth.place ? p.birth.place.split(',')[0] : '';
      dates.textContent = trunc([F.lifespan(p), place].filter(Boolean).join(' · '), 30);
      g.appendChild(dates);
      var title = svgEl('title'); title.textContent = F.fullName(p) + (F.lifespan(p) ? ' (' + F.lifespan(p) + ')' : ''); g.appendChild(title);
      g.addEventListener('click', function (e) { e.stopPropagation(); showPopover(n, e); });
      g.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); showPopover(n, e); } });
      layer.appendChild(g);

      if (n.more) {
        var ex = svgEl('g', { class: 'node expander-group', transform: 'translate(' + (layout.orientation === 'h' ? n.x + W + 12 : n.x + W / 2) + ',' + (layout.orientation === 'h' ? n.y + H / 2 : n.y + H + 14) + ')', role: 'button', tabindex: '0' });
        ex.appendChild(svgEl('circle', { class: 'expander', r: 10 }));
        var plus = svgEl('text', { x: 0, y: 4.5, 'text-anchor': 'middle' }); plus.textContent = '+';
        ex.appendChild(plus);
        var t2 = svgEl('title'); t2.textContent = 'Show more generations'; ex.appendChild(t2);
        ex.addEventListener('click', function (e) { e.stopPropagation(); state.expanded[p.id] = true; draw(); });
        layer.appendChild(ex);
      }
    });

    var labelPad = layout.orientation === 'v' ? 190 : 40;
    var rootNode = layout.nodes.filter(function (n) { return n.focus; })[0];
    fit({ minX: minX - labelPad, minY: minY - 40, maxX: maxX + 40, maxY: maxY + 40, rootX: rootNode && rootNode.x, rootY: rootNode && rootNode.y });
  }

  function applyTransform() {
    layer.setAttribute('transform', 'translate(' + state.tx + ',' + state.ty + ') scale(' + state.k + ')');
  }
  function fit(b) {
    var r = stage.getBoundingClientRect();
    var bw = b.maxX - b.minX, bh = b.maxY - b.minY;
    var k = Math.min(r.width / bw, r.height / bh, 1.3);
    var minK = r.width < 600 ? 0.7 : 0.35;
    if (k < minK) {
      // Too big to fit: show it at a readable size, anchored on the root person.
      state.k = minK;
      state.tx = r.width < 600 ? 16 - b.minX * minK : (b.rootX !== undefined ? r.width / 2 - (b.rootX + W / 2) * minK : 16 - b.minX * minK);
      state.ty = b.rootY !== undefined ? Math.max(40 - b.minY * minK, r.height / 2 - (b.rootY + H / 2) * minK) : 20 - b.minY * minK;
      if (state.view === 'descendants') { state.ty = 40 - b.minY * minK; }
      if (state.view === 'ancestors') { state.tx = 16 - b.minX * minK; }
      applyTransform();
      return;
    }
    state.k = k;
    state.tx = (r.width - bw * k) / 2 - b.minX * k;
    state.ty = Math.max(20, (r.height - bh * k) / 2) - b.minY * k;
    if (bh * k > r.height) state.ty = 20 - b.minY * k;
    applyTransform();
  }
  function zoomAt(factor, cx, cy) {
    var nk = Math.min(3, Math.max(0.15, state.k * factor));
    state.tx = cx - (cx - state.tx) * (nk / state.k);
    state.ty = cy - (cy - state.ty) * (nk / state.k);
    state.k = nk;
    applyTransform();
  }

  /* ---------------- Popover ---------------- */
  function showPopover(n, e) {
    hidePopover();
    var p = n.p;
    popover = el('div', { class: 'panel', style: 'position:absolute;z-index:5;min-width:240px;padding:14px;margin:0;box-shadow:var(--shadow)' }, [
      el('div', { style: 'display:flex;gap:10px;align-items:center' }, [U.avatar(p, 'sm'), el('div', {}, [el('strong', { text: F.fullName(p) }), el('div', { class: 'muted', style: 'font-size:.85rem', text: F.lifespan(p) })])]),
      el('div', { style: 'display:flex;gap:6px;flex-wrap:wrap;margin-top:12px' }, [
        el('a', { class: 'btn small', href: U.personUrl(p), text: 'Profile' }),
        el('button', { class: 'btn small ghost', type: 'button', text: 'Ancestors', onclick: function () { setRoot(p.id, 'ancestors'); } }),
        el('button', { class: 'btn small ghost', type: 'button', text: 'Descendants', onclick: function () { setRoot(p.id, 'descendants'); } })
      ])
    ]);
    var r = stage.getBoundingClientRect();
    var x = Math.min(e.clientX - r.left + 8, r.width - 270), y = Math.min(e.clientY - r.top + 8, r.height - 120);
    popover.style.left = Math.max(8, x) + 'px'; popover.style.top = Math.max(8, y) + 'px';
    popover.addEventListener('click', function (ev) { ev.stopPropagation(); });
    stage.appendChild(popover);
  }
  function hidePopover() { if (popover) { popover.remove(); popover = null; } }

  /* ---------------- State / controls ---------------- */
  function setRoot(id, view) {
    state.rootId = id;
    if (view) state.view = view;
    state.expanded = {};
    syncControls();
    draw();
  }
  function syncControls() {
    document.getElementById('tree-root').value = state.rootId;
    document.getElementById('tree-gens').value = String(state.gens);
    document.querySelectorAll('.seg button').forEach(function (b) { b.classList.toggle('active', b.getAttribute('data-view') === state.view); });
    history.replaceState(null, '', 'tree.html?id=' + encodeURIComponent(state.rootId) + '&view=' + state.view + '&gen=' + state.gens);
    var p = F.get(state.rootId);
    if (p) document.title = (state.view === 'ancestors' ? 'Ancestors of ' : 'Descendants of ') + F.fullName(p);
  }

  function initPanZoom() {
    var dragging = false, last = null, pinch = null, moved = false;
    stage.addEventListener('pointerdown', function (e) {
      if (e.target.closest('.panel') || e.target.closest('button')) return;
      last = { x: e.clientX, y: e.clientY, id: e.pointerId }; moved = false;
    });
    stage.addEventListener('pointermove', function (e) {
      if (!last) return;
      var dx = e.clientX - last.x, dy = e.clientY - last.y;
      if (!dragging) {
        if (Math.abs(dx) + Math.abs(dy) < 4) return;   // a click, not a drag
        dragging = true; moved = true; stage.classList.add('dragging');
        try { stage.setPointerCapture(last.id); } catch (err) { /* ignore */ }
      }
      state.tx += dx; state.ty += dy; last.x = e.clientX; last.y = e.clientY; applyTransform();
    });
    function end() { dragging = false; last = null; stage.classList.remove('dragging'); }
    stage.addEventListener('pointerup', end); stage.addEventListener('pointercancel', end);
    stage.addEventListener('click', function (e) { if (moved) { moved = false; e.stopPropagation(); } }, true);
    stage.addEventListener('wheel', function (e) {
      e.preventDefault();
      var r = stage.getBoundingClientRect();
      zoomAt(e.deltaY < 0 ? 1.12 : 1 / 1.12, e.clientX - r.left, e.clientY - r.top);
    }, { passive: false });
    stage.addEventListener('touchstart', function (e) { if (e.touches.length === 2) pinch = dist(e.touches); }, { passive: true });
    stage.addEventListener('touchmove', function (e) {
      if (e.touches.length === 2 && pinch) {
        var d = dist(e.touches), r = stage.getBoundingClientRect();
        zoomAt(d / pinch, (e.touches[0].clientX + e.touches[1].clientX) / 2 - r.left, (e.touches[0].clientY + e.touches[1].clientY) / 2 - r.top);
        pinch = d;
      }
    }, { passive: true });
    stage.addEventListener('click', hidePopover);
    function dist(t) { var dx = t[0].clientX - t[1].clientX, dy = t[0].clientY - t[1].clientY; return Math.sqrt(dx * dx + dy * dy); }
    document.getElementById('zoom-in').addEventListener('click', function () { var r = stage.getBoundingClientRect(); zoomAt(1.25, r.width / 2, r.height / 2); });
    document.getElementById('zoom-out').addEventListener('click', function () { var r = stage.getBoundingClientRect(); zoomAt(0.8, r.width / 2, r.height / 2); });
    document.getElementById('tree-fit').addEventListener('click', draw);
    window.addEventListener('resize', draw);
  }

  document.addEventListener('DOMContentLoaded', function () {
    stage = document.getElementById('tree-stage');
    svg = stage.querySelector('svg');
    layer = document.getElementById('tree-layer');
    var rootSel = document.getElementById('tree-root');
    F.all().sort(function (a, b) { return F.fullName(a).localeCompare(F.fullName(b)); }).forEach(function (p) {
      rootSel.appendChild(el('option', { value: p.id, text: F.fullName(p) + (F.lifespan(p) ? ' (' + F.lifespan(p) + ')' : '') }));
    });
    var root = F.get(U.param('id')) || F.rootPerson();
    if (!root) { stage.innerHTML = '<div class="empty-state" style="margin:40px">No people in the family file yet.</div>'; return; }
    state.rootId = root.id;
    state.view = U.param('view') === 'descendants' ? 'descendants' : 'ancestors';
    state.gens = parseInt(U.param('gen'), 10) || 4;

    rootSel.addEventListener('change', function () { setRoot(rootSel.value); });
    document.getElementById('tree-gens').addEventListener('change', function (e) { state.gens = parseInt(e.target.value, 10); state.expanded = {}; syncControls(); draw(); });
    document.querySelectorAll('.seg button').forEach(function (b) {
      b.addEventListener('click', function () { state.view = b.getAttribute('data-view'); state.expanded = {}; syncControls(); draw(); });
    });
    initPanZoom();
    syncControls();
    draw();
  });
})();
