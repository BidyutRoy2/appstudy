# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- PyPI publication (planned) — until then, install from source as shown in the README.

## [0.1.0] - 2026-11-04

### Added

- `appstudy study <url>` — same-origin crawl (depth, page budget, politeness
  delay) producing `brief.md` and `site.json`.
- `appstudy study <folder> --local` — offline study of saved HTML files.
- Visible-surface extraction only: titles, descriptions, headings, navigation,
  links, forms with labelled fields, buttons, images, colours, fonts.
- Rebuild brief model: sitemap, page inventory with heuristic page types,
  shared navigation, design tokens, calls to action, forms, build order.
- Three-page fixture site (`examples/sample-site/`) and a generated sample
  brief (`examples/sample-brief.md`).
- 13-test suite, standard library only, fully offline.
- Terminal demo image (`assets/demo.png`) and 1280×640 social preview
  (`assets/social-preview.png`).
