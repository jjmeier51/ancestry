#!/usr/bin/env python3
"""Geocode every place name in the data with OpenStreetMap Nominatim and cache
the results in data/places.json (place string -> {lat, lon, label}).

Polite by design: one request per 1.1 s, a descriptive User-Agent naming the
site, and nothing re-queried once cached (failures are cached too, as null).
Run after adding people or places:  python3 scripts/geocode_places.py
"""
import json, os, re, sys, time, urllib.parse, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
CACHE = 'data/places.json'
UA = 'meiertree.com family-tree site (https://meiertree.com)'

def places_in(data):
    out = set()
    def add(s):
        s = (s or '').strip()
        if s and not re.fullmatch(r'[?\-–.]+', s): out.add(s)
    for p in data['people']:
        for k in ('birth', 'death', 'burial'):
            if isinstance(p.get(k), dict): add(p[k].get('place'))
        for r in p.get('residences') or []: add(r.get('place'))
        for e in p.get('events') or []: add(e.get('place'))
    for f in data['families']:
        for k in ('marriage', 'divorce'):
            if isinstance(f.get(k), dict): add(f[k].get('place'))
    return sorted(out)

def query(q):
    url = 'https://nominatim.openstreetmap.org/search?' + urllib.parse.urlencode({'q': q, 'format': 'jsonv2', 'limit': 1, 'accept-language': 'en'})
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

def clean(place):
    s = re.sub(r'\([^)]*\)', ' ', place)              # "(Inova Loudoun Hospital)"
    s = re.sub(r'\b(ABT|ABOUT|PROBABLY|NEAR|OF)\b\.?', ' ', s, flags=re.I)
    s = re.sub(r'\s+', ' ', s).strip(' ,;')
    return s

def main():
    js = open('data/family.js').read().split('window.FAMILY_DATA = ', 1)[1].rstrip().rstrip(';')
    data = json.loads(js)
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    todo = [p for p in places_in(data) if p not in cache]
    print('places: %d total, %d to geocode' % (len(places_in(data)), len(todo)), file=sys.stderr)
    done = 0
    for place in todo:
        q = clean(place); parts = [x.strip() for x in q.split(',') if x.strip()]
        result = None
        # try the full string, then drop leading components (hospital, street, hamlet) until something resolves
        for i in range(0, max(1, len(parts) - 1)):
            attempt = ', '.join(parts[i:])
            try:
                hits = query(attempt)
            except Exception as e:
                print('  error for %r: %s' % (attempt, e), file=sys.stderr); hits = []
            time.sleep(1.1)
            if hits:
                h = hits[0]
                result = {'lat': round(float(h['lat']), 5), 'lon': round(float(h['lon']), 5), 'label': h.get('display_name', attempt), 'matched': attempt, 'precision': 'exact' if i == 0 else 'approximate'}
                break
        cache[place] = result
        done += 1
        if done % 25 == 0:
            json.dump(cache, open(CACHE, 'w'), indent=1, ensure_ascii=False)
            print('  %d/%d' % (done, len(todo)), file=sys.stderr)
    json.dump(cache, open(CACHE, 'w'), indent=1, ensure_ascii=False)
    ok = sum(1 for v in cache.values() if v)
    print('cached %d places, %d resolved, %d unresolved' % (len(cache), ok, len(cache) - ok))

if __name__ == '__main__':
    main()
