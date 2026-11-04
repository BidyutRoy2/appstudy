# Clean-room method

Clean-room engineering means rebuilding a thing from a *description* of what
it does, without copying its implementation. appstudy exists to produce that
description — and to make it hard to cheat, even by accident.

## What appstudy collects

Only what any visitor sees in a browser: page titles, headings, navigation
labels, form fields and their labels, button text, image alt text, and the
colours and fonts a page declares in its own markup.

## What appstudy never collects

- Source code, templates, or scripts
- Stylesheets, images, fonts, or other assets
- API responses, cookies, tokens, or anything behind a login
- Content from other origins

## How to rebuild responsibly

1. Study the site. Read the brief, not the site's source.
2. Build from the brief, in your own stack, with your own code and your own
   visual design. The brief tells you *what* to build, not *how it looks
   pixel-for-pixel*.
3. Do not reproduce copyrighted text, logos, or artwork. Headings and button
   labels in a brief are short functional phrases; long marketing copy should
   be rewritten in your own words.
4. If a site's terms or `robots.txt` forbid automated access, do not study it
   with a crawler — use the `--local` mode on copies you legitimately hold,
   or study it by hand.

A rebuild that follows these steps is original work inspired by a public
product. A rebuild that copies code or assets is not — and no tool can make
it one.
