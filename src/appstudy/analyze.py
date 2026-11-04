"""Turn crawled pages into a rebuild brief model.

The analysis stays at the level of what a visitor sees: which pages exist,
how navigation connects them, which components repeat on every page, which
forms and calls to action a rebuild needs, and which colours and fonts give
the site its look. Page-type labels are heuristics, clearly marked as such.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass, field
from urllib.parse import urlparse

from .extract import Page

#: Path keywords that suggest a page's role. Heuristic only.
PAGE_TYPE_HINTS = {
    "pricing": ("pricing", "plans", "price"),
    "docs": ("docs", "documentation", "guide", "handbook"),
    "blog": ("blog", "news", "articles", "posts"),
    "about": ("about", "company", "team"),
    "contact": ("contact", "support", "help"),
    "signup": ("signup", "sign-up", "register", "join", "get-started"),
    "login": ("login", "sign-in", "signin"),
    "changelog": ("changelog", "releases", "whats-new"),
}


def guess_page_type(page: Page) -> str:
    path = page.path.lower()
    title = page.title.lower()
    for kind, hints in PAGE_TYPE_HINTS.items():
        if any(h in path or h in title for h in hints):
            return kind
    if page.path in ("/", ""):
        return "landing"
    return "content"


@dataclass
class SiteModel:
    root_url: str
    pages: list[dict] = field(default_factory=list)
    sitemap: list[str] = field(default_factory=list)
    nav: list[str] = field(default_factory=list)
    shared_components: list[str] = field(default_factory=list)
    forms: list[dict] = field(default_factory=list)
    calls_to_action: list[str] = field(default_factory=list)
    colors: list[tuple[str, int]] = field(default_factory=list)
    fonts: list[str] = field(default_factory=list)
    page_types: dict[str, int] = field(default_factory=dict)
    total_pages: int = 0

    def to_dict(self) -> dict:
        data = asdict(self)
        data["colors"] = [{"color": c, "pages": n} for c, n in self.colors]
        return data


def analyze(pages: list[Page], root_url: str) -> SiteModel:
    model = SiteModel(root_url=root_url, total_pages=len(pages))
    color_counter: Counter[str] = Counter()
    font_counter: Counter[str] = Counter()
    nav_counter: Counter[str] = Counter()
    type_counter: Counter[str] = Counter()
    cta_counter: Counter[str] = Counter()

    for page in pages:
        model.sitemap.append(page.path)
        model.pages.append({
            "path": page.path,
            "title": page.title,
            "description": page.description,
            "type": guess_page_type(page),
            "headings": [h for _, h in page.headings],
            "forms": len(page.forms),
            "images": len(page.images),
            "text_length": page.text_length,
        })
        type_counter[guess_page_type(page)] += 1
        color_counter.update(page.colors)
        font_counter.update(page.fonts)
        for link in page.nav_links:
            nav_counter[urlparse(link).path or "/"] += 1
        for button in page.buttons:
            cta_counter[button] += 1
        for form in page.forms:
            model.forms.append({
                "page": page.path,
                "action": form.action,
                "method": form.method,
                "fields": [
                    {"kind": f.kind, "name": f.name, "type": f.type,
                     "label": f.label, "required": f.required}
                    for f in form.fields
                ],
            })

    model.nav = [path for path, _ in nav_counter.most_common()]
    # A component "repeats" if its label appears on most pages: here we treat
    # the shared navigation itself plus any CTA seen on 3+ pages as shared.
    model.shared_components = ["site navigation"] if model.nav else []
    model.shared_components += [cta for cta, n in cta_counter.items() if n >= 3 and len(pages) >= 3]
    model.calls_to_action = [cta for cta, _ in cta_counter.most_common(20)]
    model.colors = color_counter.most_common(12)
    model.fonts = [font for font, _ in font_counter.most_common(5)]
    model.page_types = dict(type_counter)
    model.sitemap = sorted(set(model.sitemap))
    return model
