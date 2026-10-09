#!/usr/bin/env python3
"""Link previews for Messages, WhatsApp, Slack and the like.

The site is hash-routed, so every #/person/... link looks the same to a link
crawler. This script writes, from the built data/family.js:

  images/og/default.png      the site card (1200x630)
  images/og/<id>.png         one card per person: portrait or initials, name,
                             lifespan, one-line summary
  p/<id>.html                a tiny page per person carrying the Open Graph
                             tags and a script that forwards to #/person/<id>
  s/<id>.html                the same for stories (site card)

Share links are https://<domain>/p/<id>. Cards are only regenerated when the
inputs change (hash kept in images/og/.manifest.json). Run by build.py; can be
run alone:  python3 scripts/build_share.py [--force]
"""
import hashlib, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
W, H = 1200, 630
BG = (10, 22, 40)
FONT_DIR = "/usr/share/fonts/opentype/inter"


def load_data():
    js = open("data/family.js", encoding="utf-8").read().split("window.FAMILY_DATA = ", 1)[1].rstrip().rstrip(";")
    return json.loads(js)


def year(s):
    m = re.search(r"\d{4}", str(s or ""))
    return m.group() if m else ""


def lifespan(p):
    b, d = year((p.get("birth") or {}).get("date")), year((p.get("death") or {}).get("date"))
    if b and d: return f"{b}–{d}"
    if b: return f"b. {b}" if not (p.get("death") or {}).get("date") and not (p.get("death") or {}).get("place") else f"{b}–?"
    if d: return f"d. {d}"
    return ""


def short_place(s):
    s = (s or "").split(",")
    return s[0].strip() if s else ""


def full_name(p):
    n = " ".join(x for x in (p.get("prefix"), p.get("given"), p.get("surname")) if x)
    if p.get("suffix"): n += " " + p["suffix"]
    return n or "Unknown"


def initials(p):
    parts = [x for x in ((p.get("given") or "").split(" ")[:1] + [(p.get("surname") or "")]) if x]
    return "".join(x[0] for x in parts).upper()[:2] or "?"


def description(p):
    if p.get("summary"): return p["summary"].strip()
    bits = []
    b, d = p.get("birth") or {}, p.get("death") or {}
    if b.get("date") or b.get("place"): bits.append("Born " + " ".join(x for x in (year(b.get("date")), short_place(b.get("place"))) if x))
    if d.get("date") or d.get("place"): bits.append("Died " + " ".join(x for x in (year(d.get("date")), short_place(d.get("place"))) if x))
    if p.get("occupation"): bits.append(p["occupation"])
    return " · ".join(bits) or "A member of the Meier family tree."


# ---------- cards ----------
def fonts():
    from PIL import ImageFont
    def f(name, size):
        try: return ImageFont.truetype(os.path.join(FONT_DIR, name), size)
        except OSError: return ImageFont.load_default()
    return f


def wrap(draw, text, font, width, max_lines):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= width: cur = t
        else:
            if cur: lines.append(cur)
            cur = w
        if len(lines) == max_lines: break
    if len(lines) < max_lines and cur: lines.append(cur)
    if len(lines) == max_lines and (len(words) > sum(len(l.split()) for l in lines)):
        last = lines[-1]
        while draw.textlength(last + "…", font=font) > width and " " in last: last = last.rsplit(" ", 1)[0]
        lines[-1] = last + "…"
    return lines


def base_card():
    from PIL import Image, ImageDraw
    # a smooth diagonal wash (dark navy to a slightly lighter navy) and a hairline frame, like the site
    im = Image.new("RGB", (2, 2)); im.putdata([(16, 34, 64), BG, BG, (8, 18, 34)])
    im = im.resize((W, H), Image.BILINEAR)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((18, 18, W - 18, H - 18), radius=28, outline=(45, 80, 140), width=2)
    return im, d


