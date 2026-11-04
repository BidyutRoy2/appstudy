"""appstudy — study how any website works, then rebuild it yourself.

A zero-dependency CLI that crawls a site's *public, visible* surface
(pages, navigation, forms, calls to action, design tokens) and writes a
structured rebuild brief. It never downloads or copies source code, never
touches anything behind a login, and only follows links on the same origin.

Clean-room by design: the brief describes what is visible, so an agent or a
human can build their own version from the description alone.
"""

__version__ = "0.1.0"
__all__ = ["__version__"]
