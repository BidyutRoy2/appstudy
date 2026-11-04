# Architecture

appstudy is deliberately boring: five small modules, standard library only,
no framework, no plugins.

```
src/appstudy/
├── __init__.py    version
├── __main__.py    python -m appstudy entry point
├── cli.py         argparse wiring, exit codes
├── crawler.py     fetching + same-origin BFS + local-folder study
├── extract.py     html.parser-based visible-surface extraction
├── analyze.py     pages -> SiteModel (sitemap, nav, tokens, forms)
└── report.py      SiteModel -> brief.md + site.json
```

Data flows one way: **fetch → extract → analyze → render**. Each stage is
independently testable, and no stage knows about the command line.

## Design decisions

- **html.parser, not a headless browser.** The brief is about the document the
  server returns. A browser would execute scripts and see more — but it would
  also be heavier, slower, and harder to keep clean-room honest.
- **No concurrency.** One request at a time with a delay. A crawler that is
  polite by construction cannot accidentally hammer a site.
- **Same-origin BFS.** Depth-first would wander down one rabbit hole; BFS
  gives the skeleton first, which is what a rebuild brief needs.
- **Dataclasses, not dicts, until the edge.** `Page` and `SiteModel` are typed;
  only the JSON writer converts to plain data.

## Adding a feature

Find the stage it belongs to, add it there, add a test that runs offline
(fixture HTML or a local HTTP server in the test), and update `docs/` plus the
README if it is user-visible.