def circle_portrait(path, size):
    from PIL import Image, ImageDraw, ImageOps
    im = Image.open(path).convert("RGB")
    im = ImageOps.fit(im, (size, size), centering=(0.5, 0.35))
    mask = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size * 4 - 1, size * 4 - 1), fill=255)
    mask = mask.resize((size, size), Image.LANCZOS)
    out = Image.new("RGB", (size, size), BG); out.paste(im, (0, 0), mask)
    return out, mask


def draw_footer(d, f, site):
    d.text((70, H - 86), site.get("domain", ""), font=f("Inter-SemiBold.otf", 28), fill=(103, 232, 249))
    t = site.get("title", "")
    tw = d.textlength(t, font=f("Inter-Medium.otf", 26))
    d.text((W - 70 - tw, H - 85), t, font=f("Inter-Medium.otf", 26), fill=(120, 140, 175))


def person_card(p, site, out):
    from PIL import Image, ImageDraw
    f = fonts()
    im, d = base_card()
    size = 250
    cx, cy = 70, (H - size) // 2 - 10
    photo = p.get("photo")
    drew = False
    if photo and os.path.exists(photo):
        try:
            por, mask = circle_portrait(photo, size); im.paste(por, (cx, cy), mask); drew = True
        except Exception: drew = False
    if not drew:
        g = Image.new("RGB", (size, size), (79, 140, 255))  # flat brand blue: smooth gradients band after palette compression
        mask = Image.new("L", (size * 4, size * 4), 0); ImageDraw.Draw(mask).ellipse((0, 0, size * 4 - 1, size * 4 - 1), fill=255); mask = mask.resize((size, size), Image.LANCZOS)
        im.paste(g, (cx, cy), mask)
        ini = initials(p); fi = f("Inter-Bold.otf", 110)
        tw = d.textlength(ini, font=fi); d.text((cx + (size - tw) / 2, cy + size / 2 - 66), ini, font=fi, fill=(10, 22, 40))
    x = cx + size + 56; maxw = W - x - 70
    name = full_name(p)
    fn = f("Inter-Bold.otf", 64)
    lines = wrap(d, name, fn, maxw, 2)
    if len(lines) == 2: fn = f("Inter-Bold.otf", 54); lines = wrap(d, name, fn, maxw, 2)
    y = 150 if len(lines) == 1 else 112
    for ln in lines: d.text((x, y), ln, font=fn, fill=(240, 244, 255)); y += (fn.size + 8)
    occ = (p.get("occupation") or "").split(";")[0].split("(")[0].strip()
    meta = " · ".join(t for t in (lifespan(p), short_place((p.get("birth") or {}).get("place")), occ if len(occ) <= 32 else "") if t)
    if meta:
        d.text((x, y + 6), wrap(d, meta, f("Inter-Medium.otf", 32), maxw, 1)[0], font=f("Inter-Medium.otf", 32), fill=(103, 232, 249)); y += 50
    desc = description(p)
    fd = f("Inter-Regular.otf", 30)
    for ln in wrap(d, desc, fd, maxw, 3): d.text((x, y + 14), ln, font=fd, fill=(170, 185, 215)); y += 42
    draw_footer(d, f, site)
    im.convert("P", palette=Image.ADAPTIVE, colors=96).save(out, optimize=True)


def default_card(site, data, out):
    from PIL import Image
    f = fonts()
    im, d = base_card()
    x = 90
    d.text((x, 150), site.get("title", "Family tree"), font=f("Inter-Bold.otf", 84), fill=(240, 244, 255))
    d.text((x, 262), site.get("tagline", ""), font=f("Inter-Medium.otf", 38), fill=(103, 232, 249))
    c = data.get("counts") or {}
    stats = " · ".join(t for t in (f"{len(data.get('people', []))} people", f"{len(data.get('families', []))} families", f"{len(data.get('stories', []))} stories") if t)
    d.text((x, 340), stats, font=f("Inter-Regular.otf", 32), fill=(170, 185, 215))
    d.text((x, 392), "Explore the tree, the people, the places and the stories.", font=f("Inter-Regular.otf", 30), fill=(170, 185, 215))
    draw_footer(d, f, site)
    im.convert("P", palette=Image.ADAPTIVE, colors=96).save(out, optimize=True)


