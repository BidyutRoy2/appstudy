"""HTML extraction for appstudy.

Parses one page with the standard library's html.parser and pulls out only
what a visitor can see: title, description, headings, navigation, links,
forms, buttons, images, and the colours/fonts declared in inline styles and
<style> blocks. No JavaScript is executed and no source code is collected.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

HEX_COLOR = re.compile(r"#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b")
FONT_FAMILY = re.compile(r"font-family\s*:\s*([^;{}]+)", re.IGNORECASE)


@dataclass
class FormField:
    kind: str  # input / select / textarea / button
    name: str
    type: str
    label: str = ""
    required: bool = False


@dataclass
class Form:
    action: str
    method: str
    fields: list[FormField] = field(default_factory=list)


@dataclass
class Page:
    url: str
    title: str = ""
    description: str = ""
    headings: list[tuple[int, str]] = field(default_factory=list)
    nav_links: list[str] = field(default_factory=list)
    links: list[str] = field(default_factory=list)
    forms: list[Form] = field(default_factory=list)
    buttons: list[str] = field(default_factory=list)
    images: list[dict] = field(default_factory=list)
    colors: list[str] = field(default_factory=list)
    fonts: list[str] = field(default_factory=list)
    text_length: int = 0
    raw_html: str = ""

    @property
    def path(self) -> str:
        return urlparse(self.url).path or "/"


class _Extractor(HTMLParser):
    def __init__(self, base_url: str):
        super().__init__(convert_charrefs=True)
        self.base_url = base_url
        self.page = Page(url=base_url)
        self._tag_stack: list[str] = []
        self._in_title = False
        self._in_heading = 0
        self._heading_buf: list[str] = []
        self._in_nav = 0
        self._in_style = False
        self._style_buf: list[str] = []
        self._in_button = False
        self._button_buf: list[str] = []
        self._current_form: Form | None = None
        self._text_buf: list[str] = []
        self._label_for: dict[str, str] = {}
        self._pending_label: str | None = None

    # -- helpers ---------------------------------------------------------
    def _abs(self, href: str) -> str:
        return urljoin(self.base_url, href.strip())

    def _visible_text(self, text: str) -> None:
        if self._in_style or self._in_title:
            return
        text = text.strip()
        if text:
            self._text_buf.append(text)

    # -- parser hooks ----------------------------------------------------
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self._tag_stack.append(tag)
        if tag == "title":
            self._in_title = True
        elif tag in ("h1", "h2", "h3"):
            self._in_heading = int(tag[1])
            self._heading_buf = []
        elif tag == "nav":
            self._in_nav += 1
        elif tag == "style":
            self._in_style = True
            self._style_buf = []
        elif tag == "meta" and attrs.get("name", "").lower() == "description":
            self.page.description = attrs.get("content", "").strip()
        elif tag == "a" and attrs.get("href"):
            raw = attrs["href"].strip()
            if raw.startswith(("#", "mailto:", "tel:", "javascript:")):
                pass
            else:
                href = self._abs(raw)
                self.page.links.append(href)
                if self._in_nav:
                    self.page.nav_links.append(href)
        elif tag == "form":
            self._current_form = Form(
                action=self._abs(attrs["action"]) if attrs.get("action") else "",
                method=(attrs.get("method") or "get").lower(),
            )
            self.page.forms.append(self._current_form)
        elif tag == "input" and self._current_form is not None:
            self._current_form.fields.append(
                FormField(
                    kind="input",
                    name=attrs.get("name", ""),
                    type=attrs.get("type", "text"),
                    label=self._label_for.get(attrs.get("id", ""), ""),
                    required="required" in attrs,
                )
            )
        elif tag == "select" and self._current_form is not None:
            self._current_form.fields.append(
                FormField(
                    kind="select",
                    name=attrs.get("name", ""),
                    type="select",
                    label=self._label_for.get(attrs.get("id", ""), ""),
                    required="required" in attrs,
                )
            )
        elif tag == "textarea" and self._current_form is not None:
            self._current_form.fields.append(
                FormField(
                    kind="textarea",
                    name=attrs.get("name", ""),
                    type="textarea",
                    label=self._label_for.get(attrs.get("id", ""), ""),
                    required="required" in attrs,
                )
            )
        elif tag == "button":
            self._in_button = True
            self._button_buf = []
            if self._current_form is not None:
                self._current_form.fields.append(
                    FormField(kind="button", name=attrs.get("name", ""), type=attrs.get("type", "submit"))
                )
        elif tag == "img":
            self.page.images.append({"src": self._abs(attrs["src"]) if attrs.get("src") else "",
                                     "alt": attrs.get("alt", "")})
        elif tag == "label" and attrs.get("for"):
            self._pending_label = attrs["for"]

        style = attrs.get("style", "")
        if style:
            self.page.colors.extend(c.lower() for c in HEX_COLOR.findall(style))
            for match in FONT_FAMILY.findall(style):
                self.page.fonts.append(match.strip())

    def handle_endtag(self, tag):
        if self._tag_stack and self._tag_stack[-1] == tag:
            self._tag_stack.pop()
        if tag == "title":
            self._in_title = False
        elif tag in ("h1", "h2", "h3") and self._in_heading:
            text = " ".join(self._heading_buf).strip()
            if text:
                self.page.headings.append((self._in_heading, text))
            self._in_heading = 0
        elif tag == "nav" and self._in_nav:
            self._in_nav -= 1
        elif tag == "style" and self._in_style:
            css = " ".join(self._style_buf)
            self.page.colors.extend(c.lower() for c in HEX_COLOR.findall(css))
            for match in FONT_FAMILY.findall(css):
                self.page.fonts.append(match.strip())
            self._in_style = False
        elif tag == "button" and self._in_button:
            text = " ".join(self._button_buf).strip()
            if text:
                self.page.buttons.append(text)
            self._in_button = False
        elif tag == "form":
            self._current_form = None
        elif tag == "label":
            self._pending_label = None

    def handle_data(self, data):
        if self._in_title:
            self.page.title += data.strip()
        elif self._in_heading:
            self._heading_buf.append(data.strip())
        elif self._in_style:
            self._style_buf.append(data)
        elif self._in_button:
            self._button_buf.append(data.strip())
        elif self._pending_label:
            self._label_for[self._pending_label] = data.strip()
        else:
            self._visible_text(data)

    def result(self) -> Page:
        self.page.text_length = sum(len(t) for t in self._text_buf)
        # De-duplicate while preserving order.
        self.page.links = list(dict.fromkeys(self.page.links))
        self.page.nav_links = list(dict.fromkeys(self.page.nav_links))
        self.page.colors = list(dict.fromkeys(self.page.colors))
        self.page.fonts = list(dict.fromkeys(self.page.fonts))
        return self.page


def extract_page(url: str, html: str) -> Page:
    """Parse one HTML document into a :class:`Page` of visible facts."""
    parser = _Extractor(url)
    parser.feed(html)
    page = parser.result()
    page.raw_html = html
    return page
