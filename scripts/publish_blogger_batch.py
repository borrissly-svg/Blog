#!/usr/bin/env python3
"""Publish a bounded batch of generated articles to Blogger with resumable deduplication."""
import json
import os
import sys
from pathlib import Path

import requests

BATCH_FILE = Path("blogger-batch.json")
STATE_FILE = Path(".blogger-batch-published.json")
API = "https://www.googleapis.com/blogger/v3"


def get_access_token():
    keys = ("BLOGGER_CLIENT_ID", "BLOGGER_CLIENT_SECRET", "BLOGGER_REFRESH_TOKEN")
    missing = [key for key in keys if not os.getenv(key, "").strip()]
    if missing:
        raise RuntimeError("Missing GitHub Actions secrets: " + ", ".join(missing))
    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": os.environ["BLOGGER_CLIENT_ID"].strip(),
            "client_secret": os.environ["BLOGGER_CLIENT_SECRET"].strip(),
            "refresh_token": os.environ["BLOGGER_REFRESH_TOKEN"].strip(),
            "grant_type": "refresh_token",
        },
        timeout=30,
    )
    if response.status_code == 401 or response.status_code == 400:
        try:
            detail = response.json().get("error_description") or response.json().get("error") or "OAuth credentials were rejected"
        except ValueError:
            detail = "OAuth credentials were rejected"
        raise RuntimeError(
            f"Google OAuth token refresh failed ({response.status_code}): {detail}. "
            "Update BLOGGER_REFRESH_TOKEN and verify BLOGGER_CLIENT_ID/SECRET in GitHub repository Actions secrets."
        )
    response.raise_for_status()
    token = response.json().get("access_token")
    if not token:
        raise RuntimeError("Google OAuth response did not include an access token.")
    return token


def load_json(path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    blog_id = os.getenv("BLOGGER_BLOG_ID", "").strip()
    if not blog_id:
        raise RuntimeError("Missing GitHub Actions secret: BLOGGER_BLOG_ID")
    posts = load_json(BATCH_FILE, [])
    if len(posts) != 500:
        raise RuntimeError(f"Expected exactly 500 generated articles; found {len(posts)}. Run scripts/build_blogger_batch.py first.")
    state = load_json(STATE_FILE, {})
    if not isinstance(state, dict):
        state = {}
    pending = [post for post in posts if post["id"] not in state]
    batch_size = int(os.getenv("BLOGGER_BATCH_SIZE", "20"))
    batch_size = max(1, min(batch_size, 50))
    if not pending:
        print("All 500 generated articles are already recorded as published.")
        return
    selected = pending[:batch_size]
    print(f"Prepared 500 articles. Already recorded: {len(state)}. This run will attempt {len(selected)}.")
    token = get_access_token()
    for post in selected:
        payload = {
            "kind": "blogger#post",
            "title": post["title"],
            "content": post["content"],
            "labels": post["labels"],
        }
        try:
            response = requests.post(
                f"{API}/blogs/{blog_id}/posts/",
                headers={"Authorization": f"Bearer {token}"},
                params={"isDraft": "false"},
                json=payload,
                timeout=45,
            )
            if response.status_code in (400, 401, 403):
                # Fail clearly and stop this batch; don't mark the post as published.
                try:
                    detail = response.json().get("error", {}).get("message", response.text[:400])
                except ValueError:
                    detail = response.text[:400]
                raise RuntimeError(f"Blogger API rejected post {post['id']} ({response.status_code}): {detail}")
            response.raise_for_status()
            result = response.json()
            state[post["id"]] = {
                "status": "published",
                "title": post["title"],
                "category": post["category"],
                "post_id": str(result.get("id", "")),
                "url": result.get("url", ""),
            }
            STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"Published {post['id']}/500 [{post['category']}]: {post['title']} -> {result.get('url', '(URL unavailable)')}")
        except requests.RequestException as exc:
            raise RuntimeError(f"Publishing stopped at article {post['id']}: {exc}") from exc
    counts = {}
    for entry in state.values():
        if entry.get("status") == "published":
            counts[entry.get("category", "Unknown")] = counts.get(entry.get("category", "Unknown"), 0) + 1
    print("Recorded published total: " + str(sum(1 for item in state.values() if item.get("status") == "published")))
    print("Published counts by category: " + json.dumps(counts, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
