# Usage guide

## Studying a live site

```bash
python3 -m appstudy study https://example.com --depth 2 --max-pages 50 --out out
```

- `--depth 0` studies only the start page.
- `--max-pages` caps the crawl; the crawler stops as soon as it hits the budget.
- `--delay` (seconds, default `0.3`) spaces requests out. Raise it for small
  sites or slow servers.

Output is always two files in `--out`:

| File | For |
|---|---|
| `brief.md` | Humans and coding agents — the rebuild spec |
| `site.json` | Scripts, dashboards, diffing two studies over time |

## Studying saved HTML (offline)

```bash
python3 -m appstudy study ./saved-site --local --out out
```

Every `*.html` under the folder becomes a page. `index.html` maps to `/`;
other files map to their path without the extension. No network access happens.

## Practical tips

- **Start shallow.** `--depth 1` on a big site gives you the skeleton in seconds;
  go deeper once you know what matters.
- **Study your own staging site** before a redesign — the brief is a neutral
  record of what the current site actually is, not what anyone remembers.
- **Diff over time.** Study the same site monthly and diff `site.json` to see
  which routes, forms, and CTAs changed.
- **Respect robots.txt.** appstudy does not fetch it automatically; check it
  yourself before studying a site you do not own, and stop if crawling is
  disallowed.
