from datetime import datetime, timezone
import feedparser

def fetch_rss(feed_url: str):
    feed = feedparser.parser(feed_url)

    items = []

    for entry in feed.entries:
        if not getattr(entry, "published_parsed", None):
           continue

        published_at = datetime(
            *entry.published_parsed[:6],
            tzinfo=timezone.utc,
        )

        item = {
            "id": entry.get("id") or entry.get("link"),
            "title": entry.get("title", "").strip(),
            "link": entry.get("link"),
            "pubished_at": published_at,
        }

        items.append(item)
    
    return item