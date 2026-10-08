#!/usr/bin/env python3
"""Merge the project handoff (research/imported/Family_History_Handoff_2026-10.md)
into the data layer:

  data/additions.json      people and families the research added beyond the GEDCOM,
                           plus parent corrections for GEDCOM people
  data/research/<id>.json  one research file per person covered by the handoff
  data/stories.json        stories from section 5
  research/*.md            sections 4, 6 and 7 copied verbatim for reference
  data/handoff_ids.json    stable ids for people created from the handoff

Re-running is safe: ids are stable and files are rewritten from the handoff.
Hand edits to research files for handoff people will be overwritten, so put
later research in researchLog entries dated after the handoff, which are kept.

Usage:  python3 scripts/import_handoff.py [--dry-run]
"""
import json, os, re, sys, unicodedata, datetime
from collections import OrderedDict, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
HANDOFF = 'research/imported/Family_History_Handoff_2026-10.md'
TODAY = '2026-10-08'
DRY = '--dry-run' in sys.argv

# ---------------------------------------------------------------- name tools
TITLES = {'capt', 'captain', 'sir', 'rev', 'vicar', 'justice', 'ensign', 'maj', 'major', 'dr', 'hon', 'judge', 'lady', 'lord',
          'gen', 'general', 'col', 'colonel', 'lieut', 'lt', 'sen', 'senator', 'rep', 'mrs', 'mr', 'pfc', 'adm', 'rear', 'admiral',
          'mastro', 'donna', 'esq', 'first', 'reverend', 'bishop', 'cardinal', 'pope', 'president', 'mayor', 'count', 'countess', 'baron'}
SUFFIXES = {'jr', 'sr', 'ii', 'iii', 'iv', '2d', '2nd', '3d', '3rd', '4th'}
PARTICLES = {'di', 'de', 'da', 'del', 'della', 'dei', 'degli', 'la', 'le', 'van', 'von', 'der', 'den', 'mc', 'mac', 'o', 'd', 'du', 'st', 'saint'}
EQUIV = [{'croup', 'grub', 'croop', 'grupp'}, {'tuttle', 'tuthill'}, {'smith', 'smyth', 'smythe', 'smyith'}, {'doll', 'dull'},
         {'petriello', 'petrillo'}, {'connole', 'cannole'}, {'ferrantino', 'ferrandino'}, {'youngs', 'young', 'younges', 'yonges'},
         {'gianetta', 'giannetta', 'genett', 'gennetti', 'genetta'}, {'cognetti', 'cognetta'}, {'dibiasi', 'dibiase', 'dibias', 'biase', 'biasi'},
         {'meier', 'mayer', 'meyer', 'myer'}, {'birkenmayer', 'birkenmaier', 'birkenmeier', 'bergenmyer', 'birkenmeyer'},
         {'heitzler', 'heizler', 'haizler', 'haitzler'}, {'ferlaino', 'farino', 'farina'}, {'lamoreaux', 'lamoureux', 'lamoreux'},
         {'wells', 'welles'}, {'mcguire', 'maguire', 'mcgwire'}, {'begelspacher', 'begelsbacher'}, {'topping', 'toppin'},
         {'marrelli', 'morrello'}, {'federer', 'furderer', 'fuerderer'}, {'senn', 'sen'}, {'tuttle', 'tuthill'}, {'dimarino', 'marino'},
         {'siconolfi', 'siconolfi'}, {'cannatello', 'canatello'}, {'mcavoy', 'macavoy'}, {'heffernan', 'hefferman'}, {'prindle', 'pringle'}]
GIVEN_EQUIV = [{'francis', 'frank', 'francesco', 'franz', 'franciscus'}, {'friedrich', 'frederick', 'fred', 'freiderich', 'friederich', 'fredrick', 'federico'},
    {'heinrich', 'henry', 'henery', 'henericus', 'harry', 'enrico', 'heinrich'}, {'johann', 'john', 'giovanni', 'johnny', 'hans', 'jean', 'johannes', 'joannes', 'jonathan', 'ioannes'},
    {'wilhelm', 'william', 'willem', 'guillaume', 'bill'}, {'maria', 'mary', 'marie', 'mollie', 'molly', 'marya'}, {'catherine', 'kathryn', 'katharina', 'caterina', 'katherine', 'catharine', 'kate', 'catharina', 'katharine'},
    {'elizabeth', 'elisabeth', 'elisabetta', 'betty', 'elisabet', 'elisabetha', 'elizabetha', 'eliza'}, {'joseph', 'josef', 'giuseppe', 'josephus', 'joe'}, {'jacob', 'jakob', 'jacobus', 'james', 'giacomo', 'jim'},
    {'anna', 'anne', 'annie', 'ann', 'anneliese'}, {'agatha', 'agathe', 'agata'}, {'mathias', 'matthias', 'matthew', 'mattia', 'mathew'}, {'margaret', 'margaretha', 'margareta', 'peggy', 'margarethe', 'gretha'},
    {'andrew', 'andreas', 'andrea'}, {'peter', 'pietro', 'pierre', 'petrus'}, {'michael', 'michele', 'michel'}, {'nicholas', 'nicola', 'nikolaus', 'nicolaus'}, {'thomas', 'tommaso', 'tom'},
    {'charles', 'karl', 'carl', 'carlo', 'carolus'}, {'christopher', 'christoph', 'christoffel', 'kristof'}, {'richard', 'dick'}, {'dorothy', 'dorothea'}, {'theresa', 'teresa', 'therese'},
    {'julia', 'juliana', 'julie'}, {'george', 'georg', 'jurgen'}, {'martin', 'martinus'}, {'stephen', 'stephan', 'steven', 'stefano'}, {'edward', 'edwardi', 'eduard'},
    {'agnes', 'agnese'}, {'rosa', 'rose', 'rosalia'}, {'grace', 'grazia'}, {'josephine', 'giuseppina', 'josephina', 'giusepina'}, {'helen', 'elena', 'ellen', 'eleanor'},
    {'raphael', 'ralph', 'raffaele'}, {'leo', 'leopold', 'leopoldo'}, {'salvatore', 'sal', 'salvador'}, {'angela', 'angelica', 'angelina'}, {'carmela', 'carmella'}, {'vincent', 'vincenzo'},
    {'gabriel', 'gabriele'}, {'dominic', 'domenico', 'dominick'}, {'anthony', 'antonio', 'anton', 'antonino', 'antoninus'}, {'louis', 'luigi', 'ludwig', 'lewis'}, {'samuel', 'sam'},
    {'sarah', 'sara'}, {'hannah', 'anna'}, {'temperance', 't'}, {'jerusha'}, {'keturah'}, {'martha'}, {'florence', 'flo'}, {'kathleen', 'kathryn'}, {'patrick', 'pat'}, {'edward', 'ned'}]
