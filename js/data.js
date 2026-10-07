/* Core data access layer. Wraps window.FAMILY_DATA with lookup helpers,
 * date parsing and relationship calculation. No dependencies. */
(function () {
  'use strict';

  var raw = window.FAMILY_DATA || { people: [], families: [], stories: [], photos: [] };
  raw.people = raw.people || [];
  raw.families = raw.families || [];
  raw.stories = raw.stories || [];
  raw.photos = raw.photos || [];

  var peopleById = {};
  var familiesById = {};
  var familiesAsSpouse = {};   // personId -> [family]
  var familyAsChild = {};      // personId -> family

  raw.people.forEach(function (p) { peopleById[p.id] = p; });
  raw.families.forEach(function (f) {
    familiesById[f.id] = f;
    f.children = f.children || [];
    [f.husband, f.wife].forEach(function (s) {
      if (!s) return;
      (familiesAsSpouse[s] = familiesAsSpouse[s] || []).push(f);
    });
    f.children.forEach(function (c) { familyAsChild[c] = f; });
  });

  /* ---------- Dates ---------- */
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
    'August', 'September', 'October', 'November', 'December'];
  var MON3 = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];

  function parseDate(str) {
    if (!str) return null;
    var s = String(str).trim();
    var out = { text: s, year: null, month: null, day: null, qualifier: '' };
    var m;
    var q = s.match(/^(ABT|ABOUT|CA|CIRCA|EST|BEF|BEFORE|AFT|AFTER|BET|BETWEEN|FROM|TO)\.?\s+(.*)$/i);
    if (q) {
      var qk = q[1].toUpperCase();
      out.qualifier = (/^(ABT|ABOUT|CA|CIRCA|EST)$/.test(qk)) ? 'about'
        : (/^(BEF|BEFORE)$/.test(qk)) ? 'before'
        : (/^(AFT|AFTER)$/.test(qk)) ? 'after'
        : 'between';
      s = q[2].split(/\s+(AND|TO)\s+/i)[0];
    }
    if ((m = s.match(/^(\d{4})(?:-(\d{1,2}))?(?:-(\d{1,2}))?$/))) {
      out.year = +m[1]; if (m[2]) out.month = +m[2]; if (m[3]) out.day = +m[3];
    } else if ((m = s.match(/^(?:(\d{1,2})\s+)?([A-Za-z]{3})[A-Za-z]*\.?\s+(\d{4})$/))) {
      var mi = MON3.indexOf(m[2].toUpperCase());
      out.year = +m[3]; if (mi >= 0) out.month = mi + 1; if (m[1]) out.day = +m[1];
    } else if ((m = s.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/))) {
      out.year = +m[3]; out.month = +m[1]; out.day = +m[2];
    } else if ((m = s.match(/(\d{4})/))) {
      out.year = +m[1];
    }
    return out;
  }

  function formatDate(str) {
    var d = parseDate(str);
    if (!d) return '';
    if (d.year === null) return d.text;
    var core = d.day && d.month ? d.day + ' ' + MONTHS[d.month - 1] + ' ' + d.year
      : d.month ? MONTHS[d.month - 1] + ' ' + d.year
      : String(d.year);
    if (d.qualifier === 'between') return d.text.replace(/^BET(WEEN)?\s+/i, 'between ').replace(/\s+AND\s+/i, ' and ');
    return d.qualifier ? d.qualifier + ' ' + core : core;
  }

  function year(str) { var d = parseDate(str); return d ? d.year : null; }

  function sortKey(str) {
    var d = parseDate(str);
    if (!d || d.year === null) return Infinity;
    return d.year * 10000 + (d.month || 0) * 100 + (d.day || 0);
  }

  /* ---------- People ---------- */
  function get(id) { return peopleById[id] || null; }
  function all() { return raw.people.slice(); }

  function fullName(p) {
    if (!p) return 'Unknown';
    var parts = [];
    if (p.given) parts.push(p.given);
    if (p.surname) parts.push(p.surname);
    var n = parts.join(' ');
    if (p.suffix) n += ' ' + p.suffix;
    return n || 'Unknown';
  }
  function shortName(p) {
    if (!p) return 'Unknown';
    var g = (p.given || '').split(/\s+/)[0];
    return [g, p.surname].filter(Boolean).join(' ') || 'Unknown';
  }
  function initials(p) {
    if (!p) return '?';
    return ((p.given || '?')[0] + (p.surname || '')[0 ] || '').toUpperCase().replace('undefined', '');
  }
  function birthYear(p) { return p && p.birth ? year(p.birth.date) : null; }
  function deathYear(p) { return p && p.death ? year(p.death.date) : null; }
  function isDeceased(p) {
    if (!p) return false;
    if (p.death && (p.death.date || p.death.place || p.death === true)) return true;
    var b = birthYear(p);
    return b !== null && (new Date().getFullYear() - b) > 105;
  }
  function lifespan(p) {
    var b = birthYear(p), d = deathYear(p);
    if (b === null && d === null) return '';
    var bs = b === null ? '?' : String(b);
    if (d !== null) return bs + ' – ' + d;
    if (isDeceased(p)) return bs + ' – ?';
    return 'b. ' + bs;
  }
  function age(p) {
    var b = p && p.birth ? parseDate(p.birth.date) : null;
    if (!b || b.year === null) return null;
    var end = p.death && p.death.date ? parseDate(p.death.date) : null;
    var ey, em, ed;
    if (end && end.year !== null) { ey = end.year; em = end.month || 7; ed = end.day || 1; }
    else if (isDeceased(p)) return null;
    else { var now = new Date(); ey = now.getFullYear(); em = now.getMonth() + 1; ed = now.getDate(); }
    var a = ey - b.year;
    if ((em < (b.month || 7)) || (em === (b.month || 7) && ed < (b.day || 1))) a--;
    return a;
  }

  function parentsFamily(id) { return familyAsChild[id] || null; }
  function parents(id) {
    var f = familyAsChild[id];
    if (!f) return [];
    return [f.husband, f.wife].map(get).filter(Boolean);
  }
  function father(id) { var f = familyAsChild[id]; return f ? get(f.husband) : null; }
  function mother(id) { var f = familyAsChild[id]; return f ? get(f.wife) : null; }
  function spouseFamilies(id) {
    return (familiesAsSpouse[id] || []).slice().sort(function (a, b) {
      return sortKey(a.marriage && a.marriage.date) - sortKey(b.marriage && b.marriage.date);
    });
  }
  function spouses(id) {
    return spouseFamilies(id).map(function (f) { return get(f.husband === id ? f.wife : f.husband); }).filter(Boolean);
  }
  function children(id) {
    var out = [];
    spouseFamilies(id).forEach(function (f) { f.children.forEach(function (c) { var p = get(c); if (p) out.push(p); }); });
    return sortByBirth(out);
  }
  function siblings(id) {
    var f = familyAsChild[id];
    if (!f) return [];
    return sortByBirth(f.children.filter(function (c) { return c !== id; }).map(get).filter(Boolean));
  }
  function sortByBirth(list) {
    return list.slice().sort(function (a, b) {
      return sortKey(a.birth && a.birth.date) - sortKey(b.birth && b.birth.date);
    });
  }

  /* Ancestors as map id -> generation distance (1 = parent). */
  function ancestorMap(id) {
    var map = {}, queue = [[id, 0]];
    while (queue.length) {
      var cur = queue.shift(), pid = cur[0], d = cur[1];
      parents(pid).forEach(function (p) {
        if (map[p.id] === undefined || map[p.id] > d + 1) {
          map[p.id] = d + 1;
          queue.push([p.id, d + 1]);
        }
      });
    }
    return map;
  }
  function descendantMap(id) {
    var map = {}, queue = [[id, 0]];
    while (queue.length) {
      var cur = queue.shift();
      children(cur[0]).forEach(function (c) {
        if (map[c.id] === undefined) { map[c.id] = cur[1] + 1; queue.push([c.id, cur[1] + 1]); }
      });
    }
    return map;
  }

  /* ---------- Relationship calculator ---------- */
  function ordinal(n) {
    var s = ['th', 'st', 'nd', 'rd'], v = n % 100;
    return n + (s[(v - 20) % 10] || s[v] || s[0]);
  }
  function greats(n) { // n = number of "great"s
    if (n <= 0) return '';
    if (n === 1) return 'great-';
    if (n === 2) return 'great-great-';
    return ordinal(n) + ' great-';
  }
  function gendered(p, m, f, u) { return p.sex === 'M' ? m : p.sex === 'F' ? f : u; }

  /* Describe how `b` is related to `a` ("b is a's ___"). */
  function relationship(aId, bId) {
    if (aId === bId) return 'self';
    var a = get(aId), b = get(bId);
    if (!a || !b) return null;

    // Spouse?
    if (spouses(aId).some(function (s) { return s.id === bId; })) return gendered(b, 'husband', 'wife', 'spouse');

    var ancA = ancestorMap(aId); ancA[aId] = 0;
    var ancB = ancestorMap(bId); ancB[bId] = 0;

    var best = null;
    Object.keys(ancA).forEach(function (k) {
      if (ancB[k] !== undefined) {
        var total = ancA[k] + ancB[k];
        if (!best || total < best.total) best = { id: k, up: ancA[k], down: ancB[k], total: total };
      }
    });

    if (!best) {
      // In-law via spouse?
      var viaSpouse = null;
      spouses(aId).forEach(function (s) {
        if (viaSpouse) return;
        var r = relationshipBlood(s.id, bId);
        if (r && r !== 'self') viaSpouse = r + '-in-law';
      });
      if (viaSpouse) return viaSpouse;
      spouses(bId).forEach(function (s) {
        if (viaSpouse) return;
        var r = relationshipBlood(aId, s.id);
        if (r && r !== 'self') viaSpouse = gendered(b, 'husband', 'wife', 'spouse') + ' of ' + possessive(a) + ' ' + r;
      });
      return viaSpouse || 'no known blood relation';
    }
    return describe(best.up, best.down, b);
  }
  function possessive(p) { return gendered(p, 'his', 'her', 'their'); }

  function relationshipBlood(aId, bId) {
    if (aId === bId) return 'self';
    var ancA = ancestorMap(aId); ancA[aId] = 0;
    var ancB = ancestorMap(bId); ancB[bId] = 0;
    var best = null;
    Object.keys(ancA).forEach(function (k) {
      if (ancB[k] !== undefined) {
        var total = ancA[k] + ancB[k];
        if (!best || total < best.total) best = { up: ancA[k], down: ancB[k], total: total };
      }
    });
    return best ? describe(best.up, best.down, get(bId)) : null;
  }

  /* up = generations from A to common ancestor; down = generations from B. */
  function describe(up, down, b) {
    if (down === 0) { // b is an ancestor of a
      if (up === 1) return gendered(b, 'father', 'mother', 'parent');
      return greats(up - 2) + 'grand' + gendered(b, 'father', 'mother', 'parent');
    }
    if (up === 0) { // b is a descendant of a
      if (down === 1) return gendered(b, 'son', 'daughter', 'child');
      return greats(down - 2) + 'grand' + gendered(b, 'son', 'daughter', 'child');
    }
    if (up === 1 && down === 1) return gendered(b, 'brother', 'sister', 'sibling');
    if (down === 1) { // b is sibling of an ancestor of a
      return greats(up - 2) + gendered(b, 'uncle', 'aunt', 'aunt/uncle');
    }
    if (up === 1) { // b is descendant of a's sibling
      return greats(down - 2) + gendered(b, 'nephew', 'niece', 'nibling');
    }
    var degree = Math.min(up, down) - 1;
    var removed = Math.abs(up - down);
    var s = ordinal(degree) + ' cousin';
    if (removed) s += ' ' + (removed === 1 ? 'once' : removed === 2 ? 'twice' : removed + ' times') + ' removed';
    return s;
  }

  /* ---------- Search ---------- */
  function search(q) {
    q = (q || '').trim().toLowerCase();
    if (!q) return [];
    var terms = q.split(/\s+/);
    return raw.people.filter(function (p) {
      var hay = (fullName(p) + ' ' + (p.nickname || '') + ' ' + (p.birth && p.birth.place || '') + ' ' + (birthYear(p) || '')).toLowerCase();
      return terms.every(function (t) { return hay.indexOf(t) >= 0; });
    }).sort(function (a, b) { return fullName(a).localeCompare(fullName(b)); });
  }

  /* ---------- Events (for timeline) ---------- */
  function events() {
    var ev = [];
    raw.people.forEach(function (p) {
      if (p.birth && p.birth.date) ev.push({ type: 'birth', date: p.birth.date, place: p.birth.place, people: [p] });
      if (p.death && p.death.date) ev.push({ type: 'death', date: p.death.date, place: p.death.place, people: [p] });
      (p.events || []).forEach(function (e) {
        if (e.date) ev.push({ type: e.type || 'event', date: e.date, place: e.place, title: e.title, description: e.description, people: [p] });
      });
    });
    raw.families.forEach(function (f) {
      if (f.marriage && f.marriage.date) {
        ev.push({ type: 'marriage', date: f.marriage.date, place: f.marriage.place, people: [get(f.husband), get(f.wife)].filter(Boolean) });
      }
    });
    raw.stories.forEach(function (s) {
      if (s.date) ev.push({ type: 'story', date: s.date, title: s.title, story: s, people: (s.people || []).map(get).filter(Boolean) });
    });
    ev.forEach(function (e) { e.key = sortKey(e.date); });
    return ev.filter(function (e) { return e.key !== Infinity; }).sort(function (a, b) { return a.key - b.key; });
  }

  function surnames() {
    var counts = {};
    raw.people.forEach(function (p) { var s = p.surname || '(unknown)'; counts[s] = (counts[s] || 0) + 1; });
    return Object.keys(counts).map(function (k) { return { name: k, count: counts[k] }; })
      .sort(function (a, b) { return b.count - a.count || a.name.localeCompare(b.name); });
  }

  function rootPerson() {
    return get(raw.rootPerson) || raw.people[0] || null;
  }

  function storiesFor(id) { return raw.stories.filter(function (s) { return (s.people || []).indexOf(id) >= 0; }); }
  function photosFor(id) { return raw.photos.filter(function (s) { return (s.people || []).indexOf(id) >= 0; }); }

  window.Family = {
    raw: raw, title: raw.title || 'Our Family History', subtitle: raw.subtitle || '',
    get: get, all: all, families: raw.families, stories: raw.stories, photos: raw.photos,
    fullName: fullName, shortName: shortName, initials: initials,
    birthYear: birthYear, deathYear: deathYear, lifespan: lifespan, age: age, isDeceased: isDeceased,
    parseDate: parseDate, formatDate: formatDate, year: year, sortKey: sortKey,
    parents: parents, father: father, mother: mother, parentsFamily: parentsFamily,
    spouses: spouses, spouseFamilies: spouseFamilies, children: children, siblings: siblings, sortByBirth: sortByBirth,
    ancestorMap: ancestorMap, descendantMap: descendantMap, relationship: relationship,
    search: search, events: events, surnames: surnames, rootPerson: rootPerson,
    storiesFor: storiesFor, photosFor: photosFor, familyById: function (id) { return familiesById[id] || null; }
  };
})();
