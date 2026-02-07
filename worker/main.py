from datetime import datetime, timezone
import urllib.parse
from dotenv import load_dotenv
import os

from fetchers.rss_fetcher import fetch_rss
from diff.comparator import filter_new_items
from db.postgres import SessionLocal, Alert
from notify.email_sender import send_email


load_dotenv()

# Read receiver email from .env
RECEIVER_EMAIL = os.getenv("ALERT_RECEIVER")

if not RECEIVER_EMAIL:
    raise Exception("ALERT_RECEIVER not set in .env")


def build_subject(alert):
    return f"New alerts for: {alert.query}"


def build_body(items):
    lines = []

    for item in items:
        lines.append(f"- {item['title']}")
        if item.get("link"):
            lines.append(f"  {item['link']}")
        lines.append("")

    return "\n".join(lines)


def build_google_news_rss(query: str) -> str:
    encoded_query = urllib.parse.quote(query)
    return f"https://news.google.com/rss/search?q={encoded_query}"


def run_worker():
    print("\n=== NotifyX Worker Started ===\n")

    db = SessionLocal()

    try:
        alerts = (
            db.query(Alert)
            .filter(Alert.is_active == True)
            .filter(Alert.frequency == "daily")
            .all()
        )

        print(f"Found {len(alerts)} active alerts.\n")

        for alert in alerts:
            print("-----------------------------------")
            print(f"Processing Alert #{alert.id}")
            print("Query:", alert.query)

            feed_url = build_google_news_rss(alert.query)

            last_checked = alert.last_checked_at

            if last_checked is None:
                print("First run → treating all items as NEW")
            else:
                print("Last checked at:", last_checked)

            # Fetch RSS
            items = fetch_rss(feed_url)

            # Filter new
            new_items = filter_new_items(items, last_checked)

            if new_items:
                print(f"\nNEW ITEMS FOUND ({len(new_items)})")

                send_email(
                    RECEIVER_EMAIL,
                    build_subject(alert),
                    build_body(new_items)
                )

                print(f"Email sent to {RECEIVER_EMAIL}")

            else:
                print("No new items.")

            # Update timestamp (important for idempotency)
            alert.last_checked_at = datetime.now(timezone.utc)
            db.commit()

            print("Updated last_checked_at.\n")

        print("\n=== Worker Run Complete ===\n")

    finally:
        db.close()


if __name__ == "__main__":
    run_worker()
