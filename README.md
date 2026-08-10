# DatatalkwithAnkit

Personal site of Ankit Dongare — AI engineer building and benchmarking LLM and vLLM inference systems.
Blog, papers/write-ups, projects, and contact.

**Live:** _(add your Vercel URL here once deployed)_

## Structure
```
index.html        the entire site (all pages, styles, and scripts)
images/           photos used in the About section
```
Pure static HTML/CSS/JS — no build step, no dependencies.

## Adding a blog post or paper
Open `index.html`, find the block marked **"HOW TO ADD A BLOG POST OR PAPER"**
near the top of the `<script>` section, and add an object to `POSTS` or `PAPERS`:

```js
{
  title:  "Your post title",
  cat:    "LLM SERVING",        // category label
  date:   "JUL 2026",
  status: "Live",               // Live | Coming soon | Draft | Planned
  desc:   "One or two sentence summary.",
  link:   "https://..."         // or "" if not published yet
}
```
Newest entries go at the top. Commit and push — Vercel redeploys automatically.

## Deploying
Connected to Vercel. Any push to `main` triggers a production deploy.

## Analytics
Vercel Web Analytics — enable in the Vercel dashboard under Project → Analytics.
The tracking script is already included in `index.html`.
