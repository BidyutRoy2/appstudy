"""Same-origin crawling for appstudy.

Fetches pages with urllib, follows only links that stay on the starting
origin, and stops at the configured depth / page budget. A politeness delay
and a browser-like User-Agent keep the crawler a good citizen. Local HTML
directories can be studied offline with :func:`study_local_dir`.
"""

from __future__ import annotations

import time
import urllib.error
import urllib.request
from collections import deque
from pathlib import Path
from urllib.parse import urldefrag, urlparse

from .extract import Page, extract_page

USER_AGENT = "appstudy/0.1 (+https://github.com/BidyutRoy2/appstudy; clean-room site study)"


def _same_origin(a: str, b: str) -> bool:
    pa, pb = urlparse(a), urlparse(b)
    return (pa.scheme, pa.netloc) == (pb.scheme, pb.netloc)


def fetch(url: str, timeout: float = 15.0) -> str | None:
    """Return the HTML of *url*, or None if it cannot be fetched as HTML."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            content_type = response.headers.get_content_type()
            if content_type != "text/html":
                return None
            charset = response.headers.get_content_charset() or "utf-8"
            return response.read().decode(charset, errors="replace")
    except (urllib.error.URLError, ValueError, TimeoutError, OSError):
        return None


def study_url(start_url: str, depth: int = 2, max_pages: int = 50,
              delay: float = 0.3) -> list[Page]:
    """Breadth-first crawl of one origin, starting at *start_url*."""
    seen: set[str] = set()
    pages: list[Page] = []
    queue: deque[tuple[str, int]] = deque([(start_url, 0)])
    while queue and len(pages) < max_pages:
        url, level = queue.popleft()
        url = urldefrag(url)[0]
        if url in seen:
            continue
        seen.add(url)
        html = fetch(url)
        if html is None:
            continue
        page = extract_page(url, html)
        pages.append(page)
        if level < depth:
            for link in page.links:
                if _same_origin(start_url, link) and urldefrag(link)[0] not in seen:
                    queue.append((link, level + 1))
        if delay:
            time.sleep(delay)
    return pages


def study_local_dir(directory: str | Path) -> list[Page]:
    """Study a folder of saved HTML files without any network access.

    Each ``*.html`` file becomes one page; ``index.html`` maps to ``/`` and
    other files map to ``/<name>``. Useful for tests, demos, and archived
    copies of a site you already own.
    """
    root = Path(directory)
    pages: list[Page] = []
    for path in sorted(root.rglob("*.html")):
        rel = path.relative_to(root)
        page_path = "/" if rel.name == "index.html" else f"/{rel.with_suffix('').as_posix()}"
        page = extract_page(f"file://{page_path}", path.read_text(encoding="utf-8", errors="replace"))
        page.url = page_path
        pages.append(page)
    return pages
