import json, os, shutil
from memory_study import write_results, scenarios
from gpu_models import model_explorer, MODELS_REVIEWED_ISO, MODELS_REVIEWED_LABEL
from content import STUDY_TITLE, STUDY_DESC, STUDY_BODY, PIPELINE_TITLE, PIPELINE_DESC, PIPELINE_BODY
CONTENT_DATE = "2026-11-17"
OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "datatalkwithankit"))  # site folder Vercel deploys
SITE = "https://www.datatalkwithankit.com"
FONTS = "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans+Condensed:wght@500;600;700&family=IBM+Plex+Sans:ital,wght@0,400;0,500;0,600;1,400&display=swap"

FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8B6CFF"/><stop offset="1" stop-color="#2ED3EA"/></linearGradient></defs><rect width="64" height="64" rx="16" fill="#0C0B14"/><text x="32" y="45" font-family="Arial,Helvetica,sans-serif" font-size="38" font-weight="700" fill="url(#g)" text-anchor="middle">A</text></svg>"""

def head(title, desc, path, og_image="/og-image.png", og_type="website", extra="", robots="index, follow, max-image-preview:large, max-snippet:-1"):
    url = SITE + path
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="Ankit Dongare">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0C0B14">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="DatatalkwithAnkit" href="/rss.xml">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="DatatalkwithAnkit">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}{og_image}">
<script>try{{if(localStorage.getItem('theme')==='light')document.documentElement.setAttribute('data-theme','light')}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/style.css">
<script defer src="/_vercel/insights/script.js"></script>
{extra}</head>
<body>
"""

NAV = [("Writing", "/blog"), ("GPU guide", "/gpu-guide"), ("Studies", "/papers"), ("Projects", "/#projects"), ("Uses", "/uses"), ("Contact", "/#contact")]

def header(active=""):
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if n == active else ""}>{n}</a>' for n, h in NAV)
    return f"""<header class="site-head">
  <div class="wrap head-inner">
    <a class="wordmark" href="/" aria-label="DatatalkwithAnkit, home">Datatalkwith<b>Ankit</b></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-nav">Menu</button>
    <nav class="nav" id="main-nav" aria-label="Main">{links}</nav>
      <button class="theme" type="button" aria-label="Switch between light and dark theme">
        <svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
        <svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4.2"/><path d="M12 2v2.2M12 19.8V22M4.9 4.9l1.6 1.6M17.5 17.5l1.6 1.6M2 12h2.2M19.8 12H22M4.9 19.1l1.6-1.6M17.5 6.5l1.6-1.6"/></svg>
      </button>
  </div>
</header>
"""

FOOTER = """<footer class="site-foot">
  <div class="wrap foot-inner">
    <span>&copy; 2026 Ankit Dongare, Washington, DC</span>
    <nav aria-label="Footer">
      <a href="/blog">Writing</a><a href="/gpu-guide">GPU guide</a><a href="/papers">Studies</a><a href="/uses">Uses</a>
      <a href="/rss.xml">RSS feed</a><a href="https://github.com/Ankycritica">GitHub</a>
    </nav>
  </div>
</footer>
<script src="/site.js" defer></script>
</body>
</html>
"""

PERSON = {"@context": "https://schema.org", "@type": "Person", "name": "Ankit Dongare",
          "url": SITE, "jobTitle": "AI Engineer",
          "sameAs": ["https://github.com/Ankycritica", "https://youtube.com/@datatalkwithankit",
                     "https://instagram.com/datatalkwithankit", "https://aurapal.org"]}


# ---- GPU data: single source for calculator and guide ----
PRICE_DATE = "Nov 9, 2026"       # shown on the site; update with prices
PRICE_DATE_ISO = "2026-11-09"     # same date, ISO; drives dateModified and sitemap lastmod
GPUS = [  # key, vendor, name, mem GB, memory type, bandwidth TB/s, interconnect, software, lowest on-demand $/GPU-hr
    ("h100",   "nv",  "NVIDIA H100",  80,  "HBM3",  "3.35", "NVLink 4, 900 GB/s", "CUDA", 1.80),
    ("h200",   "nv",  "NVIDIA H200",  141, "HBM3e", "4.8",  "NVLink 4, 900 GB/s", "CUDA", 2.09),
    ("b200",   "nv",  "NVIDIA B200",  180, "HBM3e", "8",    "NVLink 5, 1.8 TB/s", "CUDA", 4.11),
    ("b300",   "nv",  "NVIDIA B300",  288, "HBM3e", "8",    "NVLink 5, 1.8 TB/s", "CUDA", 5.57),
    ("mi300x", "amd", "AMD MI300X",   192, "HBM3",  "5.3",  "Infinity Fabric",    "ROCm", 1.99),
    ("mi325x", "amd", "AMD MI325X",   256, "HBM3e", "6",    "Infinity Fabric",    "ROCm", 2.25),
    ("mi355x", "amd", "AMD MI355X",   288, "HBM3e", "8",    "Infinity Fabric",    "ROCm", 5.99),
]
# Newest first. Add an entry whenever prices or GPUs change.
GUIDE_UPDATED_ISO = max(PRICE_DATE_ISO, MODELS_REVIEWED_ISO)
GUIDE_UPDATED_LABEL = PRICE_DATE if PRICE_DATE_ISO >= MODELS_REVIEWED_ISO else MODELS_REVIEWED_LABEL
GUIDE_CHANGELOG = [
    ("Nov 20, 2026", "Added an AI model explorer with publisher model cards, precision comparisons, and capacity estimates across all seven GPUs."),
    ("Nov 9, 2026", "Prices refreshed: H100 $1.71 → $1.80, B200 $3.75 → $4.11, B300 $4.99 → $5.57, MI300X $2.39 → $1.99."),
    ("Oct 12, 2026", "First version. Covers H100, H200, B200, B300, MI300X, MI325X, and MI355X, with prices from getdeploying.com."),
]
FIT_ROWS = "".join(f"""      <div class="fit-row {v}" data-name="{n}" data-mem="{m}" data-rate="{r}">
        <div class="fit-name">{n}<small>{m} GB per GPU</small></div>
        <div class="fit-blocks"></div>
        <div class="fit-out"></div>
      </div>
""" for k, v, n, m, mt, bw, ic, sw, r in GPUS)

_maxr = max(g[8] for g in GPUS)
BOARD_ROWS = "".join(f"""      <div class="board-row {v}"><span class="bn">{n}<small>{m} GB</small></span><span class="bb"><i style="width:{r/_maxr*100:.0f}%"></i></span><span class="bp">${r:.2f}</span></div>
""" for k, v, n, m, mt, bw, ic, sw, r in sorted(GPUS, key=lambda g: g[8]))

WEBSITE = {"@context": "https://schema.org", "@type": "WebSite", "name": "DatatalkwithAnkit", "url": SITE,
           "description": "LLM inference benchmarks, GPU comparisons and prices, and AI market analysis by Ankit Dongare.",
           "author": {"@type": "Person", "name": "Ankit Dongare"}}

def crumbs(name, path):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": SITE + path}]}

def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>\n"

H200_ROW = """<a class="post-row" href="/posts/h200-vs-mi300x" data-tags="gpus cost memory benchmarking">
  <span class="when">Aug 21, 2026</span>
  <div><h3>H200 vs MI300X: what you're actually paying for</h3><p>Memory, interconnect, and price compared. What the extra 51 GB buys, why PCIe vs NVLink decides multi-GPU scaling, and what a GPU-hour really costs.</p></div>
  <span class="status live">9 min read</span>
</a>
"""

GUIDE_ROW = """<a class="post-row" href="/gpu-guide" data-tags="gpus cost memory">
  <span class="when">Updated """ + GUIDE_UPDATED_LABEL + """</span>
  <div><h3>Which GPU should you rent for LLM inference?</h3><p>H100, H200, B200, B300, MI300X, MI325X and MI355X compared: memory, bandwidth, GPUs per model, and price. Updated every quarter.</p></div>
  <span class="status live">Guide</span>
</a>
"""

STUDY_ROW = """<a class="post-row" href="/posts/llm-memory-capacity" data-tags="gpus cost memory quantization benchmarking">
  <span class="when">Nov 17, 2026</span>
  <div><h3>What fits in GPU memory? A reproducible capacity study</h3><p>105 calculated scenarios, with the Python script, input configuration, and complete CSV. Capacity estimates, with every assumption visible.</p></div>
  <span class="status live">Study · 6 min read</span>
</a>
"""
PIPELINE_ROW = """<a class="post-row" href="/projects/video-pipeline" data-tags="automation">
  <span class="when">Project case study</span>
  <div><h3>From a sourced story to a published video</h3><p>Connecting narration, rendering, captions, checks, and publishing in a Python workflow.</p></div>
  <span class="status live">3 min read</span>
</a>
"""

# ======================= HOME =======================
home = head("Ankit Dongare · LLM Inference Benchmarks & GPU Prices",
            "AI engineer benchmarking LLM inference. Compare H100, H200, B200, B300 and MI300X GPUs, see how many a model needs, and what it costs per hour.",
            "/", extra=ld(PERSON) + ld(WEBSITE))
home += header()
home += """<main>
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <p class="hero-who">Ankit Dongare, AI engineer</p>
      <h1>I measure what language models cost to run.</h1>
      <p class="hero-lede">I work on LLM inference: GPUs, serving configs, throughput, and price. Here I share comparisons, practical tools, and reproducible studies with the assumptions and inputs behind the numbers.</p>
      <div class="hero-actions">
        <a class="btn solid" href="/posts/llm-memory-capacity">Read the memory study</a>
        <a class="btn" href="#newsletter">Get new posts by email</a>
      </div>
      <div class="hero-links" aria-label="Explore the site">
        <a href="#fit-section">Capacity calculator <span aria-hidden="true">&rarr;</span></a>
        <a href="#ai-models">AI models <span aria-hidden="true">&rarr;</span></a>
        <a href="/gpu-guide">GPU guide <span aria-hidden="true">&rarr;</span></a>
        <a href="#projects">Selected projects <span aria-hidden="true">&rarr;</span></a>
      </div>
    </div>
    <aside class="board" aria-labelledby="board-title">
      <div class="board-head">
        <h2 id="board-title">GPU price board</h2>
        <span>Lowest on-demand $/GPU-hour &middot; """ + PRICE_DATE + """</span>
      </div>
""" + BOARD_ROWS + """      <a class="board-link" href="/gpu-guide">Compare all 7 in the GPU guide</a>
    </aside>
  </div>
</section>

<section class="section" id="fit-section" aria-labelledby="fit-title">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="fit-title">Will your model fit?</h2>
      <p>Choose a model size and weight precision. Compare the three lowest estimated hourly costs, or expand to all seven GPUs.</p>
    </div>
    <div class="fit" id="fit">
      <div class="fit-controls">
        <div>
          <span class="ctl-label" id="lbl-size">Model size, in billions of parameters</span>
          <div class="seg" id="fit-size" role="group" aria-labelledby="lbl-size">
            <button type="button" data-v="8" aria-pressed="false">8B</button>
            <button type="button" data-v="32" aria-pressed="false">32B</button>
            <button type="button" data-v="70" aria-pressed="true">70B</button>
            <button type="button" data-v="123" aria-pressed="false">123B</button>
            <button type="button" data-v="405" aria-pressed="false">405B</button>
          </div>
        </div>
        <div>
          <span class="ctl-label" id="lbl-prec">Weight precision</span>
          <div class="seg" id="fit-prec" role="group" aria-labelledby="lbl-prec">
            <button type="button" data-v="fp16" aria-pressed="true">FP16</button>
            <button type="button" data-v="fp8" aria-pressed="false">FP8</button>
            <button type="button" data-v="int4" aria-pressed="false">INT4</button>
          </div>
        </div>
      </div>
      <div class="fit-summary">
        <p class="fit-need" id="fit-need" aria-live="polite"></p>
        <p class="fit-best" id="fit-best" aria-live="polite"></p>
      </div>
      <div id="fit-results">
""" + FIT_ROWS + """      </div>
      <button class="btn fit-toggle" id="fit-toggle" type="button" aria-expanded="false" aria-controls="fit-results" hidden>Show all 7 GPUs</button>
      <div class="fit-foot">
        <p>Capacity estimates, using a 20% runtime allowance and power-of-two GPU counts. Actual fit depends on the model and workload. <a class="link" href="/posts/llm-memory-capacity">Method, code, and results</a>.</p>
        <p>Prices: <a class="link" href="https://getdeploying.com">getdeploying.com</a>, """ + PRICE_DATE + """. Listed on-demand rates; availability and node minimums vary.</p>
      </div>
    </div>
  </div>
</section>

""" + model_explorer(GPUS) + """
<section class="section" id="writing" aria-labelledby="writing-title">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="writing-title">Writing &amp; studies</h2>
      <p>Finished work you can read, inspect, and use.</p>
    </div>
    <a class="feature" href="/posts/llm-memory-capacity">
      <div>
        <p class="kicker">New study · Code + inputs + results</p>
        <h3>What fits in GPU memory?</h3>
        <p>Five model sizes, three weight precisions, seven GPUs. A reproducible worksheet for the capacity question behind every rental decision.</p>
        <p class="byline">Nov 17, 2026 · Calculated estimates · 6 min read</p>
      </div>
      <div class="study-preview" aria-label="70B model memory estimates: FP16 168 GB, FP8 84 GB, INT4 42 GB">
        <span class="chart-eyebrow">70B model · Memory budget</span>
        <div><b>FP16</b><span class="preview-track"><i style="width:100%"></i></span><strong>168 GB</strong></div>
        <div><b>FP8</b><span class="preview-track"><i style="width:50%"></i></span><strong>84 GB</strong></div>
        <div><b>INT4</b><span class="preview-track"><i style="width:25%"></i></span><strong>42 GB</strong></div>
        <small>Weights + 20% planning allowance</small>
      </div>
    </a>
    <div class="posts">
""" + GUIDE_ROW + H200_ROW + """    </div>
    <p class="more"><a class="link" href="/blog">Browse all writing</a></p>
  </div>
</section>

<section class="section" id="projects" aria-labelledby="projects-title">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="projects-title">Projects</h2>
      <p>Things I've built and run. More on <a class="link" href="https://github.com/Ankycritica">GitHub</a>.</p>
    </div>
    <div class="project-grid">
      <article class="project-card">
        <a class="project-shot" href="https://www.aurapal.org/" aria-label="Visit AuraPal">
          <span class="browser-bar" aria-hidden="true"><i></i><i></i><i></i><span>aurapal.org</span></span>
          <img src="/images/aurapal-project.jpg" alt="AuraPal's live career-tools homepage with resume tools and a salary comparison" width="1350" height="926" loading="lazy">
        </a>
        <div class="project-body">
          <p class="kicker">My product · Live</p><h3>AuraPal</h3>
          <p>An AI career platform I design, build, and run. From resumes to interview preparation, the focus is turning a complex task into a useful result.</p>
          <a class="link" href="https://www.aurapal.org/">Explore AuraPal <span aria-hidden="true">&rarr;</span></a>
        </div>
      </article>
      <article class="project-card">
        <a class="project-shot" href="https://ewg-jade.vercel.app/" aria-label="Visit EWG Solutions">
          <span class="browser-bar" aria-hidden="true"><i></i><i></i><i></i><span>EWG Solutions</span></span>
          <img src="/images/ewg-project.jpg" alt="EWG Solutions' live white-glove logistics website in black and gold" width="1350" height="926" loading="lazy">
        </a>
        <div class="project-body">
          <p class="kicker">Client website · Live</p><h3>Elite White Glove</h3>
          <p>A service website for a logistics business, with clear service pages and a direct path from learning about the company to requesting a quote.</p>
          <div class="project-links"><a class="link" href="https://ewg-jade.vercel.app/">Visit website <span aria-hidden="true">&rarr;</span></a><a class="link" href="https://github.com/Ankycritica/EWG">View source</a></div>
        </div>
      </article>
    </div>
    <div class="proj">
      <h3>Video publishing workflow</h3>
      <div><p>A Python workflow connecting source checks, narration, rendering, captions, and publishing.</p><span class="tech">Python, FFmpeg, Whisper, YouTube Data API</span></div>
      <a class="link" href="/projects/video-pipeline">Read case study</a>
    </div>
    <div class="proj">
      <h3>HNH Handyman</h3>
      <div><p>A service and booking website for a local handyman business.</p><span class="tech">TypeScript · <a class="link" href="https://hnh-handyman-liart.vercel.app/">Visit website</a></span></div>
      <a class="link" href="https://github.com/Ankycritica/hnhHandyman">View source</a>
    </div>
  </div>
</section>

<section class="section" id="about" aria-labelledby="about-title">
  <div class="wrap">
    <div class="sec-head"><h2 id="about-title">About</h2></div>
    <div class="about-grid">
      <div class="about-text">
        <p>I’m Ankit, an AI engineer based in the Washington, DC area. I started with data analytics and kept following the harder questions until they led to building AI systems full time.</p>
        <p>Today I work on the practical side of large language models: how they're served, how fast they run, what they cost, and how configuration choices change all three. At work I benchmark and evaluate an enterprise LLM inference platform, measuring throughput, latency, and cost across models, serving configs, and hardware.</p>
        <p>That data background still shapes how I work. I trust measurements over opinions, and if I do something twice, I write a script for it.</p>
        <p class="stack-line">Day to day: Python, PyTorch, vLLM, Hugging Face, Docker, and AWS. The full list is on the <a class="link" href="/uses">uses page</a>.</p>
      </div>
      <div class="about-person">
        <figure class="about-portrait">
          <img src="/images/ankit-about.jpg" alt="Ankit Dongare in Washington, DC" width="1000" height="1250" loading="lazy">
          <figcaption>Ankit Dongare <span>AI engineer · Builder</span></figcaption>
        </figure>
        <ul class="creds">
          <li><strong>Inference benchmarking</strong>Evaluating an enterprise LLM inference platform at work</li>
          <li><strong>Product builder</strong>Designs, ships, and runs <a class="link" href="https://aurapal.org">Aurapal</a> in production</li>
          <li><strong>Engineer by training</strong>Mechanical engineering degree, then data analytics, then AI</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section" id="contact" aria-labelledby="contact-title">
  <div class="wrap">
    <div class="sec-head">
      <h2 id="contact-title">Stay in touch</h2>
      <p>Get new posts by email, or send me a note about a benchmark, a collaboration, or Aurapal.</p>
    </div>
    <div class="connect">
      <div class="panel" id="newsletter">
        <h2>The newsletter</h2>
        <p>New studies and write-ups, sent when they're published. Request updates by email, or follow the RSS feed.</p>
        <form id="subscribe" class="inline-form" novalidate>
          <label class="sr-only" for="sub-email">Email address</label>
          <input id="sub-email" type="email" placeholder="you@example.com" autocomplete="email">
          <button class="btn solid" type="submit">Request updates</button>
        </form>
        <p class="note">Opens your email app with a signup request for you to send.</p>
        <div class="socials">
          <a href="https://youtube.com/@datatalkwithankit">YouTube</a>
          <a href="https://instagram.com/datatalkwithankit">Instagram</a>
          <a href="https://github.com/Ankycritica">GitHub</a>
          <a href="/rss.xml">RSS feed</a>
        </div>
      </div>
      <form class="panel" id="contact-form" novalidate>
        <h2>Send a message</h2>
        <label class="field"><span>Name</span><input name="name" type="text" autocomplete="name"></label>
        <label class="field"><span>Email</span><input name="email" type="email" autocomplete="email"></label>
        <label class="field"><span>Message</span><textarea name="message" rows="4"></textarea></label>
        <button class="btn solid" type="submit">Send message</button>
        <p class="note">Opens your email app. I usually reply within two days. Or email <a class="link" href="mailto:dongare.ankit29@gmail.com">dongare.ankit29@gmail.com</a>.</p>
      </form>
    </div>
  </div>
</section>
</main>
"""
home += FOOTER
open(os.path.join(OUT, "index.html"), "w").write(home)

# ======================= BLOG =======================
blog = head("Writing on GPUs & LLM Inference · DatatalkwithAnkit",
            "Posts on LLM inference, GPUs, serving configs, and cost, by Ankit Dongare. Comparisons and reproducible studies with explicit assumptions, source code, and calculated results.",
            "/blog")
blog += header("Writing")
blog += """<main class="wrap">
  <div class="page-head">
    <h1>Writing</h1>
    <p>GPU comparisons, LLM inference benchmarks, and notes on the AI market. Benchmarks ship with the configs that produced them.</p>
  </div>
  <div class="filters" id="filters" role="group" aria-label="Filter posts by topic">
    <button type="button" data-tag="all" aria-pressed="true">All posts</button>
    <button type="button" data-tag="gpus" aria-pressed="false">GPUs</button>
    <button type="button" data-tag="vllm" aria-pressed="false">vLLM</button>
    <button type="button" data-tag="benchmarking" aria-pressed="false">Benchmarking</button>
    <button type="button" data-tag="cost" aria-pressed="false">Cost</button>
    <button type="button" data-tag="memory" aria-pressed="false">Memory</button>
    <button type="button" data-tag="quantization" aria-pressed="false">Quantization</button>
    <button type="button" data-tag="automation" aria-pressed="false">Automation</button>
  </div>
  <div class="posts">
""" + STUDY_ROW + GUIDE_ROW + H200_ROW + PIPELINE_ROW + """  </div>
  <p id="empty" class="note" hidden>No posts on that topic yet. Pick another, or <a class="link" href="/#newsletter">subscribe</a> to hear when one lands.</p>
  <div class="panel" style="margin:56px 0 72px">
    <h2>Get new posts by email</h2>
    <p>New GPU and AI infrastructure posts, sent when they're published.</p>
    <a class="btn solid" href="/#newsletter">Subscribe</a>
  </div>
</main>
"""
blog += FOOTER
open(os.path.join(OUT, "blog.html"), "w").write(blog)

# ======================= PAPERS =======================
papers = head("Studies & Benchmark Method · DatatalkwithAnkit",
              "Completed capacity studies, downloadable code and results, and a practical method for reproducible LLM inference experiments by Ankit Dongare.",
              "/papers")
papers += header("Studies")
papers += """<main class="wrap">
  <div class="page-head">
    <h1>Studies &amp; method</h1>
    <p>Completed work with inspectable inputs, followed by the method I use to plan inference experiments.</p>
  </div>
  <div class="posts">
""" + STUDY_ROW + """  </div>
  <p class="note">The capacity study reports calculated estimates. Future hardware benchmarks will include measured results and the configurations that produced them.</p>

  <section class="section" style="border-top:0;padding-bottom:40px" aria-labelledby="method-title">
    <div class="sec-head"><h2 id="method-title">How I run an experiment</h2><p>A practical checklist for a reproducible serving experiment.</p></div>
    <ol class="steps">
      <li><h3>Ask one narrow question</h3><p>Something a number can answer, not an opinion.</p></li>
      <li><h3>Fix the setup</h3><p>Same hardware, model, and workload. Warm up properly and record every parameter that could move the result.</p></li>
      <li><h3>Measure the spread</h3><p>Multiple runs, reported as a range. Latency gets percentiles, never an average alone.</p></li>
      <li><h3>Publish the raw data</h3><p>Configs, scripts, and unedited results go up next to the write-up.</p></li>
      <li><h3>Report what failed</h3><p>Runs that contradict the hypothesis get written up too. They're usually the useful ones.</p></li>
      <li><h3>Find the next question</h3><p>Every result raises a sharper question, and that becomes the next experiment.</p></li>
    </ol>
  </section>
  <div class="panel" style="margin:16px 0 72px">
    <h2>Want to collaborate on a write-up?</h2>
    <p>If you're working on LLM evaluation or inference and want a second pair of hands, I'd like to hear about it.</p>
    <a class="btn solid" href="/#contact">Send a message</a>
  </div>
</main>
"""
papers += FOOTER
open(os.path.join(OUT, "papers.html"), "w").write(papers)

# ======================= USES =======================
uses = head("Tools for LLM Benchmarking · DatatalkwithAnkit",
            "The tools, frameworks, and services Ankit Dongare uses for LLM benchmarking, building, and automation.",
            "/uses")
uses += header("Uses")
uses += """<main class="wrap uses">
  <div class="page-head">
    <h1>What I use</h1>
    <p>The tools behind the benchmarks and builds on this site. The hardware for each experiment is listed inside that post, because a result without its machine isn't a result.</p>
  </div>
  <dl style="margin-bottom:72px">
    <div class="uses-row"><dt>Serving and training</dt><dd>vLLM, PyTorch, Hugging Face Transformers, CUDA<small>vLLM is where most of my benchmarking time goes.</small></dd></div>
    <div class="uses-row"><dt>Evaluation</dt><dd>A benchmark harness I'm building, plus MLflow<small>I plan to open-source the harness alongside the first full benchmark post.</small></dd></div>
    <div class="uses-row"><dt>Infrastructure</dt><dd>Docker, AWS, GCP, Azure, and neocloud GPU providers</dd></div>
    <div class="uses-row"><dt>Building</dt><dd>Python, TypeScript, Next.js, FastAPI, SQL, Supabase</dd></div>
    <div class="uses-row"><dt>Automation</dt><dd>Python scripts, FFmpeg, Whisper, the YouTube Data API<small>If I do something twice, it becomes a script.</small></dd></div>
    <div class="uses-row"><dt>Editor</dt><dd>VS Code with a terminal always open beside it</dd></div>
    <div class="uses-row"><dt>This site</dt><dd>Plain HTML, CSS, and a little JavaScript, hosted on Vercel and deployed from GitHub<small>Set in IBM Plex.</small></dd></div>
  </dl>
</main>
"""
uses += FOOTER
open(os.path.join(OUT, "uses.html"), "w").write(uses)

# ======================= POST: H200 vs MI300X =======================
POST_DESC = "NVIDIA H200 vs AMD MI300X for LLM inference: what the extra 51 GB of memory buys, NVLink vs PCIe scaling, and real neocloud prices per GPU-hour."
article_ld = {"@context": "https://schema.org", "@type": "BlogPosting",
              "headline": "H200 vs MI300X: what you're actually paying for",
              "description": POST_DESC, "datePublished": "2026-08-21", "dateModified": "2026-10-11",
              "author": {"@type": "Person", "name": "Ankit Dongare", "url": SITE},
              "image": SITE + "/og-h200-vs-mi300x.png",
              "mainEntityOfPage": SITE + "/posts/h200-vs-mi300x",
              "keywords": "NVIDIA H200, AMD MI300X, NVLink, PCIe, LLM inference, vLLM, GPU pricing, neocloud, HBM3e, ROCm, KV cache"}
extra = ld(article_ld) + ld(crumbs("H200 vs MI300X", "/posts/h200-vs-mi300x")) + '<meta name="keywords" content="NVIDIA H200, AMD MI300X, H200 vs MI300X, NVLink vs PCIe, LLM inference, GPU pricing, neocloud, HBM3e, ROCm, KV cache">\n<meta property="article:published_time" content="2026-08-21">\n<meta property="article:author" content="Ankit Dongare">\n'
post = head("H200 vs MI300X: Memory, NVLink & Price Compared", POST_DESC,
            "/posts/h200-vs-mi300x", og_image="/og-h200-vs-mi300x.png", og_type="article", extra=extra)
post += header("Writing")
post += """<main class="wrap">
<article class="article">
  <a class="crumb" href="/blog">Back to all writing</a>
  <h1>H200 vs MI300X: what you're actually paying for</h1>
  <div class="byline-row">
    <span class="byline-avatar" aria-hidden="true"><img src="/images/ankit-about.jpg" alt="" width="120" height="150" loading="lazy"></span>
    <div><strong>Ankit Dongare</strong>Aug 21, 2026, 9 minute read</div>
  </div>
  <div class="prose">
    <p>I spent a chunk of last month on a question that sounds simple. Fixed budget, a 70B model to serve. Which GPU do I rent?</p>
    <p>Every comparison I found opened with a TFLOPS table, which is close to useless for what I was doing. Token generation isn't compute-bound. It's memory-bound. Your GPU spends most of the decode phase waiting on memory rather than doing math, so a chart of peak FLOPS is describing a bottleneck you don't have.</p>
    <p>Here's what I found once I started looking at the parts that matter.</p>

    <h2>The H200 is an H100 with better memory</h2>
    <p>That's not a criticism, it's the design. Same GH100 die, same Tensor Cores, same peak FLOPS. NVIDIA swapped the memory subsystem: six stacks of 24 GB HBM3e instead of five of 16 GB HBM3. You get 141 GB at 4.8 TB/s where the H100 gave you 80 GB at 3.35 TB/s.</p>
    <p>The consequence is more interesting than the spec. H100 and H200 perform almost identically on prefill, since chewing through your prompt is compute-bound and the compute didn't change. The gap only opens during decode. Serving chat means you live in decode, so you feel the whole 43% bandwidth increase. Doing bulk document processing with short outputs, you might barely notice.</p>
    <p>The MI300X got to its numbers a different way. AMD went chiplet, eight compute dies and four I/O dies stitched together with Infinity Fabric, and that packaging is what allowed 192 GB of HBM3 at 5.3 TB/s. More capacity <em>and</em> more bandwidth than the H200.</p>

    <figure class="figure">
      <div class="table-scroll">
      <table class="spec">
        <thead><tr><th scope="col"><span class="sr-only">Spec</span></th><th scope="col">H200 SXM</th><th scope="col">MI300X</th></tr></thead>
        <tbody>
          <tr><th scope="row">Memory</th><td>141 GB HBM3e</td><td>192 GB HBM3</td></tr>
          <tr><th scope="row">Bandwidth</th><td>4.8 TB/s</td><td>5.3 TB/s</td></tr>
          <tr><th scope="row">Architecture</th><td>Hopper, monolithic</td><td>CDNA 3, chiplet</td></tr>
          <tr><th scope="row">Power</th><td>700 W</td><td>750 W</td></tr>
          <tr><th scope="row">GPU to GPU</th><td>NVLink, 900 GB/s</td><td>Infinity Fabric, about 896 GB/s</td></tr>
          <tr><th scope="row">Software</th><td>CUDA</td><td>ROCm</td></tr>
        </tbody>
      </table>
      </div>
      <figcaption>Headline specs for the SXM and OAM versions of each GPU.</figcaption>
    </figure>

    <p>On memory, AMD wins. That part isn't really debatable. Whether it matters is a different question.</p>

    <h2>What the extra 51 GB is actually for</h2>
    <p>The useful question isn't which number is bigger. It's how many GPUs you need to hold your model.</p>
    <p>Weights run about 2 bytes per parameter at FP16, roughly 1 at FP8. Then there's KV cache, which grows with batch size and context length, and which in my experience is what actually breaks things. People size for weights, forget cache, then wonder why throughput falls apart at batch 32.</p>
    <p>A 70B model at FP16 is around 140 GB of weights. That technically fits in an H200's 141 GB and leaves you nothing for cache, so realistically you're running two. The same model on an MI300X leaves roughly 50 GB of headroom. One GPU.</p>
    <p>That's the real pitch, more than the bandwidth number. When a model fits on one device you delete a whole category of problems: no tensor parallelism, no per-layer synchronization, one thing to fail instead of eight. I'd take that simplification over a few percent of bandwidth most days.</p>
    <div class="callout"><p>Try other sizes in the <a href="/#fit-section">will-it-fit calculator</a> on the home page.</p></div>

    <h2>PCIe or NVLink, and why it decides everything above one GPU</h2>
    <p>PCIe Gen5 x16 moves about 128 GB/s bidirectional. NVLink on an H200 SXM moves 900 GB/s per GPU. Roughly seven times the bandwidth, and it's the entire reason SXM nodes exist as a product.</p>

    <figure class="figure">
      <div class="mini-chart" role="img" aria-label="GPU to GPU bandwidth: PCIe Gen5 128 GB per second, NVLink 900 GB per second">
        <div class="mc-row"><b>PCIe 5</b><div class="mc-track"><div class="mc-fill c" style="width:14%"></div></div><span>128 GB/s</span></div>
        <div class="mc-row"><b>NVLink</b><div class="mc-track"><div class="mc-fill v" style="width:100%"></div></div><span>900 GB/s</span></div>
      </div>
      <figcaption>GPU-to-GPU bandwidth, bidirectional, per GPU.</figcaption>
    </figure>

    <p>Why that gap matters so much: tensor parallelism splits each layer across GPUs, so every layer needs an all-reduce, for every token. Eighty layers and a few hundred output tokens means tens of thousands of collectives per request. Over PCIe that collective becomes the bottleneck, and you end up with expensive silicon sitting idle waiting on its neighbours.</p>
    <p>The heuristic I've settled on: PCIe is fine when each GPU runs its own copy of the model. You want NVLink when GPUs have to cooperate on one model. Four independent replicas of a 30B? PCIe cards, save the money. One 405B split eight ways? The interconnect is the thing you're buying, not the GPU.</p>
    <p>There's also an H200 NVL variant, a PCIe card that bridges up to four GPUs over NVLink. It exists for standard air-cooled racks that can't host an 8-GPU SXM baseboard. Useful, but slower than SXM once you're doing serious tensor-parallel work.</p>
    <p>One correction while I'm here, because it caught me out. Several sites list the H200 as having NVLink 5.0 at 1.8 TB/s. It doesn't. H200 is Hopper, so it's NVLink 4.0 at 900 GB/s. The 1.8 TB/s figure belongs to Blackwell. I'd built half a spreadsheet on the wrong number before I noticed, so if you're comparing tables, check that row.</p>

    <h2>Going from 1 to 8</h2>
    <p>Nobody gets linear scaling. Here's what each step buys:</p>
    <ul>
      <li><strong>One GPU</strong> is simplest and often fastest per token, assuming it fits. Zero collectives.</li>
      <li><strong>Two</strong> is the cheapest way to double memory, with a direct peer link and modest overhead.</li>
      <li><strong>Four</strong> tends to be the sweet spot for serving 70B-class models at volume.</li>
      <li><strong>Eight</strong> is the standard node, an HGX H200 or an eight-way MI300X box. On the NVIDIA side you get a full NVSwitch fabric, so any GPU talks to any other at full speed.</li>
    </ul>
    <p>This is where the picture flips. In published 8-GPU training comparisons, NVLink nodes land around 87% scaling efficiency against roughly 78% for MI300X, and the gap grows with node count. Per-chip memory doesn't help you when the constraint is how well eight chips pretend to be one.</p>
    <p>So AMD wins when you're trying to use fewer GPUs, and NVIDIA wins when you need many working together. Those are different problems, and people conflate them constantly.</p>

    <h2>What it costs, and who the neoclouds are</h2>
    <p>Neocloud is the label for GPU specialists like CoreWeave, Lambda, Nebius, Crusoe, RunPod, and GMI, as opposed to the big three. They undercut hyperscalers because selling compute is the whole business rather than a line item carrying a lot of platform overhead.</p>
    <p>The spread is genuinely wide. Published H200 rates this year have run from around $2.60 an hour at the cheap end to $6.31 at CoreWeave. That's about $2,600 a month on a single GPU, or somewhere near $21,000 a month across eight, for identical silicon. MI300X has come down further, as low as roughly $1.71 an hour at Crusoe, with spot going under a dollar.</p>
    <p>Run the memory-per-dollar math and it's stark. An H200 at $2.60 is about $0.018 per GB-hour. An MI300X at $1.71 is about $0.009. Half the price for the same gigabyte.</p>
    <p>Before acting on that, though, the hourly rate isn't the bill:</p>
    <ul>
      <li><strong>Minimum node size.</strong> CoreWeave won't sell you fewer than eight GPUs. You pay for the node whether you use it or not.</li>
      <li><strong>Egress.</strong> Moving weights and datasets out can quietly eat the savings. Some providers charge nothing, some very much do.</li>
      <li><strong>Preemption.</strong> Cheap often means spot. Fine for training with checkpoints, bad for anything user-facing.</li>
      <li><strong>Utilization.</strong> A GPU you rent and don't saturate is the most expensive one you'll ever buy.</li>
    </ul>
    <p>That last one is the one I keep relearning.</p>

    <h2>How I'd choose</h2>
    <p>I'd reach for the MI300X when the model fits in 192 GB but not 141 GB, when I'm serving long contexts where KV cache dominates, when the stack is already vLLM or SGLang on ROCm, and when cost per gigabyte matters more than shaving the last few milliseconds.</p>
    <p>I'd reach for the H200 when I'm doing tensor parallelism at four or eight GPUs, when I depend on CUDA-specific kernels, when latency consistency is a product requirement rather than a nice-to-have, or when I'm training rather than serving.</p>
    <p>Reduced to one line: AMD sells memory, NVIDIA sells interconnect and a software stack that already works. Which is the better buy depends on whether your problem is fitting the model or making a pile of GPUs behave like one.</p>
    <p>For the capacity calculation behind these choices, see the <a href="/posts/llm-memory-capacity">reproducible memory study</a>, with code, inputs, and calculated results. If a number here is wrong or has gone stale, <a href="/#contact">tell me</a> and I'll fix it.</p>
    <p style="color:var(--muted);font-size:.95rem"><em>Figures checked August 2026. GPU pricing moves fast, so check current rates before deciding anything on them.</em></p>
  </div>
  <div class="share">
    <span>Share this post</span>
    <a class="btn" href="https://twitter.com/intent/tweet?text=H200%20vs%20MI300X%3A%20what%20you%27re%20actually%20paying%20for&amp;url=https%3A%2F%2Fwww.datatalkwithankit.com%2Fposts%2Fh200-vs-mi300x">Post on X</a>
    <a class="btn" href="https://news.ycombinator.com/submitlink?u=https%3A%2F%2Fwww.datatalkwithankit.com%2Fposts%2Fh200-vs-mi300x&amp;t=H200%20vs%20MI300X%3A%20what%20you%27re%20actually%20paying%20for">Submit to Hacker News</a>
    <button class="btn" type="button" id="copy-link">Copy link</button>
  </div>
</article>
<div class="article-end">
  <div class="panel" style="margin:24px 0 72px">
    <h2>Get the next one by email</h2>
    <p>New studies and practical notes, with the assumptions and inputs behind the numbers.</p>
    <a class="btn solid" href="/#newsletter">Subscribe</a>
  </div>
</div>
</main>
"""
post += FOOTER
open(os.path.join(OUT, "posts", "h200-vs-mi300x.html"), "w").write(post)

# ======================= GUIDE: which GPU =======================
import math
GUIDE_DESC = "How many H100, H200, B200, B300, MI300X, MI325X or MI355X GPUs your LLM needs, open-weight AI model examples by GPU, and dated rental-price comparisons."
SIZES = (8, 32, 70, 123, 405)
def g_count(need, mem):
    n = max(1, math.ceil(need / mem))
    p = 1
    while p < n: p *= 2
    return p
def g_cell(n):
    return f"{n}" if n <= 8 else f"{n}<small class='sub'>{n // 8} nodes</small>"
def fit_table(bytes_pp, label):
    head_cells = "".join(f'<th scope="col">{z}B<small class="sub">{round(z*bytes_pp*1.2)} GB</small></th>' for z in SIZES)
    rows = ""
    for k, v, n, m, mt, bw, ic, sw, r in GPUS:
        cells = "".join(f"<td>{g_cell(g_count(z*bytes_pp*1.2, m))}</td>" for z in SIZES)
        rows += f'<tr><th scope="row">{n.split(" ",1)[1]}<small class="sub">{m} GB</small></th>{cells}</tr>\n'
    return f"""<table class="spec plain fit-table" data-prec="{label}"{" hidden" if label == "fp8" else ""}>
        <thead><tr><th scope="col">GPU</th>{head_cells}</tr></thead>
        <tbody>
{rows}        </tbody>
      </table>"""
spec_rows = "".join(
    f'<tr><th scope="row">{n}</th><td>{m} GB {mt}</td><td>{bw} TB/s</td><td>{ic}</td><td>{sw}</td></tr>\n'
    for k, v, n, m, mt, bw, ic, sw, r in GPUS)
price_rows = "".join(
    f'<tr><th scope="row">{n}</th><td>${r:.2f}</td><td>${r/m:.3f}</td></tr>\n'
    for k, v, n, m, mt, bw, ic, sw, r in sorted(GPUS, key=lambda g: g[8] / g[3]))
def _counts(size, bpp):
    return ", ".join(f"{g_count(size*bpp*1.2, m)} {n}" for k, v, n, m, mt, bw, ic, sw, r in GPUS)
_cheap_hr = min(GPUS, key=lambda g: g[8])
_cheap_gb = min(GPUS, key=lambda g: g[8] / g[3])
FAQ = [
    ("How much GPU memory does a 70B model need?",
     "About 140 GB for the weights at FP16, or about 70 GB at FP8. Add room for the KV cache: with 20% headroom that is about 168 GB at FP16 and 84 GB at FP8. Long contexts and large batches need more."),
    ("How many GPUs do I need to run a 70B model?",
     "At FP16 (about 168 GB with headroom): " + _counts(70, 2) + ". At FP8 (about 84 GB): " + _counts(70, 1) + ". Counts round up to 1, 2, 4 or 8 for tensor parallelism."),
    ("How many GPUs do I need to run a 405B model?",
     "At FP8 (about 486 GB with headroom): " + _counts(405, 1) + ". At FP16 (about 972 GB): " + _counts(405, 2) + ". Above 8 GPUs means more than one 8-GPU node."),
    ("Which GPU is cheapest for LLM inference?",
     f"By hourly rate, {_cheap_hr[2]} at about ${_cheap_hr[8]:.2f} per GPU-hour. By cost per GB of memory, {_cheap_gb[2]} at about ${_cheap_gb[8]/_cheap_gb[3]:.3f} per GB-hour. Prices are the lowest listed on-demand rates on getdeploying.com, " + PRICE_DATE + "."),
    ("What is the difference between the H100 and the H200?",
     "They use the same compute die. The H200 has 141 GB of HBM3e at 4.8 TB/s versus 80 GB of HBM3 at 3.35 TB/s on the H100, so it holds bigger models and generates tokens faster, while prompt processing speed is about the same."),
    ("What is the difference between the B200 and the B300?",
     "Both are NVIDIA Blackwell GPUs with 8 TB/s of memory bandwidth and NVLink 5 at 1.8 TB/s. The B300 has 288 GB of HBM3e versus 180 GB on the B200, so it fits larger models on fewer GPUs."),
]
FAQ_LD = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
FAQ_HTML = "".join(f"<details class=\"faq\"><summary>{q}</summary><p>{a}</p></details>\n" for q, a in FAQ)
guide_ld = {"@context": "https://schema.org", "@type": "TechArticle",
            "headline": "Which GPU should you rent for LLM inference?",
            "description": GUIDE_DESC, "datePublished": "2026-10-12", "dateModified": GUIDE_UPDATED_ISO,
            "author": {"@type": "Person", "name": "Ankit Dongare", "url": SITE},
            "mainEntityOfPage": SITE + "/gpu-guide", "image": SITE + "/og-gpu-guide.png",
            "keywords": "GPU for LLM inference, H100, H200, B200, B300, MI300X, MI325X, MI355X, GPU memory, tensor parallelism, NVLink, GPU rental price"}
guide = head("Best GPU for LLM Inference (2026): H100 to MI355X", GUIDE_DESC, "/gpu-guide",
             og_image="/og-gpu-guide.png", og_type="article", extra=ld(guide_ld) + ld(FAQ_LD) + ld(crumbs("GPU guide", "/gpu-guide")))
guide += header("GPU guide")
guide += """<main class="wrap">
<article class="article wide">
  <a class="crumb" href="/blog">Back to all writing</a>
  <p class="kicker-line">Living guide &middot; Last updated """ + GUIDE_UPDATED_LABEL + """</p>
  <h1>Which GPU should you rent for LLM inference?</h1>
  <div class="byline-row">
    <span class="byline-avatar" aria-hidden="true"><img src="/images/ankit-about.jpg" alt="" width="120" height="150" loading="lazy"></span>
    <div><strong>Ankit Dongare</strong>Covers 7 data-center GPUs. Updated every quarter.</div>
  </div>
  <div class="prose">
    <div class="tldr">
      <p class="tldr-h">The short version</p>
      <ol>
        <li><strong>Size the memory first.</strong> Token generation is memory-bound, so capacity and bandwidth matter more than peak FLOPS.</li>
        <li><strong>Fit on one GPU if you can.</strong> It removes tensor parallelism, synchronization, and most failure modes. The 256 to 288 GB GPUs (MI325X, B300, MI355X) fit much more on one device.</li>
        <li><strong>If you need several GPUs on one model, pay for the interconnect.</strong> NVLink nodes scale better than PCIe cards.</li>
        <li><strong>Compare the bill, not the hourly rate.</strong> Minimum node sizes, egress, preemption, and idle time change the real cost.</li>
      </ol>
    </div>

""" + model_explorer(GPUS, guide=True) + """
    <h2>Step 1: How many GPUs does your model need?</h2>
    <p>Weights take about 2 bytes per parameter at FP16 and about 1 at FP8. On top of that you need room for the KV cache, which grows with batch size and context length. I add 20% headroom as a starting point. Long contexts or big batches need more.</p>
    <p>Counts round up to 1, 2, 4 or 8, because tensor parallelism splits a model evenly across GPUs. Above 8 means more than one 8-GPU node.</p>
    <figure class="figure">
      <div class="seg guide-prec" id="guide-prec" role="group" aria-label="Precision">
        <button type="button" data-v="fp16" aria-pressed="true">FP16</button>
        <button type="button" data-v="fp8" aria-pressed="false">FP8</button>
      </div>
      <div class="table-scroll">
      """ + fit_table(2, "fp16") + """
      """ + fit_table(1, "fp8") + """
      </div>
      <figcaption>GPUs needed per model copy. Column headers show memory needed: parameters &times; bytes per parameter &times; 1.2.</figcaption>
    </figure>
    <div class="callout"><p>Try other sizes, including INT4, in the <a href="/#fit-section">will-it-fit calculator</a>.</p></div>

    <h2>Step 2: Compare the specs that matter for inference</h2>
    <figure class="figure">
      <div class="table-scroll">
      <table class="spec plain">
        <thead><tr><th scope="col">GPU</th><th scope="col">Memory</th><th scope="col">Bandwidth</th><th scope="col">GPU to GPU</th><th scope="col">Software</th></tr></thead>
        <tbody>
""" + spec_rows + """        </tbody>
      </table>
      </div>
      <figcaption>Vendor specs per GPU (SXM/OAM versions). NVLink figures are total bidirectional bandwidth per GPU.</figcaption>
    </figure>
    <p>Because decode is memory-bound, bandwidth sets the ceiling on tokens per second per GPU. The H200 has 43% more bandwidth than the H100 on the same compute die. B200, B300, and MI355X all reach 8 TB/s, about 2.4 times an H100.</p>

    <h2>Step 3: One GPU, or several working together?</h2>
    <ul>
      <li><strong>Each GPU runs its own copy of the model:</strong> PCIe cards are fine. Save the money.</li>
      <li><strong>Several GPUs share one model (tensor parallelism):</strong> every layer needs an all-reduce for every token, so the GPU-to-GPU link becomes the bottleneck. NVLink 4 moves 900 GB/s per GPU and NVLink 5 doubles that to 1.8 TB/s, versus about 128 GB/s for PCIe Gen5 x16. Buy SXM nodes.</li>
      <li><strong>Scaling to 8 GPUs:</strong> in published 8-GPU training comparisons of H200 and MI300X, NVLink nodes reached around 87% scaling efficiency versus roughly 78% for MI300X.</li>
    </ul>

    <h2>Step 4: Check the price, then the real bill</h2>
    <p>Lowest listed on-demand price per GPU-hour, sorted by price per GB of memory:</p>
    <figure class="figure">
      <div class="table-scroll">
      <table class="spec plain">
        <thead><tr><th scope="col">GPU</th><th scope="col">Per hour</th><th scope="col">Per GB per hour</th></tr></thead>
        <tbody>
""" + price_rows + """        </tbody>
      </table>
      </div>
      <figcaption>Source: lowest listed on-demand rates on <a href="https://getdeploying.com">getdeploying.com</a>, """ + PRICE_DATE + """. Some of the cheapest offers are not verified in stock, and prices change weekly.</figcaption>
    </figure>
    <p>Before you commit, check four things that change the real cost:</p>
    <ul>
      <li><strong>Minimum node size.</strong> Some providers only sell full 8-GPU nodes.</li>
      <li><strong>Egress.</strong> Moving weights and data out can erase the savings.</li>
      <li><strong>Preemption.</strong> Cheap is often spot, which is bad for anything user-facing.</li>
      <li><strong>Utilization.</strong> A GPU you rent and don't keep busy is the most expensive one.</li>
    </ul>

    <h2>My picks</h2>
    <figure class="figure">
      <div class="table-scroll">
      <table class="spec plain picks">
        <thead><tr><th scope="col">If you are&hellip;</th><th scope="col">Start with</th></tr></thead>
        <tbody>
          <tr><th scope="row">Serving a small model, 32B or under at FP8</th><td>H100, the cheapest per hour</td></tr>
          <tr><th scope="row">Fitting the most model per dollar of memory</th><td>MI325X, then MI300X</td></tr>
          <tr><th scope="row">Fitting the biggest model on one GPU</th><td>B300 or MI355X, 288 GB</td></tr>
          <tr><th scope="row">Chasing the highest tokens per second per GPU</th><td>B200, B300 or MI355X, 8 TB/s</td></tr>
          <tr><th scope="row">Running tensor parallelism across 4 or 8 GPUs</th><td>B200 or B300 on NVLink 5</td></tr>
          <tr><th scope="row">Depending on CUDA-only kernels</th><td>Any NVIDIA option</td></tr>
        </tbody>
      </table>
      </div>
    </figure>
    <p>For a deeper comparison of two of these, read <a href="/posts/h200-vs-mi300x">H200 vs MI300X: what you're actually paying for</a>.</p>

    <h2>Frequently asked questions</h2>
""" + FAQ_HTML + """
    <h2>Changelog</h2>
    <ul class="changelog">
""" + "".join(f"      <li><strong>{d}:</strong> {t}</li>\n" for d, t in GUIDE_CHANGELOG) + """
    </ul>
    <p style="color:var(--muted);font-size:.95rem"><em>Figures are estimates for planning, not quotes. If a number here is wrong or has gone stale, <a href="/#contact">tell me</a> and I'll fix it.</em></p>
  </div>
  <div class="share">
    <span>Share this guide</span>
    <a class="btn" href="https://twitter.com/intent/tweet?text=Which%20GPU%20should%20you%20rent%20for%20LLM%20inference%3F&amp;url=https%3A%2F%2Fwww.datatalkwithankit.com%2Fgpu-guide">Post on X</a>
    <button class="btn" type="button" id="copy-link">Copy link</button>
  </div>
</article>
<div class="article-end">
  <div class="panel" style="margin:24px 0 72px">
    <h2>Get updates when this guide changes</h2>
    <p>I update it every quarter with new prices and hardware.</p>
    <a class="btn solid" href="/#newsletter">Subscribe</a>
  </div>
</div>
</main>
"""
guide += FOOTER
open(os.path.join(OUT, "gpu-guide.html"), "w").write(guide)

# ======================= REPRODUCIBLE STUDY + CASE STUDY =======================
DOWNLOADS = os.path.join(OUT, "downloads")
os.makedirs(DOWNLOADS, exist_ok=True)
os.makedirs(os.path.join(OUT, "projects"), exist_ok=True)
STUDY_CONFIG = {
    "description": "Calculated memory capacity and dated rental-cost scenarios; not a hardware benchmark.",
    "memory_units": "decimal GB",
    "headroom_fraction": 0.2,
    "candidate_gpu_counts": "Powers of two; a planning convention, not a guarantee of model parallelism support.",
    "model_billions": [8, 32, 70, 123, 405],
    "bytes_per_parameter": {"FP16": 2, "FP8": 1, "INT4": 0.5},
    "price_date": PRICE_DATE_ISO,
    "price_source": "https://getdeploying.com",
    "gpus": [{"key": k, "name": n, "memory_gb": m, "hourly_usd": r} for k, v, n, m, mt, bw, ic, sw, r in GPUS],
}
open(os.path.join(DOWNLOADS, "memory-study-config.json"), "w").write(json.dumps(STUDY_CONFIG, indent=2) + "\n")
shutil.copyfile(os.path.join(os.path.dirname(__file__), "memory_study.py"), os.path.join(DOWNLOADS, "memory-study.py"))
with open(os.path.join(DOWNLOADS, "memory-study-results.csv"), "w", newline="") as stream:
    write_results(STUDY_CONFIG, stream)

study_rows = list(scenarios(STUDY_CONFIG))
chart = '<figure class="figure capacity-chart"><div class="chart-legend"><span><i class="legend-weights"></i>Weights</span><span><i class="legend-headroom"></i>Planning allowance</span></div>'
for precision in STUDY_CONFIG["bytes_per_parameter"]:
    row = next(r for r in study_rows if r["model_billions"] == 70 and r["precision"] == precision)
    weights, allowance, total = (float(row[k]) for k in ("weights_gb", "headroom_gb", "total_gb"))
    chart += f'<div class="capacity-row"><b>{precision}</b><span class="capacity-track"><i class="capacity-weight" style="width:{weights/168*100:.4f}%"></i><i class="capacity-headroom" style="width:{allowance/168*100:.4f}%"></i></span><strong>{total:g} GB</strong></div>'
chart += '<figcaption>Calculated memory budget for a 70B model, including a 20% planning allowance. Decimal GB.</figcaption></figure>'
table = '<figure class="figure"><div class="table-scroll"><table class="spec plain"><thead><tr><th scope="col">GPU</th><th scope="col">Candidate count</th><th scope="col">Est. per hour</th></tr></thead><tbody>'
for name in ("NVIDIA H100", "NVIDIA H200", "AMD MI300X"):
    row = next(r for r in study_rows if r["model_billions"] == 70 and r["precision"] == "FP16" and r["gpu"] == name)
    table += '<tr><th scope="row">' + name + '</th><td>' + str(row["gpus"]) + '</td><td>$' + row["estimated_hourly_usd"] + '</td></tr>'
table += '</tbody></table></div><figcaption>70B at FP16. Calculated candidates, using the ' + PRICE_DATE + ' price snapshot.</figcaption></figure>'

def completed_article(title, desc, path, body, label, active):
    metadata = {"@context": "https://schema.org", "@type": "TechArticle", "headline": title,
                "description": desc, "datePublished": CONTENT_DATE, "dateModified": CONTENT_DATE,
                "author": {"@type": "Person", "name": "Ankit Dongare", "url": SITE},
                "mainEntityOfPage": SITE + path, "image": SITE + "/og-image.png"}
    page = head(title + " · DatatalkwithAnkit", desc, path, og_type="article", extra=ld(metadata) + ld(crumbs(title, path)))
    page += header(active)
    page += '<main class="wrap"><article class="article"><a class="crumb" href="/blog">Back to all writing</a>'
    page += '<p class="kicker-line">' + label + '</p><h1>' + title + '</h1>'
    page += '<div class="byline-row"><span class="byline-avatar" aria-hidden="true"><img src="/images/ankit-about.jpg" alt="" width="120" height="150" loading="lazy"></span><div><strong>Ankit Dongare</strong>Nov 17, 2026</div></div>'
    page += '<div class="prose">' + body + '</div></article>'
    page += '<div class="article-end"><div class="panel article-subscribe"><h2>Get the next write-up</h2><p>Studies, practical tools, and notes on building AI systems.</p><a class="btn solid" href="/#newsletter">Get updates by email</a></div></div></main>'
    return page + FOOTER

study_body = STUDY_BODY.replace("{{study_chart}}", chart).replace("{{study_table}}", table).replace("{{price_date}}", PRICE_DATE)
open(os.path.join(OUT, "posts", "llm-memory-capacity.html"), "w").write(completed_article(STUDY_TITLE, STUDY_DESC, "/posts/llm-memory-capacity", study_body, "Study · Code, inputs, and results", "Studies"))
open(os.path.join(OUT, "projects", "video-pipeline.html"), "w").write(completed_article(PIPELINE_TITLE, PIPELINE_DESC, "/projects/video-pipeline", PIPELINE_BODY, "Project case study", "Projects"))

# ======================= 404 =======================
nf = head("Page not found · DatatalkwithAnkit", "This page doesn't exist.", "/404", robots="noindex, follow")
nf += header()
nf += """<main class="wrap"><div class="page-head" style="min-height:52vh">
  <h1>That page doesn't exist</h1>
  <p>It may have moved when the site was rebuilt. Start from the <a class="link" href="/">home page</a> or browse <a class="link" href="/blog">all writing</a>.</p>
</div></main>
"""
nf += FOOTER
open(os.path.join(OUT, "404.html"), "w").write(nf)

# ======================= static extras =======================
open(os.path.join(OUT, "favicon.svg"), "w").write(FAVICON_SVG)
open(os.path.join(OUT, "vercel.json"), "w").write(json.dumps({
    "cleanUrls": True, "trailingSlash": False,
    "redirects": [
        {"source": "/:path*", "has": [{"type": "host", "value": "datatalkwithankit.vercel.app"}],
         "destination": "https://www.datatalkwithankit.com/:path*", "permanent": True},
        {"source": "/index.html", "destination": "/", "permanent": True}
    ],
    "headers": [
        {"source": "/(.*)", "headers": [
            {"key": "X-Content-Type-Options", "value": "nosniff"},
            {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
            {"key": "X-Frame-Options", "value": "SAMEORIGIN"}]}
    ]
}, indent=2) + "\n")
open(os.path.join(OUT, "llms.txt"), "w").write(f"""# DatatalkwithAnkit

> LLM inference benchmarks, GPU comparisons and prices, and AI market analysis by Ankit Dongare, an AI engineer who benchmarks LLM serving. Benchmarks are published with their configs.

## Guides
- [Best GPU for LLM inference (2026)]({SITE}/gpu-guide): how many H100, H200, B200, B300, MI300X, MI325X or MI355X GPUs a model needs, specs, and lowest on-demand prices. Updated quarterly.

## Studies
- [What fits in GPU memory?]({SITE}/posts/llm-memory-capacity): 105 calculated capacity scenarios, with Python, JSON inputs, and CSV results. These are estimates, not measured serving benchmarks.

## Posts
- [H200 vs MI300X: what you're actually paying for]({SITE}/posts/h200-vs-mi300x): memory, NVLink vs PCIe scaling, and neocloud pricing.

## Projects
- [Video publishing workflow]({SITE}/projects/video-pipeline): project case study.

## Tools
- [AI models by GPU]({SITE}/#ai-models): publisher-sourced open-weight model examples, with GPU and precision filters and estimated memory requirements.
- [Will-it-fit calculator]({SITE}/#fit-section): GPUs needed and hourly cost for a model size and precision.

## About
- [Home]({SITE}/): who Ankit is and what he works on.
- [Uses]({SITE}/uses): tools used for benchmarking.
""")
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
urls = [("/posts/llm-memory-capacity", "0.9"), ("/projects/video-pipeline", "0.7"), ("/", "1.0"), ("/gpu-guide", "0.9"), ("/posts/h200-vs-mi300x", "0.9"), ("/blog", "0.8"), ("/papers", "0.7"), ("/uses", "0.5")]
open(os.path.join(OUT, "sitemap.xml"), "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{GUIDE_UPDATED_ISO if u in ('/', '/gpu-guide', '/blog') else CONTENT_DATE if u in ('/papers', '/posts/llm-memory-capacity', '/projects/video-pipeline') else '2026-10-12'}</lastmod><priority>{p}</priority></url>\n" for u, p in urls) +
    "</urlset>\n")
open(os.path.join(OUT, "rss.xml"), "w").write(f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>DatatalkwithAnkit</title>
    <link>{SITE}</link>
    <description>LLM inference benchmarks, GPUs, serving configs, and cost, by Ankit Dongare.</description>
    <language>en-us</language>
    <lastBuildDate>Tue, 17 Nov 2026 16:00:00 GMT</lastBuildDate>
    <atom:link href="{SITE}/rss.xml" rel="self" type="application/rss+xml"/>
    <item>
      <title>{STUDY_TITLE}</title>
      <link>{SITE}/posts/llm-memory-capacity</link>
      <guid isPermaLink="true">{SITE}/posts/llm-memory-capacity</guid>
      <description>{STUDY_DESC}</description>
      <pubDate>Tue, 17 Nov 2026 16:00:00 GMT</pubDate>
    </item>
    <item>
      <title>{PIPELINE_TITLE}</title>
      <link>{SITE}/projects/video-pipeline</link>
      <guid isPermaLink="true">{SITE}/projects/video-pipeline</guid>
      <description>{PIPELINE_DESC}</description>
      <pubDate>Tue, 17 Nov 2026 16:00:00 GMT</pubDate>
    </item>
    <item>
      <title>Which GPU should you rent for LLM inference?</title>
      <link>{SITE}/gpu-guide</link>
      <guid isPermaLink="true">{SITE}/gpu-guide</guid>
      <description>{GUIDE_DESC}</description>
      <pubDate>Mon, 12 Oct 2026 09:00:00 GMT</pubDate>
    </item>
    <item>
      <title>H200 vs MI300X: what you're actually paying for</title>
      <link>{SITE}/posts/h200-vs-mi300x</link>
      <guid isPermaLink="true">{SITE}/posts/h200-vs-mi300x</guid>
      <description>{POST_DESC}</description>
      <pubDate>Fri, 21 Aug 2026 09:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>
""")
print("built")
