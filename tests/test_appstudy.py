"""Tests for appstudy extraction, analysis, crawling and reporting."""

import json
import sys
import threading
import unittest
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from appstudy.analyze import analyze, guess_page_type  # noqa: E402
from appstudy.cli import main  # noqa: E402
from appstudy.crawler import study_local_dir, study_url  # noqa: E402
from appstudy.extract import extract_page  # noqa: E402
from appstudy.report import render_markdown, write_outputs  # noqa: E402

HERE = Path(__file__).resolve().parent
SAMPLE_SITE = HERE.parent / "examples" / "sample-site"


class ExtractTests(unittest.TestCase):
    def setUp(self):
        self.index = extract_page("http://example.test/", (SAMPLE_SITE / "index.html").read_text())

    def test_title_description_headings(self):
        self.assertEqual(self.index.title, "Acme Notes — Capture ideas fast")
        self.assertIn("tiny notes app", self.index.description)
        self.assertIn((1, "Capture ideas fast"), self.index.headings)
        self.assertIn((2, "Your second brain, minus the clutter"), self.index.headings)

    def test_nav_links_and_buttons(self):
        self.assertEqual(len(self.index.nav_links), 3)
        self.assertIn("Get started free", self.index.buttons)
        self.assertIn("Watch the demo", self.index.buttons)

    def test_form_fields_with_labels(self):
        self.assertEqual(len(self.index.forms), 1)
        form = self.index.forms[0]
        self.assertEqual(form.action, "http://example.test/signup")
        self.assertEqual(form.method, "post")
        email = [f for f in form.fields if f.name == "email"][0]
        self.assertEqual(email.label, "Work email")
        self.assertTrue(email.required)

    def test_colors_and_fonts_from_styles(self):
        self.assertIn("#111827", self.index.colors)
        self.assertIn("#4f46e5", self.index.colors)
        self.assertTrue(any("Inter" in font for font in self.index.fonts))

    def test_images(self):
        self.assertEqual(self.index.images[0]["alt"], "Notes dashboard preview")


class AnalyzeTests(unittest.TestCase):
    def setUp(self):
        self.pages = study_local_dir(SAMPLE_SITE)
        self.model = analyze(self.pages, "sample-site")

    def test_three_pages_and_types(self):
        self.assertEqual(self.model.total_pages, 3)
        self.assertEqual(self.model.page_types["landing"], 1)
        self.assertEqual(self.model.page_types["pricing"], 1)
        self.assertEqual(self.model.page_types["docs"], 1)

    def test_sitemap_and_nav(self):
        self.assertIn("/", self.model.sitemap)
        self.assertIn("/pricing", self.model.sitemap)
        self.assertIn("/docs", self.model.sitemap)
        self.assertIn("/", self.model.nav)

    def test_forms_and_ctas(self):
        self.assertEqual(len(self.model.forms), 2)
        self.assertIn("Get started free", self.model.calls_to_action)

    def test_guess_page_type(self):
        pricing = extract_page("http://x/pricing", "<title>Pricing</title>")
        self.assertEqual(guess_page_type(pricing), "pricing")


class ReportTests(unittest.TestCase):
    def test_markdown_and_json_roundtrip(self):
        model = analyze(study_local_dir(SAMPLE_SITE), "sample-site")
        md = render_markdown(model)
        self.assertIn("# Rebuild brief: sample-site", md)
        self.assertIn("## Sitemap", md)
        self.assertIn("## Forms to rebuild", md)
        self.assertIn("Clean-room brief", md)
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_outputs(model, tmp)
            data = json.loads(paths["json"].read_text())
            self.assertEqual(data["total_pages"], 3)
            self.assertEqual(len(data["pages"]), 3)


class CrawlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        handler = partial(SimpleHTTPRequestHandler, directory=str(SAMPLE_SITE))
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_live_crawl_stays_on_origin(self):
        pages = study_url(f"http://127.0.0.1:{self.port}/index.html",
                          depth=1, max_pages=10, delay=0)
        paths = sorted(p.path for p in pages)
        self.assertEqual(paths, ["/", "/docs.html", "/index.html", "/pricing.html"])


class CliTests(unittest.TestCase):
    def test_cli_local_mode(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            code = main(["study", str(SAMPLE_SITE), "--local", "--out", tmp])
            self.assertEqual(code, 0)
            self.assertTrue((Path(tmp) / "brief.md").exists())
            self.assertTrue((Path(tmp) / "site.json").exists())

    def test_cli_rejects_bare_hostname(self):
        self.assertEqual(main(["study", "example.com"]), 2)


if __name__ == "__main__":
    unittest.main()
