#!/usr/bin/env python3
"""Publish new full-content RSS items to Blogger, with URL-based deduplication."""
import json
import os
from pathlib import Path
import sys
import xml.etree.ElementTree as ET
import requests

FEED = Path("rss.xml")
STATE = Path(".blogger-published.json")
SITE = "https://borrissly-svg.github.io/Blog/"
BLOGGER_API = "https://www.googleapis.com/blogger/v3"


def get_token():
    values = [
        os.getenv("BLOGGER_CLIENT_ID", ""),
        os.getenv("BLOGGER_CLIENT_SECRET", ""),
        os.getenv("BLOGGER_REFRESH_TOKEN", ""),
    ]
    if not all(values):
        print("Blogger secrets are not configured; skipping publishing.")
        return None
    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": values[0],
            "client_secret": values[1],
            "refresh_token": values[2],
            "grant_type": "refresh_token",
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["access_token"]


def parse_feed():
    if not FEED.exists():
        raise RuntimeError("rss.xml not found. Run the RSS feed workflow first.")
    root = ET.parse(FEED).getroot()
    ns = {"content": "http://purl.org/rss/1.0/modules/content/"}
    items = []
    for node in root.findall("./channel/item"):
        title = (node.findtext("title") or "").strip()
        link = (node.findtext("link") or "").strip()
        html = node.findtext("content:encoded", namespaces=ns) or ""
        if title and link and html:
            items.append({"title": title, "link": link, "html": html})
        elif title and link:
            print(f"Skipping {title}: feed item has no full content.")
    return items


def load_state():
    if STATE.exists():
        data = json.loads(STATE.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    return {}


def save_state(state):
    STATE.write_text(
        json.dumps(state, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main():
    blog_id = os.getenv("BLOGGER_BLOG_ID", "").strip()
    if not blog_id:
        print("BLOGGER_BLOG_ID is not configured; skipping publishing.")
        return

    items = parse_feed()
    if not items:
        print("No full-content RSS items found.")
        return

    state = load_state()
    # On first setup, don't dump the whole existing feed into Blogger.
    # Publish the newest feed item only and mark the older feed as baseline.
    if not state:
        for item in items[1:]:
            state[item["link"]] = {"status": "baseline-existing"}
        save_state(state)

    token = get_token()
    if not token:
        return

    for item in reversed(items):
        link = item["link"]
        if link in state:
            continue
        content = (
            item["html"]
            + '<hr><p><em>Originally published on '
            + '<a href="' + link + '">Ethical Zenith Hackers Intelligence Blog</a>.'
            + '</em></p>'
        )
        try:
            response = requests.post(
                f"{BLOGGER_API}/blogs/{blog_id}/posts/",
                headers={"Authorization": f"Bearer {token}"},
                params={"isDraft": "false"},
                json={
                    "kind": "blogger#post",
                    "title": item["title"],
                    "content": content,
                },
                timeout=30,
            )
            response.raise_for_status()
            post = response.json()
            state[link] = {
                "status": "published",
                "blogger_post_id": str(post.get("id", "")),
                "blogger_url": post.get("url", ""),
            }
            save_state(state)
            print(f"Published: {item['title']} -> {post.get('url', '(URL unavailable)')}")
        except requests.RequestException as exc:
            print(f"Failed to publish {item['title']}: {exc}", file=sys.stderr)
            # Do not mark failed posts as completed; the next scheduled run retries.

    save_state(state)


if __name__ == "__main__":
    main()
