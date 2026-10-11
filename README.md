# DatatalkwithAnkit

Personal site of Ankit Dongare, an AI engineer benchmarking LLM inference.

Live: https://datatalkwithankit.vercel.app

Plain HTML, CSS, and JavaScript. No build step. Deployed by Vercel on every push to `main`.

## Files

| File | What it is |
|---|---|
| `index.html` | Home: intro, will-it-fit calculator, writing, projects, about, newsletter and contact |
| `blog.html` | All writing, served at `/blog` |
| `papers.html` | Papers and method, served at `/papers` |
| `uses.html` | Tools, served at `/uses` |
| `posts/*.html` | One file per post, served at `/posts/<name>` |
| `style.css`, `site.js` | Shared styles and behavior |
| `vercel.json` | Enables clean URLs (no `.html` in addresses) |
| `rss.xml`, `sitemap.xml`, `robots.txt` | Feed and search engine files |

## Publish a new post

1. Copy `posts/h200-vs-mi300x.html` to `posts/your-post-name.html`.
2. Change the title, description, date, canonical URL, JSON-LD, and body.
3. Add a row for it near the top of the list in `blog.html`, and update the featured post on `index.html` if it's the newest.
4. Add an `<item>` to `rss.xml` and a `<url>` to `sitemap.xml`.
5. Commit and push. Vercel deploys in about a minute.

## Turn on the contact form

Sign up free at formspree.io, create a form, and paste its endpoint into `FORM_ENDPOINT` at the top of `site.js`. Until then, the form opens the visitor's mail app.

## Analytics

Enable Web Analytics in the Vercel project. The script is already on every page.