# ---------- pages ----------
def page(site, url, title, desc, image, forward, kind="article"):
    e = html.escape
    base = "https://" + site.get("domain", "")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)} · {e(site.get('title', ''))}</title>
<meta name="description" content="{e(desc)}"><meta name="robots" content="noindex">
<meta property="og:type" content="{kind}"><meta property="og:site_name" content="{e(site.get('title', ''))}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{base}/{image}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:url" content="{base}/{url}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{base}/{image}">
<meta name="theme-color" content="#0a1628"><link rel="icon" href="/icon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<script>location.replace({json.dumps('/' + forward)});</script>
<style>body{{margin:0;background:#0a1628;color:#dfe6f5;font:17px/1.5 Inter,system-ui,sans-serif;display:grid;place-items:center;min-height:100vh}}a{{color:#67e8f9}}</style>
</head><body><p>Opening <a href="/{e(forward)}">{e(title)}</a>…</p></body></html>
"""


def main(force=False):
    try:
        import PIL  # noqa: F401
    except ImportError:
        print("build_share: Pillow not installed; skipping share cards", file=sys.stderr); return
    data = load_data()
    site = {k: data.get(k) for k in ("title", "shortTitle", "tagline", "domain")}
    os.makedirs("images/og", exist_ok=True); os.makedirs("p", exist_ok=True); os.makedirs("s", exist_ok=True)
    mpath = "images/og/.manifest.json"
    manifest = json.load(open(mpath)) if os.path.exists(mpath) and not force else {}
    fresh = {}
    def key(obj):
        return hashlib.sha1(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
    made = 0
    k = key({"site": site, "counts": [len(data["people"]), len(data["families"]), len(data["stories"])], "v": 2})
    if manifest.get("default") != k or not os.path.exists("images/og/default.png"):
        default_card(site, data, "images/og/default.png"); made += 1
    fresh["default"] = k
    keep = {"default.png"}
    for p in data["people"]:
        pid = p["id"]
        inputs = {k2: p.get(k2) for k2 in ("given", "surname", "prefix", "suffix", "birth", "death", "occupation", "summary", "photo")}
        photo = p.get("photo")
        if photo and os.path.exists(photo): inputs["photo_mtime"] = int(os.path.getmtime(photo))
        inputs["v"] = 3
        k = key(inputs); fresh[pid] = k; keep.add(pid + ".png")
        out = f"images/og/{pid}.png"
        if manifest.get(pid) != k or not os.path.exists(out):
            person_card(p, site, out); made += 1
        title = full_name(p) + (f" ({lifespan(p)})" if lifespan(p) else "")
        open(f"p/{pid}.html", "w", encoding="utf-8").write(page(site, f"p/{pid}", title, description(p), f"images/og/{pid}.png", f"#/person/{pid}", "profile"))
    for s in data.get("stories", []):
        sid = s["id"]
        body = re.sub(r"\s+", " ", (s.get("body") or "")).strip()
        desc = (body[:200].rsplit(" ", 1)[0] + "…") if len(body) > 200 else body
        open(f"s/{sid}.html", "w", encoding="utf-8").write(page(site, f"s/{sid}", s.get("title", "Story"), desc, "images/og/default.png", f"#/stories/{sid}"))
    # prune cards and pages of people who no longer exist
    for fn in os.listdir("images/og"):
        if fn.endswith(".png") and fn not in keep: os.remove(os.path.join("images/og", fn))
    ids = {p["id"] for p in data["people"]}
    for fn in os.listdir("p"):
        if fn.endswith(".html") and fn[:-5] not in ids: os.remove(os.path.join("p", fn))
    sids = {s["id"] for s in data.get("stories", [])}
    for fn in os.listdir("s"):
        if fn.endswith(".html") and fn[:-5] not in sids: os.remove(os.path.join("s", fn))
    json.dump(fresh, open(mpath, "w"), indent=0, sort_keys=True)
    print(f"build_share: {made} cards drawn, {len(data['people'])} person pages, {len(data.get('stories', []))} story pages")


if __name__ == "__main__":
    main(force="--force" in sys.argv)
