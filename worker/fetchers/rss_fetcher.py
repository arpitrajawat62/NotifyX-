from datetime import datetime, timezone
import feedparser

def fetch_rss(feed_url: str):
    feed = feedparser.parse(feed_url)

    items = []

    for entry in feed.entries:
        
        parsed_time = (
            getattr(entry, "published_At", None)
            or getattr(entry, "updated_parsed", None)
        )
        if not parsed_time:
            continue

        published_at = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)

        item = {
            "id": entry.get("id") or entry.get("link"),
            "title": entry.get("title", "").strip(),
            "link": entry.get("link"),
            "published_at": published_at,
        }

        items.append(item)
    
    return items
