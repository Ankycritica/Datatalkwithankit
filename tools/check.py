"""Validate the built site: HTML tag balance, internal links, JSON-LD, XML, vercel.json.
Run: python3 tools/check.py   (exit code 1 on any problem)"""
import html.parser, json, os, re, sys
import xml.dom.minidom as minidom

SITE_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "datatalkwithankit"))
VOIDS = {"meta", "link", "img", "br", "input", "hr", "source", "path", "rect", "circle", "line", "polyline"}
problems = []
os.chdir(SITE_DIR)
for f in ("rss.xml", "sitemap.xml"):
    try: minidom.parse(f)
    except Exception as e: problems.append(f"{f}: bad XML ({e})")
try: json.load(open("vercel.json"))
except Exception as e: problems.append(f"vercel.json: bad JSON ({e})")

for root, _, files in os.walk("."):
    for f in files:
        if not f.endswith(".html"): continue
        p = os.path.join(root, f); s = open(p).read()
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try: json.loads(block)
            except Exception as e: problems.append(f"{p}: bad JSON-LD ({e})")
        for u in re.findall(r'(?:href|src)="([^"#]+)"', s):
            if u.startswith(("http", "mailto", "data:", "/_vercel")): continue
            t = u.lstrip("/") or "index.html"
            if not (os.path.exists(t) or os.path.exists(t + ".html")): problems.append(f"{p}: broken link {u}")
        class P(html.parser.HTMLParser):
            def __init__(self): super().__init__(); self.stack = []
            def handle_starttag(self, t, a):
                if t not in VOIDS: self.stack.append(t)
            def handle_endtag(self, t):
                if t in VOIDS: return
                if self.stack and self.stack[-1] == t: self.stack.pop()
                else: problems.append(f"{p}: unexpected </{t}>")
        x = P(); x.feed(s)
        if x.stack: problems.append(f"{p}: unclosed {x.stack}")

print("\n".join(problems) if problems else "All checks passed.")
sys.exit(1 if problems else 0)
