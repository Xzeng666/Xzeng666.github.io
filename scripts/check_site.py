#!/usr/bin/env python3
"""Dependency-free checks for this GitHub Pages repository."""

from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
SKIP_LINK_SCHEMES = {"http", "https", "mailto", "tel", "data", "javascript"}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.links: list[tuple[str, str]] = []
        self.images: list[dict[str, str | None]] = []
        self.target_blank: list[dict[str, str | None]] = []
        self.inline_styles = 0
        self.has_main = False
        self.has_lang = False
        self.has_title = False
        self.has_description = False
        self.has_canonical = False
        self.noindex = False
        self.social_meta: set[str] = set()
        self.json_ld_blocks: list[str] = []
        self._json_ld_buffer: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.append(values["id"] or "")
        if values.get("style") is not None:
            self.inline_styles += 1
        if tag == "html" and values.get("lang"):
            self.has_lang = True
        if tag == "main":
            self.has_main = True
        if tag == "title":
            self.has_title = True
        if tag == "meta" and values.get("name", "").lower() == "description" and values.get("content"):
            self.has_description = True
        if tag == "meta" and values.get("name", "").lower() == "robots":
            self.noindex = "noindex" in (values.get("content") or "").lower()
        if tag == "meta" and values.get("content"):
            social_key = values.get("property") or values.get("name")
            if social_key:
                self.social_meta.add(social_key.lower())
        if tag == "link" and values.get("rel", "").lower() == "canonical" and values.get("href"):
            self.has_canonical = True
        if tag == "script" and values.get("type", "").lower() == "application/ld+json":
            self._json_ld_buffer = []
        if tag == "a" and values.get("href"):
            self.links.append(("href", values["href"] or ""))
            if values.get("target") == "_blank":
                self.target_blank.append(values)
        if tag in {"img", "script", "link", "source"}:
            for attr in ("src", "href", "srcset"):
                if values.get(attr):
                    self.links.append((attr, values[attr] or ""))
        if tag == "img":
            self.images.append(values)

    def handle_data(self, data: str) -> None:
        if self._json_ld_buffer is not None:
            self._json_ld_buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._json_ld_buffer is not None:
            self.json_ld_blocks.append("".join(self._json_ld_buffer))
            self._json_ld_buffer = None


def parse_pages() -> dict[Path, PageParser]:
    pages: dict[Path, PageParser] = {}
    for path in sorted(ROOT.rglob("*.html")):
        parser = PageParser()
        parser.feed(path.read_text(encoding="utf-8"))
        pages[path.resolve()] = parser
    return pages


def target_path(page: Path, raw_url: str) -> tuple[Path | None, str]:
    if not raw_url or raw_url.startswith("//"):
        return None, ""
    parsed = urlsplit(raw_url)
    if parsed.scheme.lower() in SKIP_LINK_SCHEMES or parsed.netloc:
        return None, parsed.fragment
    path_text = unquote(parsed.path)
    if not path_text:
        return page.resolve(), parsed.fragment
    candidate = (ROOT / path_text.lstrip("/")) if path_text.startswith("/") else (page.parent / path_text)
    candidate = candidate.resolve()
    if candidate.is_dir() or path_text.endswith("/"):
        candidate /= "index.html"
    return candidate, parsed.fragment


def main() -> int:
    errors: list[str] = []
    pages = parse_pages()

    for path, page in pages.items():
        rel = path.relative_to(ROOT)
        for label, passed in (
            ("html lang", page.has_lang),
            ("title", page.has_title),
            ("meta description", page.has_description),
            ("main landmark", page.has_main),
        ):
            if not passed:
                errors.append(f"{rel}: missing {label}")
        if rel.name != "404.html" and not page.noindex and not page.has_canonical:
            errors.append(f"{rel}: indexable page is missing canonical")
        if not page.noindex:
            required_social = {"og:type", "og:title", "og:description", "og:url", "twitter:card", "twitter:title", "twitter:description"}
            missing_social = sorted(required_social - page.social_meta)
            if missing_social:
                errors.append(f"{rel}: missing social metadata: {', '.join(missing_social)}")
        duplicate_ids = sorted({item for item in page.ids if page.ids.count(item) > 1})
        if duplicate_ids:
            errors.append(f"{rel}: duplicate ids: {', '.join(duplicate_ids)}")
        if page.inline_styles:
            errors.append(f"{rel}: contains {page.inline_styles} inline style attribute(s)")
        for image in page.images:
            if image.get("alt") is None:
                errors.append(f"{rel}: image missing alt: {image.get('src', '<unknown>')}")
            if not image.get("width") or not image.get("height"):
                errors.append(f"{rel}: image missing width/height: {image.get('src', '<unknown>')}")
        for link in page.target_blank:
            rel_tokens = set((link.get("rel") or "").split())
            if not {"noopener", "noreferrer"}.issubset(rel_tokens):
                errors.append(f"{rel}: target=_blank missing noopener noreferrer: {link.get('href')}")
        for index, block in enumerate(page.json_ld_blocks, start=1):
            try:
                json.loads(block)
            except json.JSONDecodeError as exc:
                errors.append(f"{rel}: invalid JSON-LD block {index}: {exc}")
        if rel == Path("index.html") and not page.json_ld_blocks:
            errors.append("index.html: missing ProfilePage JSON-LD")

        for attr, raw_url in page.links:
            candidates = raw_url.split(",") if attr == "srcset" else [raw_url]
            for candidate_url in candidates:
                clean_url = candidate_url.strip().split()[0]
                target, fragment = target_path(path, clean_url)
                if target is None:
                    continue
                try:
                    target.relative_to(ROOT)
                except ValueError:
                    errors.append(f"{rel}: path escapes repository: {clean_url}")
                    continue
                if not target.exists():
                    errors.append(f"{rel}: missing internal target: {clean_url}")
                    continue
                if fragment and target.suffix.lower() == ".html":
                    target_page = pages.get(target.resolve())
                    if target_page and fragment not in target_page.ids:
                        errors.append(f"{rel}: missing fragment #{fragment} in {target.relative_to(ROOT)}")

    sitemap = ROOT / "sitemap.xml"
    try:
        tree = ET.parse(sitemap)
        namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        for loc in tree.findall("sm:url/sm:loc", namespace):
            url = (loc.text or "").strip()
            parsed = urlsplit(url)
            candidate = ROOT / parsed.path.lstrip("/")
            if candidate.is_dir() or parsed.path.endswith("/"):
                candidate /= "index.html"
            if not candidate.exists():
                errors.append(f"sitemap.xml: missing page for {url}")
    except (ET.ParseError, OSError) as exc:
        errors.append(f"sitemap.xml: {exc}")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    expected_sitemap = "Sitemap: https://xzeng666.github.io/sitemap.xml"
    if expected_sitemap not in robots:
        errors.append("robots.txt: canonical sitemap URL is missing")

    css_text = "\n".join(path.read_text(encoding="utf-8") for path in ROOT.rglob("*.css"))
    for raw_url in re.findall(r"url\((['\"]?)(.*?)\1\)", css_text):
        value = raw_url[1]
        if value.startswith(("data:", "http:", "https:")):
            continue
        # CSS URL validation is reserved for future image/font assets.

    if errors:
        print("Static site validation failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"Static site validation passed: {len(pages)} HTML pages checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
