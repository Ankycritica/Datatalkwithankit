<div align="center">

# DatatalkwithAnkit

**Benchmarks and writing on GPUs, LLM inference, and the AI market.**

[datatalkwithankit.com](https://datatalkwithankit.com) · [Writing](https://datatalkwithankit.com/blog) · [Papers](https://datatalkwithankit.com/papers) · [RSS](https://datatalkwithankit.com/rss.xml)

</div>

---

Personal site of **Ankit Dongare**, an AI engineer who measures what language models cost to run. Every benchmark is published with its configs so anyone can rerun it.

## Highlights

- **Will-it-fit calculator**: pick a model size and precision to see how many H200 or MI300X GPUs it needs and the hourly cost.
- **Long-form posts** such as [H200 vs MI300X: what you're actually paying for](https://datatalkwithankit.com/posts/h200-vs-mi300x).
- Fast and dependency-free: plain HTML, CSS and JavaScript, light and dark themes, responsive down to phone width.
- SEO ready: canonical URLs, Open Graph images, JSON-LD, sitemap and RSS feed.

## Structure

```
datatalkwithankit/      ← the deployed site (Vercel root directory)
├── index.html          home, calculator, projects, about, contact
├── blog.html           all writing          → /blog
├── papers.html         papers and method    → /papers
├── uses.html           tools                → /uses
├── posts/              one file per post    → /posts/<name>
├── style.css, site.js  shared styles and behavior
├── images/             photos
└── vercel.json         clean URLs, redirects, security headers
```

## Publishing a post

1. Copy `datatalkwithankit/posts/h200-vs-mi300x.html` to a new file in `posts/`.
2. Update the title, description, date, canonical URL, JSON-LD and body.
3. Add it to `blog.html`, the home page list, `rss.xml` and `sitemap.xml`.
4. Push to `main`. Vercel deploys in about a minute.

## Run locally

```bash
cd datatalkwithankit && python3 -m http.server 8000
```

## Stack

HTML · CSS · JavaScript · IBM Plex · Vercel

---

© 2026 Ankit Dongare. Writing and images are not licensed for reuse without permission.
