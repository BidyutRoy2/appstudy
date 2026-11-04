# Output format

## brief.md

A Markdown document with these sections, in order:

1. Header — source URL, page/form/CTA counts, clean-room notice.
2. Sitemap — one route per line.
3. Page inventory — table: path, heuristic type, title, heading count,
   image count.
4. Navigation — links seen inside `<nav>`, most frequent first.
5. Page types — counts per heuristic type.
6. Design tokens (observed) — colours (with page counts) and font stacks.
7. Calls to action — button labels, most frequent first.
8. Forms to rebuild — per form: page, method, action, and every field
   (kind, name, type, label, required).
9. Shared components — navigation plus any CTA seen on 3+ pages.
10. What to build first — suggested build order.

## site.json

The same model as JSON:

```json
{
  "root_url": "https://example.com",
  "total_pages": 3,
  "sitemap": ["/", "/docs", "/pricing"],
  "pages": [
    {
      "path": "/",
      "title": "Acme Notes — Capture ideas fast",
      "description": "A tiny notes app for fast thinkers.",
      "type": "landing",
      "headings": ["Capture ideas fast"],
      "forms": 1,
      "images": 1,
      "text_length": 128
    }
  ],
  "nav": ["/", "/pricing", "/docs"],
  "forms": [
    {
      "page": "/",
      "action": "https://example.com/signup",
      "method": "post",
      "fields": [
        {"kind": "input", "name": "email", "type": "email",
         "label": "Work email", "required": true}
      ]
    }
  ],
  "calls_to_action": ["Get started free"],
  "colors": [{"color": "#111827", "pages": 1}],
  "fonts": ["Inter, system-ui, sans-serif"],
  "page_types": {"landing": 1, "pricing": 1, "docs": 1}
}
```

## Page-type heuristics

Types are guessed from the path and title (`pricing`, `docs`, `blog`,
`about`, `contact`, `signup`, `login`, `changelog`, `landing` for `/`,
otherwise `content`). They are labelled "heuristic" in the brief on purpose —
verify a route by visiting it before building.