GIVEN_MAP = {}
for i, g in enumerate(GIVEN_EQUIV):
    for w in g: GIVEN_MAP[w] = 'GV%d' % i
EQUIV_MAP = {}
for i, g in enumerate(EQUIV):
    for w in g: EQUIV_MAP[w] = 'EQ%d' % i

def plain(s):
    s = unicodedata.normalize('NFKD', s or '')
    return ''.join(c for c in s if not unicodedata.combining(c)).lower()

def skeleton(w):
    w = re.sub(r'[^a-z]', '', plain(w))
    if not w: return ''
    w = w.replace('ph', 'f').replace('ck', 'k').replace('tz', 'z').replace('th', 't').replace('sch', 'sh')
    w = re.sub(r'ch$', 'k', w)
    w = re.sub(r'c(?=[aoulrk])', 'k', w)
    w = w[0] + re.sub(r'[aeiouy]', '', w[1:])
    w = re.sub(r'(.)\1+', r'\1', w)
    w = re.sub(r's$', '', w) if len(w) > 2 else w
    return w

def surname_keys(s):
    out = set()
    s = re.sub(r'\(\w{1,2}\)', '', s or '')  # "Sm(y)ith" -> "Smith"
    toks = [t for t in re.split(r'[^a-z]+', plain(s)) if t]
    i = 0
    while i < len(toks):
        t = toks[i]
        if t in PARTICLES and i + 1 < len(toks):
            j = t + toks[i + 1]; out.add(EQUIV_MAP.get(j, skeleton(j))); i += 1
            # also plain next token
            out.add(EQUIV_MAP.get(toks[i], skeleton(toks[i])))
        elif t not in TITLES and t not in SUFFIXES and len(t) > 1:
            out.add(EQUIV_MAP.get(t, skeleton(t)))
        i += 1
    return {k for k in out if k}

def given_keys(s):
    s = re.sub(r'([a-z])([A-Z])', r'\1 \2', s or '')  # split CamelCase variants such as FrederickFriederich
    toks = [t for t in re.split(r'[^a-z]+', plain(s)) if t and t not in TITLES and t not in SUFFIXES]
    return [GIVEN_MAP.get(t, skeleton(t)) for t in toks if len(t) > 1]

def year_of(d):
    m = re.search(r'\d{4}', d or '')
    return int(m.group()) if m else None

