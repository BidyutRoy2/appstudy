"""appstudy command line interface."""

from __future__ import annotations

import argparse
import sys

from . import __version__
from .analyze import analyze
from .crawler import study_local_dir, study_url
from .report import write_outputs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="appstudy",
        description="Study how a website works from its public surface, "
                    "then rebuild it yourself — clean-room, zero dependencies.",
    )
    parser.add_argument("--version", action="version", version=f"appstudy {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    study = sub.add_parser("study", help="Crawl a site (or a local HTML folder) and write a rebuild brief.")
    study.add_argument("target", help="URL to study, or a folder of .html files with --local")
    study.add_argument("--local", action="store_true", help="Treat target as a local folder of HTML files")
    study.add_argument("--depth", type=int, default=2, help="Link depth to follow (default: 2)")
    study.add_argument("--max-pages", type=int, default=50, help="Maximum pages to study (default: 50)")
    study.add_argument("--delay", type=float, default=0.3, help="Seconds between requests (default: 0.3)")
    study.add_argument("--out", default="appstudy-output", help="Output directory (default: appstudy-output)")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "study":
        if args.local:
            pages = study_local_dir(args.target)
            root = args.target
        else:
            if not args.target.startswith(("http://", "https://")):
                print("error: target must be an http(s) URL (or use --local for a folder)",
                      file=sys.stderr)
                return 2
            print(f"Studying {args.target} (depth={args.depth}, max-pages={args.max_pages}) …")
            pages = study_url(args.target, depth=args.depth,
                              max_pages=args.max_pages, delay=args.delay)
            root = args.target
        if not pages:
            print("error: nothing could be studied — check the URL or folder and try again",
                  file=sys.stderr)
            return 1
        model = analyze(pages, root)
        paths = write_outputs(model, args.out)
        print(f"Studied {model.total_pages} page(s).")
        print(f"Brief:  {paths['brief']}")
        print(f"Data:   {paths['json']}")
        print(f"Forms:  {len(model.forms)}  |  CTAs: {len(model.calls_to_action)}  |  "
              f"Colours: {len(model.colors)}")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
