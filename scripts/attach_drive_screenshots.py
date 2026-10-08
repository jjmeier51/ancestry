#!/usr/bin/env python3
"""Attach the owner's Google Drive screenshots (IMG_7791–IMG_7840, converted to JPEG)
to the people they document. Run once; re-running skips files already attached.

Usage: python3 scripts/attach_drive_screenshots.py /path/to/jpg-folder
"""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
SRC = sys.argv[1]
SOURCE = 'Owner\'s Ancestry app screenshot (Google Drive folder, Oct 2026)'
ME = 'I282604492552'; BULL = 'I282608065309'; ANDREW_PRINGLE = 'I282608053685'
PLAN = [
    # (file numbers, person id, title, type, extra people)
    ([7791], ME, 'Ancestry pedigree, paternal side with dates', 'document', ['I282604492836']),
    ([7792, 7794], 'I282608055482', 'Ancestry pedigree, Tuttle / Lamoreaux / Pringle colonial line', 'document', []),
    ([7793], 'I282608055977', 'Ancestry tree: parents shown for William Wells (unsupported per research)', 'document', []),
    ([7795, 7796], 'I282608056003', 'Ancestry tree: Youngs / Horne pedigree (unproven per research)', 'document', []),
    ([7797, 7798, 7799], BULL, 'Ancestry pedigree, Topping and Bull Smith branches', 'document', ['I282608083519']),
    ([7800], ME, 'Descent from Richard "Bull" Smith, earlier chart version', 'document', [BULL]),
    ([7801], BULL, 'Notes on the Smithtown bull statue "Whisper"', 'document', []),
    ([7802], ME, 'Descent from Richard "Bull" Smith, 13-generation chart', 'document', [BULL]),
    ([7803, 7804, 7829], 'I282608064885', 'Ancestry tree: Meier pedigree with placeholder parents', 'document', ['I282608064820']),
    ([7805, 7806, 7809], 'I282608064896', 'Ancestry tree: Black Forest pedigree (Birkenmayer, Heitzler, Federer, Begelspacher)', 'document', []),
    ([7807], 'I282608060536', 'Ancestry tree: Heffernan pedigree', 'document', ['I282608060497']),
    ([7808], 'I282608064637', 'Ancestry tree: Connole pedigree', 'document', []),
    ([7810, 7811, 7812], ANDREW_PRINGLE, '1850 US Census record page for Andrew Pringle (FamilySearch)', 'record', ['I282608053719', 'I282608053741']),
    ([7813], ANDREW_PRINGLE, '1850 US Census, Plymouth Township, Luzerne County, PA (page image)', 'record', ['I282608053719', 'I282608053741']),
    ([7814], BULL, 'Smith family history: list of illustrations (Abner and Joshua Smith houses)', 'document', []),
    ([7815, 7816], BULL, 'Pelletreau, Records of the Town of Smithtown (1898): Gardiner and Bailey descents', 'document', []),
    ([7817, 7818, 7819], BULL, 'Pelletreau: abstracts of Smith family wills', 'document', ['I282608065145']),
    ([7820, 7821, 7822], BULL, 'Pelletreau: Smith land records and 1736 survey map', 'document', []),
    ([7823], BULL, 'F. K. Smith, The Family of Richard Smith: Abner and Joshua Smith houses', 'document', []),
    ([7824, 7825, 7826, 7827], BULL, 'F. K. Smith, The Family of Richard Smith (1967), pp. 119–122', 'document', []),
    ([7828], ANDREW_PRINGLE, 'Ancestry tree: Pringle, Croup, Young and Doll view', 'document', ['I282608053719']),
    ([7830, 7831, 7832, 7835, 7836], 'I282695504114', 'Ancestry tree: Petriello, Di Marino, DiBiasi and Siconolfi lines', 'document', []),
    ([7833, 7834], 'I282695503559', 'Ancestry tree: Cognetti family and Cognetta ancestors', 'document', ['I282695503581']),
    ([7837, 7838, 7839, 7840], 'I282824815192', 'Ancestry tree: Ferlaino, Fiorillo and Colosimo lines', 'document', ['I282697102554']),
]
done = 0
for nums, pid, title, typ, extra in PLAN:
    for i, n in enumerate(nums):
        src = os.path.join(SRC, 'img_%d.jpg' % n)
        if not os.path.exists(src): print('missing', src); continue
        dest = 'media/%s/ancestry-screenshot-img-%d.jpg' % (pid, n)
        rpath = 'data/research/%s.json' % pid
        if os.path.exists(rpath) and any(m.get('file') == dest for m in json.load(open(rpath)).get('media', [])): continue
        t = title + (' (%d of %d)' % (i + 1, len(nums)) if len(nums) > 1 else '')
        cmd = [sys.executable, 'scripts/attach_media.py', pid, src, '--title', t, '--type', typ, '--source', SOURCE, '--date', '2026-10', '--no-build']
        if extra: cmd += ['--people', ','.join(extra)]
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL)
        # keep the chosen file name stable
        os.replace('media/%s/img_%d.jpg' % (pid, n), dest)
        r = json.load(open(rpath))
        for m in r['media']:
            if m.get('file') == 'media/%s/img_%d.jpg' % (pid, n): m['file'] = dest
        json.dump(r, open(rpath, 'w'), indent=2, ensure_ascii=False); open(rpath, 'a').write('\n')
        done += 1
print('attached', done, 'files')
