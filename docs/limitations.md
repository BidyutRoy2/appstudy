# Limitations — read before you trust a brief

- **JavaScript-rendered content.** appstudy reads the HTML the server sends.
  Pages that render everything client-side will produce a thin brief (often
  just a title and a shell). That is a real limitation, not a bug to work
  around with a headless browser — see `docs/architecture.md` for why.
- **Heuristic page types.** Types like `pricing` or `docs` are guessed from
  paths and titles. They are labelled as heuristics in every brief; verify
  routes by visiting them.
- **Colours and fonts are observed, not designed.** The brief lists what was
  declared in inline styles and `<style>` blocks. External stylesheets are not
  fetched, so a site that keeps its design system in one CSS file will show
  fewer tokens.
- **Forms are described, not submitted.** appstudy never sends form data.
- **Same origin only.** Subdomains count as a different origin and are not
  crawled. Cross-domain navigation is visible in the link list only if it
  appears in page content — outbound links are not followed.
- **No auth, no cookies.** Anything behind a login is out of scope by design.