def parse_name(name):
    """-> dict(prefix, given, surname, suffix, nickname, aka)"""
    nick = None; aka = []
    m = re.search(r'["“]([^"”]+)["”]', name)
    if m: nick = m.group(1); name = name.replace(m.group(0), ' ')
    for m in re.finditer(r'\(([^)]*)\)', name):
        aka.append(m.group(1))
    name = re.sub(r'\([^)]*\)', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip().strip(',')
    toks = name.split(' ')
    suffix = ''
    if toks and toks[-1].lower().strip('.') in SUFFIXES: suffix = toks.pop()
    prefix = []
    while toks and toks[0].lower().strip('.') in TITLES: prefix.append(toks.pop(0))
    if not toks: toks = prefix; prefix = []
    if len(toks) == 1:
        return {'prefix': ' '.join(prefix), 'given': toks[0], 'surname': '', 'suffix': suffix, 'nickname': nick, 'aka': aka}
    surname = toks[-1] if toks else ''
    rest = toks[:-1]
    while rest and rest[-1].lower() in PARTICLES:
        surname = rest.pop() + ' ' + surname
    return {'prefix': ' '.join(prefix), 'given': ' '.join(rest), 'surname': surname, 'suffix': suffix, 'nickname': nick, 'aka': aka}

def ref_parse(ref):
    """'Name (b. 1928)' -> (name, year|None)"""
    m = re.match(r'^(.*?)\s*\(b\.\s*([^)]*)\)\s*$', ref.strip())
    if m: return m.group(1).strip(), year_of(m.group(2))
    return ref.strip(), None

# ---------------------------------------------------------------- load
lines = open(HANDOFF, encoding='utf-8').read().split('\n')
def section(start_pat, end_pat):
    starts = [i for i, l in enumerate(lines) if re.match(start_pat, l)]
    s = starts[-1]
    e = next((i for i in range(s + 1, len(lines)) if re.match(end_pat, lines[i])), len(lines))
    return s, e

import copy
tree = json.load(open('data/tree.json'))
tree_people = tree['people']; tree_fams = tree['families']
TREE_FAMS_ORIG = copy.deepcopy(tree_fams)
tp_by_id = {p['id']: p for p in tree_people}
fam_child = {}
for f in tree_fams:
    for c in f.get('children', []): fam_child[c] = f

# handoff people
records = []
i = 0; heading = ''; sub = ''
while i < len(lines):
    l = lines[i]
    if l.startswith('### '): sub = l[4:].strip()
    if l.startswith('#### '): heading = l[5:].strip()
    if l.strip() == '```json':
        j = i + 1; buf = []
        while j < len(lines) and lines[j].strip() != '```': buf.append(lines[j]); j += 1
        obj = json.loads('\n'.join(buf)); obj['_line'] = i + 1; obj['_heading'] = heading; obj['_sub'] = sub
        records.append(obj); i = j
    i += 1
print('handoff records:', len(records))

# ---------------------------------------------------------------- matching
def person_keys(given, surname, extra_surname_src=''):
    return given_keys(given), surname_keys(surname) | surname_keys(extra_surname_src)

tree_index = []
for p in tree_people:
    gk, sk = person_keys(p.get('given', ''), p.get('surname', ''))
    # tree given names sometimes carry surname-ish words; add last given token as surname candidate too
    tree_index.append((p, gk, sk, year_of((p.get('birth') or {}).get('date')), p.get('sex', 'U')))

def score(gk, sk, yr, sex, cand, rec=None):
    p, cgk, csk, cyr, csex = cand
    if not (sk & csk): return -99
    hits = rel_overlap(rec, p['id']) if rec else 0
    s = min(hits, 2) * 3
    if gk and cgk:
        if gk == cgk and len(gk) > 1: s += 1
        if gk[0] == cgk[0]: s += 3
        elif gk[0] in cgk or cgk[0] in gk: s += 2
        elif set(gk) & set(cgk): s += 1
        else: return -99
    if yr and cyr:
        d = abs(yr - cyr)
        s += 3 if d == 0 else 2 if d <= 2 else 1 if d <= 5 else (-1 if hits else -6)
    if sex in 'MF' and csex in 'MF': s += 1 if sex == csex else -4
    return s

def match_tree(name, yr, sex=None, aka=None, rec=None):
    n = parse_name(name)
    gk, sk = person_keys(n['given'] or n['prefix'], n['surname'])
    for a in (aka or []):
        an = parse_name(a); sk |= surname_keys(an['surname'])
    best = []; bs = -99
    for cand in tree_index:
        s = score(gk, sk, yr, sex or 'U', cand, rec)
        if s > bs: bs, best = s, [cand[0]]
        elif s == bs and s > -99: best.append(cand[0])
    if bs >= 4 and len(best) == 1:
        p = best[0]; cyr = year_of((p.get('birth') or {}).get('date'))
        has_rel = rec and (rec.get('parents') or rec.get('spouses') or rec.get('children'))
        if yr and cyr and abs(yr - cyr) <= 5: return p, bs, best
        if rec and rel_overlap(rec, p['id']) >= 1: return p, bs, best
        if not has_rel and not cyr: return p, bs, best
        if not rec: return p, bs, best
        return None, bs, best
    return None, bs, best

ids_path = 'data/handoff_ids.json'
hid_map = json.load(open(ids_path)) if os.path.exists(ids_path) else {}
def hkey(name, yr): return '%s|%s' % (plain(name).strip(), yr or '')
def new_hid(key):
    if key in hid_map: return hid_map[key]
    n = 1 + max([int(v[1:]) for v in hid_map.values()] or [0])
    hid_map[key] = 'H%04d' % n
    return hid_map[key]

tree_spouses = defaultdict(list); tree_parents = defaultdict(list); tree_children = defaultdict(list)
for f in tree_fams:
    h, w = f.get('husband'), f.get('wife')
    if h and w: tree_spouses[h].append(w); tree_spouses[w].append(h)
    for c in f.get('children', []):
        for par in (h, w):
            if par: tree_parents[c].append(par); tree_children[par].append(c)
def rel_names(r):
    out = []
    for x in r.get('parents') or []: out.append(ref_parse(x)[0])
    for x in r.get('spouses') or []: out.append(ref_parse((x if isinstance(x, str) else x.get('name', '')))[0])
    for x in r.get('children') or []: out.append(ref_parse(x)[0])
    return out
def _keyset(nm):
    n = parse_name(nm); return (set(given_keys(n['given'] or n['prefix'])), surname_keys(n['surname']), ref_parse(nm)[1])
def rel_overlap(r, pid, first_token_only=False):
    """Role-aware count of the record's relatives that match the tree person's relatives (name keys, compatible years)."""
    roles = [('parents', tree_parents[pid]), ('spouses', tree_spouses[pid]), ('children', tree_children[pid])]
    hits = 0
    for role, tree_ids in roles:
        refs = r.get(role) or []
        for ref in refs:
            nm = ref if isinstance(ref, str) else ref.get('name', '')
            name, yr = ref_parse(nm)
            n = parse_name(name); gk = set(given_keys(n['given'] or n['prefix'])); sk = surname_keys(n['surname'])
            for tid in tree_ids:
                hp = tp_by_id.get(tid)
                if not hp: continue
                hgk = given_keys(hp.get('given', ''))
                if not (gk and hgk and (hgk[0] in gk if first_token_only else set(hgk) & gk)): continue
                if sk and not (surname_keys(hp.get('surname', '')) & sk): continue
                hyr = year_of((hp.get('birth') or {}).get('date'))
                if yr and hyr and abs(yr - hyr) > 5: continue
                hits += 1 if sk else 0.5; break
    return hits
matched = {}; unmatched = []; ambiguous = []; claimed = {}
def claim(r, p):
    if p['id'] in claimed:
        other = claimed[p['id']]
        same = 'duplicate' in r['name'].lower() or (plain(other['name']) == plain(r['name']) and [plain(x) for x in other.get('parents') or []] == [plain(x) for x in r.get('parents') or []] and (other.get('parents') or r.get('spouses') == other.get('spouses')))
        return same  # true duplicates merge; otherwise refuse
    claimed[p['id']] = r; return True
for r in records:
    yr = year_of((r.get('birth') or {}).get('date'))
    p, s, best = match_tree(r['name'], yr, r.get('sex'), r.get('aka'), r)
    if not p and len(best) > 1 and s >= 4:
        # disambiguate same-name candidates by relatives, then by tree duplicates (same name and year)
        scored = sorted(((rel_overlap(r, b['id']), b) for b in best), key=lambda x: -x[0])
        if scored[0][0] > 0 and (len(scored) == 1 or scored[0][0] > scored[1][0]): p = scored[0][1]
        elif len({(plain(b.get('given', '')), year_of((b.get('birth') or {}).get('date'))) for b in best}) == 1: p = best[0]
        else: ambiguous.append((r['name'], yr, [b['id'] for b in best]))
    if not p:
        # second pass: same given name + a matching spouse in the tree (handles married surnames such as "Mollie Petriello")
        n = parse_name(r['name']); gk = set(given_keys(n['given'] or n['prefix'])) | ({skeleton(n['nickname'])} if n['nickname'] else set())
        for a in r.get('aka') or []: gk |= set(given_keys(parse_name(a)['given']))
        cands = [tp for tp in tree_people if given_keys(tp.get('given', '')) and given_keys(tp.get('given', ''))[0] in gk and (not yr or not year_of((tp.get('birth') or {}).get('date')) or abs(year_of(tp['birth']['date']) - yr) <= 3)]
        cands = [c for c in cands if rel_overlap(r, c['id'], True) >= 1 and (r.get('spouses') or r.get('parents'))]
        if len(cands) == 1: p = cands[0]
    if p and not claim(r, p):
        p = None
    if p: r['_id'] = p['id']; matched[r['_line']] = p['id']
    else: r['_id'] = new_hid(hkey(r['name'], yr)); unmatched.append(r)
print('matched to tree:', len(matched), 'new people:', len(unmatched), 'ambiguous (kept separate):', len(ambiguous))
for a in ambiguous: print('   ambiguous:', a)

# index of handoff records by (name, year) for reference resolution
by_hkey = defaultdict(list)
for r in records:
    yr = year_of((r.get('birth') or {}).get('date'))
    by_hkey[hkey(r['name'], yr)].append(r)
    bare = re.sub(r'\([^)]*\)', ' ', r['name']).strip()
    if bare != r['name']: by_hkey[hkey(bare, yr)].append(r)
    for a in r.get('aka', []): by_hkey[hkey(re.sub(r'\([^)]*\)', ' ', a).strip(), yr)].append(r)

def spouse_of(pid):
    out = list(tree_spouses.get(pid, []))
    for f in add_fams:
        if f.get('husband') == pid and f.get('wife'): out.append(f['wife'])
        if f.get('wife') == pid and f.get('husband'): out.append(f['husband'])
    for rr in records:
        for sp in rr.get('spouses') or []:
            nm = sp if isinstance(sp, str) else sp.get('name', '')
            if rr.get('_id') == pid: out.append(('ref', nm))
    return out
def plausible(cand_year, role, anchor):
    if not cand_year or not anchor or not role: return True
    d = cand_year - anchor
    if role == 'parents': return -75 <= d <= -13
    if role == 'children': return 13 <= d <= 75
    if role == 'spouses': return abs(d) <= 30
    return True
def resolve_ref(ref, sex_hint=None, role=None, anchor=None):
    """Resolve 'Name (b. YYYY)' to an id (tree or H). Creates a stub if needed."""
    name, yr = ref_parse(ref)
    hint = re.search(r'\((?:wife|husband|widow|spouse) of ([^)]+)\)', name)
    bare = re.sub(r'\([^)]*\)', ' ', name).strip()
    if hint:
        hint_name = plain(re.sub(r'\(b\.[^)]*\)', '', hint.group(1))).strip()
        gk = set(given_keys(bare))
        for rr in records:
            rg = set(given_keys(parse_name(re.sub(r'\([^)]*\)', ' ', rr['name']).strip())['given'] or rr['name']))
            if not (rg & gk): continue
            for sp in rr.get('spouses') or []:
                nm = sp if isinstance(sp, str) else sp.get('name', '')
                if plain(re.sub(r'\([^)]*\)', ' ', ref_parse(nm)[0])).strip() == hint_name: return rr['_id']
        other = resolve_ref(hint.group(1).strip() + (' (b. unknown)' if '(b.' not in hint.group(1) else ''), None)
        if other:
            for sid in tree_spouses.get(other, []):
                if set(given_keys(tp_by_id[sid].get('given', ''))) & gk: return sid
        name = bare
    elif bare != name: name = bare
    if not name or plain(name) in ('unknown', 'unknown mother', 'unknown father', 'unknown parents', 'n/a', 'none'): return None
    cands = by_hkey.get(hkey(name, yr), [])
    if not cands:
        # same name, any year or no year
        cands = [r for k, rs in by_hkey.items() for r in rs if k.split('|')[0] == plain(name).strip()]
        if yr: cands = sorted(cands, key=lambda r: abs((year_of((r.get('birth') or {}).get('date')) or yr + 9) - yr))
        if yr and cands and abs((year_of((cands[0].get('birth') or {}).get('date')) or yr) - yr) > 5: cands = []
    cands = [c for c in cands if plausible(year_of((c.get('birth') or {}).get('date')), role, anchor)]
    if cands:
        return cands[0]['_id']
    p, s, best = match_tree(name, yr, sex_hint)
    if p and plausible(year_of((p.get('birth') or {}).get('date')), role, anchor): return p['id']
    key = hkey(name, yr)
    stub = STUBS.get(key)
    if not stub:
        n = parse_name(name)
        stub = OrderedDict(id=new_hid(key), given=n['given'] or n['prefix'], surname=n['surname'], sex=sex_hint or 'U')
        if n['prefix']: stub['prefix'] = n['prefix']
        if n['suffix']: stub['suffix'] = n['suffix']
        if yr: stub['birth'] = {'date': str(yr)}
        stub['_stub'] = True
        STUBS[key] = stub; STUBS_BY_ID[stub['id']] = stub
    return stub['id']
STUBS = {}

# ---------------------------------------------------------------- build additions + research
additions = OrderedDict(_comment='Generated by scripts/import_handoff.py from the project handoff. People and families the research added beyond the GEDCOM, plus parent corrections. Regenerate rather than hand-edit.',
                        people=[], families=[], setParents=[])
add_fams = []  # (husband, wife) -> family dict
def find_family(h, w):
    for f in tree_fams + add_fams:
        if (f.get('husband') or None) == (h or None) and (f.get('wife') or None) == (w or None): return f
    return None
def find_or_make_family(h, w, marriage=None):
    f = find_family(h, w)
    if not f and h and w:
        # a family with one spouse missing can be completed
        for g in tree_fams + add_fams:
            if g.get('husband') == h and not g.get('wife') and not any(x.get('husband') == h and x.get('wife') for x in tree_fams + add_fams): g['wife'] = w; f = g; break
            if g.get('wife') == w and not g.get('husband') and not any(x.get('wife') == w and x.get('husband') for x in tree_fams + add_fams): g['husband'] = h; f = g; break
    if not f:
        f = OrderedDict(id='HF%04d' % (len(add_fams) + 1), children=[])
        if h: f['husband'] = h
        if w: f['wife'] = w
        add_fams.append(f)
    if marriage and (marriage.get('date') or marriage.get('place')) and not f.get('marriage'):
        f['marriage'] = {k: v for k, v in marriage.items() if v}
    return f

all_people = dict(tp_by_id)
sex_of = lambda pid: (all_people.get(pid) or STUBS_BY_ID.get(pid) or {}).get('sex', 'U')
STUBS_BY_ID = {}

# first pass: register new people so sexes are known
for r in unmatched:
    n = parse_name(r['name'])
    p = OrderedDict(id=r['_id'], given=n['given'] or n['prefix'], surname=n['surname'], sex=(r.get('sex') or 'U')[:1].upper() if r.get('sex') else 'U')
    if n['prefix']: p['prefix'] = n['prefix']
    if n['suffix']: p['suffix'] = n['suffix']
    for k in ('birth', 'death'):
        if isinstance(r.get(k), dict) and (r[k].get('date') or r[k].get('place')): p[k] = {kk: vv for kk, vv in r[k].items() if vv}
    if r.get('occupation'): p['occupation'] = r['occupation']
    p['_handoff'] = True
    all_people[p['id']] = p
    additions['people'].append(p)

CONF = {'confirmed': 'confirmed', 'probable': 'probable', 'possible': 'possible', 'speculative': 'possible', 'unverified': 'unverified'}
def tags_for(r):
    t = set()
    text = ' '.join([r.get('notable') or '', r.get('summary') or '', r.get('bio') or '', r.get('occupation') or ''])
    if r.get('military'): t.add('military')
    if r.get('notable'): t.add('notable')
    if re.search(r'\b(emigrat|immigrat|arrived in (the )?(US|United States|America|New York|Philadelphia)|came to (the US|America)|sailed)', text, re.I) and r.get('confidence') != 'unverified': t.add('immigrant')
    if re.search(r'\b(Revolutionary (War )?(patriot|soldier|service|militia)|SAR P-|DAR A)', text): t.add('patriot')
    if re.search(r'\b(mayor|senator|congress|representative|city council|postmaster|assembly|governor|president of|sheriff|magistrate|justice of the peace|deputy)\b', r.get('notable') or '', re.I): t.add('politician')
    if re.search(r'\b(architect|painter|sculptor|author|poet|writer|composer|musician|preacher)\b', r.get('notable') or '', re.I): t.add('artist')
    if re.search(r'\b(baseball|football|athlete|olympic)\b', r.get('notable') or '', re.I): t.add('athlete')
    if re.search(r'\b(founder|founded|patentee|pioneer)\b', r.get('notable') or '', re.I): t.add('founder')
    if re.search(r'\b(Rev\.|minister|vicar|priest|missionary|clergy)\b', r.get('notable') or r.get('occupation') or ''): t.add('clergy')
    if re.search(r'\bfoundling\b', text, re.I): t.add('foundling')
    return sorted(t)

research_files = {}
conflicts = []
for r in records:
    pid = r['_id']; conf = CONF.get((r.get('confidence') or 'unverified').lower(), 'unverified')
    tree_p = tp_by_id.get(pid)
    rf = OrderedDict(id=pid)
    rf['link'] = {'confidence': conf, 'note': r.get('confidenceReason', '')}
    n = parse_name(r['name'])
    # name/vitals overrides for GEDCOM people when research is confirmed/probable
    log = []
    site_root = json.load(open('data/site.json')).get('rootPerson')
    if tree_p and conf in ('confirmed', 'probable') and pid != site_root:
        tname = ' '.join(x for x in [tree_p.get('given'), tree_p.get('surname')] if x)
        rname = ' '.join(x for x in [n['given'], n['surname']] if x)
        if plain(tname) != plain(rname):
            rf['given'] = n['given'] or tree_p.get('given'); rf['surname'] = n['surname'] or tree_p.get('surname')
            if n['prefix']: rf['prefix'] = n['prefix']
            if n['suffix']: rf['suffix'] = n['suffix']
            log.append('Name in the Ancestry tree: "%s"; research uses "%s".' % (tname, rname))
        for k in ('birth', 'death'):
            rv = r.get(k) if isinstance(r.get(k), dict) else None
            tv = tree_p.get(k) or {}
            if rv and (rv.get('date') or rv.get('place')):
                merged = {kk: vv for kk, vv in rv.items() if vv}
                for kk in ('date', 'place'):
                    if not merged.get(kk) and tv.get(kk): merged[kk] = tv[kk]
                if merged != {kk: vv for kk, vv in tv.items() if vv}:
                    rf[k] = merged
                    if tv.get('date') and rv.get('date') and year_of(tv['date']) != year_of(rv['date']):
                        log.append('%s in the Ancestry tree: %s; research: %s.' % (k.capitalize(), tv.get('date'), rv.get('date')))
        if r.get('sex') and r['sex'] in ('M', 'F') and tree_p.get('sex') != r['sex']: rf['sex'] = r['sex']
        if r.get('occupation') and r['occupation'] != tree_p.get('occupation'): rf['occupation'] = r['occupation']
    elif not tree_p:
        if r.get('sex') in ('M', 'F'): rf['sex'] = r['sex']
    if n['nickname']: rf['nickname'] = n['nickname']
    aka = [a for a in (r.get('aka') or []) if plain(a) != plain(r['name'])]
    if n['aka']: aka += n['aka']
    if aka: rf['aka'] = aka
    rf['tags'] = tags_for(r)
    for k in ('summary', 'bio', 'notable'):
        if r.get(k): rf[k] = r[k]
    for k in ('funFacts', 'residences', 'military', 'events', 'facts', 'sources', 'mediaKnown', 'openQuestions'):
        if r.get(k): rf[k] = r[k]
    if r.get('occupation') and not tree_p: rf['occupation'] = r['occupation']
    rf['handoff'] = {'section': r['_sub'], 'heading': r['_heading'], 'line': r['_line']}
    entries = [{'date': TODAY, 'note': 'Imported from the project handoff (research rounds 1–3, Oct 2026).'}]
    entries += [{'date': TODAY, 'note': x} for x in log]
    # keep researchLog entries written after the handoff on re-runs
    old_path = 'data/research/%s.json' % pid
    if os.path.exists(old_path):
        try:
            old = json.load(open(old_path))
            entries += [e for e in old.get('researchLog', []) if e.get('date', '') > TODAY]
            for m in old.get('media', []): rf.setdefault('media', []).append(m)
            if old.get('photo'): rf['photo'] = old['photo']
        except Exception: pass
    rf['researchLog'] = entries
    if pid in research_files:
        # duplicate record for same tree person: keep the more confident one, note the other
        prev = research_files[pid]
        order = ['unverified', 'possible', 'probable', 'confirmed']
        if order.index(conf) > order.index(prev['link']['confidence']): research_files[pid] = rf; rf['researchLog'].append({'date': TODAY, 'note': 'A second handoff record ("%s", line %d) also maps to this person.' % (prev['handoff']['heading'], prev['handoff']['line'])})
        else: prev['researchLog'].append({'date': TODAY, 'note': 'A second handoff record ("%s", line %d) also maps to this person.' % (r['_heading'], r['_line'])})
        continue
    research_files[pid] = rf

# relationships
relinks = 0; new_links = 0
for r in records:
    pid = r['_id']; conf = CONF.get((r.get('confidence') or 'unverified').lower(), 'unverified')
    anchor = year_of((r.get('birth') or {}).get('date'))
    parents = [resolve_ref(x, None, 'parents', anchor) for x in (r.get('parents') or [])]
    parents = [x for x in parents if x]
    if parents:
        father = next((x for x in parents if sex_of(x) == 'M'), None)
        mother = next((x for x in parents if sex_of(x) == 'F'), None)
        rest = [x for x in parents if x not in (father, mother)]
        if rest and not father: father = rest.pop(0)
        if rest and not mother: mother = rest.pop(0)
        cur = fam_child.get(pid)
        cur_pair = (cur.get('husband'), cur.get('wife')) if cur else None
        if cur_pair:
            for slot, tree_par in (('father', cur_pair[0]), ('mother', cur_pair[1])):
                cand = father if slot == 'father' else mother
                if cand and cand in STUBS_BY_ID and tree_par and tree_par in tp_by_id:
                    s = STUBS_BY_ID[cand]; tp = tp_by_id[tree_par]
                    if set(given_keys(s.get('given', ''))) & set(given_keys(tp.get('given', ''))):
                        if slot == 'father': father = tree_par
                        else: mother = tree_par
        if cur_pair and len(parents) == 1:
            if father and not mother and cur_pair[0] == father: mother = cur_pair[1]
            if mother and not father and cur_pair[1] == mother: father = cur_pair[0]
        if pid in tp_by_id:
            if cur_pair and {cur_pair[0], cur_pair[1]} - {None} == {father, mother} - {None}:
                pass
            elif conf in ('confirmed', 'probable'):
                additions['setParents'].append(OrderedDict(child=pid, father=father, mother=mother, reason=r.get('confidenceReason', ''), previous=list(cur_pair) if cur_pair else None))
                relinks += 1
                if cur_pair: conflicts.append((r['name'], cur_pair, (father, mother)))
            else:
                research_files[pid]['researchLog'].append({'date': TODAY, 'note': 'Handoff gives parents %s but the link is only "%s", so the tree was not changed.' % (', '.join(x for x in r['parents']), conf)})
        else:
            f = find_or_make_family(father, mother)
            if pid not in f['children']: f['children'].append(pid); new_links += 1
    for sp in (r.get('spouses') or []):
        if isinstance(sp, str): sp = {'name': sp}
        sid = resolve_ref(sp.get('name', ''), None, 'spouses', anchor)
        if not sid: continue
        a, b = pid, sid
        if sex_of(a) == 'F' or sex_of(b) == 'M': a, b = b, a
        f = find_family(a, b) or find_family(b, a)
        if not f: f = find_or_make_family(a, b, sp.get('married')); new_links += 1
        elif sp.get('married') and not f.get('marriage'): f['marriage'] = {k: v for k, v in sp['married'].items() if v}

def nm(pid):
    p = all_people.get(pid) or STUBS_BY_ID.get(pid)
    if not p: return str(pid)
    return '%s %s (%s)%s' % (p.get('given', ''), p.get('surname', ''), year_of((p.get('birth') or {}).get('date')) or '?', '' if pid in tp_by_id else ' [new]')
DEBUG = [a.split('=', 1)[1] for a in sys.argv if a.startswith('--debug=')]
for d in DEBUG:
    for r in records:
        if plain(r['name']).startswith(plain(d)):
            print('DEBUG', r['name'], 'line', r['_line'], '-> id', r['_id'], 'parents', r.get('parents'), 'spouses', r.get('spouses'))
            for ref in (r.get('parents') or []): print('      parent ref', ref, '->', resolve_ref(ref), nm(resolve_ref(ref)) if resolve_ref(ref) else '')
    for pid, p in list(tp_by_id.items()):
        if plain(p.get('given', '') + ' ' + p.get('surname', '')).startswith(plain(d)): print('DEBUG tree', pid, p.get('given'), p.get('surname'), 'claimed by', claimed.get(pid, {}).get('name'))
for s in STUBS.values():
    s = OrderedDict((k, v) for k, v in s.items() if not k.startswith('_'))
    additions['people'].append(s)
    research_files.setdefault(s['id'], OrderedDict(id=s['id'], link={'confidence': 'unverified', 'note': 'Named only as a relative in another person\'s handoff record; not researched.'}, tags=[], researchLog=[{'date': TODAY, 'note': 'Stub created from a handoff reference.'}]))
seen_ids = set(); deduped = []
for p in additions['people']:
    p.pop('_handoff', None); p.pop('_stub', None)
    if p['id'] in seen_ids or p['id'] in tp_by_id: continue
    seen_ids.add(p['id']); deduped.append(p)
additions['people'] = deduped
research_files = {k: v for k, v in research_files.items() if k in seen_ids or k in tp_by_id}
additions['families'] = add_fams
fam_updates = []
for f, o in zip(tree_fams, TREE_FAMS_ORIG):
    upd = {}
    for k in ('husband', 'wife'):
        if f.get(k) != o.get(k): upd[k] = f.get(k)
    added = [c for c in f.get('children', []) if c not in o.get('children', [])]
    if added: upd['addChildren'] = added
    if f.get('marriage') != o.get('marriage'): upd['marriage'] = f.get('marriage')
    if upd: upd['id'] = f['id']; fam_updates.append(upd)
additions['familyUpdates'] = fam_updates
print('existing families updated:', len(fam_updates))
print('new families:', len(add_fams), 'child links added:', new_links, 'parent corrections on GEDCOM people:', relinks, 'stubs:', len(STUBS))
for c in conflicts: print('   relink %s: %s + %s  ->  %s + %s' % (c[0], nm(c[1][0]), nm(c[1][1]), nm(c[2][0]), nm(c[2][1])))
if '--review' in sys.argv:
    print('--- matches ---')
    for r in records:
        if r['_id'] in tp_by_id:
            tp = tp_by_id[r['_id']]
            print('   %-40s (%s) -> %s %s (%s)' % (r['name'][:40], year_of((r.get('birth') or {}).get('date')) or '?', tp.get('given'), tp.get('surname'), year_of((tp.get('birth') or {}).get('date')) or '?'))

# ---------------------------------------------------------------- stories
s0, s1 = section(r'^## 5\. Stories\s*$', r'^## 6\. Sources')
stories = []; cur = None; key = None
for l in lines[s0:s1]:
    if l.startswith('#### '):
        cur = OrderedDict(id='S%03d' % (len(stories) + 1), title=l[5:].strip(), date='', people=[], body='', source=''); stories.append(cur); key = None; continue
    if cur is None: continue
    m = re.match(r'^\s*-\s*\**(Approximate date|People involved|Text|Source)\**:?\**\s*(.*)$', l)
    if m:
        key = {'Approximate date': 'date', 'People involved': 'people_raw', 'Text': 'body', 'Source': 'source'}[m.group(1)]
        cur[key] = (cur.get(key) or '') + m.group(2).strip()
        continue
    if key and l.strip():
        txt = re.sub(r'^\s*-\s*', '', l).strip() if key == 'body' else l.strip().lstrip('- ')
        cur[key] = (cur.get(key) or '') + ('\n' if key == 'body' else ' ') + txt
for s in stories:
    raw = s.pop('people_raw', '') or ''
    ids = []
    for part in re.split(r';\s*', raw):
        part = part.strip()
        if not part: continue
        m = re.match(r'^(.*?\(b\.[^)]*\))', part)
        ref = m.group(1) if m else part.split(',')[0]
        if re.search(r'\bnot kin\b|town-mates?|neighbou?r', part, re.I) and not m: continue
        rid = None
        name, yr = ref_parse(ref)
        c = by_hkey.get(hkey(name, yr)) or [x for k, xs in by_hkey.items() for x in xs if k.split('|')[0] == plain(name).strip()]
        if c: rid = c[0]['_id']
        else:
            p, sc, best = match_tree(name, yr)
            if p: rid = p['id']
        if rid and rid not in ids: ids.append(rid)
    s['people'] = ids
    s['body'] = re.sub(r'\n{2,}', '\n', s['body']).strip()
    s['date'] = re.sub(r'\*\*', '', s['date']).strip()
    s['source'] = re.sub(r'\*\*', '', s['source']).strip()
print('stories:', len(stories), 'with people:', sum(1 for s in stories if s['people']))

# ---------------------------------------------------------------- reference sections
def dump_section(start_pat, end_pat, path, title):
    a, b = section(start_pat, end_pat)
    body = '\n'.join(lines[a:b]).rstrip() + '\n'
    return path, '# %s\n\n*Copied verbatim from the project handoff (research/imported/Family_History_Handoff_2026-10.md), %s. Later findings go in research/LOG.md and data/research/.*\n\n' % (title, TODAY) + body
ref_docs = [dump_section(r'^## 4\. Family lines', r'^## 5\. Stories\s*$', 'research/lines.md', 'Family lines and lineage'),
            dump_section(r'^## 6\. Sources', r'^## 7\. Open questions', 'research/sources.md', 'Sources and research done'),
            dump_section(r'^## 7\. Open questions', r'^## 8\. Memory', 'research/open-questions.md', 'Open questions and next steps'),
            dump_section(r'^## 1\. Project instructions', r'^## 2\. Files in this project', 'research/owner-preferences.md', 'Owner instructions and preferences (from the handoff)')]

if DRY:
    print('dry run; nothing written'); sys.exit()
json.dump(additions, open('data/additions.json', 'w'), indent=1, ensure_ascii=False)
json.dump(hid_map, open(ids_path, 'w'), indent=1)
os.makedirs('data/research', exist_ok=True)
for fn in os.listdir('data/research'):
    pid = fn[:-5]
    if pid.startswith('H') and pid not in research_files: os.remove('data/research/' + fn)
for pid, rf in research_files.items():
    json.dump(rf, open('data/research/%s.json' % pid, 'w'), indent=2, ensure_ascii=False)
json.dump(stories, open('data/stories.json', 'w'), indent=2, ensure_ascii=False)
for path, text in ref_docs: open(path, 'w').write(text)
print('wrote additions.json, %d research files, %d stories, %d reference docs' % (len(research_files), len(stories), len(ref_docs)))
