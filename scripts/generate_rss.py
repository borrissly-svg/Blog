#!/usr/bin/env python3
"""Build a full-content RSS feed from the static HTML articles."""
from datetime import datetime, timezone
from email.utils import format_datetime
from html import escape
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

try:
    from bs4 import BeautifulSoup
except ImportError as exc:
    raise SystemExit("Install dependencies with: pip install beautifulsoup4") from exc

SITE = "https://borrissly-svg.github.io/Blog/"
ARTICLES_DIR = Path("articles")
OUTPUT = Path("rss.xml")
MAX_ITEMS = 50
CONTENT_NS = "http://purl.org/rss/1.0/modules/content/"
ET.register_namespace("content", CONTENT_NS)

def parse_article(path: Path):
    html = path.read_text(encoding="utf-8", errors="replace")
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("article")
    if article is None:
        return None

    title_tag = article.find("h1") or soup.find("title")
    title = title_tag.get_text(" ", strip=True) if title_tag else path.stem
    description = ""
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if desc_tag:
        description = (desc_tag.get("content") or "").strip()

    canonical = soup.find("link", rel="canonical")
    link = canonical.get("href") if canonical and canonical.get("href") else SITE + path.as_posix()

    published = None
    for tag in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            data = json.loads(tag.string or tag.get_text())
            candidates = data if isinstance(data, list) else [data]
            for item in candidates:
                if isinstance(item, dict) and item.get("datePublished"):
                    published = item["datePublished"]
                    break
        except (json.JSONDecodeError, TypeError):
            continue
        if published:
            break

    if not published:
        published = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).date().isoformat()
    try:
        dt = datetime.fromisoformat(published.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        published_rfc = format_datetime(dt)
        sort_key = dt.timestamp()
    except (ValueError, TypeError):
        published_rfc = format_datetime(datetime.fromtimestamp(path.stat().st_mtime, timezone.utc))
        sort_key = path.stat().st_mtime

    # Remove scripts and forms so feeds contain the article, not page functionality.
    for element in article.find_all(["script", "style", "form", "button"]):
        element.decompose()
    content_html = str(article)
    return {
        "title": title,
        "description": description or title,
        "link": link,
        "published": published_rfc,
        "sort_key": sort_key,
        "content": content_html,
    }

def main():
    items = []
    for path in ARTICLES_DIR.rglob("*.html"):
        item = parse_article(path)
        if item:
            items.append(item)
    items.sort(key=lambda item: item["sort_key"], reverse=True)
    items = items[:MAX_ITEMS]

    rss = ET.Element("rss", {"version": "2.0"})
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = "Ethical Zenith Hackers Intelligence Blog"
    ET.SubElement(channel, "link").text = SITE
    ET.SubElement(channel, "description").text = "Cybersecurity, digital intelligence, and responsible digital asset safety articles."
    ET.SubElement(channel, "language").text = "en-us"
    ET.SubElement(channel, "lastBuildDate").text = format_datetime(datetime.now(timezone.utc))
    for item in items:
        node = ET.SubElement(channel, "item")
        ET.SubElement(node, "title").text = item["title"]
        ET.SubElement(node, "link").text = item["link"]
        ET.SubElement(node, "guid", {"isPermaLink": "true"}).text = item["link"]
        ET.SubElement(node, "pubDate").text = item["published"]
        ET.SubElement(node, "description").text = item["description"]
        encoded = ET.SubElement(node, f"{{{CONTENT_NS}}}encoded")
        encoded.text = item["content"]

    ET.indent(rss, space="  ")
    OUTPUT.write_bytes(b'<?xml version="1.0" encoding="utf-8"?>\n' + ET.tostring(rss, encoding="utf-8"))
    print(f"Generated {OUTPUT} with {len(items)} full-content articles.")

if __name__ == "__main__":
    main()
