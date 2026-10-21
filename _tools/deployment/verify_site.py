"""Verify a built Jekyll site, including deployment under a project base path."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urljoin, urlsplit


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.references = []
        self.ids = set()
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag in ("a", "link") and attrs.get("href"):
            self.references.append(attrs["href"])
        if tag in ("img", "script", "source", "video") and attrs.get("src"):
            self.references.append(attrs["src"])
        if attrs.get("poster"):
            self.references.append(attrs["poster"])
        if attrs.get("srcset"):
            self.references.extend(part.strip().split()[0] for part in attrs["srcset"].split(",") if part.strip())
        if tag == "meta" and attrs.get("property") in ("og:image", "og:url", "twitter:image", "twitter:url"):
            self.references.append(attrs.get("content", ""))
        self.references.extend(css_urls(attrs.get("style", "")))


def css_urls(text):
    return re.findall(r"url\([\"']?([^\)\"']+)", text)


def verify(site, baseurl, origin):
    site = site.resolve()
    baseurl = "/" + baseurl.strip("/") if baseurl.strip("/") else ""
    origin = origin.rstrip("/")
    pages = {path: Page(path.read_text(encoding="utf-8-sig")) for path in site.rglob("*.html")}
    errors = []
    checked = set()

    def check(reference, source):
        reference = reference.strip()
        if not reference or reference.startswith(("mailto:", "tel:", "data:", "javascript:", "//")):
            return
        parts = urlsplit(reference)
        if parts.scheme:
            if not reference.startswith(origin + baseurl + "/"):
                return
        elif baseurl and reference.startswith("/") and not (parts.path == baseurl or parts.path.startswith(baseurl + "/")):
            errors.append({"source": str(source.relative_to(site)), "reference": reference, "error": "Missing project base path"})
            return
        source_url = origin + baseurl + "/" + source.relative_to(site).as_posix()
        url = urlsplit(urljoin(source_url, reference))
        path = unquote(url.path)
        if baseurl:
            if path != baseurl and not path.startswith(baseurl + "/"):
                return
            path = path[len(baseurl):]
        target = site / path.lstrip("/")
        if target.is_dir():
            target = target / "index.html"
        elif not target.exists() and not target.suffix:
            target = target / "index.html"
        checked.add((str(source.relative_to(site)), reference))
        if not target.is_file():
            errors.append({"source": str(source.relative_to(site)), "reference": reference, "error": "Missing local file"})
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append({"source": str(source.relative_to(site)), "reference": reference, "error": "Missing heading or anchor"})

    for path, page in pages.items():
        for reference in page.references:
            check(reference, path)
    for path in site.rglob("*.css"):
        for reference in css_urls(path.read_text(encoding="utf-8-sig")):
            check(reference, path)

    for path in site.rglob("*"):
        if path.is_file() and path.suffix in (".html", ".css", ".js"):
            text = path.read_text(encoding="utf-8-sig", errors="replace")
            if re.search(r"(?:file://|https?://(?:127\.0\.0\.1|localhost)(?::\d+)?|[CDE]:[\\/])", text):
                errors.append({"source": str(path.relative_to(site)), "error": "Local-only path in published output"})
            if path.suffix == ".html" and re.search(r"Lorem ipsum|John Doe|Jane Smith", text, re.I):
                errors.append({"source": str(path.relative_to(site)), "error": "Template placeholder content"})
    for unwanted in ("_tools", "_members", "_posts", "testbed.html", "CHANGELOG.md", "README.md", "Gemfile", "Gemfile.lock"):
        if (site / unwanted).exists():
            errors.append({"source": unwanted, "error": "Development or template file included in public output"})

    required = ("index.html", "research/index.html", "team/index.html", "team/yongzan-liu/index.html", "publication/index.html", "software/index.html", "news/index.html", "contacts/index.html")
    for required_file in required:
        if not (site / required_file).is_file():
            errors.append({"source": required_file, "error": "Required website page missing"})
    return {
        "site": str(site), "url": origin + baseurl + "/", "html_pages": len(pages),
        "local_references_checked": len(checked),
        "total_bytes": sum(p.stat().st_size for p in site.rglob("*") if p.is_file()),
        "errors": errors, "passed": not errors,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=Path("_site"))
    parser.add_argument("--baseurl", default="/seeds")
    parser.add_argument("--origin", default="https://yongzanliu.github.io")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    report = verify(args.site, args.baseurl, args.origin)
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
