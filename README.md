# DatatalkwithAnkit

Personal site of **Ankit Dongare** — AI engineer building and benchmarking LLM and vLLM inference systems.

**Live:** https://datatalkwithankit.vercel.app

## Structure
```
index.html      entire site (Home, Blog, Papers, Uses, article view)
images/         photos used in the About section
og-image.png    social share preview card (1200x630)
rss.xml         feed
sitemap.xml     search engine sitemap
robots.txt
```
Static HTML/CSS/JS — no build step, no dependencies.

## Adding a blog post or paper
In `index.html`, find **"HOW TO ADD A BLOG POST OR PAPER"** near the top of the
`<script>` block, then add an object to `POSTS` or `PAPERS`:

```js
{
  title: "Your post title",
  cat: "LLM SERVING",              // category label
  tags: ["vLLM","Benchmarking"],   // drives the filter buttons
  date: "2026-08-20",              // YYYY-MM-DD
  readingTime: 7,                  // minutes; 0 hides it
  status: "Live",                  // Live | Coming soon | Draft | Planned
  desc: "One or two sentence summary.",
  link: "#post/my-slug"            // or an external URL, or "" if unpublished
}
```
Newest entries go at the top. Commit and push — Vercel redeploys automatically.
Also add the post to `rss.xml` so subscribers get it.

## Activating the contact form
1. Sign up free at formspree.io and create a form
2. Copy the endpoint (`https://formspree.io/f/xxxxxxx`)
3. Set `FORM_ENDPOINT` in `index.html`

Until set, the form falls back to opening the visitor's mail app.

## Analytics
Vercel Web Analytics — enable under Project → Analytics. Script is already included.

## Deploying
Pushes to `main` auto-deploy via Vercel.
