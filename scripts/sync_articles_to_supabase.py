import json
import os
import urllib.request

SUPABASE_URL = os.environ["SUPABASE_URL"].rstrip("/")
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_ROLE_KEY"]

with open("articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

rows = [
    {
        "number": a["number"],
        "topic": a["topic"],
        "title": a["title"],
        "keywords": a.get("keywords", ""),
        "tags": a.get("tags", ""),
        "url": a["url"],
    }
    for a in articles
]

endpoint = f"{SUPABASE_URL}/rest/v1/articles?on_conflict=number"

for start in range(0, len(rows), 500):
    batch = rows[start:start + 500]
    body = json.dumps(batch).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates,return=minimal",
        },
    )
    with urllib.request.urlopen(req) as response:
        if response.status not in (200, 201, 204):
            raise RuntimeError(f"Supabase returned HTTP {response.status}")
    print(f"Synced {min(start + 500, len(rows))}/{len(rows)} articles")

print(f"Successfully synced {len(rows)} articles to Supabase.")
