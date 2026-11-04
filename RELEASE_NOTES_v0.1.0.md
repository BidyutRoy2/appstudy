# appstudy v0.1.0 — Release notes

**Study how any website works from its public surface, then rebuild it yourself.**

## What is in this release

- `appstudy study <url>` — same-origin crawl that writes a clean-room rebuild
  brief (`brief.md`) plus machine-readable data (`site.json`).
- Offline mode: `appstudy study <folder> --local` for saved HTML.
- Visible-surface extraction only: pages, navigation, forms, calls to action,
  colours, fonts. Never code, never assets, never anything behind a login.
- Zero dependencies — Python 3.10+ standard library only.
- 13 tests, all passing, fully offline.

## Install (source — no package published yet)

```bash
git clone https://github.com/BidyutRoy2/appstudy.git
cd appstudy
python3 -m appstudy study https://example.com --depth 2 --out appstudy-output
```

## Try it in 30 seconds

```bash
python3 -m appstudy study examples/sample-site --local --out appstudy-output
```

See `examples/sample-brief.md` for what the output looks like.
